import os
import shutil


class RemoveDirsMixin:
    """ После генерации отчета очищает директории
        названия которых хранят уникальный идентификатор uuid. """

    def remove_dir(self, directory: str, _uuid: str) -> None:

        for _dir in os.listdir(directory):
            if _dir == _uuid:
                shutil.rmtree(os.path.join(directory, _dir))

    def remove_temp_tables_dirs(self, _uuid: str) -> None:

        path_to_temp_tables_results = os.path.join(
            os.getcwd(),
            'word',
            'temp_tables',
            'results',
        )

        path_to_temp_tables_templates = os.path.join(
            os.getcwd(),
            'word',
            'temp_tables',
            'templates',
        )

        folder_name = str(_uuid)

        def remove(_path, _folder_name):

            for dir_name in os.listdir(_path):
                if dir_name.endswith(_folder_name):
                    shutil.rmtree(
                        os.path.join(
                            os.getcwd(),
                            _path,
                            dir_name,
                        )
                    )

        remove(path_to_temp_tables_results, folder_name)
        remove(path_to_temp_tables_templates, folder_name)

