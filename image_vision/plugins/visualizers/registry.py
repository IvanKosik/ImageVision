from core import Plugin
from extensions.visualizers import DataVisualizerRegistry


class DataVisualizerRegistryPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.visualizers_registry = DataVisualizerRegistry()
