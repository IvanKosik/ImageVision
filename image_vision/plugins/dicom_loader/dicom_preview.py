from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QTreeWidgetItem
from plugins.dicom_loader.dicom_record import DicomRecord
from plugins.dicom_loader.dicom_tree_widget import DicomTreeWidget
from core import image_utils
import numpy as np


class DicomPreview(QWidget):
    def __init__(self, dicom_record: DicomRecord, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('DICOM Preview'))

        self.dicom_record = dicom_record

        self.dicom_tree_widget = DicomTreeWidget(dicom_record)
        self.dicom_tree_widget.item_entered.connect(self.on_dicom_tree_item_entered)

        self.image_preview_label = QLabel()

        dicom_tree_and_image_preview_splitter = QSplitter()
        dicom_tree_and_image_preview_splitter.addWidget(self.dicom_tree_widget)
        dicom_tree_and_image_preview_splitter.addWidget(self.image_preview_label)

        layout = QVBoxLayout()
        layout.addWidget(dicom_tree_and_image_preview_splitter)
        self.setLayout(layout)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_dicom_tree_item_entered(self, item, column):
        self.show_dicom_tree_item_preview(item)

    def show_dicom_tree_item_preview(self, item):
        item_dataset = item.dicom_record.dataset
        if hasattr(item_dataset, 'pixel_array'):
            image_utils.print_image_info(item_dataset.pixel_array, 'SHAPE')
            preview = image_utils.resized_image(item_dataset.pixel_array, 512)
            normalized_preview = image_utils.converted_to_normalized_uint8(preview)
            pixmap = QPixmap(image_utils.numpy_gray_image_to_qimage(normalized_preview))
            self.image_preview_label.setPixmap(pixmap)
