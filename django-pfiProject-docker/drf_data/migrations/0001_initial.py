# Generated by Django 2.2.3 on 2019-08-14 13:17

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='jobid_Model',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False, verbose_name=10)),
                ('label', models.TextField(verbose_name=10)),
            ],
            options={
                'db_table': 'drf_data_jobid_model',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='testdatav_Model',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('device_id', models.TextField(verbose_name=10)),
                ('timestamp', models.DateTimeField()),
                ('job_id', models.TextField(verbose_name=10)),
                ('chem_id', models.TextField(verbose_name=10)),
            ],
            options={
                'db_table': 'drf_data_testdatav_model',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='timestamp_Model',
            fields=[
                ('id', models.DateTimeField(primary_key=True, serialize=False)),
                ('label', models.DateTimeField()),
            ],
            options={
                'db_table': 'drf_data_timestamp_model',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='fdr_18001_0_11_Model',
            fields=[
                ('fid', models.IntegerField(primary_key=True, serialize=False)),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('title', models.TextField(verbose_name=20)),
                ('powerline', models.TextField(verbose_name=50)),
                ('voltage', models.IntegerField()),
                ('service_date', models.CharField(choices=[('%m/%d/%Y', 'Month Day Year'), ('%m/%Y', 'Month Year')], max_length=10, verbose_name='Date Choice')),
            ],
        ),
        migrations.CreateModel(
            name='testdata_Model',
            fields=[
                ('fid', models.IntegerField(primary_key=True, serialize=False)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('device_id', models.TextField(verbose_name=10)),
                ('timestamp', models.DateTimeField()),
                ('job_id', models.TextField(verbose_name=10)),
                ('concentrat', models.IntegerField()),
                ('chem_id', models.TextField(verbose_name=10)),
                ('amb_temp', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rel_humid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('precip', models.IntegerField()),
                ('air_pressu', models.IntegerField()),
                ('wind_speed', models.IntegerField()),
                ('wind_direc', models.IntegerField()),
            ],
        ),
    ]
