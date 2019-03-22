from core.data import Data


class Image(Data):
    def __init__(self, array=None, path=None):
        super().__init__(path)

        self.array = array
