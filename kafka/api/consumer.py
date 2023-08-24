import sys

from typing import Any, Callable
from abc import ABC, abstractmethod
from confluent_kafka import Consumer, TopicPartition, KafkaError


class KafkaConsumer:
    def __init__(
            self,
            bootstrap_servers: str,
            reports_topic: str,
            reports_ready_topic: str,
            timeout: float,
            group_id: str,
            enable_auto_commit: bool = False,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._reports_topic = reports_topic
        self._reports_ready_topic = reports_ready_topic
        self._timeout = timeout
        self._group_id = group_id
        self._enable_auto_commit = enable_auto_commit

        self._consumer: Consumer = self.__configure_consumer()

    def __configure_consumer(self) -> Consumer:

        conf = {
            'bootstrap.servers': self._bootstrap_servers,
            'group.id': self._group_id,
            'enable.auto.commit': self._enable_auto_commit,
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
    def reports_ready_topic(self) -> str:
        return self._reports_ready_topic

    @property
    def timeout(self) -> float:
        return self._timeout

    def __callback_print_assignment(self, consumer, partitions) -> None:
        sys.stdout.write(f'Assignment consumer {consumer} on partition {partitions}')

    def __subscribe_consumer(self, topic: str) -> None:
        self.consumer.subscribe([topic], on_assign=self.__callback_print_assignment)

    def retrieve_message_from_reports_topic(self) -> tuple[bytes, str]:

        self.__subscribe_consumer(self.reports_topic)

        try:
            while True:
                msg = self.consumer.poll(self.timeout)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        sys.stdout.write(f"Error: {msg.error().str()}")

                self.consumer.commit(message=msg)

                yield msg.key(), msg.value().decode('utf-8')

                sys.stdout.write(f'I received message into reports_topic with key {msg.key()}')
                self.wait_until_message_appears_in_reports_ready_topic(msg.key())

        except KeyboardInterrupt:
            sys.stderr.write('Завершение чтения сообщений из очереди.')

    def wait_until_message_appears_in_reports_ready_topic(self, key: bytes) -> None:

        self.__subscribe_consumer(self.reports_ready_topic)

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        sys.stdout.write(f"Error: {msg.error().str()}")

                if msg.key() == key:
                    sys.stdout.write(f'I received message in reports_READY_topic with key: {msg.key()}')
                    break

        except KeyboardInterrupt:
            sys.stderr.write('Завершение чтения сообщений из очереди.')