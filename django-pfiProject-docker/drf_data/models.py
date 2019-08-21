from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.db import models as omodels

# Create your models here.
STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published')
)

# Create your models here.
class fdr_18001_0_11_Model(models.Model):
    fid = models.IntegerField(primary_key=True)
    geometry = models.MultiLineStringField(null=False)
    title = models.TextField(20,null=False)
    powerline = models.TextField(50,null=False)
    voltage = models.IntegerField(null=False)
    MONTH_DAY_YEAR = '%m/%d/%Y'
    MONTH_YEAR = '%m/%Y'
    DATE_CHOICE= (
                  (MONTH_DAY_YEAR, 'Month Day Year'),
                  (MONTH_YEAR, 'Month Year')
                 )
    service_date = models.CharField('Date Choice', choices=DATE_CHOICE,  max_length=10, null=False)

class testdata_Model(models.Model):
    fid = models.IntegerField(primary_key=True)
    geometry = models.PointField(null=False)
    device_id = models.TextField(10,null=False)
    timestamp = models.DateTimeField(null=False)
    job_id = models.TextField(10,null=False)
    concentrat = models.IntegerField(null=False)
    chem_id = models.TextField(10,null=False)
    amb_temp = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    rel_humid = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    precip = models.IntegerField(null=False)
    air_pressu = models.IntegerField(null=False)
    wind_speed = models.IntegerField(null=False)
    wind_direc = models.IntegerField(null=False)

class testdatav_Model(omodels.Model):
    id = models.IntegerField(primary_key=True)
    device_id = models.TextField(10,null=False)
    timestamp = models.DateTimeField(null=False)
    job_id = models.TextField(10,null=False)
    chem_id = models.TextField(10,null=False)

    class Meta:
        managed = False
        db_table = "drf_data_testdatav_model"

class timestamp_Model(omodels.Model):
    id = models.DateTimeField(null=False,primary_key=True)
    label = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = "drf_data_timestamp_model"

class jobid_Model(omodels.Model):
    id = models.TextField(10,null=False,primary_key=True)
    label = models.TextField(10,null=False)

    class Meta:
        managed = False
        db_table = "drf_data_jobid_model"

