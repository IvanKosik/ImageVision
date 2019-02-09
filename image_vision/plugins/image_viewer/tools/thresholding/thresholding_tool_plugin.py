from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin

from PyQt5.QtCore import Qt


class ThresholdingToolPlugin(ImageViewerToolPlugin):
    def __init__(self, image_viewer_plugin, main_window_plugin):
        super().__init__(image_viewer_plugin, main_window_plugin,
                         'plugins.image_viewer.tools.thresholding.thresholding_tool',
                         'ThresholdingTool', 'Thresholding', Qt.CTRL + Qt.Key_6)
