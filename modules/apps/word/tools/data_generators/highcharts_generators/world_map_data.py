from modules.mixins import DataGeneratorMixin


class WorldMapDataGenerator(DataGeneratorMixin):

    flag: str = 'world_map'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
