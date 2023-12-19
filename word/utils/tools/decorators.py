import functools
import itertools
import multiprocessing
import os
import re
import time
from functools import wraps
from typing import Callable

import docx
import requests
from docx.shared import Cm

from word.tools import HighchartsCreator, MetricsGenerator
from word.local import ReportLanguagePicker
from .mixins import DiagramPickerInjector
from .auxiliary_classes import ChartColorDistribution

from docxtpl import DocxTemplate, InlineImage
from .auxiliary_functions import generate_chart_categories


def render_diagram(color_flag: str = None, context_flag: bool = False) -> Callable:
    def outter_wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner_wrapper(self, **kwargs) -> None:

            template: DocxTemplate = DocxTemplate(self._template_path)

            _position: str = self.proc_obj.settings.get('position')
            diagram_type: str = self.proc_obj.settings.get('type')
            data_labels: bool = self.proc_obj.settings.get('data_labels')

            highcharts_obj = HighchartsCreator(
                self.report_format,
                self.proc_obj.folder,
            )

            class_name = self.__class__.__name__

            path_to_image: str = os.path.join(
                os.getcwd(),
                'word',
                'highcharts_temp_images',
                f'{self.proc_obj.folder.unique_identifier}',
                class_name + '.png'
            )

            output_path: str = os.path.join(
                os.getcwd(),
                'word',
                'temp',
                f'{self.proc_obj.folder.unique_identifier}',
                f'output-{_position}-messages-{class_name}.docx'
            )

            chart_categories, chart_series, func_kwargs = func(self, diagram_type=diagram_type, **kwargs)

            chart_colors = ['#8B3A3A', '#FFC1C1']
            if chart_categories:
                chart_color_distribution = ChartColorDistribution(len(chart_categories), color_flag)
                colors_palette_obj = chart_color_distribution.set_range_of_colors()
                chart_colors = getattr(colors_palette_obj, color_flag)

            query_string: str = DiagramPickerInjector(
                highcharts_obj,
                diagram_type,
                chart_color=chart_colors,
                chart_categories=[chart.get('name') for chart in chart_categories],
                data_labels=data_labels,
                chart_series=chart_series,
            ).pick_and_execute()

            response = highcharts_obj.do_post_request_to_highcharts_server(query_string)

            highcharts_obj.save_data_as_png(response, path_to_image)

            image: InlineImage = InlineImage(template, image_descriptor=path_to_image)

            if context_flag:

                new_func_kwargs = {'context': func_kwargs, 'image': image}
                try:
                    template.render({
                        **new_func_kwargs
                    }, autoescape=True)
                except docx.image.exceptions.UnrecognizedImageError:

                    image = InlineImage(template, image_descriptor=os.path.join(
                        os.getcwd(),
                        'word',
                        'static',
                        'data_not_found.png',
                        ),
                        width=500,
                        height=500,
                    )
                    new_func_kwargs = {'context': func_kwargs, 'image': image}

                    template.render({
                        **new_func_kwargs
                    }, autoescape=True)

            else:
                func_kwargs['image'] = image

                try:
                    template.render({
                        **func_kwargs
                    }, autoescape=True)
                except docx.image.exceptions.UnrecognizedImageError:
                    func_kwargs['image'] = InlineImage(template, image_descriptor=os.path.join(
                        os.getcwd(),
                        'word',
                        'static',
                        'data_not_found.png',
                        ),
                        width=500,
                        height=500,
                    )

                    new_func_kwargs = {'image': image}

                    template.render({
                        **new_func_kwargs
                    }, autoescape=True)

            template.save(output_path)

        return inner_wrapper

    return outter_wrapper


