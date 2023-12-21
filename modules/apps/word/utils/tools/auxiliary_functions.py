def generate_chart_categories(*args) -> list[dict]:
    """ Генерируем список со словарями для передачи в Highcharts. """

    return [{'name': args[i][0], 'y': int(args[i][1])} for i in range(len(args)) if len(args[i]) == 2]


