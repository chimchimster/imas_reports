import json
import os.path
import time
import functools

from queue import Queue
from threading import Thread
from typing import Any, Callable, ContextManager

import requests

from kafka.api.consumer import KafkaConsumer
from modules.logs.decorators import tricky_loggy
from modules.tasker import TaskSelector
from modules.utils import RemoveDirsMixin
from modules.logs.handlers import LokiLogger
from modules.database.handlers import ReportStorageMySQLAPI
from redis_api.api import ReportStorageRedisAPI


class AppConsumer(RemoveDirsMixin):

    STORAGE_API_ENDPOINT = os.getenv('STORAGE_API_ENDPOINT')

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

        self._redis_storage = ReportStorageRedisAPI()

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

    @tricky_loggy
    def handle_queue(self) -> None:

        while True:
            try:
                item = self.queue.get()
                if item is None:
                    break
                item.__call__()
                self.notify_queue()
            except Exception:
                pass

    def add_task(self, task: Callable) -> None:
        self.queue.put(task)

    def notify_queue(self) -> None:
        self.queue.task_done()

    @tricky_loggy
    def consume(self) -> None:
        try:
            for key, value in self.consumer.retrieve_message_from_reports_topic():
                self.add_task(
                    self.partial_task(
                        self.process_task,
                        key,
                        value,
                    )
                )
        except Exception:
            pass

    def process_task(self, key: bytes, value: str) -> Any:

        status_message = 'ready'

        start_time, end_time = 0, 0

        query: list = json.loads(value)
        task_uuid: str = key.decode('utf-8')
        user_id: int = query[-1].get('user_id')
        report_format = query[-1].get('format').split('_')[0]
        file_extension = self.__define_file_extension(report_format)

        with LokiLogger('Process current task', report_id=key):
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
            finally:
                self.remove_dir(task_uuid)

        with LokiLogger(
                'Task processed',
                status_message,
                execution_time=round(end_time - start_time, 2),
                report_id=key,
        ):
            self.__send_file_to_storage(user_id, task_uuid, file_extension)
            self._redis_storage.connection.set(key.decode('utf-8'), status_message)

    def __send_file_to_storage(
            self,
            user_id: int,
            task_uuid: str,
            file_extension: str,
            service_name: str = 'export',
            retry: int = 0,
    ):

        if retry > 2:
            raise TimeoutError('Возникла ошибка при отправке файла в хранилище. Количество попыток %s' % retry)

        path_to_file = os.path.join(
            os.getcwd(),
            'modules',
            'apps',
            'word',
            'merged',
            task_uuid,
            task_uuid + file_extension,
        )
        print(path_to_file)
        try:
            with open(path_to_file, 'rb') as file:
                file_data = file.read()
                print(file_data)
                try:
                    url = self.__form_api_link(user_id, task_uuid, file_extension, service_name)
                    requests.put(url, data=file_data, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
                except requests.exceptions.RequestException:
                    time.sleep(5)
                    self.__send_file_to_storage(user_id, task_uuid, file_extension, service_name, retry + 1)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл с uuid {task_uuid} не был найден.')

    def __form_api_link(self, user_id: int, task_uuid: str, report_format: str, service_name: str = 'export'):

        return self.STORAGE_API_ENDPOINT + '/'.join((user_id, service_name, task_uuid, report_format))

    @staticmethod
    def __define_file_extension(report_format: str) -> str:

        if report_format == 'word':
            return '.docx'

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.queue.put(None)
        self.consume_thread.join()
        self.queue_thread.join()
