from ..mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class WorldMapDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'world_map'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
