from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path  # TODO: Use Python 3.7 type hints without imports: https://www.python.org/dev/peps/pep-0563/


class Data(QObject):
    updated = pyqtSignal()

    def __init__(self, path: Path = None):
        super().__init__()

        self.path = path

    def update(self):
        self.updated.emit()
