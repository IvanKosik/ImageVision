from .base import DataVisualizerPlugin
from .registry import DataVisualizerRegistryPlugin
from extensions.visualizers import ImageDataVisualizer


class ImageDataVisualizerPlugin(DataVisualizerPlugin):
    def __init__(self, visualizers_registry_plugin: DataVisualizerRegistryPlugin):
        super().__init__(visualizers_registry_plugin, ImageDataVisualizer)
