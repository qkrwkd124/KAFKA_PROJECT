import json
import time
import logging
from typing import Dict,Any

from confluent_kafka import Producer,Message
from faker import Faker

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

fake = Faker()

conf:Dict[str,Any] = {
    'bootstrap.servers':'localhost:29092',
    'acks':'all',
    'retries':5,
    'linger.ms':5
}


# producer = KafkaProducer(
#     bootstrap_servers = ['localhost:29092'],
#     value_serializer = lambda v: json.dumps(v).encode('utf-8'),
#     acks='all',
#     retries=5,
#     linger_ms=5
# )
# producer = Producer(conf)

producer:Producer = Producer(conf)
topic:str = 'sensor-data'

def generate_sensor_data():
    return {
        "timestamp": fake.date_time_this_year().isoformat(),
        "sensor_id": fake.bothify(text='Sensor-####'),
        "value": fake.pyfloat(min_value=20, max_value=30)
    }

def delivery_report(err:Any,msg:Message)-> None:
    if err is not None:
        logger.error("Message delivery failed: %s", err)
    else:
         # 전송한 메시지의 value는 바이트형태이므로 다시 디코딩 후 JSON 로드
        try :
            msg_data = json.loads(msg.value().decode('utf-8'))
        except Exception :
            msg_data = msg.value()
        logger.info("Message delivered to %s [%d] at offset %d",
                    msg.topic(), msg.partition(), msg.offset())


while True :
    data = generate_sensor_data()
    
    try :
        # produce() 함수로 메시지를 전송합니다.
        # value는 JSON 문자열로 변환한 후 UTF-8 인코딩 처리합니다.
        producer.produce(topic,value=json.dumps(data).encode('utf-8'),callback=delivery_report)
        # 메시지를 전송하고 버퍼에 넣습니다.
        producer.poll(0)
    except Exception as e :
        logger.error("Failed to send message %s, error: %s", data, e)
    
    time.sleep(5) # 1초마다 메시지를 전송