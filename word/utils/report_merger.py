import os
import docx
from utils import FolderManager
from docxcompose.composer import Composer


class MergeReport:
    def __init__(self):
        self.path_to_folder: str = os.getcwd() + '/word/temp/'
        self.path_to_templates: str = os.getcwd() + '/word/temp_templates/'
        self.path_to_result: str = os.getcwd() + '/word/merged/'
        self.folder: FolderManager = None

    def set_path_to_folder(self, folder):
        self.path_to_folder += str(folder)

    def set_path_to_result(self, folder):
        folder.flag = 'result'
        self.path_to_result += str(folder)

    def set_path_to_templates(self, folder):
        folder.flag = 'templates'
        self.path_to_templates += str(folder)

    def create_result_folder(self):
        os.chdir('./word/merged')
        os.mkdir(f'result_{self.folder.unique_identifier}')
        os.chdir('../..')

    def merge(self):

        self.set_path_to_folder(self.folder)
        self.set_path_to_templates(self.folder)

        master = docx.Document(self.path_to_templates + '/out.docx')
        composer = Composer(master)

        file_order = [file for file in os.listdir(self.path_to_folder)]
        file_order.sort()

        for idx, file in enumerate(file_order):

            file_path = os.path.join(self.path_to_folder, file)

            if os.path.isfile(file_path) and file.endswith('.docx'):
                doc = docx.Document(file_path)

                if file_path.endswith('table.docx'):
                    run = master.add_paragraph().add_run()
                    run.add_break(docx.enum.text.WD_BREAK.PAGE)

                composer.append(doc)

                if idx == 0:
                    run = master.add_paragraph().add_run()
                    run.add_break(docx.enum.text.WD_BREAK.PAGE)

        self.create_result_folder()
        self.set_path_to_result(self.folder)
        output_file = os.path.join(self.path_to_result, 'merged_output.docx')
        composer.save(output_file)