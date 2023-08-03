import os
import json


class ReportLanguagePicker:

    langs_dir = os.getcwd() + '/local/langs'

    def __init__(self, document_format):
        try:
            self._language = document_format.split('_')[1]
        except IndexError:
            self._language = 'rus'

    def __call__(self, *args, **kwargs):

        if not self._language:
            return

        for file_name in os.listdir(self.langs_dir):
            if file_name.lower().startswith(self._language):
                with open(self.langs_dir + '/' + file_name) as file:
                    return json.load(file)





