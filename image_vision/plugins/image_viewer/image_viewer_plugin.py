from core.plugin import Plugin
from plugins.image_viewer.image_viewer import ImageViewer
from plugins.image_viewer.model_image_viewer import ModelImageViewer
from plugins.main_window.main_window_plugin import MainWindowPlugin

from PyQt5.QtCore import Qt


class ImageViewerPlugin(Plugin):
    def __init__(self, main_window_plugin):
        super().__init__()

        self.main_window_plugin = main_window_plugin

        self.image_viewer = None

        self.toggle_mask_visibility_action = None

    def install_core(self):
        super().install_core()

        self.image_viewer = ModelImageViewer(self.main_window_plugin.main_window)

    def install_gui(self):
        super().install_gui()

        main_window = self.main_window_plugin.main_window
        main_window.setCentralWidget(self.image_viewer)

        view_menu = main_window.menuBar().addMenu('View')
        self.toggle_mask_visibility_action = view_menu.addAction(
            'Show/Hide Mask', self.image_viewer.toogle_mask_visibility, Qt.CTRL + Qt.Key_M)

        toggle_image_view_action = view_menu.addAction(
            'Image View', self.image_viewer.toogle_image_view, Qt.CTRL + Qt.Key_I)

        view_menu.addAction('Next Image', self.image_viewer.show_next_image, Qt.CTRL + Qt.Key_Right)
        view_menu.addAction('Previous Image', self.image_viewer.show_previous_image, Qt.CTRL + Qt.Key_Left)
