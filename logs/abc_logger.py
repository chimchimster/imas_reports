import sys
import pytz
import functools
import threading

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Callable
from abc import ABC, ABCMeta, abstractmethod


class LoggerMeta(ABCMeta):

    def __new__(cls, name, bases, attrs, frmt_type=None):
        instance = super().__new__(cls, name, bases, attrs)

        class LogModel(BaseModel):
            logged_at: str
            level: str = 'DEBUG'
            message: Optional[str]
            params: Optional[tuple]
            k_params: Optional[dict]

        instance._model = LogModel

        match frmt_type:
            case 'json':
                instance._format = 'json'
            case 'orm':
                instance._format = 'orm'
            case _:
                instance._format = 'default'

        instance._cur_log = None
        instance._has_exc = None
        instance._logged_at = None

        return instance


def cleanup_logger_object(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self):
        func(self)

        self._message = ''
        # self._k_params = {k: v for (k, v) in self._k_params.items() if k == 'report_id'}
        self._level = 'DEBUG'
        # self._params = tuple()
        self._exception = False

    return wrapper


class LoggerHandler(ABC, metaclass=LoggerMeta):

    def __init__(
            self,
            message: str = None,
            *params,
            level: str = 'DEBUG',
            **k_params,
    ):
        self._message = message
        self._params = params
        self._level = level
        self._k_params = k_params
        self._exception = False

    @classmethod
    @abstractmethod
    def setup(cls):
        """ Logger initial setup. """

    @abstractmethod
    def send_log(self):
        """ Sends log to destination. """

    def __enter__(self):

        if self._message is not None:
            self.__fork_thread()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self._message is not None:
            self.__join_thread()

        if exc_type:
            self._exception = True
            self._level = 'ERROR'
            self._message = (f'Exception: row {exc_tb.tb_lineno}, '
                             f'func {exc_tb.tb_frame.f_code.co_name}, '
                             f'file {exc_tb.tb_frame.f_code.co_filename}.')
            self._k_params['type'] = str(exc_type)
            self._k_params['exc_val'] = str(exc_val)
            self.__send_log()

    def __parse_log_format(self):
        """ Defining a format of log depends on logger behavior. """

        __model_instance = self._model(
            logged_at=self._logged_at,
            level=self._level,
            message=self._message,
            params=self._params,
            k_params=self._k_params,
        )
        match self._format:

            case 'json':
                return __model_instance.model_dump()
            case 'orm':
                return __model_instance
            case _:
                return (
                    f'Logged at: {self._logged_at} - {self._level} '
                    f'{self._message}.*^2 {self._params}.^1] {self._k_params}.^1}}'
                )

    def __fork_thread(self):
        self.thread = threading.Thread(target=self.__send_log())
        self.thread.start()

    def __join_thread(self):
        self.thread.join()

    # @cleanup_logger_object
    def __send_log(self):

        if self._message is not None:

            self._logged_at = datetime.now(tz=pytz.timezone('Asia/Almaty')).strftime('%d-%m-%Y %H:%M:%S')

            self._cur_log = self.__parse_log_format()

            try:
                self.send_log()
            except Exception as e:
                sys.stderr.write(str(e))
        else:
            pass
