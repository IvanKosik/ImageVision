from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin


class ClusterSegmentationToolPlugin(ImageViewerToolPlugin):
    def __init__(self, image_viewer_plugin, main_window_plugin):
        super().__init__(image_viewer_plugin, main_window_plugin,
                         'plugins.image_viewer.tools.cluster_segmentation.cluster_segmentation_tool',
                         'ClusterSegmentationTool', 'Clustering')
