from ..mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class SmiDistributionDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'smi_distribution'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
