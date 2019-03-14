from core.image import Image

from PyQt5.QtCore import QObject, pyqtSignal


class ImageLoader(QObject):
    image_loaded = pyqtSignal(Image)

    def __init__(self):
        super().__init__()
