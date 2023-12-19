import pprint
import sys

from .abc_logger import LoggerHandler


class LokiLogger(LoggerHandler, frmt_type='json'):
    """ Logger for stack Grafana + Loki. """

    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, level='DEBUG', **kwargs)

    @classmethod
    def setup(cls):
        pass

    def send_log(self):
        """ Sends logs into standard output in parsed format. """

        match self._level.lower():
            case 'debug' | 'warning':
                stream = sys.stdout
            case 'error' | 'critical':
                stream = sys.stderr
            case _:
                stream = None

        printer = pprint.PrettyPrinter(stream=stream)

        printer.pprint(self._cur_log)
