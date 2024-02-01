from modules.apps.word.mixins import PropertyMethodsMixin
from modules.data_manager.data_manager import DataManager
from modules.logs.decorators import tricky_loggy


class ExcelDataManager(DataManager, PropertyMethodsMixin):

    def __init__(self, *args):
        super().__init__(*args)

    @tricky_loggy
    def distribute_content(self):
        pass