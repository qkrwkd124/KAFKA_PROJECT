# AdminClient는 Kafka 클러스터와 상호작용하기 위해 사용되는 Kafka의 관리 API
from confluent_kafka.admin import NewPartitions, AdminClient, NewTopic


# Kafka AdminClient 생성
# admin_client = AdminClient({'bootstrap.servers':'localhost:29092,localhost:29093,localhost:29094'})
admin_client = AdminClient({'bootstrap.servers':'localhost:29092'})

# 토픽정보
def get_topic_info(topic_name:str) -> None :
    metadata = admin_client.list_topics(timeout=5)
    topic_metadata = metadata.topics.get(topic_name)

    if topic_metadata:
        print(f"Topic: {topic_metadata.topic}")
        print(f"Partitions: {len(topic_metadata.partitions)}")
    else:
        print(f"Topic '{topic_name}' does not exist.")

# 토픽생성
def create_topic(topic_name:str) -> None :

    new_topic = NewTopic(
        topic=topic_name,       # 토픽이름
        num_partitions=3,       # 파티션 수
        replication_factor=1    # 복제 계수
    )
    try :
        futures = admin_client.create_topics([new_topic])
        # 각 토픽 생성 Future의 결과를 확인합니다.
        for topic, future in futures.items():
            try:
                # future.result()를 호출하여 작업 완료까지 기다립니다.
                future.result(timeout=10)
                print(f"Topic '{topic}' created successfully!")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
        
        # print(f"Topic '{topic_name}' created successfully!")
    except Exception as e :
        print(e)


# 토픽삭제
def delete_topic(topic_name:str) -> None :

    try :
        admin_client.delete_topics([topic_name])
        print(f"Topic '{topic_name}' deleted successfully!")
    except Exception as e :
        print(e)


if __name__ == '__main__' :

    # topic_name = "LogTopic"
    topic_name = "sensor-data"
    
    create_topic(topic_name)
    # delete_topic(topic_name)
    # get_topic_info(topic_name)