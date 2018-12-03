from plugins.image_viewer.tools.image_viewer_tool_plugin import ImageViewerToolPlugin


class CropToolPlugin(ImageViewerToolPlugin):
    def __init__(self):
        super().__init__('plugins.image_viewer.tools.crop.crop_tool',
                         'CropTool', 'Crop')
