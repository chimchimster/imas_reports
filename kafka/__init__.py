import os
from .api import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv


load_dotenv()


def load_kafka_settings() -> tuple:

    KAFKA_BROKER = os.environ.get('KAFKA_BROKER', None)
    KAFKA_TOPIC_REPORTS = os.environ.get('KAFKA_TOPIC_REPORTS', None)
    KAFKA_TOPIC_REPORTS_READY = os.environ.get('KAFKA_TOPIC_REPORTS_READY', None)


    return KAFKA_BROKER, KAFKA_TOPIC_REPORTS, KAFKA_TOPIC_REPORTS_READY