import os
import uuid
import docx
import shutil

from typing import Any
from docxcompose.composer import Composer
from multiprocessing import Process, Semaphore
from docxtpl import DocxTemplate, InlineImage
from ..tools import TableStylesGenerator, SchedulerStylesGenerator


class ProcessDataGenerator(Process):

    def __init__(self, proc_obj: Any):
        super().__init__()
        self.proc_obj = proc_obj
        self.templates: dict = {
            'table':
                os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_templates',
                    f'{self.proc_obj.folder.unique_identifier}',
                    'template_parts',
                    'table.docx'
                ),
            'table_of_contents':
                os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_templates',
                    f'{self.proc_obj.folder.unique_identifier}',
                    'template_parts',
                    'table_of_contents.docx'
                ),
            'tags':
                os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_templates',
                    f'{self.proc_obj.folder.unique_identifier}',
                    'template_parts',
                    'tags.docx'
                ),
            'base': os.path.join(
                os.getcwd(),
                'word',
                'temp_templates',
                f'{self.proc_obj.folder.unique_identifier}',
                'template_parts',
                'base.docx'
            ),
        }

    def run(self) -> None:

        self.proc_obj.generate_data()

        data = self.proc_obj.data_collection

        report_format = self.proc_obj._static_rest_data.get('format', 'word_rus')
        report_lang = report_format.split('_')[1]

        if self.proc_obj.flag == 'table':

            def create_temp_table_folder():
                pass

            def chunk_data_process(_pointer: int, proc_data: dict, _semaphore: Semaphore):

                def copy_table_template(_uuid: uuid, _path_to_copied_file: str) -> None:
                    table_docx_obj = self.templates.get('table')

                    shutil.copy(table_docx_obj, _path_to_copied_file)

                _uuid: uuid = uuid.uuid4()

                path_to_copied_file: str = os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_tables',
                    'templates',
                    str(pointer) + '_' + str(_uuid) + '.docx',
                )

                _output_path = os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_tables',
                    'results',
                    str(pointer) + '_' + str(_uuid) + '.docx',
                )

                copy_table_template(_uuid, path_to_copied_file)

                _template: DocxTemplate = DocxTemplate(path_to_copied_file)

                try:
                    _template.render(
                        {
                            'columns': proc_data[0].keys(),
                            'data': proc_data,
                            'is_table': True,
                        }, autoescape=True)

                    _semaphore.release()

                except IndexError:
                    raise IndexError('Невозможно сформировавть таблицу по причине нехватки данных!')

                settings: dict = {k: v for (k, v) in self.proc_obj._rest_data.items()}

                tags: str = self.proc_obj._data.get('query_ar')

                tags_highlight_settings: dict = self.proc_obj._rest_data.get('tag_highlight')

                static_rest_data: dict = self.proc_obj._static_rest_data

                if self.proc_obj._rest_data.get('table'):
                    styles = TableStylesGenerator(_template, tags, settings, tags_highlight_settings, static_rest_data)
                    styles.apply_table_styles()
                else:
                    styles = SchedulerStylesGenerator(_template, tags, settings, tags_highlight_settings)
                    styles.apply_scheduler_styles()

                _template.save(_output_path)

            def merge_procs_tables() -> None:
                path_to_results = os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_tables',
                    'results',
                )

                path_to_out_file = os.path.join(
                    os.getcwd(),
                    'word',
                    'temp_tables',
                    'out.docx',
                )

                master = docx.Document(path_to_out_file)
                composer = Composer(master)

                for file in os.listdir(path_to_results):
                    doc = docx.Document(
                        os.path.join(
                            path_to_results,
                            file,
                        )
                    )

                    composer.append(doc)

                composer.save('output.docx')

            semaphore = Semaphore(0)
            procs = []
            step = 10

            for pointer, chunk in enumerate(range(0, len(data), step)):
                process = Process(target=chunk_data_process, args=(pointer, data[chunk:chunk+step], semaphore,))
                procs.append(process)
                process.start()

            for prc in procs:
                prc.join()

            for _ in procs:
                semaphore.acquire()

            merge_procs_tables()

            # template = DocxTemplate(self.templates.get('table'))
            #
            # position = self.proc_obj._rest_data.get('position')
            #
            # output_path = os.path.join(
            #     os.getcwd(),
            #     'word',
            #     'temp',
            #     f'{self.proc_obj.folder.unique_identifier}',
            #     f'output-{position}-table.docx',
            # )
            #
            # table_name = self.proc_obj._rest_data.get('id')
            # table = self.proc_obj._rest_data.get('table')
            #
            # try:
            #     template.render(
            #         {
            #             'columns': data[0].keys(),
            #             'data': data,
            #             'is_table': table,
            #             'table_name': table_name,
            #             'lang': report_lang,
            #         }, autoescape=True)
            # except IndexError:
            #     raise IndexError('Невозможно сформировавть таблицу по причине нехватки данных!')
            #
            # settings = {k: v for (k, v) in self.proc_obj._rest_data.items()}
            #
            # tags = self.proc_obj._data.get('query_ar')
            #
            # tags_highlight_settings = self.proc_obj._rest_data.get('tag_highlight')
            #
            # static_rest_data = self.proc_obj._static_rest_data
            #
            # if self.proc_obj._rest_data.get('table'):
            #     styles = TableStylesGenerator(template, tags, settings, tags_highlight_settings, static_rest_data)
            #     styles.apply_table_styles()
            # else:
            #     styles = SchedulerStylesGenerator(template, tags, settings, tags_highlight_settings)
            #     styles.apply_scheduler_styles()
            #
            # template.save(output_path)

        elif self.proc_obj.flag == 'content':

            template = DocxTemplate(self.templates.get('table_of_contents'))

            position = self.proc_obj._rest_data.get('position')

            output_path = os.path.join(
                os.getcwd(),
                'word',
                'temp',
                f'{self.proc_obj.folder.unique_identifier}',
                f'output-{position}-content.docx',
            )

            has_soc = data.get('soc', {})
            has_smi = data.get('smi', {})

            try:
                template.render(
                    {
                        'table_of_contents_soc': has_soc,
                        'table_of_contents_smi': has_smi,
                        'lang': report_lang,
                    }, autoescape=True)
            except IndexError:
                raise IndexError('Невозможно сформировать оглавление по причине нехватки данных!')

            template.save(output_path)

        elif self.proc_obj.flag == 'tags':

            template = DocxTemplate(self.templates.get('tags'))

            position = self.proc_obj._rest_data.get('position')

            output_path = os.path.join(
                os.getcwd(),
                'word',
                'temp',
                f'{self.proc_obj.folder.unique_identifier}',
                f'output-{position}-atags.docx',
            )

            try:
                template.render({
                    'tags': data,
                    'lang': report_lang,
                }, autoescape=True)
            except IndexError:
                raise IndexError('Невозможно сформировать теги по причине нехватки данных!')
            template.save(output_path)

        elif self.proc_obj.flag == 'base':

            position = 0

            template = DocxTemplate(self.templates.get('base'))

            output_path = os.path.join(
                os.getcwd(),
                'word',
                'temp',
                f'{self.proc_obj.folder.unique_identifier}',
                f'output-{position}-base.docx',
            )

            project_name = data.get('project_name')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            date_of_export = data.get('date_of_export')

            template.render({
                'project_name': project_name,
                'date_start': start_time,
                'date_end': end_time,
                'date_of_export': date_of_export,
                'lang': report_lang,
            }, autoescape=True)

            template.save(output_path)
