from plugin import Plugin
from plugins.image_viewer.image_viewer import ImageViewer
from plugins.main_window.main_window_plugin import MainWindowPlugin

from PyQt5.QtCore import Qt


class ImageViewerPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.image_viewer = None

        self.toggle_mask_visibility_action = None

    def install_core(self, plugin_manager):
        super().install_core(plugin_manager)

        main_window = plugin_manager.plugin(MainWindowPlugin.name()).main_window
        self.image_viewer = ImageViewer(main_window)

    def install_gui(self, plugin_manager):
        super().install_gui(plugin_manager)

        main_window = plugin_manager.plugin(MainWindowPlugin.name()).main_window
        main_window.setCentralWidget(self.image_viewer)

        view_menu = main_window.menuBar().addMenu('View')
        self.toggle_mask_visibility_action = view_menu.addAction(
            'Show/Hide Mask', self.image_viewer.toogle_mask_visibility, Qt.CTRL + Qt.Key_M)

        toggle_image_view_action = view_menu.addAction(
            'Image View', self.image_viewer.toogle_image_view, Qt.CTRL + Qt.Key_I)
