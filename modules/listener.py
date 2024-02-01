""" Entry point for Kafka consumer. """
import os
import sys
import signal

sys.path.append(
    os.path.join(
        os.getcwd()
    )
)

from kafka import load_kafka_settings
from consumer import AppConsumer
from modules.logs.handlers import LokiLogger


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':

    bootstrap_server, reports_topic, sasl_username, sasl_password = load_kafka_settings()

    try:
        with LokiLogger('Start consumer'):
            with AppConsumer(
                    bootstrap_server=bootstrap_server,
                    reports_topic=reports_topic,
                    consumer_timeout=1.0,
                    producer_timeout=1000,
                    group_id='none',
                    sasl_username=sasl_username,
                    sasl_password=sasl_password,
            ):
                while True:
                    pass
    except KeyboardInterrupt:
        killer = GracefulKiller()
        sys.exit(0)
