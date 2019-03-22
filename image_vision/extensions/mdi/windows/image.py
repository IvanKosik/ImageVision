from .base import DataViewerSubWindow
from extensions.viewers import ImageViewer


class ImageViewerSubWindow(DataViewerSubWindow):
    def __init__(self, viewer: ImageViewer):
        super().__init__(viewer)
