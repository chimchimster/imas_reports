import os
from dotenv import load_dotenv


load_dotenv()


def load_kafka_settings() -> tuple:

    KAFKA_BROKER = os.environ.get('KAFKA_BROKER')
    KAFKA_TOPIC_REPORTS = os.environ.get('KAFKA_TOPIC_REPORTS')
    KAFKA_TOPIC_REPORTS_READY = os.environ.get('KAFKA_TOPIC_REPORTS_READY')
    KAFKA_SASL_USERNAME = os.environ.get('KAFKA_SASL_USERNAME')
    KAFKA_SASL_PASSWORD = os.environ.get('KAFKA_SASL_PASSWORD')

    return KAFKA_BROKER, KAFKA_TOPIC_REPORTS, KAFKA_TOPIC_REPORTS_READY, KAFKA_SASL_USERNAME, KAFKA_SASL_PASSWORD
