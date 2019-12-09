#from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer
from .models import Powerline, drf_mscnt, drf_mscnt_Timestamp, drf_mscnt_Jobid, drf_gcmv, drf_gcmv_Timestamp, drf_gcmv_Jobid
from drf_queryfields import QueryFieldsMixin

class Powerline_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = Powerline
        geo_field = 'geom'
        id_field = 'id'
        fields = ('id', 'title', 'powerline', 'voltage', 'service_date')

class drf_mscnt_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = drf_mscnt
        geo_field = 'geom'
        id_field = 'id'
        fields = ('id', 'bore_id', 'job_id', 'instrument', 'chemical_id', 'measurement_value',
                  'units', 'timestamp', 'status', 'comment')

class drf_mscnt_Timestamp_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = drf_mscnt_Timestamp
        id_field = 'id'
        fields = ('__all__')

class drf_mscnt_Jobid_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = drf_mscnt_Jobid
        id_field = 'id'
        fields = ('__all__')

class drf_gcmv_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = drf_gcmv
        geo_field = 'geom'
        id_field = 'id'
        fields = ('id', 'bore_id', 'job_id', 'instrument', 'chemical_id', 'measurement_value',
                  'units', 'timestamp', 'status', 'comment')

class drf_gcmv_Timestamp_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = drf_gcmv_Timestamp
        id_field = 'id'
        fields = ('__all__')

class drf_gcmv_Jobid_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = drf_gcmv_Jobid
        id_field = 'id'
        fields = ('__all__')

