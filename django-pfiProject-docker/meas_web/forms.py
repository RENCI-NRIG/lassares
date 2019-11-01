from meas_web.models import Measurement
from django.contrib.admin import widgets
from django.forms import ModelForm

class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ('bore_id', 'job_id', 'device_id', 'chemical_id', 'concentration', 'date', 'time', 'status', 'comment', 'geom')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MeasurementForm, self).__init__(*args, **kwargs)

