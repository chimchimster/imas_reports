from dataclasses import dataclass
import uuid


@dataclass
class FolderUUID:
    unique_identifier: uuid = None

    def __str__(self):
        return str(self.unique_identifier)