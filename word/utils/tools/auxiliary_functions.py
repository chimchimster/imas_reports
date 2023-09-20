def generate_chart_categories(*args) -> list[dict]:
    """ Генерируем список со словарями для передачи в Highcharts. """

    return [{'name': args[i][0], 'y': int(args[i][1])} for i in range(len(args)) if len(args[i]) == 2]


def determine_size_of_diagram(diagram_type: str) -> tuple:
    """ Определяем размер диаграммы для вставки в шаблон. """

    __available_sizes_of_diagrams__ = {
        'bar': (5, 5),
        'column': (5, 5),
        'linear': (17, 7),
        'pie': (5, 5)
    }

    return __available_sizes_of_diagrams__[diagram_type]