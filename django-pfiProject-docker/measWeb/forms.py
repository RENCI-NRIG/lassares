from django.forms import ModelForm
from measWeb.models import Measurement
from django.contrib.admin import widgets

class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ['id', 'jobId', 'boreId', 'deviceId', 'chemicalId', 'concentration', 'date', 'time', 'status', 'comment','position']
    def __init__(self, *args, **kwargs):
        super(MeasurementForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        self.fields['time'].widget = widgets.AdminTimeWidget()
