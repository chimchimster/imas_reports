import re

from word.local import ReportLanguagePicker
from docxtpl import DocxTemplate, InlineImage
from .table_style import TableStylesGenerator


class SchedulerStylesGenerator(TableStylesGenerator):

    def __init__(
            self,
            template: DocxTemplate,
            settings: dict,
            static_settings: dict,
            tags: list,
            tags_highlight_settings: dict,
    ) -> None:
        super().__init__(
            template,
            settings,
            static_settings,
            tags,
            tags_highlight_settings,
        )

    def apply_scheduler_styles(self):

        def manage_styles(_paragraph, _curr_run, _prev_run, _rows):

            prev_run_text = _prev_run.text.rstrip(':')

            def get_setting():
                for row in _rows:
                    _id = row.get('id')
                    if self.translator_smi.get(_id) == prev_run_text or self.translator_soc.get(_id) == prev_run_text:
                        return row
                return None

            _setting = get_setting()

            if _setting:
                self.apply_run_styles(_curr_run, _setting)

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
                _curr_run._r.text = _curr_run._r.text.lstrip()
                _paragraph._p.remove(_prev_run._r)

            if prev_run_text == '№':
                _paragraph._p.remove(_curr_run._r)
                _paragraph._p.remove(_prev_run._r)

        if not self._settings:
            return

        scheduler = self.template.paragraphs

        _format = self.static_settings.get('format', 'word_rus')

        dict_languages = ReportLanguagePicker(_format)()

        link_name = dict_languages.get('link', 'Ссылка')

        prev_run = None
        rows = self.settings['list_rows']
        for paragraph in scheduler:
            for idx, run in enumerate(paragraph.runs, start=1):
                curr_run = run

                if prev_run:
                    self.highlight_tag(curr_run, paragraph, self.tags, prev_run.text, self.tags_highlight_settings)

                if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .?=-]*', curr_run.text.strip()):
                    if prev_run.text.strip(':') == 'URL':
                        self.add_hyperlink(paragraph, curr_run.text.strip(), link_name, '#0000FF', '#000080')

                        paragraph._p.remove(curr_run._r)

                if idx % 2 == 0:
                    manage_styles(paragraph, curr_run, prev_run, rows)
                else:
                    prev_run = run