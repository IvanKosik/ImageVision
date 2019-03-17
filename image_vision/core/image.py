from core.data import Data


class Image(Data):
    def __init__(self, array=None):
        super().__init__()

        self.array = array
