from typing import Any

from tools import WordCreator, PDFCreator


class TaskSelector:
    """ Класс-менеджер определяющий выбор класса генерации отчетов. """

    accessible_classes = {
        'docx': WordCreator,
        'pdf': PDFCreator,
    }

    def __init__(self,
                 query: list,
                 task_uuid: str,
                 report_type: str) -> None:
        self._query = query
        self._task_uuid = task_uuid
        self._report_type = report_type

    @property
    def query(self) -> list:
        return self._query

    @property
    def task_uuid(self) -> str:
        return self._task_uuid

    @property
    def report_type(self) -> str:
        return self._report_type

    def select_particular_class(self) -> None:
        """ Метод инкапсулирующий логику выбора класса-генератора отчета. """

        _instance_of = self.accessible_classes.get(self.report_type)

        if not _instance_of:
            return

        instance: Any = _instance_of(self.query, self.task_uuid)
        instance.render_report()
