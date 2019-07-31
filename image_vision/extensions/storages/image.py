from core import FlatImage

from PyQt5.QtCore import QObject, pyqtSignal


class ImageStorage(QObject):
    image_added = pyqtSignal(FlatImage)

    def __init__(self):
        super().__init__()

        self._images = []

    def add_image(self, image: FlatImage):
        self._images.append(image)
        print('Storage images:', self._images)
        self.image_added.emit(image)
