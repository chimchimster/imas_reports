import os

from flask import request, send_from_directory
from flask_restful import Resource

from tools.HTMLWordCreator import HTMLWordCreator


class HTMLTester(Resource):

    def get(self):
        print(request.__dict__)
        query = request.query_string.decode()

        report = HTMLWordCreator(query)

        export_file = report.render_report()

    def post(self):

        query = request.get_json()

        report = HTMLWordCreator(query)

        report.render_report()

        return send_from_directory(os.getcwd() + '/result/', 'merged_output.docx')






