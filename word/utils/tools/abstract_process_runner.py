from abc import ABC, abstractmethod
from typing import Any


class AbstractRunner(ABC):

    def __init__(
            self,
            proc_object: Any,
            data: list[dict],
            report_format: str,
    ) -> None:
        self._proc_obj = proc_object
        self._data = data
        self._report_format = report_format
        self._report_lang = report_format.split('_')[1]  # TODO: от этого "ужаса" нужно избавиться на уровне клиентской части

    @abstractmethod
    def run_proc_obj(self) -> None:
        """ Метод ответственный за логику каждого из runner's. """


