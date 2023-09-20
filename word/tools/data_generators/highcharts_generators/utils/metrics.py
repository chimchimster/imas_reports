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
    def count_percentage_of_smi_distribution(categories_distribution: dict) -> dict:
        """ Считаем процентное соотношение по СМИ. """

        distribution_percents = {k: 0 for k, _ in categories_distribution.items()}
        categories_distribution_names = list(categories_distribution.keys())

        total = sum(categories_distribution.values())

        for name in categories_distribution_names:
            distribution_percents[name] = round(categories_distribution[name] * 100 / total, 2)

        return distribution_percents
