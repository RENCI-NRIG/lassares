from rest_framework import viewsets
from .serializers import fdr_18001_0_11_Serializer, testdata_Serializer, testdatav_Serializer, timestamp_Serializer, jobid_Serializer
from .models import fdr_18001_0_11_Model, testdata_Model, testdatav_Model, timestamp_Model, jobid_Model
from .filters import TestdataFilter, TestdatavFilter, TimestampFilter, JobidFilter

# Create your views here.
class fdr_18001_0_11_View(viewsets.ReadOnlyModelViewSet):
    queryset = fdr_18001_0_11_Model.objects.all()
    serializer_class = fdr_18001_0_11_Serializer

class testdata_View(viewsets.ModelViewSet):
    queryset = testdata_Model.objects.all()
    serializer_class = testdata_Serializer
    filter_class = TestdataFilter

class testdatav_View(viewsets.ModelViewSet):
    queryset = testdatav_Model.objects.all()
    serializer_class = testdatav_Serializer
    filter_class = TestdatavFilter

class timestamp_View(viewsets.ModelViewSet):
    queryset = timestamp_Model.objects.all()
    serializer_class = timestamp_Serializer
    filter_class = TimestampFilter

class jobid_View(viewsets.ModelViewSet):
    queryset = jobid_Model.objects.all()
    serializer_class = jobid_Serializer
    filter_class = JobidFilter


