import sys

from pprint import pformat

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer
from pygments.style import Style
from pygments.token import Token

from .abc_logger import LoggerHandler


class FormatterStyleOnSuccess(Style):
    styles = {
        Token.String: 'ansiyellow',
        Token.Number: 'ansibrightblue',
    }


class FormatterStyleOnError(Style):
    styles = {
        Token.String: 'ansibrightred',
        Token.Number: 'ansibrightblue',
    }


class LokiLogger(LoggerHandler, frmt_type='json'):
    """ Logger for stack Grafana + Loki. """

    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, level='DEBUG', **kwargs)
        self._formatter_style = None

    @classmethod
    def setup(cls):
        pass

    def send_log(self):
        """ Sends logs into standard output in parsed format. """

        match self._level.lower():
            case 'debug':
                self._formatter_style = FormatterStyleOnSuccess
            case 'error':
                self._formatter_style = FormatterStyleOnError
            case _:
                self._formatter_style = None

        if not self._formatter_style:
            update_style = {}
        else:
            update_style = {'style': self._formatter_style}

        print(
            highlight(
                pformat(self._cur_log),
                PythonLexer(),
                Terminal256Formatter(**update_style)),
            end="",
        )

