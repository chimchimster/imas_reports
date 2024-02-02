from modules.mixins import DataGeneratorMixin


class MostPopularSocDataGenerator(DataGeneratorMixin):

    flag: str = 'most_popular_soc'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
