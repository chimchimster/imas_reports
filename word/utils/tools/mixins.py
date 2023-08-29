from typing import Any


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