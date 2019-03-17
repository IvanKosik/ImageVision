from core import Data
from .registry import DataVisualizerRegistry
from extensions.mdi import MdiArea

from PyQt5.QtCore import QObject, pyqtSignal


class DataVisualizationManager(QObject):
    data_visualized = pyqtSignal()

    def __init__(self, visualizers_registry: DataVisualizerRegistry, mdi_area: MdiArea):
        super().__init__()

        self.visualizers_registry = visualizers_registry
        self.mdi_area = mdi_area

    def can_visualize_data(self, data: Data) -> bool:
        return self.visualizers_registry.contains(type(data))

    def visualize_data(self, data: Data):
        print('Visualize data:', type(data))
        visualizer_cls = self.visualizers_registry.visualizer_cls(type(data))
        visualizer = visualizer_cls(self.mdi_area)
        visualizer.visualize_data(data)
        self.data_visualized.emit()
