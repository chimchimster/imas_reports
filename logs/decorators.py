import functools
from typing import Callable

from utils import FolderUUID
from .handlers import LokiLogger


def tricky_loggy(func: Callable) -> Callable:

    attributes = {
        'proc_obj': 'proc_obj.folder.unique_identifier',
        'folder': 'folder.unique_identifier',
        '_folder': '_folder.unique_identifier',
        '_task_uuid': '_task_uuid',
    }

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> None:

        unique_identifier = None

        for key, value in attributes.items():
            if hasattr(self, key):
                try:
                    unique_identifier = eval(f'{self}' + '.' + value)
                    print(globals())
                    print(unique_identifier)
                    break
                except Exception as e:
                    print(e)

        if args and isinstance(args[0], FolderUUID):
            unique_identifier = args[0].unique_identifier

        with LokiLogger(None, report_id=unique_identifier):
            return func(self, *args, **kwargs)

    return wrapper
