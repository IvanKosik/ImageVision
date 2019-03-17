from core import Data

from PyQt5.QtCore import QObject, pyqtSignal

import abc


class DataVisualizerMeta(abc.ABCMeta, type(QObject)):
    _DATA_TYPES = ()

    @property
    def data_types(cls) -> tuple:
        return cls._DATA_TYPES


class DataVisualizer(QObject, metaclass=DataVisualizerMeta):
    #% _DATA_TYPES = ()

    data_visualized = pyqtSignal()

    def __init__(self, mdi_area):
        super().__init__()

        self.mdi_area = mdi_area

    @property
    def data_types(self):
        return type(self).data_types

    def visualize_data(self, data: Data):
        self._visualize_data(data)
        self.data_visualized.emit()

    @abc.abstractmethod
    def _visualize_data(self, data: Data):
        ...
