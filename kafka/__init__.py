import os
from .api import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv


load_dotenv()


def load_kafka_settings() -> tuple:

    KAFKA_BROKER = os.environ.get('KAFKA_BROKER', None)
    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', None)

    return KAFKA_BROKER, KAFKA_TOPIC