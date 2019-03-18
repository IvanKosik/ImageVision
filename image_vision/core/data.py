from PyQt5.QtCore import QObject, pyqtSignal


class Data(QObject):
    updated = pyqtSignal()

    def __init__(self):
        super().__init__()

    def update(self):
        self.updated.emit()
