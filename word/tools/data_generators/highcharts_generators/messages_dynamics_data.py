from ..mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class MessagesDynamicsDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'message_dynamic'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
