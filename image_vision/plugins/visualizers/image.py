from .base import DataVisualizerPlugin
from .registry import DataVisualizerRegistryPlugin
from extensions.visualizers.image import FlatImageVisualizer


class FlatImageVisualizerPlugin(DataVisualizerPlugin):
    def __init__(self, visualizers_registry_plugin: DataVisualizerRegistryPlugin):
        super().__init__(visualizers_registry_plugin, FlatImageVisualizer)
