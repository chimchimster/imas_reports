from logs.decorators import tricky_loggy
from .mixins import DataGeneratorMixin
from word.mixins import PropertyMethodsMixin


class TotalMessagesCountDataGenerator(DataGeneratorMixin, PropertyMethodsMixin):

    flag: str = 'count'

    def __init__(self, response_part, settings, static_settings):
        super().__init__(response_part, settings, static_settings)
        self._data_collection = {}

    @tricky_loggy
    def generate_data(self):
        total_messages_count: int = self.response_part.get('total_count', 0)
        positive_messages_count: int = self.response_part.get('pos_count', 0)
        neutral_messages_count: int = self.response_part.get('neu_count', 0)
        negative_messages_count: int = self.response_part.get('neg_count', 0)

        self.data_collection['total_count'] = total_messages_count
        self.data_collection['pos_count'] = positive_messages_count
        self.data_collection['neu_count'] = neutral_messages_count
        self.data_collection['neg_count'] = negative_messages_count
