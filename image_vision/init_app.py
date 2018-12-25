from core.plugin_manager import PluginManager
from plugins.main_window.main_window_plugin import MainWindowPlugin
from plugins.dicom_loader.dicom_loader_plugin import DicomLoaderPlugin
from plugins.image_viewer.image_viewer_plugin import ImageViewerPlugin
from plugins.image_viewer.tools.smart_brush_segmentation.smart_brush_segmentation_tool_plugin import SmartBrushSegmentationToolPlugin
from plugins.image_viewer.tools.polygon_segmentation.polygon_segmentation_tool_plugin import PolygonSegmentationToolPlugin
from plugins.image_viewer.tools.crop.crop_tool_plugin import CropToolPlugin
from plugins.image_viewer.tools.grab_cut_segmentation.grab_cut_segmentation_tool_plugin import GrabCutSegmentationToolPlugin
from plugins.image_viewer.exclusive_tool_manager.image_viewers_exclusive_tool_manager_plugin import ImageViewersExclusiveToolManagerPlugin
from plugins.image_viewer.tools.ann_prediction.ann_prediction_tool_plugin import AnnPredictionToolPlugin
from plugins.ann_tester.ann_tester_plugin import AnnTesterPlugin


print('init_app')

image_viewer_plugin = ImageViewerPlugin()
smart_brush_plugin = SmartBrushSegmentationToolPlugin()
polygon_segmentation_tool_plugin = PolygonSegmentationToolPlugin()
crop_plugin = CropToolPlugin()
grab_cut_plugin = GrabCutSegmentationToolPlugin()
# smart_brush_plugin = ImageViewerToolPlugin(SmartBrushSegmentationTool, 'Smart Brush')
# polygon_segmentation = ImageViewerToolPlugin(PolygonSegmentationTool, 'Polygon')

exclusive_tool_plugins = [smart_brush_plugin, grab_cut_plugin, crop_plugin, polygon_segmentation_tool_plugin]
exclusive_tool_manager_plugin = ImageViewersExclusiveToolManagerPlugin(exclusive_tool_plugins)

plugins = [MainWindowPlugin(), image_viewer_plugin, DicomLoaderPlugin()] + exclusive_tool_plugins + [exclusive_tool_manager_plugin, AnnPredictionToolPlugin()] #exclusive_tool_plugins  #polygon_segmentation_tool_plugin]#smart_brush_plugin]#, polygon_segmentation]

plugin_manager = PluginManager()
for plugin in plugins:
    plugin_manager.install_plugin(plugin)

smart_brush_plugin.activate_tool()
#polygon_segmentation_tool_plugin.activate_tool()
# crop_plugin.activate_tool()
#grab_cut_plugin.activate_tool()

# image_viewer_plugin.image_viewer.drop_file('tests/start_image.png')
# image_viewer_plugin.image_viewer.drop_file('D:/Projects/Temp/ImReg/Dicoms/Test/O9-P_20111116_001_002_t1_se_tra.hdr')
