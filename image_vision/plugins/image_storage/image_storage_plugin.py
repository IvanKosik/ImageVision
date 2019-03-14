from core.plugin import Plugin

from plugins.image_storage.image_storage import ImageStorage


class ImageStoragePlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.image_storage = ImageStorage()
