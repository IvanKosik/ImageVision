from plugins.loaders.base import FileLoaderPlugin
from plugins.loaders.registry import FileLoaderRegistryPlugin


class ImageFileLoaderPlugin(FileLoaderPlugin):
    def __init__(self, loaders_registry_plugin: FileLoaderRegistryPlugin, file_loader_cls):
        super().__init__(loaders_registry_plugin, file_loader_cls)
