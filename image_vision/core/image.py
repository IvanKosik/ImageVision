from PyQt5.QtCore import QObject


class Image(QObject):
    def __init__(self, data=None):
        super().__init__()

        self.data = data
