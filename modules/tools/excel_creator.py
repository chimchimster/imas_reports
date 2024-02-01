from .abstract_creator import Creator


class ExcelCreator(Creator):

    def __init__(self, *args):
        super().__init__(*args)

    def generate_document(self, response: dict) -> None:

        print(response)