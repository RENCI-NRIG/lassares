from meas_web.models import Measurement
from django.contrib.admin import widgets
from django.forms import ModelForm
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget

class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ('bore_id', 'job_id', 'device_id', 'chemical_id', 'concentration', 'date', 'time', 'status', 'comment', 'geometry')
        widgets = {
            'geometry': GooglePointFieldWidget,
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MeasurementForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        self.fields['time'].widget = widgets.AdminTimeWidget()

