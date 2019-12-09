# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models

# Create your models here.
STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published')
)

class mscnt(models.Model):
    bore_id = models.CharField(max_length=20)
    job_id = models.CharField(max_length=20)
    instrument = models.CharField(max_length=20)
    chemical_id = models.CharField(max_length=20)
    measurement_value = models.CharField(max_length=20)
    units = models.CharField(max_length=20)
    date = models.DateField('date')
    time = models.TimeField('time')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    comment = models.CharField(max_length=1000, null=True, default="")
    geom = models.PointField(null=False)

    def toString(self):
        #{DeviceX0001 2018-05-17 09:21:20.3 51.517016 -0.144819} {JobY001 CH5OH 10000.0 ppm}
        retVal = "{" + self.instrument + " " +  str(self.date) + " " + str(self.time) + "} {" + self.bore_id + " " + self.job_id + " " + self.chemical_id + " " + self.measurement_value + " " + self.units + " " + self.geom + "}"
        return retVal

class gcmv(models.Model):
    bore_id = models.CharField(max_length=20)
    job_id = models.CharField(max_length=20)
    instrument = models.CharField(max_length=20)
    chemical_id = models.CharField(max_length=20)
    measurement_value = models.CharField(max_length=20)
    units = models.CharField(max_length=20)
    date = models.DateField('date')
    time = models.TimeField('time')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    comment = models.CharField(max_length=1000, null=True, default="")
    geom = models.PointField(null=False)

    def toString(self):
        #{DeviceX0001 2018-05-17 09:21:20.3 51.517016 -0.144819} {JobY001 CH5OH 10000.0 ppm}
        retVal = "{" + self.instrument + " " +  str(self.date) + " " + str(self.time) + "} {" + self.bore_id + " " +     self.job_id + " " + self.chemical_id + " " + self.measurement_value + " " + self.units + " " + self.geom + "}"
        return retVal

