
from modules.mixins import DataGeneratorMixin


class TopSocDataGenerator(DataGeneratorMixin):

    flag: str = 'soc_top'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
