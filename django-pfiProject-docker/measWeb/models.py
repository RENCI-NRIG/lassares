# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from geoposition import Geoposition
from geoposition.fields import GeopositionField


# Create your models here.
STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published')
)

class Measurement(models.Model):
    boreId = models.CharField(max_length=200)
    jobId = models.CharField(max_length=200)
    deviceId = models.CharField(max_length=200)
    chemicalId = models.CharField(max_length=200)
    concentration = models.CharField(max_length=200)
    date = models.DateField('date')
    time = models.TimeField('time')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    comment = models.CharField(max_length=1000, null=True, default="")
    position = GeopositionField(default=('0,0'))

    def toString(self):
        #{DeviceX0001 2018-05-17 09:21:20.3 51.517016 -0.144819} {JobY001 CH5OH 10000.0 ppm}
        retVal = "{" + self.deviceId + " " +  str(self.date) + " " + str(self.time) + " " + str(self.position.latitude) + " " + str(self.position.longitude) + "} {" + self.boreId + " " + self.jobId + " " + self.chemicalId + " " + self.concentration + " ppm}"
        return retVal
