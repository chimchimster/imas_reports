import os
from functools import wraps
from typing import Callable

from docx.shared import Cm
from word.tools import HighchartsCreator, MetricsGenerator
from word.local import ReportLanguagePicker
from .mixins import DiagramPickerInjector

from docxtpl import DocxTemplate, InlineImage
from .auxiliary_functions import generate_chart_categories


def render_diagram(color_flag: str = None, context_flag: bool = False) -> Callable:
    colors_palette = {
        'sentiments': ['#1BB394', '#EC5D5D', '#F2C94C'],
        'distribution': ['#1BB394', '#EC5D5D'],
        'smi_distribution': [
            '#181bba', '#2528e8', '#2125eb', '#2327fa',
            '#3918a8', '#3e1ab8', '#431bcc', '#491de0',
            '#4f1ff2', '#5421ff', '#4816a6', '#571cc7',
            '#611de0',
        ],
        'soc_distribution': [
            '#181bba', '#2528e8', '#2125eb', '#2327fa',
            '#3918a8', '#3e1ab8', '#431bcc', '#491de0',
            '#4f1ff2', '#5421ff', '#4816a6', '#571cc7',
            '#611de0',
        ],
        'media_top': [
            '#181bba', '#2528e8', '#2125eb', '#2327fa',
            '#3918a8', '#3e1ab8', '#431bcc', '#491de0',
            '#4f1ff2', '#5421ff', '#4816a6', '#571cc7',
            '#611de0',
        ],
        'soc_top': [
            '#181bba', '#2528e8', '#2125eb', '#2327fa',
            '#3918a8', '#3e1ab8', '#431bcc', '#491de0',
            '#4f1ff2', '#5421ff', '#4816a6', '#571cc7',
            '#611de0',
        ],
    }

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

            query_string: str = DiagramPickerInjector(
                highcharts_obj,
                diagram_type,
                chart_color=colors_palette.get(color_flag),
                chart_categories=[chart.get('name') for chart in chart_categories],
                data_labels=data_labels,
                chart_series=chart_series,
            ).pick_and_execute()

            response: str = highcharts_obj.do_post_request_to_highcharts_server(query_string)

            highcharts_obj.save_data_as_png(response, path_to_image)

            image: InlineImage = InlineImage(template, image_descriptor=path_to_image)

            if context_flag:

                new_func_kwargs = {'context': func_kwargs, 'image': image}

                template.render({
                    **new_func_kwargs
                }, autoescape=True)
            else:
                func_kwargs['image'] = image
                template.render({
                    **func_kwargs
                }, autoescape=True)

            template.save(output_path)

        return inner_wrapper

    return outter_wrapper


def throw_params_for_distribution_diagram(
        category_names_key: str = None,
        title_key: str = None,
        distribution_keys: tuple[str, str] = None,
        distribution_translate: bool = False,
):
    def outter_wrapper(func: Callable):
        @wraps(func)
        def inner_wrapper(self, **kwargs) -> tuple:

            diagram_type: str = kwargs.pop('diagram_type')
            distribution: list[dict] = self.proc_obj.response_part.get(category_names_key)
            title: str = ReportLanguagePicker(self.report_format)().get('titles').get(title_key)

            distribution: list[dict] = [
                {d[distribution_keys[0]]: int(d[distribution_keys[1]]) for _, _ in d.items()} for d in distribution
            ]

            distribution_union: dict = {}

            for s_m_d in distribution:
                distribution_union.update(s_m_d)

            if distribution_translate:
                categories_translate: dict = ReportLanguagePicker(self.report_format)().get('categories_smi')
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
            context.update(distribution_union)
            for key, value in context.items():
                context[key] = [int(value), percentages_of_soc_distribution[key]]

            context['title'] = title

            return chart_categories, chart_series, context

        return inner_wrapper

    return outter_wrapper
