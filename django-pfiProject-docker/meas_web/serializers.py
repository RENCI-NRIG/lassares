from rest_framework_gis.serializers import GeoFeatureModelSerializer
from meas_web.models import mscnt, gcmv
from drf_queryfields import QueryFieldsMixin

class mscnt_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = mscnt
        geo_field = 'geom'
        fields = ('id', 'job_id', 'bore_id', 'instrument', 'chemical_id', 'measurement_value',
                  'units', 'date', 'time', 'status', 'comment')

class gcmv_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = gcmv
        geo_field = 'geom'
        fields = ('id', 'job_id', 'bore_id', 'instrument', 'chemical_id', 'measurement_value',
                  'units', 'date', 'time', 'status', 'comment')




