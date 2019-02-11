from PyQt5.Qt import Qt, QColor, QPainter, QStyle, QSize
from PyQt5.QtCore import QObject, QModelIndex, QAbstractItemModel, QMargins
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QWidget, QColorDialog


class ColorTableItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(20, 20)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        # else:
        #     painter.fillRect(option.rect, self.color_by_model_index(index))

        # background_color = option.palette.highlight() if option.state & QStyle.State_Selected else Qt.white
        # painter.fillRect(option.rect, background_color)

        margins = QMargins(3, 2, 3, 2)
        painter.fillRect(option.rect - margins, self.color_by_model_index(index))

        painter.restore()

    def color_by_model_index(self, index: QModelIndex) -> QColor:
        return index.model().data(index, Qt.DisplayRole)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        color_dialog = QColorDialog()#self.color_by_model_index(index))
        color_dialog.setOption(QColorDialog.ShowAlphaChannel)
        return color_dialog

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor.setCurrentColor(self.color_by_model_index(index))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        color = editor.selectedColor()
        if color.isValid():  # when dialog was closed by Cancel or Close button, the color is invalid
            model.setData(index, editor.selectedColor(), Qt.EditRole)
