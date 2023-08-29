import pandas as pd


class DataSorter:

    def __init__(self, data: list[dict], order: dict):
        self._data = data
        self._order = order

    @property
    def data(self):
        return self._data

    @property
    def order(self):
        return self._order

    def sort_data(self) -> list[dict]:

        if not self.order:
            return self.data

        date = self.order.get('date')
        predominantly = self.order.get('predominantly')
        sentiments = self.order.get('sentiments')
        categories = self.order.get('categories')

        data = pd.DataFrame(self.data)

        table_data = self.delete_unused_sentiments(data, sentiments)

        table_data = self.delete_unused_categories(table_data, categories)

        if sentiments and categories:
            if predominantly == 0:
                sorted_table_data = self.sort_by_sentiment_category_date(table_data, date)
            else:
                sorted_table_data = self.sort_by_category_sentiment_date(table_data, date)
        elif sentiments != 0:
            sorted_table_data = self.sort_by_sentiment_date(table_data, date)
        elif categories != 0:
            sorted_table_data = self.sort_by_category_date(table_data, date)
        else:
            sorted_table_data = self.sort_by_date(table_data, date)

        sorted_table_data = sorted_table_data.to_dict(orient='records')

        return sorted_table_data

    @staticmethod
    def delete_unused_sentiments(
            dataframe: pd.DataFrame,
            sentiments: list[int],
    ) -> pd.DataFrame:
        if sentiments:
            mask = None
            for idx, sentiment in enumerate(sentiments):
                if idx == 0 and sentiment == 0:
                    mask = (dataframe['sentiment'] != 1)
                elif idx == 1 and sentiment == 0:
                    mask = (mask & (dataframe['sentiment'] != -1))
                elif idx == 2 and sentiment == 0:
                    mask = (mask & (dataframe['sentiment'] != 0))

            if mask is not None:
                dataframe = dataframe[mask]

        return dataframe

    @staticmethod
    def delete_unused_categories(
            dataframe: pd.DataFrame,
            categories: list[str],
    ) -> pd.DataFrame:

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

        if categories:
            mask = None
            if 'name_cat' in dataframe.columns:
                mask = dataframe['name_cat'].isin(categories)
            elif 'type' in dataframe.columns:
                mask = dataframe['type'].map(soc_types).isin(categories)
            if mask is not None:
                dataframe = dataframe[mask]

        return dataframe

    @staticmethod
    def sort_by_sentiment_category_date(
            dataframe: pd.DataFrame,
            date: int,
    ) -> pd.DataFrame:

        sort_key = None
        if 'name_cat' in dataframe.columns:
            sort_key = [
                'sentiment',
                'name_cat',
                'nd_date',
            ]
        elif 'type' in dataframe.columns:
            sort_key = [
                'sentiment',
                'type',
                'date',
            ]

        if sort_key is not None:
            sorted_dataframe = dataframe.sort_values(by=sort_key, ascending=date == 1)
            return sorted_dataframe

        return dataframe

    @staticmethod
    def sort_by_category_sentiment_date(
            dataframe: pd.DataFrame,
            date: int,
    ) -> pd.DataFrame:

        sort_key = None
        if 'name_cat' in dataframe.columns:
            sort_key = [
                'name_cat',
                'sentiment',
                'nd_date',
            ]
        elif 'type' in dataframe.columns:
            sort_key = [
                'type',
                'sentiment',
                'date',
            ]

        if sort_key is not None:
            sorted_dataframe = dataframe.sort_values(by=sort_key, ascending=date == 1)
            return sorted_dataframe

        return dataframe

    @staticmethod
    def sort_by_sentiment_date(dataframe: pd.DataFrame, date: int) -> pd.DataFrame:

        if dataframe.empty:
            return dataframe

        sort_key = None
        if 'nd_date' in dataframe.columns:
            sort_key = [
                'sentiment',
                'nd_date',
            ]
        elif 'date' in dataframe.columns:
            sort_key = [
                'sentiment',
                'date',
            ]

        if sort_key is not None:
            sorted_dataframe = dataframe.sort_values(by=sort_key, ascending=date == 1)
            return sorted_dataframe

        return dataframe

    @staticmethod
    def sort_by_category_date(
            dataframe: pd.DataFrame,
            date: int,
    ) -> pd.DataFrame:

        if dataframe.empty:
            return dataframe

        sort_key = None
        if 'nd_date' in dataframe.columns:
            sort_key = [
                'name_cat',
                'nd_date',
            ]
        elif 'date' in dataframe.columns:
            sort_key = [
                'type',
                'date',
            ]

        if sort_key is not None:
            sorted_dataframe = dataframe.sort_values(by=sort_key, ascending=date == 1)
            return sorted_dataframe

        return dataframe

    @staticmethod
    def sort_by_date(dataframe: pd.DataFrame, date: int) -> pd.DataFrame:

        sorted_dataframe = None

        if 'nd_date' in dataframe.columns:
            sorted_dataframe = dataframe.sort_values(by='nd_date', ascending=date == 1)
        elif 'date' in dataframe.columns:
            sorted_dataframe = dataframe.sort_values(by='date', ascending=date == 1)
        if sorted_dataframe is not None:
            return sorted_dataframe

        return dataframe
