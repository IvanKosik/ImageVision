from core.plugin import Plugin

from plugins.image_loading.image_loader import ImageLoader
from plugins.image_loading.image_format_loader_registry_plugin import ImageFormatLoaderRegistryPlugin
from plugins.image_storage.image_storage_plugin import ImageStoragePlugin


class ImageLoaderPlugin(Plugin):
    def __init__(self, image_format_loader_registry_plugin: ImageFormatLoaderRegistryPlugin,
                 image_storage_plugin: ImageStoragePlugin):
        super().__init__()

        self.image_loader = ImageLoader(image_format_loader_registry_plugin.image_format_loader_registry,
                                        image_storage_plugin.image_storage)
