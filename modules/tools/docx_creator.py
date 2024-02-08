from .abstract_creator import Creator
from modules.apps.word.utils import WordDataManager, MergeReport
from modules.folder import FolderUUID


class WordCreator(Creator):

    def __init__(self, *args):
        super().__init__(*args)
        self.folder = FolderUUID(unique_identifier=self._task_uuid)

    def generate_document(self, response: dict) -> None:

        manager = WordDataManager(
            self._client_side_settings,
            response,
            self.folder,
        )
        manager.folder = self.folder
        manager.distribute_content()
        manager.apply_processes()

        merger: MergeReport = MergeReport()
        setattr(merger, 'folder', self.folder)
        merger.merge()
