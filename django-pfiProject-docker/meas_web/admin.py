# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.admin.sites import AdminSite
from meas_web.models import Measurement

from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget

import os

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'bore_id', 'device_id', 'chemical_id', 'concentration', 'date', 'time', 'status', 'comment', 'geom')
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(Measurement, MeasurementAdmin)
