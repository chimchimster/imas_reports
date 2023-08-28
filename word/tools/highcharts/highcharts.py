import json
import os
from typing import Any, Callable

import requests
from dataclasses import dataclass
from functools import wraps


class HighchartsCreator:

    def __init__(self, lang: str) -> None:
        self._lang = lang
        self._headers: dict = {
            'content-type': 'application/json',
            'Accept': 'application/json',
        }
        self._highcharts_server: str = self.__get_highcharts_server()
        self._highcharts_settings_storage_object = HighchartsObject()

    @property
    def lang(self) -> str:
        return self._lang

    @staticmethod
    def __get_highcharts_server() -> str:
        from dotenv import load_dotenv

        load_dotenv()

        return os.environ.get('HIGHCHARTS_SERVER')

    def generate_bar_diagram(self):
        chart_categories = [
            {
                'name': 'name1',
                'y': 100,
            },
            {
                'name': 'name2',
                'y': 200,
            },
            {
                'name': 'name3',
                'y': 300,
            }]

        chart_series = [
            {
                'type': 'bar',
                'data': chart_categories
            },
        ]
        chart_colors = ['#1BB394', '#EC5D5D', '#F2C94C']

        bar_object = HighchartsObject(
            _series=chart_series,
            _colors=chart_colors,
            _categories=[x.get('name') for x in chart_categories],
            _width=445,
            _height=550,
            _font_size=11,
            _labels=True,
            _data_labels=True,
        )

        data = {
            'infile': {
                'colors': bar_object.colors,
                'title': {
                    'text': None
                },
                'chart': {
                    'type': 'bar',
                    'width': bar_object.width,
                    'height': bar_object.height
                },
                'xAxis': {
                    'gridLineWidth': 0,
                    'categories': bar_object.categories,
                    'title': {
                        'text': None,
                    },
                    'labels': {
                        'enabled': bar_object.labels,
                        'style': {
                            'width': '160px',
                            'fontSize': bar_object.font_size,
                            'lineHeight': '7px',
                            'fontWeight': 'bold',
                            'color': '#4F4F4F',
                        },
                    },
                },
                'yAxis': {
                    'gridLineWidth': 0,
                    'title': {
                        'text': None,
                    },
                    'labels': {
                        'enabled': False,
                    },
                },
                'legend': {
                    'enabled': False,
                },
                'series': bar_object.series,
                'plotOptions': {
                    'bar': {
                        'dataLabels': {
                            'enabled': bar_object.data_labels,
                            'style': {
                                'color': bar_object.colors,
                                'fontSize': bar_object.font_size,
                                'fontWeight': 'bold',
                            }
                        },
                        'colorByPoint': bar_object.color_by_point,
                    },
                },
            }
        }

        data = json.dumps(data)

        res = requests.post(self._highcharts_server,
                            data=data.encode(),
                            headers=self._headers,
                            verify=False)

        with open('bytes-png.png', 'wb') as f:
            for r in res:
                f.write(r)


@dataclass
class HighchartsObject:
    _series: list | None = None
    _colors: list | None = None
    _categories: list | None = None
    _width: int | None = None
    _height: int | None = None
    _font_size: int | None = None
    _labels: bool = False
    _data_labels: bool = False
    _color_by_point: bool = False
    _legend: bool = False

    @staticmethod
    def check_type_of_value(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(instance, value: Any, allowed_type: Any) -> None:
            if not isinstance(value, allowed_type):
                raise TypeError(f'Атрибут {func.__name__} должен быть типа {allowed_type}.')
            func(instance, value)

        return wrapper

    @property
    def series(self) -> list | None:
        return self._series

    @series.setter
    @check_type_of_value
    def series(self, value: list, allowed_type=list) -> None:
        self._series = value

    @property
    def colors(self) -> list | None:
        return self._colors

    @colors.setter
    @check_type_of_value
    def colors(self, value: list, allowed_type=list) -> None:
        self._colors = value

    @property
    def categories(self) -> list | None:
        return self._categories

    @categories.setter
    @check_type_of_value
    def categories(self, value: list, allowed_type=list) -> None:
        self._categories = value

    @property
    def width(self) -> int | None:
        return self._width

    @width.setter
    @check_type_of_value
    def width(self, value: int, allowed_type=int) -> None:
        self._width = value

    @property
    def height(self) -> int | None:
        return self._height

    @height.setter
    @check_type_of_value
    def height(self, value: int, allowed_type=int) -> None:
        self._height = value

    @property
    def font_size(self) -> int | None:
        return self._font_size

    @font_size.setter
    @check_type_of_value
    def font_size(self, value: int, allowed_type=int) -> None:
        self._font_size = value

    @property
    def labels(self) -> bool | None:
        return self._labels

    @labels.setter
    @check_type_of_value
    def labels(self, value: bool, allowed_type=bool) -> None:
        self._labels = value

    @property
    def data_labels(self) -> bool | None:
        return self._data_labels

    @data_labels.setter
    @check_type_of_value
    def data_labels(self, value: bool, allowed_type=bool) -> None:
        self._data_labels = value

    @property
    def color_by_point(self) -> bool | None:
        return self._color_by_point

    @color_by_point.setter
    @check_type_of_value
    def color_by_point(self, value: bool, allowed_type=bool) -> None:
        self._color_by_point = value

    @property
    def legend(self) -> bool | None:
        return self._legend

    @legend.setter
    @check_type_of_value
    def legend(self, value: bool, allowed_type=bool) -> None:
        self._legend = value


if __name__ == '__main__':
    h = HighchartsCreator('rus')
    h.generate_bar_diagram()
