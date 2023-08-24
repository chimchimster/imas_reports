import json

from threading import Thread
from tasker import TaskSelector
from utils import RemoveDirsMixin
from typing import Any, Callable, ContextManager, Tuple
from kafka import load_kafka_settings, KafkaConsumer, KafkaProducer


class KafkaManager(RemoveDirsMixin):

    def __init__(
            self,
            bootstrap_servers: str,
            reports_topic: str,
            reports_ready_topic: str,
            producer_timeout: int,
            consumer_timeout: float,
            group_id: str,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._reports_topic = reports_topic
        self._reports_ready_topic = reports_ready_topic
        self._producer_timeout = producer_timeout
        self._consumer_timeout = consumer_timeout
        self._group_id = group_id

    @property
    def bootstrap_servers(self):
        return self._bootstrap_servers

    @property
    def reports_topic(self):
        return self._reports_topic

    @property
    def reports_ready_topic(self):
        return self._reports_ready_topic

    @property
    def producer_timeout(self):
        return self._producer_timeout

    @property
    def consumer_timeout(self):
        return self._consumer_timeout

    @property
    def group_id(self):
        return self._group_id

    def __enter__(self) -> ContextManager:

        self.consumer = KafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            reports_topic=self.reports_topic,
            reports_ready_topic=self.reports_ready_topic,
            timeout=self.consumer_timeout,
            group_id=self.group_id,
        )

        self.consume_thread: Thread = Thread(target=self.consume)
        self.consume_thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.consume_thread.join()

    def consume(self) -> None:

        for key, value in self.consumer.retrieve_message_from_reports_topic():
            print(key, value)
            self.process_task(key, value)

    def process_task(self, key: bytes, value: str) -> Any:

        query: list = json.loads(value)

        task_uuid: str = key.decode('utf-8')

        task: TaskSelector = TaskSelector(
            query,
            task_uuid,
            'docx',
        )
        task.select_particular_class()

        self.remove_dir(task_uuid)

        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            topic=self.reports_ready_topic,
            timeout=self.producer_timeout,
        )

        producer.send_message(
            key=str(task_uuid),
        )
        producer.producer_poll()
        producer.producer_flush()

        print(f'I have done task {task_uuid}')