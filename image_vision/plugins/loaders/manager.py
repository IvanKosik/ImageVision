from core import Plugin
from extensions.loaders import FileLoadingManager
from .registry import FileLoaderRegistryPlugin


class FileLoadingManagerPlugin(Plugin):
    def __init__(self, loaders_registry_plugin: FileLoaderRegistryPlugin):
        super().__init__()

        self.loading_manager = FileLoadingManager(loaders_registry_plugin.loaders_registry)
