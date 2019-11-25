from __future__ import unicode_literals
import os
import jwt
import json
from functools import wraps
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from six.moves.urllib import request as req
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from .serializers import Powerline_Serializer, drf_Measurement_Serializer, drf_Timestamp_Serializer, drf_Jobid_Serializer
from .models import Powerline, drf_Measurement, drf_Timestamp, drf_Jobid
from .filters import drf_Measurement_Filter, drf_Timestamp_Filter, drf_Jobid_Filter
#from rest_framework_gis.filters import InBBoxFilter

def get_token_auth_header(request):
    #Obtains the access token from the Authorization Header
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token

def requires_scope(required_scope):
    #Determines if the required scope is present in the access token
    #Args:
    #    required_scope (str): The scope required to access the resource
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
            API_IDENTIFIER = os.environ.get('API_IDENTIFIER')
            jsonurl = req.urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
            jwks = json.loads(jsonurl.read())
            cert = '-----BEGIN CERTIFICATE-----\n' + jwks['keys'][0]['x5c'][0] + '\n-----END CERTIFICATE-----'
            certificate = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
            public_key = certificate.public_key()
            decoded = jwt.decode(token, public_key, audience=API_IDENTIFIER, algorithms=['RS256'])

            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

@csrf_exempt
@api_view(['GET', 'POST'])
def powerline_list(request):
    #List Powerlines, or create a new powerline.
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        powerlines = Powerline.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(powerlines, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Powerline_Serializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/powerlines/?page=' + str(nextPage), 'prevlink': '/api/powerlines/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = Powerline_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def powerline_detail(request, id):
    #Retrieve, update or delete a powerline instance.
    try:
        powerline = Powerline.objects.get(id=id)
    except Powerline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Powerline_Serializer(powerline,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Powerline_Serializer(powerline,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        powerline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class drf_Powerline_View(viewsets.ModelViewSet):
    queryset = Powerline.objects.all()
    serializer_class = Powerline_Serializer

class drf_Measurement_View(viewsets.ModelViewSet):
    queryset = drf_Measurement.objects.all()
    serializer_class = drf_Measurement_Serializer
    filter_class = drf_Measurement_Filter
    #bbox_filter_field = 'point'
    #filter_backends = (InBBoxFilter, )
    #bbox_filter_include_overlapping = True # Optional

class drf_Timestamp_View(viewsets.ModelViewSet):
    queryset = drf_Timestamp.objects.all()
    serializer_class = drf_Timestamp_Serializer
    filter_class = drf_Timestamp_Filter

class drf_Jobid_View(viewsets.ModelViewSet):
    queryset = drf_Jobid.objects.all()
    serializer_class = drf_Jobid_Serializer
    filter_class = drf_Jobid_Filter


