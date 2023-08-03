from ..tools import TagsGenerator, ContentGenerator, TableContentGenerator
from .data_threads import ThreadDataGenerator


class DataManager:
    def __init__(self, rest_data, result_data):
        self._rest_data = rest_data
        self._result_data = result_data
        self.threads_objs = []

    def distribute_content(self):

        static_rest_data = self._rest_data[-1]

        for data in self._rest_data:
            match data.get('id'):
                case 'tags':
                    tags_obj = TagsGenerator(self._result_data, data)
                    self.threads_objs.append(tags_obj)
                case 'contents':
                    contents_obj = ContentGenerator(self._result_data, data)
                    self.threads_objs.append(contents_obj)
                case 'smi':
                    smi_table_obj = TableContentGenerator(self._result_data, data, static_rest_data, 'smi')
                    self.threads_objs.append(smi_table_obj)
                case 'soc':
                    soc_table_obj = TableContentGenerator(self._result_data, data, static_rest_data, 'soc')
                    self.threads_objs.append(soc_table_obj)

    def apply_threads(self):

        threads = []

        for thread_obj in self.threads_objs:
            thread = ThreadDataGenerator(thread_obj)
            threads.append(thread)
            thread.start()

        for thr in threads:
            thr.join()