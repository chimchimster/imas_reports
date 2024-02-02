from modules.data_manager.data_manager import DataManager
from modules.logs.decorators import tricky_loggy


class ExcelDataManager(DataManager):

    def __init__(self, *args):
        super().__init__(*args)

    @tricky_loggy
    def distribute_content(self):

        print(self.client_side_settings)

        for k, v in self.response.items():

            with open('new.txt', 'a') as file:
                file.write(k + " " + str(v) + '\n')

        # for client_side_setting in self.client_side_settings:
        #