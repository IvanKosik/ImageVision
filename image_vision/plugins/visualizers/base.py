from core import Plugin
from .registry import DataVisualizerRegistryPlugin


class DataVisualizerPlugin(Plugin):
    def __init__(self, visualizers_registry_plugin: DataVisualizerRegistryPlugin, data_visualizer_cls):
        super().__init__()

        self.visualizers_registry = visualizers_registry_plugin.visualizers_registry
        self.data_visualizer_cls = data_visualizer_cls

    def _install(self):
        self.visualizers_registry.register_visualizer_cls(self.data_visualizer_cls)

    def _remove(self):
        self.visualizers_registry.unregister_visualizer_cls(self.data_visualizer_cls)
