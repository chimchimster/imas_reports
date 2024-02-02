from modules.logs.decorators import tricky_loggy
from modules.mixins import DataGeneratorMixin


class TagsGenerator(DataGeneratorMixin):

    flag: str = 'tags'

    def __init__(self, response_part, settings, static_settings):
        super().__init__(response_part, settings, static_settings)
        self._folder = None
        self._data_collection = []

    @tricky_loggy
    def generate_data(self):

        self._data_collection.append(self._response_part.get('analyzer_tags_changed'))