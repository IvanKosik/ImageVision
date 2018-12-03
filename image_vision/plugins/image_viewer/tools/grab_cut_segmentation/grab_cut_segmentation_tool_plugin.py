from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin

from PyQt5.QtCore import Qt


class GrabCutSegmentationToolPlugin(ImageViewerToolPlugin):
    def __init__(self):
        super().__init__('plugins.image_viewer.tools.grab_cut_segmentation.grab_cut_segmentation_tool',
                         'GrabCutSegmentationTool', 'Grab Cut', Qt.CTRL + Qt.Key_2)
