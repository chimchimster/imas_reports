import abc


class DataManager(abc.ABC):

    def __init__(
            self,
            client_side_settings: list,
            response: dict,
    ):
        self._client_side_settings = client_side_settings
        self._response = response

    @abc.abstractmethod
    def distribute_content(self):
        """ Distributes content for particular report. """