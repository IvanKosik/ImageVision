from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin

from PyQt5.QtCore import Qt


class SmartBrushSegmentationToolPlugin(ImageViewerToolPlugin):
    def __init__(self, image_viewer_plugin, main_window_plugin):
        super().__init__(image_viewer_plugin, main_window_plugin,
                         'plugins.image_viewer.tools.smart_brush_segmentation.smart_brush_segmentation_tool',
                         'SmartBrushSegmentationTool', 'Smart Brush', Qt.CTRL + Qt.Key_1)
