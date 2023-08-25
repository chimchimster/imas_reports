import sys

from threading import Thread, Event
from typing import Any, Callable
from abc import ABC, abstractmethod
from confluent_kafka import Consumer, TopicPartition, KafkaError


class KafkaConsumer:
    def __init__(
            self,
            bootstrap_server: str,
            reports_topic: str,
            reports_ready_topic: str,
            timeout: float,
            group_id: str,
            enable_auto_commit: bool = False,
    ) -> None:
        self._bootstrap_server = bootstrap_server
        self._reports_topic = reports_topic
        self._reports_ready_topic = reports_ready_topic
        self._timeout = timeout
        self._group_id = group_id
        self._enable_auto_commit = enable_auto_commit

        self._consumer: Consumer = self.__configure_consumer()

    def __configure_consumer(self) -> Consumer:

        conf = {
            'bootstrap.servers': self.bootstrap_server,
            'group.id': self.group_id,
            'enable.auto.commit': self.enable_auto_commit,
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
        print(f'Assignment consumer {consumer} on partition {partitions}')

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
                        sys.stdout.write(f"Error: {msg.error().str()}")

                self.consumer.commit(message=msg)
                yield msg.key(), msg.value().decode('utf-8')

        except KeyboardInterrupt:
            sys.stderr.write('Завершение чтения сообщений из брокера сообщений.')

    def wait_until_message_appears_in_reports_ready_topic(self, key: bytes) -> None:

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

                print(msg.key())

                if msg.key() == key:
                    print(msg.key(), msg.value())
                    print(f'I received message in reports_READY_topic with key: {msg.key()}')
                    break

        except KeyboardInterrupt:
            sys.stderr.write('Завершение чтения сообщений из брокера сообщений.')