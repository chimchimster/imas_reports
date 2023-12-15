import sys
import threading

from abc import ABC, abstractmethod


class LoggerHandler(ABC):

    @classmethod
    @abstractmethod
    def setup(cls):
        """ Logger initial setup. """

    @abstractmethod
    def parse_log_format(self):
        """ Prepare log formatted string depends on log destination. """

    @abstractmethod
    def send_log(self, message, *params, level='DEBUG', **k_params):
        """ Sends log to destination. """

    def __new__(cls, *args, **kwargs):
        cls.setup()
        return super().__new__(cls)

    def __enter__(self):
        self.__fork_thread()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__join_thread()

    def __fork_thread(self):
        self.thread = threading.Thread(target=self.__send_log())
        self.thread.start()

    def __join_thread(self):
        self.thread.join()

    def __send_log(self):
        try:
            self.send_log()
        except Exception as e:
            sys.stderr.write(str(e))