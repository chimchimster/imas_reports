from typing import Any
from multiprocessing import Process

from modules.logs.decorators import tricky_loggy
from modules.apps.word.utils.tools import *
from modules.mixins import FabricMixin


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
        'smi_distribution': SmiDistributionProcess,
        'soc_distribution': SocDistributionProcess,
        'media_top': TopMediaProcess,
        'soc_top': TopSocialProcess,
        'most_popular_soc': MostPopularSocProcess,
        'top_negative': TopNegativeProcess,
        'smi_top_negative': SmiTopNegativeProcess,
        'soc_top_negative': SocTopNegativeProcess,
        'world_map': WorldMapProcess,
        'kaz_map': KazakhstanMapProcess,
    }

    def __init__(self, proc_obj: Any):
        super().__init__()
        self.proc_obj = proc_obj

    @tricky_loggy
    def run(self) -> None:

        self.proc_obj.generate_data()

        data: Any = self.proc_obj.data_collection

        report_format: str = self.proc_obj.static_settings.get('format', 'word_rus')

        process_type: str = self.proc_obj.flag

        self.select_particular_class(process_type, self.proc_obj, data, report_format, apply=True)