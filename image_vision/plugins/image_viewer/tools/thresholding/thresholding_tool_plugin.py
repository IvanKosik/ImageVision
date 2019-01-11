from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin

from PyQt5.QtCore import Qt


class ThresholdingToolPlugin(ImageViewerToolPlugin):
    def __init__(self):
        super().__init__('plugins.image_viewer.tools.thresholding.thresholding_tool',
                         'ThresholdingTool', 'Thresholding', Qt.CTRL + Qt.Key_6)
