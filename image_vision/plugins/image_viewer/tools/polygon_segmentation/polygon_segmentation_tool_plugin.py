from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin


class PolygonSegmentationToolPlugin(ImageViewerToolPlugin):
    def __init__(self):
        super().__init__('plugins.image_viewer.tools.polygon_segmentation.polygon_segmentation_tool',
                         'PolygonSegmentationTool', 'Polygon')
