import time

from datetime import datetime

from modules.logs.decorators import tricky_loggy
from modules.mixins import DataGeneratorMixin


class BasePageDataGenerator(DataGeneratorMixin):
    """ Генерирует заглавную страницу docx документа.
        Флаг 'base' исплользуется в word/utils/data_threads
        в переопределенном методе run объекта ThreadDataGenerator. """

    flag: str = 'base'

    def __init__(self, response_part, settings, static_settings):
        super().__init__(response_part, settings, static_settings)
        self._data_collection = {}

    @tricky_loggy
    def generate_data(self) -> None:
        project_name: str = self._response_part.get('analyzer_name', 'Undefined')
        start_time: str = self._response_part.get('s_date', 'undefined') + ' ' + self._response_part.get('s_time', 'undefined')
        end_time: str = self._response_part.get('f_date', 'undefined') + ' ' + self._response_part.get('f_time', 'undefined')
        date_of_export: str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        self._data_collection['project_name'] = project_name
        self._data_collection['start_time'] = start_time
        self._data_collection['end_time'] = end_time
        self._data_collection['date_of_export'] = date_of_export
