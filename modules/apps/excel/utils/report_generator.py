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

    def generate_excel_document(self):

        data = self.__sort_data()
        print(data)