import time
import os.path
import multiprocessing
import multiprocessing.managers

from flask_socketio import Namespace, emit

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

        prc_count = len(multiprocessing.active_children())

        with LokiLogger('Tracking processes count', prc_count):

            multiprocessing.Process(target=self.__fork_on_message, args=(msg,)).start()

    def __check_for_key_in_redis(self, msg: str, q: multiprocessing.Queue, timeout: int = 5000) -> bool:

        with LokiLogger('Trying to find key in Redis', report_id=msg):
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.getdel(msg)
                    if has_key:
                        q.put(True)
                        return True
                    end = time.time()
            q.put(False)
            return False

    def __send_file_to_client(self, filename: str, q: multiprocessing.Queue):

        with LokiLogger('Sending file to client', report_id=filename):
            try:
                with open(
                        os.path.join(
                            self.path_to_file_dir,
                            filename,
                            filename + '.docx',
                        ), 'rb') as file:
                    file_data = file.read()
                    emit('message', {'file_data': file_data})
                    q.put(None)
            except FileNotFoundError:
                q.put(None)

    def __fork_on_message(self, msg: str):

        redis_queue = multiprocessing.Queue()
        prc_redis = multiprocessing.Process(target=self.__check_for_key_in_redis, args=(msg, redis_queue))
        prc_redis.start()

        has_key = None
        while redis_queue.empty():
            if not redis_queue.empty():
                has_key = redis_queue.get()
                break

        # if prc_redis.is_alive():
        #     prc_redis.terminate()

        if has_key:

            file_queue = multiprocessing.Queue()
            prc_file = multiprocessing.Process(target=self.__send_file_to_client, args=(msg, file_queue))
            prc_file.start()

            while file_queue.empty():
                if not file_queue.empty():
                    # if prc_file.is_alive():
                    #     prc_file.terminate()
                    break

