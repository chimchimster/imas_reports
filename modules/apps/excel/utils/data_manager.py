from modules.data_manager.data_manager import DataManager
from modules.logs.decorators import tricky_loggy
from modules.models.rest_api import IMASResponseAPIModel


class ExcelDataManager(DataManager):

    def __init__(self, *args):
        super().__init__(*args)

    @tricky_loggy
    def distribute_content(self):

        response_model = IMASResponseAPIModel(**self._response)