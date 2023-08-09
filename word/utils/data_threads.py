from threading import Thread
from docxtpl import DocxTemplate, InlineImage
from ..tools import TableStylesGenerator, SchedulerStylesGenerator


class ThreadDataGenerator(Thread):

    templates = {
        'table': 'word/templates/template_parts/table.docx',
        'table_of_contents': 'word/templates/template_parts/table_of_contents.docx',
        'tags': 'word/templates/template_parts/tags.docx',
        'base': 'word/templates/template_parts/base.docx',
    }

    def __init__(self, thread_obj):
        super().__init__()
        self.thread_obj = thread_obj

    def run(self) -> None:

        self.thread_obj.generate_data()

        data = self.thread_obj.data_collection

        report_format = self.thread_obj._static_rest_data.get('format', 'word_rus')
        report_lang = report_format.split('_')[1]

        if self.thread_obj.flag == 'table':

            template = DocxTemplate(self.templates.get('table'))

            position = self.thread_obj._rest_data.get('position')

            output_path = f'word/temp/output-{position}-table.docx'

            table_name = self.thread_obj._rest_data.get('id')
            table = self.thread_obj._rest_data.get('table')

            try:
                template.render(
                    {
                        'columns': data[0].keys(),
                        'data': data,
                        'is_table': table,
                        'table_name': table_name,
                        'lang': report_lang,
                    }, autoescape=True)
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

            template = DocxTemplate(self.templates.get('table_of_contents'))

            position = self.thread_obj._rest_data.get('position')

            output_path = f'word/temp/output-{position}-content.docx'

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

        elif self.thread_obj.flag == 'tags':

            template = DocxTemplate(self.templates.get('tags'))

            position = self.thread_obj._rest_data.get('position')

            output_path = f'word/temp/output-{position}-atags.docx'

            try:
                template.render({
                    'tags': data,
                    'lang': report_lang,
                }, autoescape=True)
            except IndexError:
                raise IndexError('Невозможно сформировать теги по причине нехватки данных!')
            template.save(output_path)

        elif self.thread_obj.flag == 'base':

            position = 0

            template = DocxTemplate(self.templates.get('base'))
            output_path = f'word/temp/output-{position}-base.docx'

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