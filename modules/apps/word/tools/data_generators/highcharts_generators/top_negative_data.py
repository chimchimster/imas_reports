from modules.mixins import DataGeneratorMixin


class TopNegativeDataGenerator(DataGeneratorMixin):

    flag: str = 'top_negative'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
