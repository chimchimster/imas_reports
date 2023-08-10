import os
import shutil
import time

from utils import FolderManager
from .data_threads import ThreadDataGenerator
from ..tools import BasePageDataGenerator, TagsGenerator, ContentGenerator, TableContentGenerator


class DataManager:
    def __init__(self, rest_data, result_data):
        self._rest_data = rest_data
        self._result_data = result_data
        self.threads_objs = []
        self.folder = FolderManager(flag='temp')

    def distribute_content(self):

        self.create_temp_folder()
        self.create_temp_templates()

        static_rest_data = self._rest_data[-1]

        for data in self._rest_data:
            match data.get('id'):
                case 'tags':
                    tags_obj = TagsGenerator(self._result_data, static_rest_data, data)
                    setattr(tags_obj, 'folder', self.folder)
                    self.threads_objs.append(tags_obj)
                case 'contents':
                    contents_obj = ContentGenerator(self._result_data, static_rest_data, data)
                    setattr(contents_obj, 'folder', self.folder)
                    self.threads_objs.append(contents_obj)
                case 'smi':
                    smi_table_obj = TableContentGenerator(self._result_data, data, static_rest_data, 'smi')
                    setattr(smi_table_obj, 'folder', self.folder)
                    self.threads_objs.append(smi_table_obj)
                case 'soc':
                    soc_table_obj = TableContentGenerator(self._result_data, data, static_rest_data, 'soc')
                    setattr(soc_table_obj, 'folder', self.folder)
                    self.threads_objs.append(soc_table_obj)
                case _:
                    base_page_obj = BasePageDataGenerator(self._result_data, static_rest_data)
                    setattr(base_page_obj, 'folder', self.folder)
                    self.threads_objs.append(base_page_obj)

    def apply_threads(self):

        threads = []

        for thread_obj in self.threads_objs:
            thread = ThreadDataGenerator(thread_obj)
            threads.append(thread)
            thread.start()

        for thr in threads:
            thr.join()

    def create_temp_folder(self):
        os.chdir('./word/temp')
        os.mkdir(f'temp_{self.folder.unique_identifier}')
        os.chdir('../..')

    def create_temp_templates(self):
        os.chdir('./word')
        shutil.copytree('./templates', f'./temp_templates/templates_{self.folder}')
        os.chdir('..')