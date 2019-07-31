from .base import DataViewerSubWindow
from extensions.viewers import FlatImageViewer


class ImageViewerSubWindow(DataViewerSubWindow):
    def __init__(self, viewer: FlatImageViewer):
        super().__init__(viewer)
