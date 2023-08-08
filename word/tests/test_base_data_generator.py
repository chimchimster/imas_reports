import time
from datetime import datetime
import os
import json
import pytest
from ..tools import BasePageDataGenerator


@pytest.fixture(scope='class')
def result_data():
    """ Фикстура основана на получаемых данных с REST API. """

    with open(f'{os.getcwd()}/test_json/result_data.JSON', 'r') as file:
        yield json.load(file)


@pytest.fixture(scope='class')
def static_rest_data():
    """ Фикстура основана на статических данных вшитых в запрос к REST API. """

    with open(f'{os.getcwd()}/test_json/static_rest_data.JSON', 'r') as file:
        yield json.load(file)


@pytest.fixture(scope='class')
def base_page_obj(result_data: dict, static_rest_data: dict):
    """ Фикстура основана на объекте генерирующем данные для заглавной страницы. """

    yield BasePageDataGenerator(
        result_data,
        static_rest_data,
    )


class TestBasePageDataGenerator:
    def test_object(self, base_page_obj: BasePageDataGenerator):
        """ А PyTest работает? """

        assert isinstance(base_page_obj, object) is True, 'Объект не является потомком object'

    def test_can_form_title(self, base_page_obj: BasePageDataGenerator, title: str = 'python'):
        """ Формируется ли имя проекта в объекте REST? """

        base_page_obj.generate_data()
        assert base_page_obj.data_collection.get('project_name') == title, 'Неверно сформирован заголовок'

    def test_can_form_date(self, base_page_obj: BasePageDataGenerator):
        """ Формируется ли дата проекта в объекте REST? """

        base_page_obj.generate_data()

        assert base_page_obj.data_collection.get('start_time') == '2023-08-06 00:00', 'Неверно сформировалось начальное время отчета!'
        assert base_page_obj.data_collection.get('end_time') == '2023-08-06 23:59', 'Неверно сформировалось конечное время отчета!'
        assert base_page_obj.data_collection.get('date_of_export') == datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S'), 'Неверно сформировалась дата загрузки отчета!'

    def test_can_form_undefined_title(self, base_page_obj: BasePageDataGenerator):
        """ В случае, если ключа 'analyzer_name' не будет в запросе с REST. """

        base_page_obj._result_data.pop('analyzer_name', None)
        base_page_obj.generate_data()

        assert base_page_obj.data_collection.get('project_name') == 'Undefined', 'При отсутствии ключа значение должно быть Undefined!'

    def test_can_form_undefined_date(self, base_page_obj: BasePageDataGenerator):
        """ В случае, если ключей 's_date', 's_time', 'f_date' и 'f_time' не будет
         в запросе с REST. """

        base_page_obj._result_data.pop('s_date', None)
        base_page_obj._result_data.pop('f_date', None)
        base_page_obj._result_data.pop('s_time', None)
        base_page_obj._result_data.pop('f_time', None)
        base_page_obj.generate_data()

        assert base_page_obj.data_collection.get('start_time') == 'undefined undefined', 'При отсутствии ключа значение должно быть Undefined!'
        assert base_page_obj.data_collection.get('end_time') == 'undefined undefined', 'При отсутствии ключа значение должно быть Undefined!'


