import pandas as pd
from modules.sorting import DataSorter


class ExcelReportGenerator:

    def __init__(self, data, settings):
        self._data = data
        self._settings = settings

    def __sort_data(self):

        for setting in self._settings:
            if order := setting.get('order'):
                return DataSorter(self._data, order).sort_data()

    @staticmethod
    def __prepare_mass_media_table_data(
            mass_media_data,
            mass_media_table_settings
    ):

        mapping = {
            'title': 'title',
            'content': 'full_text',
            'date': 'not_date',
            'resource_name': 'resource',
            'resource_page_url': 'resource_link',
            'link': 'news_link',
            'sentiment': 'sentiment',
            'category': 'category',
        }

        if columns := mass_media_table_settings.get('columns'):
            for column in columns:
                pass


    def generate_excel_document(self):

        data = self.__sort_data()

        if not data:
            return

        dataframe = pd.DataFrame(data)
        print(dataframe)
