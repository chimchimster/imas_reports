import re
import json
import requests
from docx.shared import Mm, RGBColor
from docxtpl import DocxTemplate, InlineImage
import jinja2


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

    def mark_word(self, value, word_to_mark):

        marked_value = value.replace(word_to_mark, f'<span style="background-color: #FFFF00;">{word_to_mark}</span>')
        return marked_value

    def generate_word_document(self, result):
        template_path = 'templates/template_parts/table.docx'
        output_path = 'output.docx'

        template = DocxTemplate(template_path)

        data = TableContentGenerator(result, type='soc')
        data.generate_data()
        data = data.data_collection

        template.render({'columns': data[0].keys(), 'data': data}, autoescape=True)

        template.save(output_path)

    def generate_string(self) -> str:
        """ Формирование строки из словаря пришедшего в POST-запросе. """

        request_string = ''

        self._rest_data[-1]['format'] = 'pdf'
        self._rest_data[-1]['location'] = 2
        self._rest_data[-1]['full_text'] = 1

        request_string += '&'.join(['='.join([key, str(val)]) for (key, val) in self._rest_data[-1].items()])

        return request_string

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


class TableContentGenerator:

    translator_smi = {
        'title': 'Заголовок',
        'not_date': 'Дата',
        'content': 'Краткое содержание',
        'resource_name': 'Наименование СМИ',
        'res_link': 'URL',
        'sentiment': 'Тональность',
        'name_cat': 'Категория',
    }

    translator_soc = {
        'date': 'Дата',
        'text': 'Пост',
        'resource_name': 'Наименование СМИ',
        'res_link': 'URL',
        'sentiment': 'Тональность',
        'type': 'Соцсеть',
    }

    def __init__(self, data, type='smi'):
        self._data = data
        self._type = type
        self.data_collection = []

    def generate_data(self):
        if self._type == 'smi':
            f_news = self._data.get('f_news')
            if f_news:
                self.__apply_translator(self.translator_smi, f_news)
        else:
            f_news2 = self._data.get('f_news2')
            if f_news2:
                self.__apply_translator(self.translator_soc, f_news2)

    def __apply_translator(self, translator, news):
        for i in range(len(news)):
            result = {translator[k]: v for (k, v) in news[i].items() if k in translator}
            self.data_collection.append(result)
