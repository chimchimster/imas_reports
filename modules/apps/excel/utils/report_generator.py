from collections import namedtuple
from typing import Any

import xlsxwriter

from modules.sorting import DataSorter
from modules.apps.localization import ReportLanguagePicker
from modules.models.rest_api import ItemsMassMediaModel, ItemsSocialMediaModel
from .excel_cell import Bouncer


worksheet_cursor = namedtuple(
    'Cursor',
    ['worksheet', 'bouncer']
)


class ExcelReportGenerator:

    def __init__(self, data, settings, task_uuid):
        self._data = data
        self._settings = settings
        report_format = settings[-1].get('format')
        self._lang_dict = ReportLanguagePicker(report_format)()
        self._task_uuid = task_uuid

    def __sort_data(self):

        for setting in self._settings:
            if order := setting.get('order'):
                return DataSorter(self._data, order).sort_data()

    def generate_excel_document(self):

        sheets_data = self.__prepare_sheets()

        workbook = xlsxwriter.Workbook(self._task_uuid + '.xlsx')

        sheets = {}
        for key, value in sheets_data.items():
            sheet_name = value.get('sheet_name')
            if sheet_name not in workbook.sheetnames:
                worksheet = workbook.add_worksheet(sheet_name)
                row_bouncer = Bouncer()
                sheets[sheet_name] = worksheet_cursor(worksheet, row_bouncer)
            data = value.get('data')
            title = self._lang_dict.get(key)

            bouncer = sheets[sheet_name].bouncer
            title_position = bouncer.position
            sheets[sheet_name].worksheet.write(title_position, title_position, title)
            bouncer.jump(1)

            if isinstance(data, (list, tuple)):
                for model in data:
                    col = -1
                    for attr_value in {k: v for k, v in vars(model).items() if k != 'lang'}.values():
                        sheets[sheet_name].worksheet.write(sheets[sheet_name].bouncer.position, col + 1, str(attr_value))
                        col += 1
                    sheets[sheet_name][1] += 1
            else:
                sheets[sheet_name][0].write(sheets[sheet_name][1], 0, str(data))
                sheets[sheet_name][1] += 1

        workbook.close()

    def __prepare_sheets(self):

        meta_mapping = {}

        for setting in self._settings:
            setting_name = setting.get('id')
            match setting_name:
                case 'tags':
                    meta_mapping[setting_name] = {
                        'sheet_name': self._lang_dict.get('sheet_name').get('common'),
                        'data': getattr(self._data, setting_name)
                    }
                case 'category':
                    mass_media_data = getattr(self._data, 'category_mass_media')
                    social_media_data = getattr(self._data, 'category_social_media')
                    meta_mapping[setting_name] = {
                        'sheet_name': self._lang_dict.get('sheet_name').get('common'),
                        'data': {
                            'smi': mass_media_data,
                            'soc': social_media_data,
                        }
                    }

        return meta_mapping

    @staticmethod
    def __get_table_model_values(model: Any, setting: dict) -> list:

        attrs = setting.get('columns')

        values_list = []
        for attr in attrs:
            attr_name = attr.get('id')
            attr_value = getattr(model, attr_name, '')
            values_list.append(attr_value)

        return values_list
