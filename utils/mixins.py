import os
import shutil


class RemoveDirsMixin:
    def remove_dir(self, directory: str, _uuid: str) -> None:

        for _dir in os.listdir(directory):
            if _dir == _uuid:
                shutil.rmtree(os.path.join(directory, _dir))