import os
import shutil

from .tools import FabricMixin
from word.mixins import PropertyMethodsMixin
from .data_processes import ProcessDataGenerator
from ..tools import (BasePageDataGenerator, TagsGenerator, ContentGenerator, SentimentsDataGenerator,
                     TableContentGenerator, TotalMessagesCountDataGenerator, MessagesDynamicsDataGenerator)


class DataManager(FabricMixin, PropertyMethodsMixin):

    __available_classes__ = {
        'smi': TableContentGenerator,
        'soc': TableContentGenerator,
        'contents': ContentGenerator,
        'tags': TagsGenerator,
        'count': TotalMessagesCountDataGenerator,
        'message_dynamic': MessagesDynamicsDataGenerator,
        'sentiments': SentimentsDataGenerator,
    }

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

        for client_side_setting in self.client_side_settings[:-1]:

            obj_type = client_side_setting.get('id')

            # Обработка всех классов кроме, базового отвечающего за главную страницу.
            if obj_type:
                gen_obj = self.select_particular_class(
                    obj_type,
                    self.response,
                    client_side_setting,
                    self.static_client_side_settings,
                    apply=False,
                )
                setattr(gen_obj, 'folder', self.folder)
                self.procs_objs.append(gen_obj)

        # Главную страницу мы обрабатываем в любом случае.
        # Наличие клиентских настроек не играет никакой роли.
        # Нужны только вшитые (статические) клиентские настройки.
        base_page_obj = BasePageDataGenerator(
            self.response,
            None,
            self.static_client_side_settings,
        )
        base_page_obj.folder = self.folder
        self.procs_objs.append(base_page_obj)

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
            )
        ):
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