

class Bouncer:

    def __init__(self):
        self.position = 0

    def jump(self, direction: int):
        if self.position > 0:
            self.position += direction
        else:
            raise IndexError('Can not jump on cell with negative value.')
