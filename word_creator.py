import re

from flask import send_from_directory

from .data_manager import DataManager, MergeReport
import requests


class HTMLWordCreator:
    api_url = 'https://rest.imas.kz/'
    relative_api = 'export-apis?'
    relative_api_folders = 'export-api-folders?'

    def __init__(self, rest_data):
        self._rest_data = rest_data

    def render_report(self):

        response_string = self.generate_string()

        an_id = self._rest_data[-1].get('an_id')

        query_url = self.__define_query_url(an_id)

        response = requests.get(query_url + response_string)

        if response.status_code == 200:
            result = response.json()

            self.generate_word_document(result)

    def generate_word_document(self, result):

        manager = DataManager(self._rest_data, result)
        manager.distribute_content()
        manager.apply_threads()

        merger = MergeReport()
        merger.merge()


    def generate_string(self) -> str:
        """ Формирование строки из словаря пришедшего в POST-запросе. """

        request_string = ''

        self._rest_data[-1]['format'] = 'pdf'
        self._rest_data[-1]['location'] = 2
        self._rest_data[-1]['full_text'] = 1

        request_string += '&'.join(['='.join([key, str(val)]) for (key, val) in self._rest_data[-1].items()])

        return request_string

    @classmethod
    def __define_query_url(cls, value: str) -> str:
        """ Определяем строку для запроса. """

        try:
            int(value)
            return cls.api_url + cls.relative_api
        except:
            return cls.api_url + cls.relative_api_folders

    @staticmethod
    def parse_string(query_string: str) -> dict:
        """ Формирование словаря из данных пришедших в виде строки с REST. """

        return dict(re.findall(r'([^&=]+)=([^&]*)', query_string))




