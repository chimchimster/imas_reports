from ..mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class MostPopularSocDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'most_popular_soc'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
