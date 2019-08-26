#from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer
from .models import fdr_18001_0_11, drf_Measurement, drf_Timestamp, drf_Jobid
from drf_queryfields import QueryFieldsMixin

class fdr_18001_0_11_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = fdr_18001_0_11
        geo_field = 'geom'
        id_field = 'fid'
        fields = ('fid', 'title', 'powerline', 'voltage', 'service_date')

class drf_Measurement_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = drf_Measurement
        geo_field = 'geom'
        id_field = 'fid'
        fields = ('fid', 'bore_id', 'job_id', 'device_id', 'chemical_id', 'concentration',
                  'timestamp', 'status', 'comment')

class drf_Timestamp_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = drf_Timestamp
        id_field = 'id'
        fields = ('__all__')

class drf_Jobid_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = drf_Jobid
        id_field = 'id'
        fields = ('__all__')

