import rest_framework_filters as filters
from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import InBBoxFilter
from .models import drf_Measurement, drf_Timestamp, drf_Jobid

class geo_Measurement_Filter(GeoFilterSet):
   bbox_filter_field = 'point'
   filter_backends = (InBBoxFilter, )
   bbox_filter_include_overlapping = True # Optional

class drf_Measurement_Filter(filters.FilterSet):
   geo_Measurement = filters.RelatedFilter(filterset=geo_Measurement_Filter, )
   class Meta:
        model = drf_Measurement
        fields = {
            'id': ['exact'],
            'bore_id': ['exact'],
            'job_id': ['exact'],
            'device_id': ['exact'],
            'chemical_id': ['exact'],
            'concentration':  ['exact', 'lt', 'gt', 'lte', 'gte'],
            'timestamp': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'status': ['exact'],
            'comment': ['exact']
        }

class drf_Timestamp_Filter(filters.FilterSet):
   class Meta:
        model = drf_Timestamp
        fields = {
            'id': ['exact'],
            'label': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }

class drf_Jobid_Filter(filters.FilterSet):
   class Meta:
        model = drf_Jobid
        fields = {
            'id': ['exact'],
            'label': ['exact'],
        }

