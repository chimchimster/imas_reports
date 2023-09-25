from typing import Any
from collections import Counter
from datetime import datetime, timedelta


class MetricsGenerator:

    @staticmethod
    def define_timedelta(start_date: str, end_date: str) -> list:
        """ Определяем даты (временные промежутки по оси X) для chart_categories. """

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        if start_date_obj == end_date_obj:
            return [f'0{date}:00' if date < 10 else f'{date}:00' for date in range(24)]

        timedelta_days = (end_date_obj - start_date_obj).days
        date_list = [start_date_obj + timedelta(days=date) for date in range(timedelta_days + 1)]
        return [date.strftime('%Y-%m-%d') for date in date_list]

    @staticmethod
    def count_messages(soc_news: list[dict], smi_news: list[dict]) -> list | None:
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

        count(soc_news)
        count(smi_news)

        if len(counter) == 1:
            # Значит отчет должен формироваться не по дням, а по часам. TODO: Костыль, будет время перепишу!
            counter.clear()
            count(soc_news, '%H')
            count(smi_news, '%H')

        if counter:
            return list(counter.values().__reversed__())
        return

    @staticmethod
    def count_percentage_of_sentiments(positive: int, negative: int, neutral: int) -> dict:
        """ Ситчаем процентное соотношение тональностей. """

        sentiments_percents = {'pos': 0, 'neg': 0, 'neu': 0}

        total = positive + negative + neutral

        sentiments_percents['pos'] = round(positive * 100 / total, 2)
        sentiments_percents['neg'] = round(negative * 100 / total, 2)
        sentiments_percents['neu'] = round(neutral * 100 / total, 2)

        return sentiments_percents

    @staticmethod
    def count_percentage_of_distribution(smi_count: int, soc_count: int) -> dict:
        """ Ситчаем процентное соотношение по СМИ, Соцсетям. """

        distribution_percents = {'smi': 0, 'soc': 0}

        total = smi_count + soc_count

        distribution_percents['smi'] = round(smi_count * 100 / total, 2)
        distribution_percents['soc'] = round(soc_count * 100 / total, 2)

        return distribution_percents

    @staticmethod
    def count_percentage_of_smi_soc_distribution(distribution: dict) -> dict:
        """ Считаем процентное соотношение по СМИ. """

        distribution_percents = {k: 0 for k, _ in distribution.items()}
        categories_distribution_names = list(distribution.keys())

        total = sum(map(int, distribution.values()))

        for name in categories_distribution_names:
            distribution_percents[name] = round(int(distribution[name]) * 100 / total, 2)

        return distribution_percents

    @staticmethod
    def define_most_popular_resources(metrics: list[dict, ...]) -> int:
        """ Определяем по какой именно соц сети будет вестись подсчет публикаций. """

        count_metrix_by_type_of_soc = Counter([dct['type'] for dct in metrics])
        max_soc_metrix = max(Counter([dct['type'] for dct in metrics]).values())

        return next((key for key, val in count_metrix_by_type_of_soc.items() if val == max_soc_metrix), 0)

    @staticmethod
    def count_most_popular_metrics(
            metrics: list[dict, ...],
            keys: tuple[str, ...] = ('resource_name', 'type'),
            param: Any = None
    ) -> list[dict, ...]:
        """ Считаем сколько публикаций было по каждому конкретному ресурсу. """

        if not param:
            param = MetricsGenerator.define_most_popular_resources(metrics)

        list_of_keys = [dct[keys[0]] for dct in metrics if dct[keys[1]] == param]

        count_keys = sorted(Counter(list_of_keys).items(), key=lambda x: x[1], reverse=True)[:20]

        return [{"resource_name": count_keys[i][0], "counter": count_keys[i][1]} for i in range(len(count_keys))]

    @staticmethod
    def count_top_negative(
            metrics_soc: list[dict, ...],
            metrics_smi: list[dict, ...],
            which: list[str],
    ) -> list[dict, ...]:
        """ Считаем ТОП негативных источников. """

        negative_sentiment = -1

        negative_soc = MetricsGenerator.count_most_popular_metrics(
            metrics_soc,
            keys=("resource_name", "sentiment"),
            param=negative_sentiment,
        )
        negative_smi = MetricsGenerator.count_most_popular_metrics(
            metrics_smi,
            keys=("RESOURCE_NAME", "sentiment"),
            param=negative_sentiment,
        )

        if len(which) == 2:
            return negative_soc + negative_smi
        if which[-1] == 'soc':
            return negative_soc
        else:
            return negative_smi


