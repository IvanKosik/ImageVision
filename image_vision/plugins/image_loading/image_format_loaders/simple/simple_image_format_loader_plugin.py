from plugins.image_loading.image_format_loaders.image_format_loader_plugin import ImageFormatLoaderPlugin
from plugins.image_loading.image_format_loader_registry_plugin import ImageFormatLoaderRegistryPlugin
from .simple_image_format_loader import SimpleImageFormatLoader


class SimpleImageFormatLoaderPlugin(ImageFormatLoaderPlugin):
    def __init__(self, image_format_loader_registry_plugin: ImageFormatLoaderRegistryPlugin):
        super().__init__(image_format_loader_registry_plugin, SimpleImageFormatLoader)
