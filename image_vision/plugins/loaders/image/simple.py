from .base import ImageFileLoaderPlugin
from extensions.loaders.image import SimpleImageFileLoader
from plugins.loaders.registry import FileLoaderRegistryPlugin


class SimpleImageFileLoaderPlugin(ImageFileLoaderPlugin):
    def __init__(self, loaders_registry_plugin: FileLoaderRegistryPlugin):
        super().__init__(loaders_registry_plugin, SimpleImageFileLoader)
