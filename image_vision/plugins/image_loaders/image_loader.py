from core.image import Image

from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path


class ImageLoader(QObject):
    image_loaded = pyqtSignal(Image)

    def __init__(self, formats: list):
        super().__init__()

        self.formats = formats

    def load_image(self, path: Path):
        pass
