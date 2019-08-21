from meas_web.models import Measurement
from kafka import KafkaProducer
import os

def publish_message(producer_instance, topic_name, value):
    try:
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message' + str(ex))
        return False
    return True

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=[os.getenv('KAFKA_HOST', 'localhost:9092')], api_version=(0, 10))
        print('bootstrap_servers' + os.getenv('KAFKA_HOST'))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

def push_measurement_to_elk_stack(meas):
    print ("Push measurement request received")
    print (meas.toString())
    producer = connect_kafka_producer()
    retVal = False
    if producer is not None:
        print ("Push measurement to kafka")
        retVal = publish_message(producer, 'pft', meas.toString())
    return retVal
