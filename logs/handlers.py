import sys
from datetime import datetime
from typing import Any

from absctract_logger import LoggerHandler


class StdOutLogger(LoggerHandler):

    @classmethod
    def setup(cls):
        pass

    def parse_log_format(self):
        pass

    def send_log(self, message: Any, *params, level='DEBUG', **k_params):

        logged_at = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.3')
        std_view = sys.stdout if level == 'DEBUG' else sys.stderr

        view = self.__class__.__name__ + logged_at + ':' + message
        if params is not None:
            view += ";".join(params)
        if k_params is not None:
            view += ":".join(tuple(k_params.items()))

        std_view.write(view)
