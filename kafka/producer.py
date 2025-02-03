import json
import time

from confluent_kafka import Producer
from faker import Faker

fake = Faker()

conf = {'bootstrap.servers':'localhost:29092,localhost:29093,localhost:29094'}
producer = Producer(conf)
topic = 'sensor-data'

def generate_sensor_data():
    return {
        "timestamp": fake.date_time_this_year().isoformat(),
        "sensor_id": fake.bothify(text='Sensor-####'),
        "value": fake.pyfloat(min_value=20, max_value=30)
    }


def delivery_report(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
