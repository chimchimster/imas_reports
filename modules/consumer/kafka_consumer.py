import json
import time
import functools

from queue import Queue
from threading import Thread
from typing import Any, Callable, ContextManager

from kafka.api.consumer import KafkaConsumer
from modules.tasker import TaskSelector
from modules.utils import RemoveDirsMixin
from modules.logs.handlers import LokiLogger


class AppConsumer(RemoveDirsMixin):

    def __init__(
            self,
            bootstrap_server: str,
            reports_topic: str,
            producer_timeout: int,
            consumer_timeout: float,
            group_id: str,
            sasl_username: str,
            sasl_password: str,
    ):
        self._bootstrap_server = bootstrap_server
        self._reports_topic = reports_topic
        self._producer_timeout = producer_timeout
        self._consumer_timeout = consumer_timeout
        self._group_id = group_id
        self._sasl_username = sasl_username
        self._sasl_password = sasl_password

    def __enter__(self) -> ContextManager:

        self._queue: Queue = Queue()

        self.consumer: KafkaConsumer = KafkaConsumer(
            bootstrap_server=self.bootstrap_server,
            reports_topic=self.reports_topic,
            timeout=self.consumer_timeout,
            group_id=self.group_id,
            sasl_username=self._sasl_username,
            sasl_password=self._sasl_password,
        )

        self.consume_thread: Thread = Thread(target=self.consume)
        self.consume_thread.start()

        self.queue_thread: Thread = Thread(target=self.handle_queue)
        self.queue_thread.start()

        return self

    def __del__(self):
        self.queue_thread.join()
        self.consume_thread.join()

    @property
    def bootstrap_server(self):
        return self._bootstrap_server

    @property
    def reports_topic(self):
        return self._reports_topic

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

        start_time, end_time = 0, 0

        with LokiLogger('Process current task', report_id=key):
            query: list = json.loads(value)
            task_uuid: str = key.decode('utf-8')

            try:
                start_time = time.time()
                task: TaskSelector = TaskSelector(
                    query,
                    task_uuid,
                    'docx',
                )
                task.select_particular_class()
                end_time = time.time()
            except Exception:
                status_message = 'error'

            self.remove_dir(task_uuid)

        with LokiLogger(
                'Task processed',
                status_message,
                execution_time=round(end_time - start_time, 2),
                report_id=key,
        ):
            pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.queue.put(None)
        self.consume_thread.join()
        self.queue_thread.join()
