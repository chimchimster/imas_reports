import re

from .table_style import TableStylesGenerator


class SchedulerStylesGenerator(TableStylesGenerator):

    def __init__(self, template, tags, settings=None, tags_highlight_settings=None):
        super().__init__(template, tags, settings, tags_highlight_settings)

    def apply_scheduler_styles(self):

        def manage_styles(paragraph, curr_run, prev_run, rows):

            prev_run_text = prev_run.text.rstrip(':')

            def get_setting():
                for row in rows:
                    id = row.get('id')
                    if self.translator_smi.get(id) == prev_run_text or self.translator_soc.get(id) == prev_run_text:
                        return row
                return None

            setting = get_setting()

            if setting:
                self.apply_run_styles(curr_run, setting)

            if prev_run_text in (
                    'Заголовок',
                    'Краткое содержание',
                    'Пост',
                    'Хабарлама тақырыбы',
                    'Қысқаша мазмұны',
                    'Title',
                    'Summary',
                    'Post',
            ):
                paragraph._p.remove(prev_run._r)

            if prev_run_text == '№':
                paragraph._p.remove(curr_run._r)
                paragraph._p.remove(prev_run._r)

        if not self._settings:
            return

        scheduler = self._template.paragraphs

        prev_run = None
        rows = self._settings['list_rows']
        for paragraph in scheduler:
            for idx, run in enumerate(paragraph.runs, start=1):
                curr_run = run

                if prev_run:
                    self.highlight_tag(curr_run, paragraph, self._tags, prev_run.text, self._tags_highlight_settings)

                if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .?=-]*', curr_run.text.strip()):
                    if prev_run.text.strip(':') == 'URL':
                        self.add_hyperlink(paragraph, curr_run.text.strip(), 'Ссылка', '#0000FF', '#000080')

                        paragraph._p.remove(curr_run._r)

                if idx % 2 == 0:
                    manage_styles(paragraph, curr_run, prev_run, rows)
                else:
                    prev_run = run