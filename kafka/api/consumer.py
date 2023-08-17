import sys
from abc import ABC, abstractmethod
from typing import Any

from confluent_kafka import Consumer, TopicPartition, KafkaError


class KafkaConsumer(ABC):
    def __init__(
            self,
            bootstrap_servers: str,
            topic: str,
            timeout: float,
            group_id: str,
            enable_auto_commit: bool = False,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
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
    def topic(self) -> str:
        return self._topic

    @property
    def timeout(self) -> float:
        return self._timeout

    def __assign_consumer_to_topic_and_partition(self) -> None:
        self.consumer.assign([TopicPartition(self.topic, 0), ])

    def retrieve_message(self) -> tuple[bytes, str]:

        self.__assign_consumer_to_topic_and_partition()

        while True:
            msg = self.consumer.poll(self.timeout)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    sys.stdout.write(f"Error: {msg.error().str()}")

            yield msg.key(), msg.value().decode('utf-8')

    @abstractmethod
    def consume(self) -> tuple[str]:
        """ Метод обрабатывающий сообщения в очереди задач. """

    @abstractmethod
    def process_task(self, key: bytes, value: str) -> Any:
        """ Метод обрабатывабщий операции полученные из очереди задач. """
