from core import Data
from .base import DataVisualizer

from typing import Type


class DataVisualizerRegistry:
    def __init__(self):
        super().__init__()

        self._registry = {}

    def register_visualizer_cls(self, visualizer_cls: Type[DataVisualizer]):
        for data_type in visualizer_cls.data_types:
            assert data_type not in self._registry, 'Duplicate data type of visualizer'
            self._registry[data_type] = visualizer_cls

    def unregister_visualizer_cls(self, visualizer_cls: Type[DataVisualizer]):
        for data_type in visualizer_cls.data_types:
            assert self._registry[data_type] == visualizer_cls, 'Data type registered for other visualizer'
            del self._registry[data_type]

    def visualizer_cls(self, data_type: Type[Data]) -> Type[DataVisualizer]:
        return self._registry[data_type]

    def contains(self, data_type: Type[Data]) -> bool:
        return data_type in self._registry
