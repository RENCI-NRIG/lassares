from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.db import models as omodels

# Create your models here.
STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published')
)

# Create your models here.
class Powerline(models.Model):
    #id = models.IntegerField(primary_key=True)
    geom = models.MultiLineStringField(null=False)
    title = models.TextField(50,null=False)
    powerline = models.TextField(20,null=False)
    voltage = models.IntegerField(null=False)
    service_date = models.TextField(10,null=True)
    #MONTH_DAY_YEAR = '%m/%d/%Y'
    #MONTH_YEAR = '%m/%Y'
    #DATE_CHOICE= (
    #              (MONTH_DAY_YEAR, 'Month Day Year'),
    #              (MONTH_YEAR, 'Month Year')
    #             )
    #service_date = models.CharField('Date Choice', choices=DATE_CHOICE,  max_length=10, null=False)


class drf_Measurement(models.Model):
    id = models.IntegerField(primary_key=True)
    bore_id = models.CharField(max_length=20)
    job_id = models.CharField(max_length=20)
    device_id = models.CharField(max_length=20)
    chemical_id = models.CharField(max_length=20)
    concentration = models.CharField(max_length=20)
    timestamp = models.DateTimeField(null=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    comment = models.CharField(max_length=1000, null=True, default="")
    geom = models.PointField(null=False)

    class Meta:
        managed = False
        db_table = "drf_measurement"

class drf_Timestamp(omodels.Model):
    id = models.DateTimeField(null=False,primary_key=True)
    label = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = "drf_timestamp"

class drf_Jobid(omodels.Model):
    id = models.TextField(10,null=False,primary_key=True)
    label = models.TextField(10,null=False)

    class Meta:
        managed = False
        db_table = "drf_jobid"

