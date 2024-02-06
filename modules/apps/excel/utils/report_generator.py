import xlsxwriter
from modules.sorting import DataSorter

from modules.apps.localization import ReportLanguagePicker


class ExcelReportGenerator:

    def __init__(self, data, settings, task_uuid):
        self._data = data
        self._settings = settings
        report_format = settings[-1].get('format')
        self._lang = ReportLanguagePicker(report_format)()
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
                row_cnt = 0
                sheets[sheet_name] = [worksheet, row_cnt]
            data = value.get('data')
            if isinstance(data, (list, tuple)):
                for d in data:
                    col = 0
                    for attr_value in vars(d).values():
                        sheets[sheet_name][0].write(sheets[sheet_name][1], col + 1, str(attr_value))
                        col += 1
                        sheets[sheet_name][1] += 1
            else:
                sheets[sheet_name][0].write(0, 0, str(data))

        workbook.close()

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
                        'data': mass_media_data + social_media_data
                    }

        return meta_mapping
