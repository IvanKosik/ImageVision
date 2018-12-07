from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from plugins.dicom_loader.dicom_loader import DicomDir, DicomRecord


class DicomPreview(QWidget):
    def __init__(self, dicom_dir: DicomDir, parent: QWidget = None):
        super().__init__(parent)

        self.dicom_dir = dicom_dir

        print('eee')
        self.tree_widget = self.create_tree_view()
        print('treeeee', self.tree_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

    def create_tree_view(self):
        tree_widget = QTreeWidget()
        tree_widget.setColumnCount(1)
        print('col')

        top_level_item = self.create_dicom_record_tree_item(self.dicom_dir)
        print('top')

        tree_widget.addTopLevelItem(top_level_item)

        self.create_child_items(top_level_item)
        # for child_record in self.dicom_dir.children:
        #     QTreeWidgetItem

        return tree_widget

    def create_child_items(self, dicom_record: DicomRecord, parent_item: QTreeWidgetItem):
        for child_record in dicom_record.children:
            child_item = self.create_dicom_record_tree_item(child_record, parent_item)
            self.create_child_items(child_record, child_item)

    def create_dicom_record_tree_item(self, dicom_record, parent_item=None):
        return QTreeWidgetItem(parent_item, [str(self.dicom_record.id)])
