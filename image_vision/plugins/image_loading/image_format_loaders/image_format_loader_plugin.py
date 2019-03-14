from core.plugin import Plugin
from plugins.image_loading.image_format_loader_registry_plugin import ImageFormatLoaderRegistryPlugin


class ImageFormatLoaderPlugin(Plugin):
    def __init__(self, image_format_loader_registry_plugin: ImageFormatLoaderRegistryPlugin,
                 image_format_loader_cls):
        super().__init__()

        self.image_format_loader_registry = image_format_loader_registry_plugin.image_format_loader_registry
        self.image_format_loader_cls = image_format_loader_cls

    def _install(self):
        self.image_format_loader_registry.register_loader_cls(self.image_format_loader_cls)

    def _remove(self):
        self.image_format_loader_registry.unregister_loader_cls(self.image_format_loader_cls)
