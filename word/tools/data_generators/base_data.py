class BasePageDataGenerator:

    flag = 'base'

    def __init__(self, result_data, static_rest_data):
        self._result_data = result_data
        self._static_rest_data = static_rest_data
        self.data_collection = {}

    def generate_data(self):
        project_name = self._result_data.get('analyzer_name', 'Undefined')
        start_time = self._result_data.get('s_date', '') + ' ' + self._result_data.get('s_time', '')
        end_time = self._result_data.get('f_date', '') + ' ' + self._result_data.get('f_time')

        self.data_collection['project_name'] = project_name
        self.data_collection['start_time'] = start_time
        self.data_collection['end_time'] = end_time