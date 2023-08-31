from .mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class TagsGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'tags'

    def __init__(self, response_part, settings, static_settings):
        super().__init__(response_part, settings, static_settings)
        self._folder = None
        self._data_collection = []

    def generate_data(self):

        self.data_collection.append(self.response_part.get('analyzer_tags_changed'))