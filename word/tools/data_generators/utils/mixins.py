from abc import ABC, abstractmethod


class DataGeneratorMixin(ABC):
    """ Класс задающий основные параметры для всех классов генераторов данных. """

    def __init__(
            self,
            response_part: dict,
            settings: dict | None,
            static_settings: dict,
    ):
        self._response_part = response_part
        self._settings = settings
        self._static_settings = static_settings

    @abstractmethod
    def generate_data(self) -> None:
        """ Метод генерирующий данные исходя из полученных настроек. """