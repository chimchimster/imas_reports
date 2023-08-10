import uuid


class FolderManager:
    def __init__(self, flag: str) -> None:
        self.unique_identifier: uuid = uuid.uuid4()
        self.flag = flag

    def __str__(self) -> str:
        if self.flag == 'temp':
            return f'temp_{self.unique_identifier}'
        elif self.flag == 'result':
            return f'result_{self.unique_identifier}'
        elif self.flag == 'templates':
            return f'templates_temp_{self.unique_identifier}'