from extensions.viewers import FlatImageViewer
from extensions.loaders import FileLoadingManager

from PyQt5.QtCore import QObject


class ViewerDirDataWalker(QObject):
    def __init__(self, image_viewer: FlatImageViewer, loading_manager: FileLoadingManager):
        super().__init__()

        self.image_viewer = image_viewer
        self.loading_manager = loading_manager

        self._image_dir = None
        self._dir_images = None
        self._dir_image_index = None

    def show_next_image(self):
        path = self.image_viewer.image.path
        print('show next path:', path)

    def show_previous_image(self):
        pass
