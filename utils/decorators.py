from typing import Callable
from functools import wraps


def clear_dir(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        return result

    return wrapper

