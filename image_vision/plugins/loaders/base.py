from core import Plugin
from .registry import FileLoaderRegistryPlugin


class FileLoaderPlugin(Plugin):
    def __init__(self, loaders_registry_plugin: FileLoaderRegistryPlugin, file_loader_cls):
        super().__init__()

        self.loaders_registry = loaders_registry_plugin.loaders_registry
        self.file_loader_cls = file_loader_cls

    def _install(self):
        self.loaders_registry.register_loader_cls(self.file_loader_cls)

    def _remove(self):
        self.loaders_registry.unregister_loader_cls(self.file_loader_cls)
