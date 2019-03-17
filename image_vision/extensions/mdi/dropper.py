from extensions.loaders import FileLoadingManager
from extensions.visualizers import DataVisualizationManager

from PyQt5.QtCore import QObject, QEvent

from pathlib import Path


class MdiAreaFileDropper(QObject):
    def __init__(self, loading_manager: FileLoadingManager, visualization_manager: DataVisualizationManager):
        super().__init__()

        self.loading_manager = loading_manager
        self.visualization_manager = visualization_manager
        self.dragged_file_path = None

    def eventFilter(self, watched_obj, event):
        if event.type() == QEvent.DragEnter:
            self.on_drag_enter(event)
            return True
        elif event.type() == QEvent.Drop:
            self.on_drop(event)
            return True
        else:
            return super().eventFilter(watched_obj, event)

    def on_drag_enter(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            self.dragged_file_path = Path(mime_data.urls()[0].toLocalFile())
            if self.loading_manager.can_load_file(self.dragged_file_path):
                event.accept()
                return
        event.ignore()

    def on_drop(self, event):
        print('drop', self.dragged_file_path)
        data = self.loading_manager.load_file(self.dragged_file_path)
        self.visualization_manager.visualize_data(data)
