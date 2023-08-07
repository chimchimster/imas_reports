import os
import docx

from docxcompose.composer import Composer


class MergeReport:
    path_to_folder = os.getcwd() + '/word/temp/'
    path_to_templates = os.getcwd() + '/word/templates/'
    path_to_result = os.getcwd() + '/word/merged/'

    def merge(self):

        master = docx.Document(self.path_to_templates + 'out.docx')
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

        output_file = os.path.join(self.path_to_result, 'merged_output.docx')
        composer.save(output_file)