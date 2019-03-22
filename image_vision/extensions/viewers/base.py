from core import Data

from PyQt5.QtWidgets import QWidget


class DataViewer(QWidget):
    def __init__(self, data: Data = None):
        super().__init__()

        self.data = data
