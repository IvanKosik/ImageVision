from core import Plugin
from extensions.loaders import FileLoaderRegistry


class FileLoaderRegistryPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.loaders_registry = FileLoaderRegistry()
