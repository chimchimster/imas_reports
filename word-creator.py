import re
import json
import requests
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
import jinja2


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

        response = requests.get(query_url + query_string)

        if response.status_code == 200:
            result = response.json()

            # for key, val in result.items():
            #     if key == 'f_news':
            #         print(val)

            self.generate_word_document(result)

    def mark_word(self, value, word_to_mark):
        marked_value = value.replace(word_to_mark, f'<mark>{word_to_mark}</mark>')
        return marked_value


    def generate_word_document(self, result):
        template_path = 'templates/template_parts/table.docx'
        output_path = 'output.docx'

        template = DocxTemplate(template_path)

        data = self.generate_table(result)
        jinja_env = jinja2.Environment()
        jinja_env.filters['mark_word'] = self.mark_word
        template.render({'columns': list(data[0].keys()), 'data_length': range(1, len(data) + 1), 'data': data}, jinja_env, autoescape=True)

        template.save(output_path)

    def generate_table(self, data: dict):

        translator = {
            'title': 'Заголовок',
            'date': 'Дата',
            'content': 'Краткое содержание',
            'resource_name': 'Наименование СМИ',
            'news_link': 'URL',
            'sentiment': 'Тональность',
        }

        table_data = []

        f_news = data.get('f_news')

        if f_news:

            for i in range(len(f_news)):
                result = {translator[k]:v for (k, v) in f_news[i].items() if k in translator}
                table_data.append(result)
        table_data.append({'tag': 'Python'})
        return table_data

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
