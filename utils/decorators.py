from typing import Callable
from functools import wraps
from .garbage_collector import clear


def clear_dir(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        clear()

        return result

    return wrapper

