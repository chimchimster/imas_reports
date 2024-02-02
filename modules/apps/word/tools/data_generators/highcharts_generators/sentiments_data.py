from modules.mixins.mixins import DataGeneratorMixin


class SentimentsDataGenerator(DataGeneratorMixin):

    flag: str = 'sentiments'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
