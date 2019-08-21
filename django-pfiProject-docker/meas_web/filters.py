import rest_framework_filters as filters
from meas_web.models import Measurement

class Measurement_Filter(filters.FilterSet):
   class Meta:
      model = Measurement
      fields = {
          'bore_id': ['exact'],
          'job_id': ['exact'],
          'device_id': ['exact'],
          'chemical_id': ['exact'],
          'concentration': ['exact', 'lt', 'gt', 'lte', 'gte'],
          'date': ['exact', 'lt', 'gt', 'lte', 'gte'],
          'time': ['exact', 'lt', 'gt', 'lte', 'gte'],
          'status': ['exact'],
          'comment': ['exact']
      }

