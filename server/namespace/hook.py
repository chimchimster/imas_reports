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
    path_to_file_dir = None
    STORAGE_API_ENDPOINT = os.getenv('STORAGE_API_ENDPOINT')

    def __new__(cls, *args, **kwargs):

        if cls.r_con is None:
            cls.r_con = ReportStorageRedisAPI()
        if cls.path_to_file_dir is None:
            cls.path_to_file_dir = os.path.join(
                os.getcwd(),
                'modules',
                'apps',
                'word',
                'merged',
            )

        return super().__new__(cls)

    def on_connect(self):
        print(f"Присоеденился клиент")

    def on_disconnect(self):
        print(f"Клиент отключился")

    def on_message(self, msg: str):

        threading.Thread(target=self.__fork_on_message(msg,)).start()

    def __check_for_key_in_redis(
            self,
            msg: str,
            redis_event: threading.Event,
            redis_q: queue.Queue,
            timeout: int = 5000,
            receive_type: str = ''
    ) -> None:

        with LokiLogger('Trying to find key in Redis' + ' ' + receive_type, report_id=msg):
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.getdel(msg)
                    if has_key is not None:
                        print(has_key)
                        has_key = has_key.decode('utf-8')
                        with LokiLogger('Key found in Redis', has_key, report_id=msg):
                            if receive_type == 'second time':
                                redis_q.put(has_key)
                            redis_event.set()
                            return
                    end = time.time()

            with LokiLogger('Key doesnt found in Redis', msg):
                redis_q.put('error')

    def __send_file_to_client(
            self,
            file_uuid: str,
            status: str
    ) -> None:

        with LokiLogger('Sending file to client', report_id=file_uuid):

            if status is None or status == 'error':
                emit('message', {'file_data': b'Error during constructing report'})
            else:
                try:
                    response = requests.get(self.STORAGE_API_ENDPOINT + '/api/v1/files/file/download/', params={
                        'file_uuid': file_uuid
                    })
                except requests.exceptions.RequestException as e:
                    raise e

                emit('message', {'file_data': response.content}, callback=lambda: print('OKЭY'))

    def __start_redis_thr(
            self,
            msg: str,
            redis_event: threading.Event,
            redis_q: queue.Queue,
            receive_type: str
    ) -> threading.Thread:
        thr_redis = threading.Thread(
            target=self.__check_for_key_in_redis,
            args=(msg, redis_event, redis_q),
            kwargs={'receive_type': receive_type}
        )
        thr_redis.start()
        return thr_redis

    def __fork_on_message(self, msg: str, timeout: int = 5000):

        redis_event, redis_q = threading.Event(), queue.Queue()

        thr_r1 = self.__start_redis_thr(msg, redis_event, redis_q, receive_type='first time')
        thr_r1.join()

        start, end = time.time(), time.time()
        while end - start < timeout:

            if redis_event.is_set():

                redis_event.clear()

                self.__start_redis_thr(msg, redis_event, redis_q, receive_type='second time')

                while end - start < timeout:

                    status = redis_q.get()

                    if status is not None or status != 'error':
                        thr_send_file = threading.Thread(
                            target=self.__send_file_to_client,
                            args=(msg, status)
                        )
                        thr_send_file.start()
                        break
                    end = time.time()
