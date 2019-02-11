from widgets.color_table_item_delegate import ColorTableItemDelegate

from PyQt5.QtWidgets import QTableView, QWidget


class ColormapTableView(QTableView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setItemDelegateForColumn(1, ColorTableItemDelegate())
