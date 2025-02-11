import json
import time
import logging

from confluent_kafka import Producer
from kafka import KafkaProducer
from faker import Faker

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

fake = Faker()

conf = {'bootstrap.servers':'localhost:29092,localhost:29093,localhost:29094'}
producer = KafkaProducer(
    bootstrap_servers = ['localhost:29092','localhost:29093','localhost:29094'],
    value_serializer = lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=5,
    linger_ms=5
)
# producer = Producer(conf)
topic = 'sensor-data'

def generate_sensor_data():
    return {
        "timestamp": fake.date_time_this_year().isoformat(),
        "sensor_id": fake.bothify(text='Sensor-####'),
        "value": fake.pyfloat(min_value=20, max_value=30)
    }


while True :
    data = generate_sensor_data()
    
    try :
        future = producer.send(topic,value=data)
        record_metadata = future.get(timeout=10)
        logger.info("Sent: %s, topic: %s, partition: %d, offset: %d",
                    data, record_metadata.topic, record_metadata.partition, record_metadata.offset)
    except Exception as e :
        logger.error("Failed to send message %s, error: %s", data, e)
    
    time.sleep(1)