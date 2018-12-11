from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QVBoxLayout, QAbstractItemView
from PyQt5.QtGui import QPixmap
from plugins.dicom_loader.dicom_record import DicomRecordType, DicomRecord, DicomDir, DicomPatient, DicomStudy, DicomSeries, DicomImage
from core import image_utils


def create_dicom_record_tree_item(dicom_record: DicomRecord, parent: QTreeWidgetItem = None):
    return DICOM_RECORD_TYPES_TREE_ITEMS[dicom_record.type](dicom_record, parent)


class DicomRecordTreeItem(QTreeWidgetItem):
    def __init__(self, dicom_record: DicomRecord, parent: QTreeWidgetItem = None):
        super().__init__(parent, [str(dicom_record.id)])
        self.dicom_record = dicom_record

        self.create_children(dicom_record)

    def create_children(self, dicom_record: DicomRecord):
        for child_record in dicom_record.children.values():
            create_dicom_record_tree_item(child_record, self)


class DicomDirTreeItem(DicomRecordTreeItem):
    def __init__(self, dicom_dir: DicomDir, parent: QTreeWidgetItem = None):
        super().__init__(dicom_dir, parent)


class DicomPatientTreeItem(DicomRecordTreeItem):
    def __init__(self, dicom_patient: DicomPatient, parent: QTreeWidgetItem = None):
        super().__init__(dicom_patient, parent)


class DicomStudyTreeItem(DicomRecordTreeItem):
    def __init__(self, dicom_study: DicomStudy, parent: QTreeWidgetItem = None):
        super().__init__(dicom_study, parent)


class DicomSeriesTreeItem(DicomRecordTreeItem):
    def __init__(self, dicom_series: DicomSeries, parent: QTreeWidgetItem = None):
        super().__init__(dicom_series, parent)


class DicomImageTreeItem(DicomRecordTreeItem):
    def __init__(self, dicom_image: DicomImage, parent: QTreeWidgetItem = None):
        super().__init__(dicom_image, parent)


DICOM_RECORD_TYPES_TREE_ITEMS = {
    DicomRecordType.DIR: DicomDirTreeItem,
    DicomRecordType.PATIENT: DicomPatientTreeItem,
    DicomRecordType.STUDY: DicomStudyTreeItem,
    DicomRecordType.SERIES: DicomSeriesTreeItem,
    DicomRecordType.IMAGE: DicomImageTreeItem
}


class DicomTreeWidget(QTreeWidget):
    item_entered = pyqtSignal(QTreeWidgetItem, int)

    def __init__(self, dicom_record: DicomRecord, parent: QWidget = None):
        super().__init__(parent)

        self.dicom_record = dicom_record

        self.setColumnCount(1)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        top_level_item = create_dicom_record_tree_item(dicom_record)
        self.addTopLevelItem(top_level_item)

        self.add_series_previews()

        self.setMouseTracking(True)
        self.itemEntered.connect(self.item_entered)

    def add_series_previews(self, expand_to_series=True):
        for i in range(self.topLevelItemCount()):
            top_level_item = self.topLevelItem(i)
            self.add_child_item_series_previews(top_level_item, expand_to_series)

    def add_child_item_series_previews(self, item, expand_to_series=True):
        item.setExpanded(expand_to_series)
        for i in range(item.childCount()):
            child_item = item.child(i)
            if isinstance(child_item, DicomSeriesTreeItem):
                self.add_series_preview(child_item)
            else:
                self.add_child_item_series_previews(child_item, expand_to_series)

    def add_series_preview(self, series_item):
        if series_item.childCount() > 0:
            first_dicom_image_dataset = series_item.child(0).dicom_record.dataset
            if first_dicom_image_dataset is not None and hasattr(first_dicom_image_dataset, 'pixel_array'):
                preview = image_utils.resized_image(first_dicom_image_dataset.pixel_array, 128)
                normalized_preview = image_utils.converted_to_normalized_uint8(preview)
                pixmap = QPixmap(image_utils.numpy_gray_image_to_qimage(normalized_preview))

                preview_label = QLabel()
                preview_label.setPixmap(pixmap)

                layout = QVBoxLayout()
                layout.setSpacing(0)
                layout.setContentsMargins(3, 5, 3, 3)
                layout.addWidget(QLabel(series_item.text(0)))
                layout.addWidget(preview_label)

                # Clear series item text (we will display it inside the widget)
                series_item.setText(0, '')

                series_preview_widget = QWidget()
                series_preview_widget.setLayout(layout)
                self.setItemWidget(series_item, 0, series_preview_widget)
