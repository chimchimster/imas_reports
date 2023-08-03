from threading import Thread
from docxtpl import DocxTemplate
from ..tools import TableStylesGenerator, SchedulerStylesGenerator


class ThreadDataGenerator(Thread):

    templates = {
        'table': 'templates/template_parts/table.docx',
        'table_of_contents': 'templates/template_parts/table_of_contents.docx',
        'tags': 'templates/template_parts/tags.docx',
    }

    def __init__(self, thread_obj):
        super().__init__()
        self.thread_obj = thread_obj

    def run(self) -> None:

        self.thread_obj.generate_data()

        data = self.thread_obj.data_collection

        if self.thread_obj.flag == 'table':

            template = DocxTemplate(self.templates['table'])

            position = self.thread_obj._rest_data.get('position')

            output_path = f'temp/output-{position}-table.docx'

            table_name = self.thread_obj._rest_data.get('id')
            table = self.thread_obj._rest_data.get('table')

            try:
                template.render({'columns': data[0].keys(), 'data': data, 'is_table': table, 'table_name': table_name}, autoescape=True)
            except IndexError:
                raise IndexError('Невозможно сформировавть таблицу по причине нехватки данных!')

            settings = {k: v for (k, v) in self.thread_obj._rest_data.items()}

            tags = self.thread_obj._data.get('query_ar')

            tags_highlight_settings = self.thread_obj._rest_data.get('tag_highlight')

            static_rest_data = self.thread_obj._static_rest_data

            if self.thread_obj._rest_data.get('table'):
                styles = TableStylesGenerator(template, tags,  settings, tags_highlight_settings, static_rest_data)
                styles.apply_table_styles()
            else:
                styles = SchedulerStylesGenerator(template, tags, settings, tags_highlight_settings)
                styles.apply_scheduler_styles()

            template.save(output_path)

        elif self.thread_obj.flag == 'content':

            template = DocxTemplate(self.templates['table_of_contents'])

            position = self.thread_obj._rest_data.get('position')

            output_path = f'temp/output-{position}-content.docx'

            has_soc = data.get('soc', {})
            has_smi = data.get('smi', {})

            try:
                template.render({'table_of_contents_soc': has_soc, 'table_of_contents_smi': has_smi}, autoescape=True)
            except IndexError:
                raise IndexError('Невозможно сформировать оглавление по причине нехватки данных!')

            template.save(output_path)

        elif self.thread_obj.flag == 'tags':

            template = DocxTemplate(self.templates['tags'])

            position = self.thread_obj._rest_data.get('position')

            output_path = f'temp/output-{position}-atags.docx'

            try:
                template.render({'tags': data}, autoescape=True)
            except IndexError:
                raise IndexError('Невозможно сформировать теги по причине нехватки данных!')
            template.save(output_path)
