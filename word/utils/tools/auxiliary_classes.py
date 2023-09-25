import random
from colour import Color


class ChartColorPalette:
    sentiments: list
    distribution: list
    smi_distribution: list
    soc_distribution: list
    media_top: list
    soc_top: list
    most_popular_soc: list
    top_negative: list
    smi_top_negative: list
    soc_top_negative: list


class ChartColorDistribution:
    def __init__(self, chart_length: int, chart_type: str):
        self._chart_length = chart_length
        self._chart_type = chart_type

    @property
    def chart_length(self) -> int:
        return self._chart_length

    @property
    def chart_type(self) -> str:
        return self._chart_type

    def set_range_of_colors(self) -> ChartColorPalette:

        palettes = ['#8B3A3A', '#FFC1C1'], ['#104E8B', '#63B8FF']

        chart_color_palette_obj = ChartColorPalette()

        if self.chart_type not in ('sentiments', 'distribution'):

            choice = random.choice(palettes)

            setattr(
                chart_color_palette_obj,
                self.chart_type,
                [str(color) for color in Color(choice[0]).range_to(Color(choice[1]), self.chart_length)],
            )
        elif self.chart_type == 'sentiments':
            setattr(chart_color_palette_obj, self.chart_type, ['#1BB394', '#EC5D5D', '#F2C94C'])
        else:
            setattr(chart_color_palette_obj, self.chart_type, ['#1874CD', '#CD5555'])

        return chart_color_palette_obj
