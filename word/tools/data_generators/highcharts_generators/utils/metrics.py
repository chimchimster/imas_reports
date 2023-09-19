from datetime import datetime, timedelta


class MetricsGenerator:

    def __init__(
            self,
            smi_news: list[dict] = None,
            soc_news: list[dict] = None,
            start_date: str = None,
            end_date: str = None,
            positive_count: int = None,
            negative_count: int = None,
            neutral_count: int = None,
            soc_count: int = None,
            smi_count: int = None,
    ) -> None:
        self._smi_news = smi_news
        self._soc_news = soc_news
        self._start_date = start_date
        self._end_date = end_date
        self._positive_count = positive_count
        self._negative_count = negative_count
        self._neutral_count = neutral_count
        self._soc_count = soc_count
        self._smi_count = smi_count

    @property
    def soc_count(self) -> int:
        return self._soc_count

    @property
    def smi_count(self) -> int:
        return self._smi_count

    @property
    def smi_news(self) -> list:
        return self._smi_news

    @property
    def soc_news(self) -> list:
        return self._soc_news

    @property
    def start_date(self) -> str:
        return self._start_date

    @property
    def end_date(self) -> str:
        return self._end_date

    @property
    def positive(self) -> int:
        return self._positive_count

    @property
    def negative(self) -> int:
        return self._negative_count

    @property
    def neutral(self) -> int:
        return self._neutral_count

    def define_timedelta(self) -> list:
        """ Определяем даты (временные промежутки по оси X) для chart_categories. """

        start_date_obj = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(self.end_date, '%Y-%m-%d')

        if start_date_obj == end_date_obj:
            return [f'0{date}:00' if date < 10 else f'{date}:00' for date in range(24)]

        timedelta_days = (end_date_obj - start_date_obj).days
        date_list = [start_date_obj + timedelta(days=date) for date in range(timedelta_days + 1)]
        return [date.strftime('%Y-%m-%d') for date in date_list]

    def count_messages(self) -> list | None:
        """ Считаем количество сообщений по дням/часам. """

        counter = {}

        def count(messages: list, date_format: str = '%d-%m-%Y') -> None:

            for data in messages:
                timestamp = None
                if 'nd_date' in data:
                    timestamp = datetime.fromtimestamp(data['nd_date'])
                elif 'date' in data:
                    timestamp = datetime.fromtimestamp(data['date'])

                if not timestamp:
                    return

                timestamp = timestamp.strftime(date_format)

                if timestamp not in counter:
                    counter[timestamp] = 0
                else:
                    counter[timestamp] += 1

        count(self.soc_news)
        count(self.smi_news)

        if len(counter) == 1:
            """ Значит отчет должен формироваться не по дням, а по часам. """
            counter.clear()
            count(self.soc_news, '%H')
            count(self.smi_news, '%H')

        if counter:
            return list(counter.values().__reversed__())
        return

    def count_percentage_of_sentiments(self) -> dict:
        """ Ситчаем процентное соотношение тональностей. """

        sentiments_percents = {'pos': 0, 'neg': 0, 'neu': 0}

        total = self.positive + self.negative + self.neutral

        sentiments_percents['pos'] = round(self.positive * 100 / total, 2)
        sentiments_percents['neg'] = round(self.negative * 100 / total, 2)
        sentiments_percents['neu'] = round(self.neutral * 100 / total, 2)

        return sentiments_percents

    def count_percentage_of_distribution(self) -> dict:
        """ Ситчаем процентное соотношение по СМИ, Соцсетям. """

        distribution_percents = {'smi': 0, 'soc': 0}

        total = self.smi_count + self.soc_count

        distribution_percents['smi'] = round(self.smi_count * 100 / total, 2)
        distribution_percents['soc'] = round(self.soc_count * 100 / total, 2)

        return distribution_percents