from modules.mixins import DataGeneratorMixin


class MessagesDynamicsDataGenerator(DataGeneratorMixin):

    flag: str = 'message_dynamic'

    def __init__(self, *args):
        super().__init__(*args)
        self._data_collection = None

    def generate_data(self) -> None:
        pass
