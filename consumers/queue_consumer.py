import functools
import json
import os
from threading import Thread
from queue import Queue
from typing import Any, Callable, ContextManager
from utils import RemoveDirsMixin
from tools import WordCreator, PDFCreator
from kafka import load_kafka_settings, KafkaConsumer


class QueueConsumer(KafkaConsumer, RemoveDirsMixin):
    def __init__(self, queue: Queue, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._queue = queue

    def __enter__(self) -> ContextManager:
        self.consume_thread = Thread(target=self.consume)
        self.tasks_thread = Thread(target=self.queue_worker)

        self.consume_thread.start()
        self.tasks_thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.queue.put(None)
        self.consume_thread.join()
        self.queue.join()
        self.tasks_thread.join()
        super().__exit__(exc_type, exc_val, exc_tb)

    @property
    def queue(self) -> Queue:
        return self._queue

    def consume(self) -> None:
        while True:
            key, value = next(self.retrieve_message())

            self.add_task(
                self.partial_task(
                    self.process_task,
                    key,
                    value,
                )
            )

    def queue_worker(self) -> None:
        while True:
            item = self.queue.get()
            if item is None:
                break
            item.__call__()
            self.queue.task_done()

    def partial_task(self, task: Callable, *args) -> Callable:

        return functools.partial(task, *args)

    def add_task(self, task: Callable) -> None:
        self.queue.put(task)

    def notify_queue(self) -> None:
        self.queue.task_done()

    def process_task(self, key: bytes, value: str) -> Any:

        query: list = json.loads(value)

        task_uuid = key.decode('utf-8')

        report = WordCreator(query, task_uuid)

        report.render_report()

        # response = send_from_directory(
        #     os.path.join(
        #         os.getcwd(),
        #         'word',
        #         'merged',
        #         task_uuid,
        #     ),
        #     'merged_output.docx',
        # )

        dirs_to_delete = [
            os.path.join(
                os.getcwd(),
                'word',
                'merged',
            ),
            os.path.join(
                os.getcwd(),
                'word',
                'temp',
            ),
            os.path.join(
                os.getcwd(),
                'word',
                'temp_templates',
            ),
        ]

        for _dir in dirs_to_delete:
            self.remove_dir(_dir, task_uuid)

        self.remove_temp_tables_dirs(task_uuid)

        print(f'I have done task {task_uuid}')
        # return response