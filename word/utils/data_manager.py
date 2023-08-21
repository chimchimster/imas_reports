import os
import shutil

from word.mixins import PropertyMethodsMixin
from .data_processes import ProcessDataGenerator
from ..tools import BasePageDataGenerator, TagsGenerator, ContentGenerator, TableContentGenerator


class DataManager(PropertyMethodsMixin):
    def __init__(
            self,
            client_side_settings: list,
            response: dict,
    ):
        self._client_side_settings = client_side_settings
        self._response = response
        self._procs_objs: list = []
        self._folder = None

    def distribute_content(self) -> None:

        self.create_temp_folder()
        self.create_temp_templates()

        for client_side_setting in self.client_side_settings:
            match client_side_setting.get('id'):
                case 'tags':
                    tags_obj: TagsGenerator = TagsGenerator(
                        self.response,
                        client_side_setting,
                        self.static_client_side_settings,
                    )
                    tags_obj.folder = self.folder
                    self.procs_objs.append(tags_obj)
                case 'contents':
                    contents_obj: ContentGenerator = ContentGenerator(
                        self.response,
                        client_side_setting,
                        self.static_client_side_settings,
                    )
                    contents_obj.folder = self.folder
                    self.procs_objs.append(contents_obj)
                case 'smi':
                    smi_table_obj = TableContentGenerator(
                        self.response,
                        client_side_setting,
                        self.static_client_side_settings,
                        'smi',
                    )
                    smi_table_obj.folder = self.folder
                    self.procs_objs.append(smi_table_obj)
                case 'soc':
                    soc_table_obj = TableContentGenerator(
                        self.response,
                        client_side_setting,
                        self.static_client_side_settings,
                        'soc',
                    )
                    soc_table_obj.folder = self.folder
                    self.procs_objs.append(soc_table_obj)
                case _:
                    base_page_obj = BasePageDataGenerator(
                        self.response,
                        self.static_client_side_settings,
                    )
                    base_page_obj.folder = self.folder
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