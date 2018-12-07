from core.plugin import Plugin
from plugins.dicom_loader.dicom_loader import DicomLoader
from plugins.dicom_loader.dicom_preview import DicomPreview
from plugins.main_window.main_window_plugin import MainWindowPlugin

from PyQt5.QtCore import Qt


class DicomLoaderPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.dicom_loader = None
        # self.image_viewer = None

        self.dicom_preview = None

    def install_core(self, plugin_manager):
        super().install_core(plugin_manager)

        self.dicom_loader = DicomLoader()
        # self.image_viewer = plugin_manager.plugin(ImageViewer.name()).image_viewer

    def install_gui(self, plugin_manager):
        super().install_gui(plugin_manager)

        main_window = plugin_manager.plugin(MainWindowPlugin.name()).main_window

        file_menu = main_window.menuBar().addMenu('File')
        load_dicom_action = file_menu.addAction(
            'Load DICOM', self.load_dicom, Qt.CTRL + Qt.Key_D)

    def load_dicom(self):
        dicom_dir = self.dicom_loader.load_dicom()
        self.dicom_preview = DicomPreview(dicom_dir)
        self.dicom_preview.show()
