from core.colormap import Colormap

from PyQt5.QtCore import Qt, QObject, QAbstractTableModel, QModelIndex
from PyQt5.Qt import QBrush, QColor

from typing import Any


class ColormapTableModel(QAbstractTableModel):
    def __init__(self, colormap: Colormap, parent: QObject = None):
        super().__init__(parent)

        self.colormap = colormap

        self.headers = ('Class', 'Color')

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.colormap.lut.shape[0]

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        # BackgroundRole most likely will be overriden by a widget palette and a general application style
        if role == Qt.BackgroundRole:
            return QBrush(Qt.blue)

        if role == Qt.ForegroundRole:
            return QBrush(Qt.red)

        if role == Qt.DisplayRole and orientation == Qt.Horizontal and section < len(self.headers):
            return self.headers[section]
        else:
            return super().headerData(section, orientation, role)
            # return None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        color_class = index.row()

        if index.column() == 0:
            return color_class
        elif index.column() == 1:
            color = self.colormap.lut[color_class]
            return QColor(color[0], color[1], color[2], color[3])

    def setData(self, index: QModelIndex, value: Any, role: int = None):
        if index.isValid() and role == Qt.EditRole:
            color_class = index.row()

            self.colormap.set_class_color(color_class, value)

            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = super().flags(index)
        if index.column() == 1:
            flags = flags | Qt.ItemIsEditable
        return flags

    def activate_color_class(self, color_class: int):
        self.colormap.set_active_color_class(color_class)


    '''

    insertRows(), removeRows()
    
    '''
