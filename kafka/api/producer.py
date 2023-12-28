from confluent_kafka import Producer, KafkaError
from modules.logs.handlers import LokiLogger


class KafkaProducer:
    def __init__(
            self,
            bootstrap_server: str,
            topic: str,
            timeout: int,
            sasl_username: str,
            sasl_password: str,
    ) -> None:
        self._bootstrap_server = bootstrap_server
        self._topic = topic
        self._timeout = timeout
        self._sasl_username = sasl_username
        self._sasl_password = sasl_password

        self._producer = self.__configure_producer()

    def __configure_producer(self) -> Producer:

        conf = {
            'bootstrap.servers': self.bootstrap_server,
            'security.protocol': 'SASL_PLAINTEXT',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': self._sasl_username,
            'sasl.password': self._sasl_password,
        }

        prdcr: Producer = Producer(conf)

        return prdcr

    @property
    def bootstrap_server(self) -> str:
        return self._bootstrap_server

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def producer(self) -> Producer:
        return self._producer

    @property
    def timeout(self) -> float:
        return self._timeout

    def producer_poll(self) -> None:
        self.producer.poll(self.timeout)

    def producer_flush(self) -> None:
        self.producer.flush()

    def send_message(self, key: str, message: bytes) -> None:
        """ Метод кладет в очередь задач сообщение
        с уникальным идентификатором по которому определяется партиция."""

        def on_delivery(error: KafkaError, msg: str) -> None:
            """ Колбэк - доставлено ли сообщение. """

            if error is not None:
                with LokiLogger(
                        'Error while sending message into broker',
                        report_id=key,
                        error=error,
                ):
                    pass
            else:
                with LokiLogger(
                        'Success on sending message into broker',
                        report_id=key,
                        broker_partition=msg.partition(),
                        broker_topic=msg.topic()
                ):
                    pass

        with LokiLogger('Producing message into broker', report_id=key):
            try:
                self.producer.produce(
                    topic=self.topic,
                    key=key,
                    value=message,
                    callback=on_delivery,
                )
            except KafkaError:
                raise KafkaError
