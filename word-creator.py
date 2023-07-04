import re
import json
import requests
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage


class HTMLWordCreator:
    api_url = 'https://rest.imas.kz/'
    relative_api = 'export-apis?'
    relative_api_folders = 'export-api-folders?'

    def __init__(self, rest_data):
        self._rest_data = rest_data

    def render_report(self):
        query_params = self.parse_string(self._rest_data)

        def apply_values_in_query_params_for_rest(key: str, value: str) -> None:
            """ Замыкание необходимо, чтобы проверить ключи и значения
                для REST. Относится к TODO -> Изменить REST! """

            if query_params.get(key):  # REST может обрабатывать только определенные значения ключей
                query_params[key] = value
            else:
                query_params.setdefault(key, value)

        # TODO: исправить вынужденные костыли (REST)
        if not query_params.get('format') or query_params['format'] not in ('pdf', 'wor', 'exc'):
            return

        apply_values_in_query_params_for_rest('format', 'pdf')
        apply_values_in_query_params_for_rest('location', '2')
        apply_values_in_query_params_for_rest('full_text', '1')

        an_id = query_params.get('an_id')
        query_url = self.__define_query_url(an_id)

        query_string = '&'.join(['='.join([key, val]) for (key, val) in query_params.items()])

        # response = requests.get(query_url + query_string)
        #
        # if response.status_code == 200:
        #     print(response.json())

        self.generate_word_document()

    def generate_word_document(self):
        template_path = 'templates/base.docx'
        output_path = 'output.docx'

        data = {
            'title': 'Заголовок документа',
            'content': 'Содержимое документа',
        }

        template = DocxTemplate(template_path)

        myimage = InlineImage(template, image_descriptor='static/girl.jpeg')

        data['my_image'] = myimage

        template.render(data)

        template.save(output_path)



    @staticmethod
    def parse_string(query_string: str) -> dict:
        """ Формирование словаря из данных пришедших в виде строки с REST. """

        return dict(re.findall(r'([^&=]+)=([^&]*)', query_string))

    @classmethod
    def __define_query_url(cls, value: str) -> str:
        """ Определяем строку для запроса. """

        try:
            int(value)
            return cls.api_url + cls.relative_api
        except:
            return cls.api_url + cls.relative_api_folders
