from core import Plugin
from extensions.viewers import FlatImageViewer
from extensions.mdi import MdiArea
from extensions.mdi.windows import ImageViewerSubWindow
from extensions.loaders import FileLoadingManager
from extensions.window import MenuType
from plugins.window import MainWindowPlugin
from plugins.mdi import MdiAreaPlugin
from plugins.loaders import FileLoadingManagerPlugin

from PyQt5.QtCore import QObject, Qt

import os


class ImageLayerFileWalker(QObject):
    def __init__(self, image_viewer: FlatImageViewer, loading_manager: FileLoadingManager):
        super().__init__()

        self.image_viewer = image_viewer
        self.loading_manager = loading_manager

        self._main_layer_image_dir = None
        self._main_layer_dir_images = None
        self._main_layer_image_index = None

    @property
    def main_layer(self):
        return self.image_viewer.layers[0]

    @property
    def main_layer_image_dir(self):
        if self._main_layer_image_dir is None:
            self._main_layer_image_dir = self.main_layer.image_path.parent
        return self._main_layer_image_dir

    @property
    def main_layer_dir_images(self):
        if self._main_layer_dir_images is None:
            self._main_layer_dir_images = sorted(os.listdir(self.main_layer_image_dir))
        return self._main_layer_dir_images

    @property
    def main_layer_image_index(self):
        if self._main_layer_image_index is None:
            self._main_layer_image_index = self.main_layer_dir_images.index(self.main_layer.image_path.name)
        return self._main_layer_image_index

    def show_next_image(self):
        self._show_image_with_index(self.main_layer_image_index + 1)

    def show_previous_image(self):
        self._show_image_with_index(self.main_layer_image_index - 1)

    def _show_image_with_index(self, index: int):
        index = index % len(self.main_layer_dir_images)
        next_file_name = self.main_layer_dir_images[index]
        # next_file_path = self.main_layer_image_dir / next_file_name
        # next_image = self.loading_manager.load_file(next_file_path)
        # self.main_layer.image = next_image
        self._main_layer_image_index = index

        # update images of all layers
        for layer in self.image_viewer.layers:
            layer_image_dir = layer.image_path.parent
            layer.image = self.loading_manager.load_file(layer_image_dir / next_file_name)


class MdiImageLayerFileWalker(QObject):
    def __init__(self, mdi_area: MdiArea, loading_manager: FileLoadingManager):
        super().__init__()

        self.mdi_area = mdi_area
        self.loading_manager = loading_manager

        self.image_layer_file_walkers = {}  # DataViewerSubWindow: ImageLayerFileWalker

    def show_next_image(self):
        walker = self._image_layer_file_walker()
        if walker is not None:
            walker.show_next_image()

    def show_previous_image(self):
        walker = self._image_layer_file_walker()
        if walker is not None:
            walker.show_previous_image()

    def _image_layer_file_walker(self):
        active_sub_window = self.mdi_area.activeSubWindow()
        if not isinstance(active_sub_window, ImageViewerSubWindow):
            return

        image_layer_file_walker = self.image_layer_file_walkers.get(active_sub_window)
        if image_layer_file_walker is None:
            image_layer_file_walker = ImageLayerFileWalker(active_sub_window.viewer, self.loading_manager)
            self.image_layer_file_walkers[active_sub_window] = image_layer_file_walker
        return image_layer_file_walker


class ImageLayerFileWalkerPlugin(Plugin):
    def __init__(self, main_window_plugin: MainWindowPlugin, mdi_area_plugin: MdiAreaPlugin,
                 loading_manager_plugin: FileLoadingManagerPlugin):
        super().__init__()

        self.main_window = main_window_plugin.main_window

        self.mdi_image_layer_file_walker = MdiImageLayerFileWalker(
            mdi_area_plugin.mdi_area, loading_manager_plugin.loading_manager)

    def _install(self):
        self.main_window.add_menu_action(MenuType.VIEW, 'Next Image',
                                         self.mdi_image_layer_file_walker.show_next_image,
                                         Qt.CTRL + Qt.Key_Right)
        self.main_window.add_menu_action(MenuType.VIEW, 'Previous Image',
                                         self.mdi_image_layer_file_walker.show_previous_image,
                                         Qt.CTRL + Qt.Key_Left)

    def _remove(self):
        raise NotImplementedError
