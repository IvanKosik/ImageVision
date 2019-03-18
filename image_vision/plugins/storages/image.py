from core import Plugin

from extensions.storages import ImageStorage


class ImageStoragePlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.image_storage = ImageStorage()
