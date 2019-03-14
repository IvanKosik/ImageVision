from core.image import Image

from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path


class ImageLoader(QObject):
    image_loaded = pyqtSignal(Image)

    def __init__(self, image_format_loader_registry, image_storage):
        super().__init__()

        self.image_format_loader_registry = image_format_loader_registry
        self.image_storage = image_storage

    def can_load_image(self, path: Path):
        image_format = path.suffix[1:]  # remove dot
        return self.image_format_loader_registry.contains_format(image_format)

    def load_image(self, path: Path):
        print('Image loader: load_image')
        image_format = path.suffix[1:]  # remove dot
        format_loader_cls = self.image_format_loader_registry.loader_cls(image_format)
        format_loader = format_loader_cls()
        image = format_loader.load_image(path)
        self.image_storage.add_image(image)
        return image
