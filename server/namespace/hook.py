import time
import os.path
import multiprocessing
import multiprocessing.managers

from flask_socketio import Namespace, emit, call

from reports.redis_api.api import ReportStorageRedisAPI
from reports.modules.logs.handlers import LokiLogger


class SocketWebHookNamespace(Namespace):

    r_con = None
    path_to_file_dir = os.path.join(
        os.getcwd(),
        'modules',
        'apps',
        'word',
        'merged',
    )

    def __new__(cls, *args, **kwargs):

        if cls.r_con is None:
            cls.r_con = ReportStorageRedisAPI()

        return super().__new__(cls)

    def on_connect(self):
        print(f"Присоеденился клиент")

    def on_disconnect(self):
        print(f"Клиент отключился")

    def on_message(self, msg: str):

        multiprocessing.Process(target=self.__fork_on_message(msg,)).start()

    def __check_for_key_in_redis(self, msg: str, q: multiprocessing.Queue, timeout: int = 5000) -> bool:

        with LokiLogger('Trying to find key in Redis', report_id=msg):
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.get(msg)
                    if has_key:
                        q.put(True)
                        with LokiLogger('Key found in Redis', msg):
                            return True
                    end = time.time()
            q.put(False)
            with LokiLogger('Key doesnt found in Redis', msg):
                return False

    def __send_file_to_client(self, filename: str):

        with LokiLogger('Sending file to client', report_id=filename):
            try:
                with open(
                        os.path.join(
                            self.path_to_file_dir,
                            filename,
                            filename + '.docx',
                        ), 'rb') as file:
                    file_data = file.read()
                    emit('message', {'file_data': file_data}, callback=lambda: print('OKЭY'))
            except FileNotFoundError:
                raise FileNotFoundError

    def __fork_on_message(self, msg: str):

        redis_queue = multiprocessing.Queue()
        prc_redis = multiprocessing.Process(target=self.__check_for_key_in_redis, args=(msg, redis_queue))
        prc_redis.start()

        has_key = None
        while redis_queue.empty():
            if not redis_queue.empty():
                has_key = redis_queue.get()
                break

        if prc_redis.is_alive():
            prc_redis.terminate()

        if has_key:
            prc_file = multiprocessing.Process(target=self.__send_file_to_client(msg))
            prc_file.start()


