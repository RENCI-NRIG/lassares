# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.admin.sites import AdminSite
from measWeb.models import Measurement

from kafka import KafkaProducer
import os

def publish_message(producer_instance, topic_name, value):
    try:
        #value_bytes=bytes(value)
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message' + str(ex))

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=[os.getenv('KAFKA_HOST', 'localhost:9092')], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

def push_measurement_to_elk_stack(modeladmin, request, queryset):
    print ("I am here")
    producer = connect_kafka_producer()
    for obj in queryset:
        publish_message(producer, 'pft', obj.toString())
        obj.status='p'
        obj.save()

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('jobId', ,'boreId', 'deviceId', 'chemicalId', 'concentration', 'date', 'time', 'status', 'comment','position')
    actions = [push_measurement_to_elk_stack]

admin.site.register(Measurement, MeasurementAdmin)
