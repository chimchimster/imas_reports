import os.path
import multiprocessing
import shutil
import time

from reports.redis_api.api import ReportStorageRedisAPI

from flask_socketio import Namespace, emit


class SocketWebHookNamespace(Namespace):

    sema = None
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
        if cls.sema is None:
            cls.sema = multiprocessing.Semaphore(3)

        return super().__new__(cls)

    def on_connect(self):
        print(f"Присоеденился клиент")

    def on_disconnect(self):
        print(f"Клиент отключился")

    def on_message(self, msg: str):

        self.__fork_on_message(msg)

    def __check_for_key_in_redis(self, msg: str, q: multiprocessing.Queue, timeout: int = 5000) -> bool:

        with self.sema:
            if self.r_con is not None:
                start = end = time.time()
                while end - start < timeout:
                    has_key = self.r_con.connection.get(msg)
                    if has_key:
                        q.put(True)
                        return True
                    end = time.time()
            q.put(False)
            return False

    def __send_file_to_client(self, filename: str, q: multiprocessing.Queue):

        with self.sema:
            try:
                with open(
                        os.path.join(
                            self.path_to_file_dir,
                            filename,
                            filename + '.docx',
                        ), 'rb') as file:
                    file_data = file.read()
                    emit('message', {'file_data': file_data})
                    q.put(True)
            except FileNotFoundError:
                q.put(False)

    def __fork_on_message(self, msg: str):

        multiprocessing.active_children()

        mul_queue = multiprocessing.Queue()
        prc_redis = multiprocessing.Process(target=self.__check_for_key_in_redis, args=(msg, mul_queue))
        prc_redis.start()

        has_key = mul_queue.get()
        if has_key:
            prc_file = multiprocessing.Process(target=self.__send_file_to_client(msg, mul_queue))
            prc_file.start()

    def __remove_dir(self, dir_name: str):

        for _dir in os.listdir(self.path_to_file_dir):
            if _dir == dir_name:
                shutil.rmtree(
                    os.path.join(
                        self.path_to_file_dir,
                        _dir,
                    )
                )
