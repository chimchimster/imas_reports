from typing import Any
from docxtpl import DocxTemplate

from modules.utils import FolderUUID


class PropertyMethodsMixin:
    @property
    def client_side_settings(self) -> list:
        return self._client_side_settings

    @property
    def task_uuid(self) -> str:
        return self._task_uuid

    @property
    def response(self) -> dict:
        return self._response

    @property
    def static_client_side_settings(self) -> dict:
        if self.client_side_settings:
            return self.client_side_settings[-1]

    @property
    def procs_objs(self) -> Any:
        return self._procs_objs

    @property
    def response_part(self) -> dict:
        return self._response_part

    @property
    def data_collection(self) -> Any:
        return self._data_collection

    @property
    def settings(self) -> dict:
        return self._settings

    @property
    def static_settings(self) -> dict:
        return self._static_settings

    @property
    def type(self) -> str:
        return self._type

    @property
    def folder(self) -> FolderUUID:
        return self._folder

    @folder.setter
    def folder(self, value) -> None:
        if not isinstance(value, FolderUUID):
            raise TypeError('Передаваемое значение должно быть объектом типа FolderUUID.')
        self._folder = value

    @property
    def tags_highlight_settings(self) -> dict:
        return self._tags_highlight_settings

    @property
    def tags(self) -> list:
        return self._tags

    @property
    def template(self) -> DocxTemplate:
        return self._template
