import os
import shutil

from .data_threads import ProcessDataGenerator
from ..tools import BasePageDataGenerator, TagsGenerator, ContentGenerator, TableContentGenerator


class DataManager:
    def __init__(self, rest_data, result_data):
        self._rest_data = rest_data
        self._result_data = result_data
        self.procs_objs = []

    def distribute_content(self):

        self.create_temp_folder()
        self.create_temp_templates()

        static_rest_data = self._rest_data[-1]

        for data in self._rest_data:
            match data.get('id'):
                case 'tags':
                    tags_obj = TagsGenerator(self._result_data, static_rest_data, data)
                    setattr(tags_obj, 'folder', self.folder)
                    self.procs_objs.append(tags_obj)
                case 'contents':
                    contents_obj = ContentGenerator(self._result_data, static_rest_data, data)
                    setattr(contents_obj, 'folder', self.folder)
                    self.procs_objs.append(contents_obj)
                case 'smi':
                    smi_table_obj = TableContentGenerator(self._result_data, data, static_rest_data, 'smi')
                    setattr(smi_table_obj, 'folder', self.folder)
                    self.procs_objs.append(smi_table_obj)
                case 'soc':
                    soc_table_obj = TableContentGenerator(self._result_data, data, static_rest_data, 'soc')
                    setattr(soc_table_obj, 'folder', self.folder)
                    self.procs_objs.append(soc_table_obj)
                case _:
                    base_page_obj = BasePageDataGenerator(self._result_data, static_rest_data)
                    setattr(base_page_obj, 'folder', self.folder)
                    self.procs_objs.append(base_page_obj)

    def _execute_process(self, proc_obj):
        process = ProcessDataGenerator(proc_obj)
        if process:
            process.run()

    def apply_processes(self):

        procs = []

        for proc_obj in self.procs_objs:
            proc = ProcessDataGenerator(proc_obj)
            procs.append(proc)
            proc.start()

        for prc in procs:
            prc.join()

    def create_temp_folder(self):
        os.chdir(
            os.path.join(
                os.getcwd(),
                'word',
                'temp',
            )
        )

        if not os.path.exists(os.path.join(
                os.getcwd(),
                f'{self.folder.unique_identifier}',
            )):
            os.mkdir(
                os.path.join(
                    os.getcwd(),
                    f'{self.folder.unique_identifier}',
                )
            )

        os.chdir('../..')

    def create_temp_templates(self):
        os.chdir(
            os.path.join(
                os.getcwd(),
                'word',
            )
        )

        if not os.path.exists(
            os.path.join(
                os.getcwd(),
                'temp_templates',
                f'{self.folder.unique_identifier}',
            )
        ):
            shutil.copytree(
                os.path.join(
                    os.getcwd(),
                    'templates',
                ),
                os.path.join(
                    os.getcwd(),
                    'temp_templates',
                    f'{self.folder.unique_identifier}',
                ),
            )
        os.chdir('..')