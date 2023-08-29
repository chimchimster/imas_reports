from typing import Any
from multiprocessing import Process
from .tools import TableProcess, ContentProcess, TagsProcess, BaseProcess, TotalMessagesCountProcess


class ProcessDataGenerator(Process):

    __available_classes__ = {
        'table': TableProcess,
        'content': ContentProcess,
        'tags': TagsProcess,
        'base': BaseProcess,
        'count': TotalMessagesCountProcess,
    }

    def __init__(self, proc_obj: Any):
        super().__init__()
        self.proc_obj = proc_obj

    def run(self) -> None:

        self.proc_obj.generate_data()

        data: Any = self.proc_obj.data_collection

        report_format: str = self.proc_obj.static_settings.get('format', 'word_rus')

        process_type: str = self.proc_obj.flag

        self.select_particular_class(process_type, self.proc_obj, data, report_format)

    @classmethod
    def select_particular_class(cls, process_type: str, *args) -> None:

        _instance_of = cls.__available_classes__.get(process_type)

        if not _instance_of:
            return

        instance: Any = _instance_of(*args)
        instance.run_proc_obj()
