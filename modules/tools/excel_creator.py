from .abstract_creator import Creator
from modules.apps.excel.utils import ExcelDataManager


class ExcelCreator(Creator):

    def __init__(self, *args):
        super().__init__(*args)

    def generate_document(self, response: dict) -> None:

        manager = ExcelDataManager(
            self._client_side_settings,
            response,
            self._task_uuid,
        )
        manager.distribute_content()