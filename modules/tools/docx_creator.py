from modules.apps.word.utils import WordDataManager, MergeReport
from modules.logs.decorators import tricky_loggy
from modules.utils import FolderUUID

from .abstract_creator import Creator


class WordCreator(Creator):

    def __init__(self, *args):
        super().__init__(*args)
        self.folder = FolderUUID(unique_identifier=self._task_uuid)

    def generate_document(self, response: dict) -> None:

        manager = WordDataManager(
            self.client_side_settings,
            response,
        )
        manager.folder = self.folder
        manager.distribute_content()
        manager.apply_processes()

        merger: MergeReport = MergeReport()
        setattr(merger, 'folder', self.folder)
        merger.merge()
