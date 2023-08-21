import os
import shutil


class RemoveDirsMixin:
    """ После генерации отчета очищает директории
        названия которых хранят уникальный идентификатор uuid. """

    dirs_to_delete = [
        os.path.join(
            os.getcwd(),
            'word',
            'merged',
        ),
        os.path.join(
            os.getcwd(),
            'word',
            'temp',
        ),
        os.path.join(
            os.getcwd(),
            'word',
            'temp_templates',
        ),
        os.path.join(
            os.getcwd(),
            'word',
            'temp_tables',
            'results',
        ),
        os.path.join(
            os.getcwd(),
            'word',
            'temp_tables',
            'templates',
        ),
    ]
    
    def remove_dir(self, _uuid: str) -> None:
        """ Метод удаляющий директории. """
        
        for directory in self.dirs_to_delete:
            for dir_name in os.listdir(directory):
                if dir_name == _uuid or dir_name.endswith(_uuid):
                    shutil.rmtree(
                        os.path.join(
                            directory,
                            dir_name,
                        )
                    )

