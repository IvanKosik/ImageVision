from plugins.image_loading.image_loader import ImageLoader

from PyQt5.QtCore import QObject, QEvent

from pathlib import Path


class ImageViewerDrop(QObject):
    def __init__(self, image_loader: ImageLoader):
        super().__init__()

        self.image_loader = image_loader
        self.dragged_image_path = None

    def eventFilter(self, watched_obj, event):
        if event.type() == QEvent.DragEnter:
            self.on_drag_enter(event)
            return True
        elif event.type() == QEvent.DragMove:
            event.accept()
            return True
        elif event.type() == QEvent.Drop:
            self.on_drop(event)
            return True
        else:
            return super().eventFilter(watched_obj, event)

    def on_drag_enter(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            self.dragged_image_path = Path(mime_data.urls()[0].toLocalFile())
            if self.image_loader.can_load_image(self.dragged_image_path):
                event.accept()
                return
        event.ignore()

    def on_drop(self, event):
        print('drop', self.dragged_image_path)
        image = self.image_loader.load_image(self.dragged_image_path)
        # show image in image_viewer