from ..mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class TopMediaDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'media_top'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
