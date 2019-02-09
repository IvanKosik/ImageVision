from core.plugin import Plugin
from plugins.dicom_loader.dicom_loader import DicomLoader
from plugins.dicom_loader.dicom_preview import DicomPreview
from plugins.main_window.main_window_plugin import MainWindowPlugin

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from pathlib import Path


class DicomLoaderPlugin(Plugin):
    def __init__(self, main_window_plugin):
        super().__init__()

        self.main_window_plugin = main_window_plugin

        self.dicom_loader = None
        # self.image_viewer = None

        self.dicom_preview = None

    def install_core(self):
        super().install_core()

        self.dicom_loader = DicomLoader()
        # self.image_viewer = plugin_manager.plugin(ImageViewer.name()).image_viewer

    def install_gui(self):
        super().install_gui()

        main_window = self.main_window_plugin.main_window

        file_menu = main_window.menuBar().addMenu('File')
        load_dicom_action = file_menu.addAction(
            'Load DICOM', self.load_dicom, Qt.CTRL + Qt.Key_D)

    def load_dicom(self):
        dicom_path = Path(QFileDialog.getExistingDirectory(caption=self.tr('Select DICOM Directory')))
        # dicom_path = Path('D:/Projects/C++/Qt/5/BodySnitches/Builds/BodySnitches/!DicomDatasets/FantasticNine/09-Kydryavcev/2011.12.09/DICOM')
        dicom_dir = self.dicom_loader.load_dicom(dicom_path)
        self.dicom_preview = DicomPreview(dicom_dir)
        self.dicom_preview.setGeometry(100, 100, 1200, 800)
        self.dicom_preview.show()
