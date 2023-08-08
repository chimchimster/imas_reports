import time
from datetime import datetime


class BasePageDataGenerator:
    """ Генерирует заглавную страницу docx документа.
        Флаг 'base' исплользуется в word/utils/data_threads
        в переопределенном методе run объекта ThreadDataGenerator. """

    flag = 'base'

    def __init__(self, result_data: dict, static_rest_data: dict) -> None:
        self._result_data = result_data
        self._static_rest_data = static_rest_data
        self.data_collection = {}

    def generate_data(self) -> None:
        project_name: str = self._result_data.get('analyzer_name', 'Undefined')
        start_time: str = self._result_data.get('s_date', 'undefined') + ' ' + self._result_data.get('s_time', 'undefined')
        end_time: str = self._result_data.get('f_date', 'undefined') + ' ' + self._result_data.get('f_time', 'undefined')
        date_of_export: str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        self.data_collection['project_name'] = project_name
        self.data_collection['start_time'] = start_time
        self.data_collection['end_time'] = end_time
        self.data_collection['date_of_export'] = date_of_export