from core import Plugin
from core.colormap import Colormap
from extensions.visualizers import DataVisualizationManager
from extensions.loaders import FileLoadingManager
from extensions.mdi.windows import DataViewerSubWindow, ImageViewerSubWindow
from plugins.visualizers import DataVisualizationManagerPlugin
from plugins.loaders import FileLoadingManagerPlugin

from PyQt5.QtCore import QObject


class ImageViewerPathOverlayer(QObject):
    def __init__(self, visualization_manager: DataVisualizationManager,
                 loading_manager: FileLoadingManager):
        super().__init__()

        self.visualization_manager = visualization_manager
        self.loading_manager = loading_manager

        self.visualization_manager.data_visualized.connect(self._on_data_visualized)

    def _on_data_visualized(self, data_viewer_sub_window: DataViewerSubWindow):
        if isinstance(data_viewer_sub_window, ImageViewerSubWindow):
            image_viewer = data_viewer_sub_window.viewer
            image_path = image_viewer.layers[0].image_path
            image_dir = image_path.parents[1]
            mask_path = image_dir / 'Masks' / image_path.name
            print('mask', mask_path.exists(), mask_path)
            if mask_path.exists():
                image_viewer.add_layer('Mask', self.loading_manager.load_file(mask_path), Colormap())


class ImageViewerPathOverlayerPlugin(Plugin):
    def __init__(self, visualization_manager_plugin: DataVisualizationManagerPlugin,
                 loading_manager_plugin: FileLoadingManagerPlugin):
        super().__init__()

        self.image_viewer_path_overlayer = ImageViewerPathOverlayer(
            visualization_manager_plugin.visualization_manager, loading_manager_plugin.loading_manager)