def throw_params_for_distribution_diagram(
        category_names_key: str = None,
        title_key: str = None,
        distribution_keys: tuple[str, str] = None,
        distribution_translate: bool = False,
        has_distribution: str = None,
):
    def outter_wrapper(func: Callable):
        @wraps(func)
        def inner_wrapper(self, **kwargs) -> tuple:

            report_language = ReportLanguagePicker(self.report_format)

            diagram_type: str = kwargs.pop('diagram_type')

            title: str = report_language().get('titles').get(title_key)

            if not has_distribution:
                distribution: list[dict, ...] = self.proc_obj.response_part.get(category_names_key)
            elif has_distribution == 'count_most_popular_metrix':
                metrics_soc = self.proc_obj.response_part.get('f_news2')
                distribution: list[dict, ...] = MetricsGenerator.count_most_popular_metrics(metrics_soc)
                title += ' ' + report_language().get('categories_soc').get(
                    str(MetricsGenerator.define_most_popular_resources(metrics_soc))
                )
            elif has_distribution == 'count_top_negative':
                metrix_soc = self.proc_obj.response_part.get('f_news2')
                metrix_smi = self.proc_obj.response_part.get('f_news')
                distribution: list[dict, ...] = MetricsGenerator.count_top_negative(
                    metrics_smi=metrix_smi,
                    metrics_soc=metrix_soc,
                    which=['soc', 'smi']
                )

                title = report_language().get('titles').get('top_negative')
            elif has_distribution == 'count_top_negative_smi':
                metrix_soc = self.proc_obj.response_part.get('f_news2')
                metrix_smi = self.proc_obj.response_part.get('f_news')
                distribution: list[dict, ...] = MetricsGenerator.count_top_negative(
                    metrics_smi=metrix_smi,
                    metrics_soc=metrix_soc,
                    which=['smi']
                )
                title = report_language().get('titles').get('smi_top_negative')
            elif has_distribution == 'count_top_negative_soc':
                metrix_soc = self.proc_obj.response_part.get('f_news2')
                metrix_smi = self.proc_obj.response_part.get('f_news')
                distribution: list[dict, ...] = MetricsGenerator.count_top_negative(
                    metrics_smi=metrix_smi,
                    metrics_soc=metrix_soc,
                    which=['soc']
                )
                title = report_language().get('titles').get('soc_top_negative')

            distribution: list[dict] = [
                {d[distribution_keys[0]]: d[distribution_keys[1]] for _, _ in d.items()} for d in distribution
            ]

            distribution_union: dict = {}

            for s_m_d in distribution:
                distribution_union.update(s_m_d)

            if distribution_translate:
                categories_translate: dict = report_language().get('categories_smi')
                distribution_union: dict = {categories_translate[k]: v for k, v in distribution_union.items()}

            percentages_of_soc_distribution: dict = MetricsGenerator().count_percentage_of_smi_soc_distribution(
                distribution_union)

            args: tuple = tuple([(k, v) for k, v in distribution_union.items()])

            chart_categories: list[dict] = generate_chart_categories(*args)

            chart_series: list[dict] = [
                {
                    'type': diagram_type,
                    'data': chart_categories,
                },
            ]

            context = {}

            if len(distribution_union) > 20:
                distribution_union = dict(
                    zip(list(distribution_union.keys())[:20], list(distribution_union.values())[:20])
                )

            for key, value in distribution_union.items():
                context[
                    re.sub(r'^\s+|\s+$', '', re.sub(r'[\r\n]+', ' ', key))
                ] = [int(value), percentages_of_soc_distribution[key]]

            context['title'] = title

            return chart_categories, chart_series, context

        return inner_wrapper

    return outter_wrapper


def render_map(
        json_marking_title: str = None,
        region_key: str = None,
        stat_map_key: str = None,
        map_type: str = None,
):
    def outer_wrapper(func: Callable):
        @functools.wraps(func)
        def inner_wrapper(self):

            template: DocxTemplate = DocxTemplate(self._template_path)

            countries_or_regions_hc = self.proc_obj.response_part.get(region_key) if region_key is not None else None
            stat_map = self.proc_obj.response_part.get(stat_map_key)

            path_to_stats_map = os.path.join(
                os.getcwd(),
                'word',
                'static',
                'geo',
                json_marking_title,
            )

            position = self.proc_obj.settings.get('position')

            path_to_image: str = os.path.join(
                os.getcwd(),
                'word',
                'highcharts_temp_images',
                f'{self.proc_obj.folder.unique_identifier}',
                self.__class__.__name__ + '.png'
            )

            output_path: str = os.path.join(
                os.getcwd(),
                'word',
                'temp',
                f'{self.proc_obj.folder.unique_identifier}',
                f'output-{position}-messages-{self.__class__.__name__}.docx'
            )

            length = self.proc_obj.settings.get('length')
            number = self.proc_obj.settings.get('number')
            percent = self.proc_obj.settings.get('percent')

            with open(path_to_stats_map, 'r') as stats_map_file:

                highcharts_map_creator_object = HighchartsCreator(self.report_format, self.proc_obj.folder)

                query_string = highcharts_map_creator_object.world_or_kz_map(
                    stats_map_file.read(),
                    stat_map,
                )

                response = highcharts_map_creator_object.do_post_request_to_highcharts_server(query_string)

                response = requests.get(f'{highcharts_map_creator_object.highcharts_server}/{response.text}')

                highcharts_map_creator_object.save_data_as_png(response, path_to_image)

                image: InlineImage = InlineImage(template, image_descriptor=path_to_image, width=Cm(23), height=Cm(15))

                context_items = MetricsGenerator.count_world_or_kz_map(
                    stat_map,
                    countries_or_regions_hc,
                    self.report_format
                )[:length]

                langs_dict = ReportLanguagePicker(self.report_format)()

                title = langs_dict.get('titles').get(map_type)

                context = {
                    'title': title,
                    'image': image,
                    'data': itertools.zip_longest(
                        context_items[:len(context_items) // 2], context_items[len(context_items) // 2 + 1:],
                        fillvalue=''
                    ),
                    'number': number,
                    'percent': percent,
                }

                try:
                    template.render(context, autoescape=True)
                except docx.image.exceptions.UnrecognizedImageError:
                    context['image'] = InlineImage(
                        template,
                        image_descriptor=os.path.join(
                            os.getcwd(),
                            'word',
                            'static',
                            'data_not_found.png',
                        ),
                        width=500,
                        height=500,
                       )

                    template.render({
                        **context
                    }, autoescape=True)

                template.save(output_path)

        return inner_wrapper

    return outer_wrapper
