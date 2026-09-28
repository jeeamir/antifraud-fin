import json
import os
from aiokafka import AIOKafkaProducer


def create_kafka_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS',
            'localhost:9092'
        ),

        value_serializer=lambda value: json.dumps(
            value,
            default=str,
        ).encode('utf-8'),
    )

