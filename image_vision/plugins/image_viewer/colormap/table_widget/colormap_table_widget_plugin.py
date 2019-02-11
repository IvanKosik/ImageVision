from core.plugin import Plugin
from plugins.image_viewer.colormap.table_widget.colormap_table_view import ColormapTableView
from plugins.main_window.main_window import MainWindow
from plugins.image_viewer.colormap.table_widget.colormap_table_model import ColormapTableModel

from PyQt5.Qt import Qt, QSizePolicy
from PyQt5.QtWidgets import QTableView, QDockWidget


class ColoormapTableWidgetPlugin(Plugin):
    def __init__(self, main_window_plugin):
        super().__init__()

        self.main_window_plugin = main_window_plugin

        self.colormap_table_widget = None

    def install_gui(self):
        super().install_gui()

        self.colormap_table_widget = ColormapTableView()
        table_model = ColormapTableModel()
        self.colormap_table_widget.setModel(table_model)
        self.colormap_table_widget.resizeColumnsToContents()

        colormap_dock_widget = QDockWidget('Colormap')
        colormap_dock_widget.setWidget(self.colormap_table_widget)

        self.main_window_plugin.main_window.addDockWidget(Qt.LeftDockWidgetArea, colormap_dock_widget)
