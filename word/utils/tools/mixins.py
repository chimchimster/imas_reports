from typing import Any
from abc import ABC, abstractmethod


class FabricMixin:

    __available_classes__ = {}

    @classmethod
    def select_particular_class(cls, obj_type: str, *args, apply: bool = True) -> Any:
        """ Метод либо определяющий у какого из экзмепляров
            будет вызван метод apply(), либо возвращающий экземпляр класса. """

        _instance_of = cls.__available_classes__.get(obj_type)

        tbl_types = ('smi', 'soc')

        if not _instance_of:
            return

        if obj_type in tbl_types:
            instance = _instance_of(*args, obj_type)
        else:
            instance: Any = _instance_of(*args)

        if apply:
            instance.apply()
        else:
            return instance


class AbstractRunnerMixin(ABC):

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
    def apply(self) -> None:
        """ Метод ответственный за логику каждого из runner's. """


class PropertyProcessesMixin:
    @property
    def data(self) -> list[dict] | dict:
        return self._data

    @property
    def report_format(self) -> str:
        return self._report_format

    @property
    def proc_obj(self) -> Any:
        return self._proc_obj

    @property
    def template_path(self) -> str:
        return self._template_path

    @property
    def report_lang(self) -> str:
        return self._report_lang


class DiagramPickerMixin:

    __available_methods__ = {
        'pie': '',
        'bar': '',
        'column': '',
        'linear': '',
    }

