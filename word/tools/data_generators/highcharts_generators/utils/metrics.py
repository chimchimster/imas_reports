from datetime import datetime, timedelta


class MetricsGenerator:

    def __init__(
            self,
            smi_news: int,
            soc_news: int,
            start_date: str,
            end_date: str,
    ) -> None:
        self._smi_news = smi_news
        self._soc_news = soc_news
        self._start_date = start_date
        self._end_date = end_date

    @property
    def smi_news(self) -> int:
        return self._smi_news

    @property
    def soc_news(self) -> int:
        return self._soc_news

    @property
    def start_date(self) -> str:
        return self._start_date

    @property
    def end_date(self) -> str:
        return self._end_date

    def define_timedelta(self) -> list:
        """ Определяем даты (временные промежутки по оси X) для chart_categories. """

        start_date_obj = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(self.end_date, '%Y-%m-%d')

        if start_date_obj == end_date_obj:
            return [f'0{date}:00' if date < 10 else f'{date}:00' for date in range(24)]

        timedelta_days = (end_date_obj - start_date_obj).days
        date_list = [start_date_obj + timedelta(days=date) for date in range(timedelta_days + 1)]
        return [date.strftime('%Y-%m-%d') for date in date_list]