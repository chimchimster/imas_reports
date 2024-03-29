from confluent_kafka import Consumer, KafkaError
from modules.logs.handlers import LokiLogger


class KafkaConsumer:
    def __init__(
            self,
            bootstrap_server: str,
            reports_topic: str,
            timeout: float,
            group_id: str,
            enable_auto_commit: bool = False,
            sasl_username: str = None,
            sasl_password: str = None,
    ) -> None:
        self._bootstrap_server = bootstrap_server
        self._reports_topic = reports_topic
        self._timeout = timeout
        self._group_id = group_id
        self._enable_auto_commit = enable_auto_commit
        self._sasl_username = sasl_username
        self._sasl_password = sasl_password

        self._consumer: Consumer = self.__configure_consumer()

    def __configure_consumer(self) -> Consumer:

        conf = {
            'bootstrap.servers': self.bootstrap_server,
            'group.id': self.group_id,
            'enable.auto.commit': self.enable_auto_commit,
            'auto.offset.reset': 'latest',
            'security.protocol': 'SASL_PLAINTEXT',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': self._sasl_username,
            'sasl.password': self._sasl_password,
        }

        cnsmr: Consumer = Consumer(conf)

        return cnsmr

    @property
    def consumer(self) -> Consumer:
        return self._consumer

    @property
    def reports_topic(self) -> str:
        return self._reports_topic

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def bootstrap_server(self) -> str:
        return self._bootstrap_server

    @property
    def group_id(self) -> str:
        return self._group_id

    @property
    def enable_auto_commit(self) -> bool:
        return self._enable_auto_commit

    @staticmethod
    def __callback_print_assignment(consumer, partitions) -> None:
        if partitions:
            with LokiLogger('Assignment consumer', str(consumer), *partitions):
                pass

    def __subscribe_consumer(self, topics: list[str]) -> None:

        self.consumer.subscribe(topics, on_assign=self.__callback_print_assignment)

    def retrieve_message_from_reports_topic(self) -> tuple[bytes, str]:

        self.__subscribe_consumer(
            [
                self.reports_topic,
             ],
        )

        try:
            while True:
                msg = self.consumer.poll(self.timeout)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        with LokiLogger('Broker retrieving message error', msg.error().str()):
                            pass

                self.consumer.commit(message=msg)
                yield msg.key(), msg.value().decode('utf-8')

        except KeyboardInterrupt:
            with LokiLogger('Ending consume messages up from broker'):
                pass
