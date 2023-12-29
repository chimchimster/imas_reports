import queue
import time
import os.path
import threading

from flask_socketio import Namespace, emit, call

from reports.redis_api.api import ReportStorageRedisAPI
from reports.modules.logs.handlers import LokiLogger


class SocketWebHookNamespace(Namespace):

    r_con = None
    path_to_file_dir = None

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

    def __check_for_key_in_redis(self, msg: str, q: queue.Queue, timeout: int = 5000) -> bool:

        with LokiLogger('Trying to find key in Redis', report_id=msg):
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.getdel(msg)
                    if has_key is not None:
                        has_key = has_key.decode('utf-8')
                        q.put(has_key)
                        with LokiLogger('Key found in Redis', has_key, report_id=msg):
                            return True
                    end = time.time()
            q.put(None)
            with LokiLogger('Key doesnt found in Redis', msg):
                return False

    def __send_file_to_client(self, filename: str):

        with LokiLogger('Sending file to client', report_id=filename):

            with open(os.path.join(
                        self.path_to_file_dir,
                        filename,
                        filename + '.docx',
                    ), 'rb') as file:
                file_data = file.read()
                emit('message', {'file_data': file_data}, callback=lambda: print('OKЭY'))

    def __fork_on_message(self, msg: str):

        redis_queue = queue.Queue()
        prc_redis = threading.Thread(target=self.__check_for_key_in_redis, args=(msg, redis_queue))
        prc_redis.run()

        while not redis_queue.empty():

            has_key = redis_queue.get()

            if has_key not in ('error', None):
                prc_file = threading.Thread(target=self.__send_file_to_client, args=(msg,))
                prc_file.run()
                break
            else:
                return
