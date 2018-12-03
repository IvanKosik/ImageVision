from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin

from PyQt5.QtCore import Qt


class AnnPredictionToolPlugin(ImageViewerToolPlugin):
    def __init__(self):
        super().__init__('plugins.image_viewer.tools.ann_prediction.ann_prediction_tool',
                         'AnnPredictionTool', 'Ann Prediction', Qt.CTRL + Qt.Key_5)
