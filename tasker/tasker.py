from tools import WordCreator, PDFCreator


class TaskSelector:

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
    def query(self):
        return self._query

    @property
    def task_uuid(self):
        return self._task_uuid

    @property
    def report_type(self):
        return self._report_type

    def select_particular_class(self) -> None:

        _instance_of = self.accessible_classes.get(self.report_type)

        if not _instance_of:
            return

        _instance_of(self.query, self.task_uuid)
        _instance_of.render_report()
