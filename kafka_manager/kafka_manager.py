import functools
import json

from queue import Queue
from threading import Thread
from tasker import TaskSelector
from utils import RemoveDirsMixin
from typing import Any, Callable, ContextManager, Tuple
from kafka import load_kafka_settings, KafkaConsumer, KafkaProducer


class KafkaManager(RemoveDirsMixin):

    def __init__(
            self,
            bootstrap_server: str,
            reports_topic: str,
            reports_ready_topic: str,
            producer_timeout: int,
            consumer_timeout: float,
            group_id: str,
    ):
        self._bootstrap_server = bootstrap_server
        self._reports_topic = reports_topic
        self._reports_ready_topic = reports_ready_topic
        self._producer_timeout = producer_timeout
        self._consumer_timeout = consumer_timeout
        self._group_id = group_id

    def __enter__(self) -> ContextManager:

        self._queue: Queue = Queue()

        self.consumer: KafkaConsumer = KafkaConsumer(
            bootstrap_server=self.bootstrap_server,
            reports_topic=self.reports_topic,
            reports_ready_topic=self.reports_ready_topic,
            timeout=self.consumer_timeout,
            group_id=self.group_id,
        )

        self.consume_thread: Thread = Thread(target=self.consume)
        self.consume_thread.start()

        self.queue_thread: Thread = Thread(target=self.handle_queue)
        self.queue_thread.start()

        return self

    @property
    def bootstrap_server(self):
        return self._bootstrap_server

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

    @property
    def queue(self) -> Queue:
        return self._queue

    @staticmethod
    def partial_task(task: Callable, *args) -> Callable:

        return functools.partial(task, *args)

    def handle_queue(self) -> None:

        while True:
            item = self.queue.get()
            if item is None:
                break
            item.__call__()
            self.notify_queue()

    def add_task(self, task: Callable) -> None:
        self.queue.put(task)

    def notify_queue(self) -> None:
        self.queue.task_done()

    def consume(self) -> None:
        for key, value in self.consumer.retrieve_message_from_reports_topic():
            self.add_task(
                self.partial_task(
                    self.process_task,
                    key,
                    value,
                )
            )

    def process_task(self, key: bytes, value: str) -> Any:

        status_message = 'done'

        query: list = json.loads(value)

        task_uuid: str = key.decode('utf-8')

        try:
            task: TaskSelector = TaskSelector(
                query,
                task_uuid,
                'docx',
            )
            task.select_particular_class()
        except Exception:
            status_message = 'error'

        self.remove_dir(task_uuid)

        producer = KafkaProducer(
            bootstrap_server=self.bootstrap_server,
            topic=self.reports_ready_topic,
            timeout=self.producer_timeout,
        )

        producer.send_message(
            key=str(task_uuid),
            message=f'{status_message}'
        )
        producer.producer_poll()
        producer.producer_flush()

        print(f'I have done task {task_uuid}')

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.queue.put(None)
        self.consume_thread.join()
        self.queue_thread.join()