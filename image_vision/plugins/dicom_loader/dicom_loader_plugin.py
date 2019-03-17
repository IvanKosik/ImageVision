from core.plugin import Plugin
from plugins.dicom_loader.dicom_loader import DicomLoader
from plugins.dicom_loader.dicom_preview import DicomPreview
from plugins.window.main import MainWindowPlugin

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from pathlib import Path


class DicomLoaderPlugin(Plugin):
    def __init__(self, main_window_plugin: MainWindowPlugin):
        super().__init__()

        self.main_window = main_window_plugin.main_window

        self.dicom_loader = DicomLoader()

        self.dicom_preview = None

        self.file_menu = self.main_window.menuBar().addMenu('File')
        self.load_dicom_action = None

    def _install(self):
        self.load_dicom_action = self.file_menu.addAction(
            'Load DICOM', self.load_dicom, Qt.CTRL + Qt.Key_D)

    def _remove(self):
        self.file_menu.removeAction(self.load_dicom_action)

    def load_dicom(self):
        dicom_path = Path(QFileDialog.getExistingDirectory(caption=self.tr('Select DICOM Directory')))
        # dicom_path = Path('D:/Projects/C++/Qt/5/BodySnitches/Builds/BodySnitches/!DicomDatasets/FantasticNine/09-Kydryavcev/2011.12.09/DICOM')
        dicom_dir = self.dicom_loader.load_dicom(dicom_path)
        self.dicom_preview = DicomPreview(dicom_dir)
        self.dicom_preview.setGeometry(100, 100, 1200, 800)
        self.dicom_preview.show()
