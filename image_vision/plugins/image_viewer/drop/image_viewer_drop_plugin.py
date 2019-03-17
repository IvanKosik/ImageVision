from core.plugin import Plugin

from .image_viewer_drop import ImageViewerDrop
from plugins.image_viewer.image_viewer_plugin import ImageViewerPlugin
from plugins.loaders.manager import ImageLoaderPlugin


class ImageViewerDropPlugin(Plugin):
    def __init__(self, image_viewer_plugin: ImageViewerPlugin, image_loader_plugin: ImageLoaderPlugin):
        super().__init__()

        self.image_viewer = image_viewer_plugin.image_viewer
        self.image_viewer_drop = ImageViewerDrop(image_loader_plugin.image_loader)

    def _install(self):
        # self.image_viewer.viewport().setAcceptDrops(True)
        self.image_viewer.viewport().installEventFilter(self.image_viewer_drop)

    def _remove(self):
        self.image_viewer.viewport().removeEventFilter(self.image_viewer_drop)
