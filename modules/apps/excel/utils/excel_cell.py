

class Bouncer:

    def __init__(self, start):
        self.position = start

    def jump(self, direction: int):
        if self.position >= -1:
            self.position += direction
        else:
            raise IndexError('Can not jump on cell with negative value. Only -1 is allowed.')

    def set_to(self, start):
        if start >= -1:
            self.position = start
        else:
            raise IndexError('Can not set position with negative value. Only -1 is allowed.')