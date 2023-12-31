import os
import shutil
import multiprocessing

from modules.apps.word.tools import *
from modules.apps.word.utils.tools import FabricMixin
from modules.apps.word.mixins import PropertyMethodsMixin
from modules.apps.word.utils.data_processes import ProcessDataGenerator
from modules.logs.decorators import tricky_loggy


class DataManager(FabricMixin, PropertyMethodsMixin):

    __available_classes__ = {
        'smi': TableContentGenerator,
        'soc': TableContentGenerator,
        'contents': ContentGenerator,
        'tags': TagsGenerator,
        'count': TotalMessagesCountDataGenerator,
        'message_dynamic': MessagesDynamicsDataGenerator,
        'sentiments': SentimentsDataGenerator,
        'distribution': DistributionDataGenerator,
        'smi_distribution': SmiDistributionDataGenerator,
        'soc_distribution': SocDistributionDataGenerator,
        'media_top': TopMediaDataGenerator,
        'soc_top': TopSocDataGenerator,
        'most_popular_soc': MostPopularSocDataGenerator,
        'top_negative': TopNegativeDataGenerator,
        'smi_top_negative': SmiTopNegativeDataGenerator,
        'soc_top_negative': SocTopNegativeDataGenerator,
        'world_map': WorldMapDataGenerator,
        'kaz_map': KazakhstanMapDataGenerator,
    }

    sema = multiprocessing.Semaphore(5)

    def __init__(
            self,
            client_side_settings: list,
            response: dict,
    ):
        self._client_side_settings = client_side_settings
        self._response = response
        self._procs_objs: list = []
        self._folder = None

    @tricky_loggy
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

    @tricky_loggy
    def apply_processes(self):

        for proc_obj in self.procs_objs:
            proc = ProcessDataGenerator(proc_obj)
            with self.sema:
                proc.start()
                proc.join()

    @tricky_loggy
    def create_temp_folder(self):
        os.chdir(
            os.path.join(
                os.getcwd(),
                'modules',
                'apps',
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

        os.chdir('../../../..')

    @tricky_loggy
    def create_temp_templates(self):
        os.chdir(
            os.path.join(
                os.getcwd(),
                'modules',
                'apps',
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
