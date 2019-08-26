import rest_framework_filters as filters
from .models import drf_Measurement, drf_Timestamp, drf_Jobid

class drf_Measurement_Filter(filters.FilterSet):
   class Meta:
        model = drf_Measurement
        fields = {
            'fid': ['exact'],
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

