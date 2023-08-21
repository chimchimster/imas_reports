from word.mixins import PropertyMethodsMixin


class TagsGenerator(PropertyMethodsMixin):

    flag: str = 'tags'

    def __init__(
            self,
            response_part: dict,
            settings: dict,
            static_settings: dict,
    ):
        self._response_part = response_part
        self._settings = settings
        self._static_settings = static_settings
        self._folder = None
        self._data_collection = []

    def generate_data(self):

        self.data_collection.append(self.response_part.get('analyzer_tags_changed'))