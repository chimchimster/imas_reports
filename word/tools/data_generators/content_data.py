class ContentGenerator:

    flag = 'content'

    def __init__(self, data, rest_data):
        self._data = data
        self._rest_data = rest_data
        self.data_collection = {'soc': [], 'smi': []}

    def generate_data(self):

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

        def check_length_of_title_or_text(post):

            post = post.strip()

            if len(post) > 150:
                return post[:cut] + ' ...'

            return post

        if self._rest_data.get('id') == 'contents':
            count_soc = self._rest_data.get('soc')
            count_smi = self._rest_data.get('smi')

            soc_posts = self._data.get('f_news2')
            smi_posts = self._data.get('f_news')

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