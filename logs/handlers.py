from pprint import pformat

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.style import Style
from pygments.token import Generic, Literal

from .abc_logger import LoggerHandler
from .loki_lexer import LokiLexer


class FormatterStyleOnSuccess(Style):
    styles = {
        Generic.Error: 'ansigreen',
        Literal.Date: 'ansimagenta',
    }


class FormatterStyleOnError(Style):
    styles = {
        Generic.Error: 'ansired',
        Literal.Date: 'ansimagenta',
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

        print(self.__get_log_separator(title=self.__class__.__name__))

        print(
            highlight(
                pformat(self._cur_log),
                LokiLexer(),
                Terminal256Formatter(**update_style)),
            end="",
        )

    @staticmethod
    def __get_log_separator(title='', length=50, char='*'):
        separator = char * length
        return f'{separator}\n{title.center(length)}\n{separator}'
