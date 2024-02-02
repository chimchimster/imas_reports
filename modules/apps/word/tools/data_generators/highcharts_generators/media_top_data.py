from modules.mixins.mixins import DataGeneratorMixin


class TopMediaDataGenerator(DataGeneratorMixin):

    flag: str = 'media_top'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
