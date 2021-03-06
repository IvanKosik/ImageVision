from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin


class PolygonSegmentationToolPlugin(ImageViewerToolPlugin):
    def __init__(self, image_viewer_plugin, main_window_plugin):
        super().__init__(image_viewer_plugin, main_window_plugin,
                         'plugins.image_viewer.tools.polygon_segmentation.polygon_segmentation_tool',
                         'PolygonSegmentationTool', 'Polygon')
