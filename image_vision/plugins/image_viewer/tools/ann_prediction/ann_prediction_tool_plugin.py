from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin

from PyQt5.QtCore import Qt


class AnnPredictionToolPlugin(ImageViewerToolPlugin):
    def __init__(self, image_viewer_plugin, main_window_plugin):
        super().__init__(image_viewer_plugin, main_window_plugin,
                         'plugins.image_viewer.tools.ann_prediction.ann_prediction_tool',
                         'AnnPredictionTool', 'Ann Prediction', Qt.CTRL + Qt.Key_5)
