from core.plugin import Plugin
from plugins.image_viewer.colormap_table_widget.colormap_table_view import ColormapTableView
from plugins.image_viewer.colormap_table_widget.colormap_table_model import ColormapTableModel

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDockWidget


class ColormapTableWidgetPlugin(Plugin):
    def __init__(self, main_window_plugin, image_viewer_plugin):
        super().__init__()

        self.main_window_plugin = main_window_plugin
        self.image_viewer_plugin = image_viewer_plugin

        self.colormap_table_view = None

    def install_gui(self):
        super().install_gui()

        colormap_table_model = ColormapTableModel(self.image_viewer_plugin.image_viewer.colormap)

        self.colormap_table_view = ColormapTableView(colormap_table_model)
        self.colormap_table_view.resizeColumnsToContents()

        colormap_dock_widget = QDockWidget('Colormap')
        colormap_dock_widget.setWidget(self.colormap_table_view)

        self.main_window_plugin.main_window.addDockWidget(Qt.LeftDockWidgetArea, colormap_dock_widget)
