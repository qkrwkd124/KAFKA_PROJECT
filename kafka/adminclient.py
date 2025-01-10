# AdminClient는 Kafka 클러스터와 상호작용하기 위해 사용되는 Kafka의 관리 API
from confluent_kafka.admin import NewPartitions, AdminClient, NewTopic


# Kafka AdminClient 생성
admin_client = AdminClient({'bootstrap.servers':'localhost:29092,localhost:29093,localhost:29094'})

def get_topic_info(topic_name:str) -> None :
    metadata = admin_client.list_topics(timeout=5)
    topic_metadata = metadata.topics.get(topic_name)

    if topic_metadata:
        print(f"Topic: {topic_metadata.topic}")
        print(f"Partitions: {len(topic_metadata.partitions)}")
    else:
        print("Topic 'example_topic' does not exist.")


def create_topic(topic_name:str) -> None :

    new_topic = NewTopic(
        topic=topic_name,       # 토픽이름
        num_partitions=3,       # 파티션 수
        replication_factor=1    # 복제 계수
    )
    
    admin_client.create_topics([new_topic])

    print("Topic 'example_topic' created successfully!")

def delete_topic(topic_name:str) -> None :

    admin_client.delete_topic([topic_name])
    
    print("Topic 'example_topic' deleted successfully!")
    

if __name__ == '__main__' :

    topic_name = "LogTopic"
    # create_topic()
    get_topic_info(topic_name)