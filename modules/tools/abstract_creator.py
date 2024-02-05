import os
import abc

import requests

from modules.logs.decorators import tricky_loggy


class Creator(abc.ABC):

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
        self._static_client_side_settings = self._client_side_settings[-1]

    @tricky_loggy
    def render_report(self) -> None:
        """ Method which requests data from REST API. """

        response_string: str = self.__generate_string()

        an_id: str = self._static_client_side_settings.get('an_id')

        query_url: str = self.__define_query_url(an_id)

        response: requests = requests.get(query_url + response_string)

        if response.status_code == 200:

            response_json: dict = response.json()

            self.generate_document(response_json)

    @abc.abstractmethod
    def generate_document(self, response: dict) -> None:
        """ Method which helps to generate document. """

    @tricky_loggy
    def __generate_string(self) -> str:
        """ Forms string from POST request dictionary. """

        request_string = ''

        request_data: dict = {k: v for (k, v) in self._static_client_side_settings.items()}

        request_data['format'] = 'pdf'
        request_data['location'] = 2
        request_data['full_text'] = 1

        request_string += '&'.join(['='.join([key, str(val)]) for (key, val) in request_data.items()])

        return request_string

    @classmethod
    def __define_query_url(cls, value: str) -> str:
        """ Defining query string. """

        try:
            int(value)
            return cls.api_url + cls.relative_api
        except TypeError:
            return cls.api_url + cls.relative_api_folders