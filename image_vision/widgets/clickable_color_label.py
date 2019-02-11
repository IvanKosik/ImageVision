from PyQt5.Qt import QColor, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget


class ClickableColorLabel(QLabel):
    def __init__(self, color: QColor = QColor(), parent: QWidget = None):
        super().__init__(parent)

        self.color = color

        self.update_color()

    def color(self) -> QColor:
        return self.color

    def update_color(self):
        # self.setPalette(QPalette(color));  # This variant does not work for TableWidgetItems
        pixmap = QPixmap(self.width(), self.height())
        pixmap.fill(self.color)
        self.setPixmap(pixmap)
