from datetime import datetime
from operator import itemgetter

from .utils import DataSorter
from word.local import ReportLanguagePicker
from word.mixins import PropertyMethodsMixin


class TableContentGenerator(PropertyMethodsMixin):

    flag: str = 'table'

    translator_smi: dict = {}
    translator_soc: dict = {}

    def __init__(
            self,
            response_part: dict,
            settings: dict,
            static_settings: dict,
            _type: str,
    ) -> None:
        self._response_part = response_part
        self._settings = settings
        self._static_settings = static_settings
        self._type = _type
        self._data_collection = []
        self.pick_language('content')

    def pick_language(self, _type):

        obj_format = self.static_settings.get('format')

        if not obj_format:
            obj_format = 'word_rus'

        language_dicts = ReportLanguagePicker(obj_format)()

        smi = language_dicts.get(_type, {}).get('translator_smi', {})
        soc = language_dicts.get(_type, {}).get('translator_soc', {})

        self.translator_smi.update(smi)
        self.translator_soc.update(soc)

    def generate_data(self):

        soc_types = {
            1: 'Вконтакте',
            2: 'Facebook',
            3: 'Twitter',
            4: 'Instagram',
            5: 'LinkedIn',
            6: 'Youtube',
            7: 'Одноклассники',
            8: 'Мой Мир',
            9: 'Telegram',
            10: 'TikTok',
        }

        def sort_data(table_data) -> list[list]:
            """ Данная функция работает, но применяет сортировки значительно медленее, чем Pandas.
                Поэтому функция использоваться в дальнейшем не будет. Оставляю ее как архивную. """

            order = self.settings.get('order')

            if not order:
                return table_data

            date = order.get('date')
            predominantly = order.get('predominantly')
            sentiments = order.get('sentiments')
            categories = order.get('categories')

            def delete_unused_sentiments(_table_data):

                if not _table_data:
                    return []

                if sentiments:
                    for idx, sentiment in enumerate(sentiments):
                        if idx == 0 and sentiment == 0:
                            _table_data = [table for table in _table_data if table['sentiment'] != 1]
                        elif idx == 1 and sentiment == 0:
                            _table_data = [table for table in _table_data if table['sentiment'] != -1]
                        elif idx == 2 and sentiment == 0:
                            _table_data = [table for table in _table_data if table['sentiment'] != 0]

                    return _table_data

                return _table_data

            def delete_unused_categories(_table_data):

                if not _table_data:
                    return []

                if categories:
                    if _table_data[0].get('name_cat'):
                        return [table for table in _table_data if table['name_cat'] in categories]
                    elif _table_data[0].get('type'):
                        return [table for table in _table_data if soc_types[table['type']] in categories]

                return _table_data

            def sort_by_sentiment_category_date(_table_data):

                if not _table_data:
                    return []

                sentiment_index = {1: 0, 0: 1, -1: 2}

                category_index = {category: i for i, category in enumerate(categories)}

                if _table_data[0].get('name_cat'):
                    return sorted(_table_data, key=lambda x: (
                        sentiment_index[x['sentiment']], category_index.get(x['name_cat'], len(categories)), x['nd_date']),
                                  reverse=date == 0)
                elif _table_data[0].get('type'):
                    return sorted(_table_data, key=lambda x: (
                        sentiment_index[x['sentiment']], category_index.get(x['type'], len(categories)), x['date']),
                                  reverse=date == 0)

                return _table_data

            def sort_by_category_sentiment_date(_table_data):

                if not _table_data:
                    return []

                sentiment_index = {1: 0, 0: 1, -1: 2}

                category_index = {category: i for i, category in enumerate(categories)}

                if _table_data[0].get('name_cat'):
                    return sorted(_table_data, key=lambda x: (
                        category_index.get(x['name_cat'], len(categories)), sentiment_index[x['sentiment']], x['nd_date']),
                                  reverse=date == 0)
                elif _table_data[0].get('type'):
                    return sorted(_table_data, key=lambda x: (
                        category_index.get(x['type'], len(categories)), sentiment_index[x['sentiment']], x['date']),
                                  reverse=date == 0)

                return _table_data

            def sort_by_sentiment_date(_table_data):

                if not _table_data:
                    return []

                if _table_data[0].get('nd_date'):
                    return sorted(_table_data, key=lambda x: (x['sentiment'], x['nd_date']), reverse=date == 0)
                elif _table_data[0].get('date'):
                    return sorted(_table_data, key=lambda x: (x['sentiment'], x['date']), reverse=date == 0)

                return _table_data

            def sort_by_category_date(_table_data):

                if not _table_data:
                    return []

                if _table_data[0].get('nd_date'):
                    return sorted(_table_data, key=lambda x: (x['name_cat'], x['nd_date']), reverse=date == 0)
                elif _table_data[0].get('date'):
                    return sorted(_table_data, key=lambda x: (x['type'], x['date']), reverse=date == 0)

                return _table_data

            def sort_by_date(_table_data):

                if not _table_data:
                    return []

                if _table_data[0].get('nd_date'):
                    return sorted(_table_data, key=itemgetter('nd_date'), reverse=date == 0)
                elif _table_data[0].get('date'):
                    return sorted(_table_data, key=itemgetter('date'), reverse=date == 0)

                return _table_data

            table_data = delete_unused_sentiments(table_data)

            table_data = delete_unused_categories(table_data)

            if sentiments and categories:
                if predominantly == 0:
                    sorted_table_data = sort_by_sentiment_category_date(table_data)
                else:
                    sorted_table_data = sort_by_category_sentiment_date(table_data)
            elif sentiments != 0:
                sorted_table_data = sort_by_sentiment_date(table_data)
            elif categories != 0:
                sorted_table_data = sort_by_category_date(table_data)
            else:
                sorted_table_data = sort_by_date(table_data)

            return sorted_table_data

        def translate(_key: str, _translator_type):

            order = self.settings.get('order')

            table_data = self.response_part.get(_key, [{}])

            news = DataSorter(table_data, order).sort_data()

            if news:
                self.__apply_translator(_translator_type, news)

        if self._type == 'smi':
            translate('f_news', self.translator_smi)
        else:
            translate('f_news2', self.translator_soc)

    def __apply_translator(self, translator, news):

        translator_for_rest_soc = {
            'number': 'number',
            'content': 'full_text',
            'date': 'date',
            'resource': 'resource_name',
            'news_link': 'news_link',
            'sentiment': 'sentiment',
            'category': 'type',
        }

        translator_for_rest_smi = {
            'number': 'number',
            'title': 'title',
            'content': 'full_text',
            'date': 'not_date',
            'resource': 'RESOURCE_NAME',
            'news_link': 'news_link',
            'sentiment': 'sentiment',
            'category': 'name_cat',
        }

        to_sort = {}
        to_delete = []

        def delete_unused_columns(_table, translator_type):
            for tbl in _table['columns']:
                column_name = tbl.get('id') if tbl.get('position') == 0 else None
                if column_name:
                    to_delete.append(translator_type[column_name])

        def sort_columns(_table, translator_type):
            for tbl in _table['columns']:
                to_sort[tbl.get('id')] = tbl['position']
            return {translator[translator_type[k]]: v for (k, v) in to_sort.items()}

        def update_collection():

            def choose_tag(_tags, value_string):

                for _tag in _tags:
                    if _tag.lower() in value_string.lower():
                        return _tag.lower()
                return ''

            text_length = self.settings.get('text_length')
            tags = self.response_part.get('query_ar')

            for i in range(len(news)):
                news[i] = {**{'number': i + 1}, **news[i]}

                if news[i].get('date'):
                    news[i]['date'] = datetime.fromtimestamp(news[i]['date']).strftime('%d-%m-%Y')

                if news[i].get('type'):
                    self.__match_social_medias(news[i])

                result = {}

                for key, value in news[i].items():

                    value = value.strip() if isinstance(value, str) else value

                    if key in translator:
                        if translator[key] in (
                                'Пост',
                                'Краткое содержание',
                                'Қысқаша мазмұны',
                                'Post',
                                'Title',
                                'Summary',
                        ):
                            tag = choose_tag(tags, value)
                            temp_val = value.lower()

                            if len(value) <= text_length:
                                result[translator[key]] = value
                                continue

                            if tag == '':
                                result[translator[key]] = (
                                        value[:text_length] + ' ...') if text_length < len(value) \
                                    else value[:text_length]
                                continue

                            tag_start = temp_val.find(tag)
                            if tag_start != -1:
                                tag_end = tag_start + len(tag)
                                left = max(0, tag_start - (text_length - len(tag)) // 2)
                                right = min(len(value), tag_end + (text_length - len(tag)) // 2)
                                result[translator[key]] = '...' + value[left:right] + '...'
                        else:
                            result[translator[key]] = value

                sorted_result = {k: v for (k, v) in sorted(result.items(), key=lambda x: to_sort[x[0]])}
                self.data_collection.append(sorted_result)

        if self.settings.get('id') == 'soc':
            delete_unused_columns(self.settings, translator_for_rest_soc)
        elif self.settings.get('id') == 'smi':
            delete_unused_columns(self.settings, translator_for_rest_smi)

        news = [{k: v for (k, v) in n.items() if k not in to_delete} for n in news]

        if self.settings.get('id') == 'soc':
            to_sort = sort_columns(self.settings, translator_for_rest_soc)
        elif self.settings.get('id') == 'smi':
            to_sort = sort_columns(self.settings, translator_for_rest_smi)

        update_collection()

    def __match_social_medias(self, data):
        match data.get('type'):
            case 1:
                data['type'] = 'Вконтакте'
            case 2:
                data['type'] = 'Facebook'
            case 3:
                data['type'] = 'Twitter'
            case 4:
                data['type'] = 'Instagram'
            case 5:
                data['type'] = 'LinkedIn'
            case 6:
                data['type'] = 'Youtube'
            case 7:
                data['type'] = 'Одноклассники'
            case 8:
                data['type'] = 'Мой Мир'
            case 9:
                data['type'] = 'Telegram'
            case 10:
                data['type'] = 'TikTok'