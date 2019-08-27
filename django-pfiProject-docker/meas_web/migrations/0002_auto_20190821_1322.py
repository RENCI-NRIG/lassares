# Generated by Django 2.2.3 on 2019-08-21 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meas_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='bore_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chemical_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='concentration',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='device_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='job_id',
            field=models.CharField(max_length=20),
        ),
    ]