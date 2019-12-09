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
from meas_web.models import mscnt, gcmv
from meas_web.serializers import mscnt_Serializer, gcmv_Serializer

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
def mscnt_list(request):
    #List Mass Spectrometer Count, or create a new Measurement.
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        measurements = mscnt.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(measurements, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = mscnt_Serializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/mscnt/?page=' + str(nextPage), 'prevlink': '/api/mscnt/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = mscnt_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def mscnt_detail(request, id):
    #Retrieve, update or delete a Mass Spectrometer Count instance.
    try:
        measurement = mscnt.objects.get(id=id)
    except mscnt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = mscnt_Serializer(measurement,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = mscnt_Serializer(measurement,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        measurement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
def gcmv_list(request):
    #List Gas Chromatograph Millivolt, or create a new Measurement.
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        measurements = gcmv.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(measurements, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = gcmv_Serializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/gcmv/?page=' + str(nextPage), 'prevlink': '/api/gcmv/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = gcmv_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def gcmv_detail(request, id):
    #Retrieve, update or delete a Gas Chromatograph Millivolt instance.
    try:
        measurement = gcmv.objects.get(id=id)
    except gcmv.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = gcmv_Serializer(measurement,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = gcmv_Serializer(measurement,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        measurement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

