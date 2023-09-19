from typing import Any
from multiprocessing import Process
from .tools import (TableProcess, ContentProcess, TagsProcess, BaseProcess, SentimentsProcess, DistributionProcess,
                    TotalMessagesCountProcess, MessagesDynamicsProcess, FabricMixin)


class ProcessDataGenerator(FabricMixin, Process):

    __available_classes__ = {
        'table': TableProcess,
        'content': ContentProcess,
        'tags': TagsProcess,
        'base': BaseProcess,
        'count': TotalMessagesCountProcess,
        'message_dynamic': MessagesDynamicsProcess,
        'sentiments': SentimentsProcess,
        'distribution': DistributionProcess,
    }

    def __init__(self, proc_obj: Any):
        super().__init__()
        self.proc_obj = proc_obj

    def run(self) -> None:

        self.proc_obj.generate_data()

        data: Any = self.proc_obj.data_collection

        report_format: str = self.proc_obj.static_settings.get('format', 'word_rus')

        process_type: str = self.proc_obj.flag

        self.select_particular_class(process_type, self.proc_obj, data, report_format, apply=True)