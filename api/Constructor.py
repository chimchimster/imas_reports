import os

from flask_restful import Resource
from flask import request, send_from_directory

from tools import WordCreator, PDFCreator


class ReportDocx(Resource):

    def post(self):

        query = request.get_json()

        report = WordCreator(query)

        report.render_report()

        return send_from_directory(os.getcwd() + '/result/', 'merged_output.docx')


class ReportPDF(Resource):
    def post(self):

        query = request.get_data()
        print(query)





