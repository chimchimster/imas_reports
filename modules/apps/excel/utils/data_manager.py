from modules.data_manager.data_manager import DataManager
from modules.logs.decorators import tricky_loggy
from modules.models.rest_api import IMASResponseAPIModel
from .report_generator import ExcelReportGenerator


class ExcelDataManager(DataManager):

    def __init__(self, *args):
        super().__init__(*args)

    @tricky_loggy
    def distribute_content(self):

        response_model = IMASResponseAPIModel(**self._response)

        excel_gen = ExcelReportGenerator(response_model, self._client_side_settings)
        excel_gen.generate_excel_document()