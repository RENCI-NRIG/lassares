#from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer
from .models import fdr_18001_0_11_Model, testdata_Model, testdatav_Model, timestamp_Model, jobid_Model
from drf_queryfields import QueryFieldsMixin

class fdr_18001_0_11_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = fdr_18001_0_11_Model
        geo_field = 'geometry'
        id_field = 'fid'
        fields = ('fid', 'title', 'powerline', 'voltage', 'service_date')

class testdata_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = testdata_Model
        geo_field = 'geometry'
        id_field = 'fid'
        fields = ('fid', 'device_id', 'timestamp', 'job_id', 'concentrat', 'chem_id',
                  'amb_temp', 'rel_humid', 'precip', 'air_pressu', 'wind_speed', 'wind_direc')

class testdatav_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = testdatav_Model
        id_field = 'id'
        fields = ('id', 'device_id', 'timestamp', 'job_id', 'chem_id')

class timestamp_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = timestamp_Model
        id_field = 'id'
        fields = ('__all__')

class jobid_Serializer(QueryFieldsMixin, ModelSerializer):
    class Meta:
        model = jobid_Model
        id_field = 'id'
        fields = ('__all__')

