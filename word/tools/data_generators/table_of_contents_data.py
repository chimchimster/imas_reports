from word.mixins import PropertyMethodsMixin


class ContentGenerator(PropertyMethodsMixin):

    flag: str = 'content'

    def __init__(
            self,
            response_part,
            settings,
            static_settings,
    ) -> None:
        self._response_part = response_part
        self._settings = settings
        self._static_settings = static_settings
        self._data_collection = {'soc': [], 'smi': []}

    def generate_data(self) -> None:

        cut = 150

        def collect_titles_or_texts(news, counter, key):

            if counter > 50:
                counter = 50

            for idx in range(counter):
                try:
                    text_obj = news[idx][key][:cut].strip()

                    self.data_collection.append(text_obj + ' ...' if len(text_obj) == cut else text_obj)
                except IndexError:
                    pass

        def check_length_of_title_or_text(_post):

            _post = _post.strip()

            if len(_post) > 150:
                return _post[:cut] + ' ...'

            return _post

        if self.settings.get('id') == 'contents':
            count_soc = self.settings.get('soc')
            count_smi = self.settings.get('smi')

            soc_posts = self.response_part.get('f_news2')
            smi_posts = self.response_part.get('f_news')

            if count_smi > 0:
                collect_titles_or_texts(smi_posts, count_smi, 'title')
            else:

                for post in smi_posts:
                    self.data_collection['smi'].append(check_length_of_title_or_text(post.get('title')))

            if count_soc > 0:
                collect_titles_or_texts(soc_posts, count_soc, 'full_text')
            else:

                for post in soc_posts:
                    self.data_collection['soc'].append(check_length_of_title_or_text(post.get('full_text')))

        for key, value in self.data_collection.items():
            self.data_collection[key] = {k: v for (k, v) in enumerate(value, start=1)}