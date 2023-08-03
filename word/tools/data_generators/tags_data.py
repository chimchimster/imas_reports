class TagsGenerator:

    flag = 'tags'

    def __init__(self, data, rest_data):
        self._data = data
        self._rest_data = rest_data
        self.data_collection = []

    def generate_data(self):

        self.data_collection.append(self._data.get('analyzer_tags_changed'))