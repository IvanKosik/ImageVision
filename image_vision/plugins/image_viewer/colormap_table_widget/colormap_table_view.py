from widgets.color_table_item_delegate import ColorTableItemDelegate
from plugins.image_viewer.colormap_table_widget.colormap_table_model import ColormapTableModel
from core import settings

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTableView, QWidget, QAbstractItemView


class ColormapTableView(QTableView):
    def __init__(self, model: ColormapTableModel, parent: QWidget = None):
        super().__init__(parent)

        self.setModel(model)

        self.setItemDelegateForColumn(1, ColorTableItemDelegate())

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.selectionModel().currentRowChanged.connect(self.on_selected_row_changed)

    def on_selected_row_changed(self, current_index: QModelIndex, previous_index: QModelIndex):
        # selected_color_class_changed
        class_column_number = 0
        class_model_index = self.model().index(current_index.row(), class_column_number)
        selected_color_class = class_model_index.data()

        self.model().activate_color_class(selected_color_class)
        #% settings.selected_color_class = selected_color_class
