from core import Plugin
from extensions.visualizers import DataVisualizationManager
from .registry import DataVisualizerRegistryPlugin
from plugins.mdi import MdiAreaPlugin


class DataVisualizationManagerPlugin(Plugin):
    def __init__(self, visualizers_registry_plugin: DataVisualizerRegistryPlugin,
                 mdi_area_plugin: MdiAreaPlugin):
        super().__init__()

        self.visualization_manager = DataVisualizationManager(visualizers_registry_plugin.visualizers_registry,
                                                              mdi_area_plugin.mdi_area)
