import os
import re
import requests

from logs.decorators import tricky_loggy
from utils import FolderUUID
from word.mixins import PropertyMethodsMixin
from word.utils import DataManager, MergeReport


class WordCreator(PropertyMethodsMixin):

    api_url = os.environ.get('REST_ENDPOINT')
    relative_api = 'export-apis?'
    relative_api_folders = 'export-api-folders?'

    def __init__(
            self,
            client_side_settings: list,
            task_uuid: str,
    ) -> None:
        self._client_side_settings = client_side_settings
        self._task_uuid = task_uuid

    @tricky_loggy
    def render_report(self) -> None:
        """ Метод-прокладка TODO: как только в компании переработают REST необходимо от него избавиться """

        response_string: str = self.generate_string()

        an_id: str = self.static_client_side_settings.get('an_id')

        query_url: str = self.__define_query_url(an_id)

        response: requests = requests.get(query_url + response_string)

        if response.status_code == 200:
            response_json: dict = response.json()

            self.generate_word_document(response_json)

    @tricky_loggy
    def generate_word_document(self, response: dict) -> None:
        """ Метод контролирующий этапы создания docx документа.
            Начиная с получения данных, распределения процессов,
            а также соединения мелких отчетов воедино. """

        folder: FolderUUID = FolderUUID(
            unique_identifier=self._task_uuid,
        )

        manager: DataManager = DataManager(
            self.client_side_settings,
            response,
        )
        manager.folder = folder
        manager.distribute_content()
        manager.apply_processes()

        setattr(self, 'folder', folder)

        merger: MergeReport = MergeReport()
        setattr(merger, 'folder', folder)
        merger.merge()

    @tricky_loggy
    def generate_string(self) -> str:
        """ Формирование строки из словаря пришедшего в POST-запросе. """

        request_string = ''

        request_data: dict = {k: v for (k, v) in self.static_client_side_settings.items()}

        request_data['format'] = 'pdf'
        request_data['location'] = 2
        request_data['full_text'] = 1

        request_string += '&'.join(['='.join([key, str(val)]) for (key, val) in request_data.items()])

        return request_string

    @classmethod
    def __define_query_url(cls, value: str) -> str:
        """ Определяем строку для запроса. """

        try:
            int(value)
            return cls.api_url + cls.relative_api
        except TypeError:
            return cls.api_url + cls.relative_api_folders

    @staticmethod
    def __parse_string(query_string: str) -> dict:
        """ Формирование словаря из данных пришедших в виде строки с REST. """

        return dict(re.findall(r'([^&=]+)=([^&]*)', query_string))




