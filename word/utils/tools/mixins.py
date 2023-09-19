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


class DiagramPickerInjector:
    """ Класс-инъектор, получает инстанс класса и в зависимости от условия применяет необходимый метод. """

    __available_diagrams__ = {}

    def __init__(self, instance: Any, type_of_diagram: str, *args, **kwargs):
        self._instance = instance
        self._type_of_diagram = type_of_diagram
        self._args = args
        self._kwargs = kwargs
        self._set_diagrams()

    @property
    def instance(self) -> Any:
        return self._instance

    @property
    def func_args(self) -> tuple:
        return self._args

    @property
    def func_kwargs(self) -> dict:
        return self._kwargs

    @property
    def type_of_diagram(self) -> str:
        return self._type_of_diagram

    def _set_diagrams(self):
        self.__available_diagrams__['pie'] = self._instance.pie
        self.__available_diagrams__['column'] = self._instance.column
        self.__available_diagrams__['linear'] = self._instance.linear
        self.__available_diagrams__['bar'] = self._instance.bar

    def pick_and_execute(self) -> str:
        """ Выбираем нужную диаграмму из доступных и отправляем на отрисовку. """

        return self.__available_diagrams__.get(self.type_of_diagram)(*self.func_args, **self.func_kwargs)