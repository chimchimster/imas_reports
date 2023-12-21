import functools
from typing import Callable, Any

from modules.utils import FolderUUID
from modules.logs.handlers import LokiLogger


def tricky_loggy(func: Callable) -> Callable:

    attributes = {
        'proc_obj': ['unique_identifier', 'folder', 'proc_obj'],
        'folder': ['unique_identifier', 'folder'],
        '_folder': ['unique_identifier', '_folder'],
        '_task_uuid': ['_task_uuid'],
    }

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> None:

        unique_identifier = None

        for key, value in attributes.items():
            if hasattr(self, key):
                unique_identifier = deep_attr_search(self, value)
                break

        if args and isinstance(args[0], FolderUUID):
            unique_identifier = args[0].unique_identifier

        with LokiLogger(None, report_id=unique_identifier):
            return func(self, *args, **kwargs)

    return wrapper


def deep_attr_search(obj: Any, attr_names: list[str]):

    if not attr_names:
        return obj

    if hasattr(obj, attr_names[-1]):
        obj = getattr(obj, attr_names[-1])
        attr_names.pop()
        return deep_attr_search(obj, attr_names)
    else:
        return None

