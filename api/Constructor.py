import os

from flask_restful import Resource
from flask import request, send_from_directory

from tools import WordCreator, PDFCreator
from utils import RemoveDirsMixin


class ReportDocx(Resource, RemoveDirsMixin):
    """ В ответ на POST запрос формирует отчет в формате docx. """

    def post(self):

        query = request.get_json()

        report = WordCreator(query)

        report.render_report()

        _uuid = str(report.folder.unique_identifier)

        response = send_from_directory(os.path.join(os.getcwd(), 'word', 'merged', _uuid), 'merged_output.docx')

        dirs_to_delete = [
            os.path.join(os.getcwd(), 'word', 'merged'),
            os.path.join(os.getcwd(), 'word', 'temp'),
            os.path.join(os.getcwd(), 'word', 'temp_templates'),
        ]

        for _dir in dirs_to_delete:
            self.remove_dir(_dir, _uuid)

        return response


class ReportPDF(Resource):
    def post(self):

        query = request.get_data()
        print(query, flush=True)





