import pydantic

from modules.data_manager.data_manager import DataManager
from modules.logs.decorators import tricky_loggy
from modules.models.rest_api import IMASResponseAPIModel
from .report_generator import ExcelReportGenerator


class ExcelDataManager(DataManager):

    def __init__(self, *args):
        super().__init__(*args)
        self._lang = self._static_client_side_settings.get('format').split('_')[-1]

    @tricky_loggy
    def distribute_content(self):

        response_model = IMASResponseAPIModel(
            lang=self._lang,
            **self._response
        )
        print(self._lang)
        for model in response_model.items_mass_media:
            model.__setattr__('lang', self._lang)

        excel_gen = ExcelReportGenerator(response_model, self._client_side_settings)
        excel_gen.generate_excel_document()
