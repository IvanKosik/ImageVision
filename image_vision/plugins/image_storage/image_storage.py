from core.image import Image

from PyQt5.QtCore import QObject, pyqtSignal


class ImageStorage(QObject):
    image_added = pyqtSignal(Image)

    def __init__(self):
        super().__init__()

        self._images = []

    def add_image(self, image: Image):
        self._images.append(image)
        print('Storage images:', self._images)
        self.image_added.emit(image)
