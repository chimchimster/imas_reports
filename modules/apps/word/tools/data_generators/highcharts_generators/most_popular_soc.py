from modules.apps.word.mixins import PropertyMethodsMixin
from modules.apps.word.tools.data_generators.mixins import DataGeneratorMixin


class MostPopularSocDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'most_popular_soc'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
