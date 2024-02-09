import queue
import time
import os.path
import threading

import requests
from flask_socketio import Namespace, emit, call

from reports.redis_api.api import ReportStorageRedisAPI
from reports.modules.logs.handlers import LokiLogger


class SocketWebHookNamespace(Namespace):

    r_con = None
    queues = None
    storage_endpoint = None

    def __new__(cls, *args, **kwargs):

        if cls.r_con is None:
            cls.r_con = ReportStorageRedisAPI(
                host=os.getenv('REDIS_HOST'),
                port=os.getenv('REDIS_PORT'),
                db=os.getenv('REDIS_DB'),
                password=os.getenv('REDIS_PASSWORD')
            )
        if cls.storage_endpoint is None:
            cls.storage_endpoint = os.getenv('STORAGE_API_ENDPOINT')

        return super().__new__(cls)

    def on_connect(self):
        print(f"Присоеденился клиент")

    def on_disconnect(self):
        print(f"Клиент отключился")

    def on_message(self, msg: str, timeout: int = 5000):

        response_q = queue.Queue()
        thr_retrieve_message = threading.Thread(target=self.__fork_on_message(msg, response_q))
        thr_retrieve_message.start()
        print('BIG COCK')
        start = end = time.time()
        while end - start < timeout:
            print(response_q)
            if not response_q.empty():
                response = response_q.get(block=False)
                if response is not None:
                    with LokiLogger('Sending data via websocket', report_id=msg):
                        emit('message', {'file_data': response.content}, callback=lambda: print('OKЭY'))
            end = time.time()

    def __check_for_key_in_redis(
            self,
            msg: str,
            redis_event: threading.Event,
            redis_q: queue.Queue,
            timeout: int = 5000,
    ) -> None:

        with LokiLogger('Trying to find key in Redis', report_id=msg):
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.getdel(msg)
                    if has_key is not None:
                        has_key = has_key.decode('utf-8')
                        with LokiLogger('Key found in Redis', has_key, report_id=msg):
                            redis_q.put(has_key)
                            redis_event.set()
                            return
                    end = time.time()

            with LokiLogger('Key doesnt found in Redis', msg):
                redis_q.put('error')
                return

    def __retrieve_response(
            self,
            file_uuid: str,
            status: str,
            response_q: queue.Queue,
    ) -> None:

        with LokiLogger('Retrieving data from storage', status, report_id=file_uuid):

            if status is None or status == 'error':
                response_q.put(None)
            else:
                try:
                    response = requests.get(self.storage_endpoint + '/api/v1/files/file/download/', params={
                        'file_uuid': file_uuid
                    })
                    if response.status_code == 200:
                        response_q.put(response.content, block=False)
                    else:
                        response_q.put(None)
                except requests.exceptions.RequestException as e:
                    raise e

    def __start_redis_thr(
            self,
            msg: str,
            redis_event: threading.Event,
            redis_q: queue.Queue,
    ) -> threading.Thread:
        thr_redis = threading.Thread(
            target=self.__check_for_key_in_redis,
            args=(msg, redis_event, redis_q),
        )
        thr_redis.start()
        return thr_redis

    def __fork_on_message(self, msg: str, response_q: queue.Queue, timeout: int = 5000):

        redis_event, redis_q = threading.Event(), queue.Queue()

        thr_redis = self.__start_redis_thr(msg, redis_event, redis_q)
        thr_redis.join()

        start = end = time.time()
        while end - start < timeout:

            if redis_event.is_set():

                while end - start < timeout:

                    status = redis_q.get()

                    if status is not None or status != 'error':
                        thr_send_file = threading.Thread(
                            target=self.__retrieve_response,
                            args=(msg, status, response_q)
                        )
                        thr_send_file.start()
                        break
                    end = time.time()
