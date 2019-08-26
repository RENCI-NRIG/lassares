from rest_framework_gis.serializers import GeoFeatureModelSerializer
from meas_web.models import Measurement
from drf_queryfields import QueryFieldsMixin

class Measurement_Serializer(QueryFieldsMixin, GeoFeatureModelSerializer):
    class Meta:
        model = Measurement
        geo_field = 'geom'
        fields = ('bore_id', 'job_id', 'device_id', 'chemical_id', 'concentration',
                  'date', 'time', 'status', 'comment')

