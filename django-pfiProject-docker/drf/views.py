from rest_framework import viewsets
from .serializers import fdr_18001_0_11_Serializer, drf_Measurement_Serializer, drf_Timestamp_Serializer, drf_Jobid_Serializer
from .models import fdr_18001_0_11, drf_Measurement, drf_Timestamp, drf_Jobid
from .filters import drf_Measurement_Filter, drf_Timestamp_Filter, drf_Jobid_Filter

# Create your views here.
class fdr_18001_0_11_View(viewsets.ReadOnlyModelViewSet):
    queryset = fdr_18001_0_11.objects.all()
    serializer_class = fdr_18001_0_11_Serializer

class drf_Measurement_View(viewsets.ModelViewSet):
    queryset = drf_Measurement.objects.all()
    serializer_class = drf_Measurement_Serializer
    filter_class = drf_Measurement_Filter

class drf_Timestamp_View(viewsets.ModelViewSet):
    queryset = drf_Timestamp.objects.all()
    serializer_class = drf_Timestamp_Serializer
    filter_class = drf_Timestamp_Filter

class drf_Jobid_View(viewsets.ModelViewSet):
    queryset = drf_Jobid.objects.all()
    serializer_class = drf_Jobid_Serializer
    filter_class = drf_Jobid_Filter


