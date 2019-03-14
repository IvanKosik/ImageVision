from core.plugin import Plugin

from .image_loader import ImageLoader


class ImageLoaderPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.image_loader = ImageLoader()

    def _install(self):
        pass
