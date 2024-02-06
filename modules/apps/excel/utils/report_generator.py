import pandas as pd
from modules.sorting import DataSorter

from modules.apps.localization import ReportLanguagePicker


class ExcelReportGenerator:

    def __init__(self, data, settings):
        self._data = data
        self._settings = settings
        self._lang = ReportLanguagePicker(settings[-1].get('format').split('_')[-1])()

    def __sort_data(self):

        for setting in self._settings:
            if order := setting.get('order'):
                return DataSorter(self._data, order).sort_data()

    def generate_excel_document(self):

        sheets_data = self.__prepare_sheets()
        [print((x.lang, x.name_cat)) for x in self._data.category_mass_media]

    def __prepare_sheets(self):

        meta_mapping = {}

        for setting in self._settings:
            setting_name = setting.get('id')
            match setting_name:
                case 'tags':
                    meta_mapping[setting_name] = {
                        'sheet_name': self._lang.get('sheet_name').get('common'),
                        'data': getattr(self._data, setting_name)
                    }
                case 'category':
                    mass_media_data = getattr(self._data, 'category_mass_media')
                    social_media_data = getattr(self._data, 'category_social_media')
                    meta_mapping[setting_name] = {
                        'sheet_name': self._lang.get('sheet_name').get('common'),
                        'data': [
                            [data for data in mass_media_data],
                            []
                        ]
                    }

        return meta_mapping
