from core.plugin import Plugin

from plugins.image_loading.image_format_loader_registry import ImageFormatLoaderRegistry


class ImageFormatLoaderRegistryPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.image_format_loader_registry = ImageFormatLoaderRegistry()
