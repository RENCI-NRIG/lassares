#from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer
from .models import Powerline, drf_Measurement, drf_Timestamp, drf_Jobid
from drf_queryfields import QueryFieldsMixin

class Powerline_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = Powerline
        geo_field = 'geom'
        id_field = 'id'
        fields = ('id', 'title', 'powerline', 'voltage', 'service_date')

class drf_Measurement_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = drf_Measurement
        geo_field = 'geom'
        id_field = 'id'
        fields = ('id', 'bore_id', 'job_id', 'device_id', 'chemical_id', 'concentration',
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

