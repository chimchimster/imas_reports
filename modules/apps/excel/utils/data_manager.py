import pydantic

from modules.data_manager.data_manager import DataManager
from modules.logs.decorators import tricky_loggy
from modules.models.rest_api import IMASResponseAPIModel
from .report_generator import ExcelReportGenerator


class ExcelDataManager(DataManager):

    def __init__(self, *args):
        super().__init__(*args)
        self._document_format = self._static_client_side_settings.get('format')
        try:
            self._lang = self._document_format.split('_')[-1]
        except IndexError:
            raise IndexError('Wrong document format.')

    @tricky_loggy
    def distribute_content(self):

        response_model = IMASResponseAPIModel(
            lang=self._lang,
            **self._response
        )

        self.__set_language_to_models(response_model)
        excel_gen = ExcelReportGenerator(response_model, self._client_side_settings, self._task_uuid)
        excel_gen.generate_excel_document()

    def __set_language_to_models(self, response_model):

        for key in vars(response_model):
            collection_of_models = getattr(response_model, key)
            if isinstance(collection_of_models, (list, tuple)):
                for model in collection_of_models:
                    setattr(model, 'lang', self._lang)
                    if hasattr(model, 'translate_model_fields'):
                        model.translate_model_fields(self._document_format)
