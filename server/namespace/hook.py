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
            event: threading.Event,
            timeout: int = 5000,
            receive_type: str = ''
    ) -> bool:

        with LokiLogger('Trying to find key in Redis' + ' ' + receive_type, report_id=msg):
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.getdel(msg)
                    if has_key is not None:
                        has_key = has_key.decode('utf-8')
                        event.set()
                        with LokiLogger('Key found in Redis', has_key, report_id=msg):
                            return True
                    end = time.time()

            with LokiLogger('Key doesnt found in Redis', msg):
                return False

    def __send_file_to_client(self, file_uuid: str, file_ready_event: threading.Event):

        with LokiLogger('Sending file to client', report_id=file_uuid):

            if self.__check_for_key_in_redis(file_uuid, file_ready_event, receive_type='second time'):
                try:
                    response = requests.get(self.STORAGE_API_ENDPOINT + '/api/v1/files/file/download/', params={
                        'file_uuid': file_uuid
                    })
                except requests.exceptions.RequestException:
                    raise requests.exceptions.RequestException

                emit('message', {'file_data': response.content}, callback=lambda: print('OKЭY'))

    def __fork_on_message(self, msg: str):

        redis_event = threading.Event()
        file_ready_event = threading.Event()

        thr_redis = threading.Thread(
            target=self.__check_for_key_in_redis,
            args=(msg, redis_event),
            kwargs={'receive_type': 'first time'}
        )
        thr_redis.run()

        while True:
            if redis_event.is_set():
                thr_send_file = threading.Thread(target=self.__send_file_to_client, args=(msg, file_ready_event))
                thr_send_file.run()
                break
