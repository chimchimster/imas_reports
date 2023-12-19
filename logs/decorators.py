import functools
from typing import Callable
from .handlers import LokiLogger


def tricky_loggy(func: Callable) -> Callable:
    unique_identifier = None

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        nonlocal unique_identifier
        unique_identifier = self.proc_obj.folder.unique_identifier

        with LokiLogger(None, report_id=unique_identifier):
            func(self, *args, **kwargs)

    return wrapper



