import os
import json
import requests

from functools import wraps
from typing import Any, Callable
from dataclasses import dataclass
from word.local import ReportLanguagePicker


class HighchartsCreator:

    def __init__(self, report_format: str, folder) -> None:
        self._report_format = report_format
        self._folder = folder
        self._headers: dict = {
            'content-type': 'application/json',
            'Accept': 'application/json',
        }
        self._highcharts_server: str = self.__get_highcharts_server()
        self._highcharts_settings_storage_object = HighchartsObject()

    @property
    def folder(self):
        return self._folder

    @property
    def report_format(self) -> str:
        return self._report_format

    @staticmethod
    def __get_highcharts_server() -> str:

        return os.environ.get('HIGHCHARTS_SERVER')

    @staticmethod
    def generate_query_for_bar_diagram(
            chart_categories: list[dict],
            chart_series: list[dict],
            chart_colors: list[str],
            width: int,
            height: int,
            font_size: int,
            labels: bool,
            data_labels: bool,
    ) -> str:
        bar_object = HighchartsObject(
            _series=chart_series,
            _colors=chart_colors,
            _categories=chart_categories,
            _width=width,
            _height=height,
            _font_size=font_size,
            _labels=labels,
            _data_labels=data_labels,
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

        return json.dumps(data)

    @staticmethod
    def generate_query_for_column_diagram(

            chart_categories: list[dict],
            chart_series: list[dict],
            chart_color: list[str],
            width: int,
            height: int,
            labels: bool,
            data_labels: bool,
            color_by_point: bool,
            font_size: int,
    ) -> str:
        column_obj = HighchartsObject(
            _categories=chart_categories,
            _series=chart_series,
            _colors=chart_color,
            _width=width,
            _height=height,
            _labels=labels,
            _data_labels=data_labels,
            _color_by_point=color_by_point,
            _font_size=font_size,
        )

        data = {
            'infile': {
                'colors': column_obj.colors,
                'title': {
                    'text': None
                },
                'chart': {
                    'type': 'column',
                    'width': column_obj.width,
                    'height': column_obj.width
                },
                'xAxis': {
                    'gridLineWidth': 0,
                    'categories': column_obj.categories,
                    'title': {
                        'text': None,
                    },
                    'labels': {
                        'enabled': column_obj.labels,
                        'style': {
                            'width': '160px',
                            'fontSize': column_obj.font_size,
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
                'series': column_obj.series,
                'plotOptions': {
                    'column': {
                        'dataLabels': {
                            'enabled': column_obj.data_labels,
                            'style': {
                                'color': column_obj.colors,
                            }
                        },
                        'colorByPoint': column_obj.color_by_point,
                    },
                },
            }
        }

        return json.dumps(data)

    @staticmethod
    def generate_query_for_pie_diagram(
            chart_categories: list[dict],
            chart_series: list[dict],
            chart_color: list[str],
            width: int,
            labels: bool,
            font_size: int,
            legend: bool,
    ) -> str:
        pie_obj = HighchartsObject(
            _series=chart_series,
            _categories=chart_categories,
            _colors=chart_color,
            _width=width,
            _labels=labels,
            _font_size=font_size,
            _legend=legend,
        )

        data = {
            'infile': {
                'colors': pie_obj.colors,
                'chart': {
                    'plotBackgroundColor': None,
                    'plotBorderWidth': None,
                    'plotShadow': False,
                    'width': width,
                },
                'credits': {
                    'enabled': False,
                },
                'title': {
                    'text': None,
                },
                'tooltip': {
                    'pointFormat': None,
                },
                'legend': {
                    'enabled': pie_obj.legend,
                },
                'plotOptions': {
                    'pie': {
                        'allowPointSelect': False,
                        'cursor': 'pointer',
                        'dataLabels': {
                            'enabled': pie_obj.labels,
                            'format': '{point.y}',
                            'style': {
                                'fontSize': pie_obj.font_size,
                            },
                        },
                    }
                },
                'series': pie_obj.series,
            }
        }

        return json.dumps(data)

    def generate_query_for_linear_diagram(
            self,
            chart_categories: list[dict],
            chart_series: list[dict],
    ) -> str:
        linear_obj = HighchartsObject(
            _series=chart_series,
            _categories=chart_categories,
        )

        langs_dict: dict = ReportLanguagePicker(self.report_format)()

        y_title: str = langs_dict.get('messages_dynamics')

        data = {
            'infile': {
                'chart': {
                    'type': 'area',
                    'width': 900,
                    'height': 300,
                },
                'title': {
                    'text': None,
                },
                'xAxis': {
                    'title': {
                        'text': None,
                    },
                    'categories': linear_obj.categories,
                    'allowDecimals': False,
                    'labels': {
                        'formatter': None,
                    },
                },
                'yAxis': {
                    'title': {
                        'text': y_title,
                    },
                    'labels': {
                        'formatter': None
                    },
                    'min': 0,
                },
                'legend': {
                    'enabled': False,
                },
                'plotOptions': {
                    'area': {
                        'fillColor': {
                            'linearGradient': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 1},
                            'stops': [
                            ],
                        },
                        'marker': {
                            'radius': 1,
                        },
                        'cursor': 'pointer',
                        'lineWidth': 1,
                        'states': {
                            'hover': {
                                'lineWidth': 0.3,
                            },
                        },
                        'threshold': None,
                    },
                    'series': {
                        'allowPointSelect': True,
                        'marker': {
                            'states': {
                                'select': {
                                    'fillColor': 'red',
                                    'lineWidth': 1.5,
                                    'lineColor': 'red',
                                },
                            },
                        },
                    },
                },
                'series': [{
                    'type': 'areaspline',
                    'data': linear_obj.series,
                }],
            },
        }

        return json.dumps(data)

    def do_post_request_to_highcharts_server(self, data: str) -> requests.models.Response:
        response = requests.post(
            self._highcharts_server,
            data=data.encode(),
            headers=self._headers,
            verify=False,
        )
        return response

    def save_data_as_png(self, response: requests.models.Response, path_to_image: str) -> None:

        path_to_highcharts_temp_images = os.path.join(
            os.getcwd(),
            'word',
            'highcharts_temp_images',
        )

        def create_highcharts_temp_images_directory() -> None:
            if not os.path.exists(path_to_highcharts_temp_images):
                os.mkdir(path_to_highcharts_temp_images)

        def create_unique_folder() -> None:

            if not os.path.exists(
                    os.path.join(
                        path_to_highcharts_temp_images,
                        f'{self.folder.unique_identifier}'
                    )
            ):
                os.mkdir(
                    os.path.join(
                        path_to_highcharts_temp_images,
                        f'{self.folder.unique_identifier}'
                    )
                )

        create_highcharts_temp_images_directory()
        create_unique_folder()

        with open(path_to_image, 'wb') as file:
            for _bytes in response:
                file.write(_bytes)


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
