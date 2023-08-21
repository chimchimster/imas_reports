import time
from datetime import datetime
from word.mixins import PropertyMethodsMixin


class BasePageDataGenerator(PropertyMethodsMixin):
    """ Генерирует заглавную страницу docx документа.
        Флаг 'base' исплользуется в word/utils/data_threads
        в переопределенном методе run объекта ThreadDataGenerator. """

    flag: str = 'base'

    def __init__(self, response_part: dict, static_settings: dict) -> None:
        self._response_part = response_part
        self._static_settings = static_settings
        self._data_collection = {}

    def generate_data(self) -> None:
        project_name: str = self.response_part.get('analyzer_name', 'Undefined')
        start_time: str = self.response_part.get('s_date', 'undefined') + ' ' + self.response_part.get('s_time', 'undefined')
        end_time: str = self.response_part.get('f_date', 'undefined') + ' ' + self.response_part.get('f_time', 'undefined')
        date_of_export: str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        self.data_collection['project_name'] = project_name
        self.data_collection['start_time'] = start_time
        self.data_collection['end_time'] = end_time
        self.data_collection['date_of_export'] = date_of_export