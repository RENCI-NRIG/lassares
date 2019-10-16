from __future__ import unicode_literals
import os
import jwt
import json
from functools import wraps
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from six.moves.urllib import request as req
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from meas_web.models import Measurement
from meas_web.serializers import Measurement_Serializer
from meas_web.filters import Measurement_Filter
from meas_web.forms import MeasurementForm

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
def measurement_list(request):
    #List  Measurement, or create a new Measurement.
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        measurements = Measurement.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(measurements, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Measurement_Serializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/measurements/?page=' + str(nextPage), 'prevlink': '/api/measurements/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = Measurement_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def measurement_detail(request, pk):
    #Retrieve, update or delete a measurement instance.
    try:
        measurement = Measurement.objects.get(pk=pk)
    except Measurement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Measurement_Serializer(measurement,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Measurement_Serializer(measrement, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        measurement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MeasDRF(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = Measurement_Serializer
    filter_class = Measurement_Filter

class MeasList(ListView):
    model = Measurement
    template_name = "meas_web/measurement_list.html"

class MeasChange(FormMixin, MultipleObjectMixin, View):
    model = Measurement
    form_class = MeasurementForm
    template_name = "meas_web/measurement_list.html"
    success_url = reverse_lazy('meas_web:measurement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        list_of_ids=request.POST.getlist('_selected_action')
        action=request.POST.get('action')
        print (list_of_ids)
        for obj in self.get_queryset():
            if str(obj.id) in list_of_ids:
                if action == 'delete':
                    return redirect(reverse_lazy('meas_web:measurement_delete',  kwargs={'pk': obj.id}))
        return redirect(self.get_success_url())

class MeasChangeList(LoginRequiredMixin, View):
    template_name = "meas_web/measurement_list.html"

    def get(self, request, *args, **kwargs):
        view = MeasList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MeasChange.as_view()
        return view(request, *args, **kwargs)

class MeasCreate(LoginRequiredMixin, CreateView):
    model = Measurement
    form_class = MeasurementForm
    success_url = reverse_lazy('meas_web:measurement_list')

class MeasUpdate(LoginRequiredMixin, UpdateView):
    model = Measurement
    form_class = MeasurementForm
    success_url = reverse_lazy('meas_web:measurement_list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if 'delete' in self.request.POST:
            return redirect(reverse_lazy('meas_web:measurement_delete',  kwargs={'pk': self.object.id}))
        form.save()
        return super().form_valid(form)

class MeasDelete(LoginRequiredMixin, DeleteView):
    model = Measurement
    success_url = reverse_lazy('meas_web:measurement_list')

@login_required
def index(request):
    return render(request, 'meas_web/index.html')
