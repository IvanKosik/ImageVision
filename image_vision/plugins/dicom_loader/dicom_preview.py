from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QLabel
from plugins.dicom_loader.dicom_record import DicomRecordType, DicomRecord, DicomDir, DicomPatient, DicomStudy, DicomSeries, DicomImage


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
    def __init__(self, dicom_record: DicomRecord, parent: QWidget = None):
        super().__init__(parent)

        self.dicom_record = dicom_record

        self.setColumnCount(1)

        top_level_item = create_dicom_record_tree_item(dicom_record)
        self.addTopLevelItem(top_level_item)

        self.add_series_previews()

    def add_series_previews(self):
        for i in range(self.topLevelItemCount()):
            top_level_item = self.topLevelItem(i)
            self.add_child_item_series_previews(top_level_item)

    def add_child_item_series_previews(self, item):
        for i in range(item.childCount()):
            child_item = item.child(i)
            if isinstance(child_item, DicomSeriesTreeItem):
                self.add_series_preview(child_item)
            else:
                self.add_child_item_series_previews(child_item)

    def add_series_preview(self, series_item):
        print('child_item series')
        # series_preview_widget = QLabel()
        # series_preview_widget.setPixmap()
        # previewLabel->setPixmap(preview);

        if series_item.childCount() > 0:
            print('sss')
            # if series_item.child(0).dicom_record.dataset is not None and series_item.child(0).dicom_record.dataset.pixel_array is not None:
            #     print('SHAPE:', series_item.child(0).dicom_record.dataset.pixel_array.shape)

        # self.setItemWidget(series_item, 0, series_preview_widget)


class DicomPreview(QWidget):
    def __init__(self, dicom_dir: DicomDir, parent: QWidget = None):
        super().__init__(parent)

        self.dicom_dir = dicom_dir
        self.dicom_tree_widget = DicomTreeWidget(dicom_dir)

        layout = QVBoxLayout()
        layout.addWidget(self.dicom_tree_widget)
        self.setLayout(layout)
