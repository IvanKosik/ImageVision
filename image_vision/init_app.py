from gui_application import GuiApplication
from core.plugin_manager import PluginManager
from plugins.interactive_console.interactive_console_plugin import InteractiveConsolePlugin
from plugins.main_window.main_window_plugin import MainWindowPlugin
from plugins.dicom_loader.dicom_loader_plugin import DicomLoaderPlugin
from plugins.image_loaders.nifti.nifti_image_loader_plugin import NiftiImageLoaderPlugin
from plugins.image_viewer.image_viewer_plugin import ImageViewerPlugin
from plugins.image_viewer.colormap_table_widget.colormap_table_widget_plugin import ColormapTableWidgetPlugin
from plugins.image_viewer.tools.smart_brush_segmentation.smart_brush_segmentation_tool_plugin import SmartBrushSegmentationToolPlugin
from plugins.image_viewer.tools.cluster_segmentation.cluster_segmentation_tool_plugin import ClusterSegmentationToolPlugin
from plugins.image_viewer.tools.polygon_segmentation.polygon_segmentation_tool_plugin import PolygonSegmentationToolPlugin
from plugins.image_viewer.tools.crop.crop_tool_plugin import CropToolPlugin
from plugins.image_viewer.tools.grab_cut_segmentation.grab_cut_segmentation_tool_plugin import GrabCutSegmentationToolPlugin
from plugins.image_viewer.exclusive_tool_manager.image_viewers_exclusive_tool_manager_plugin import ImageViewersExclusiveToolManagerPlugin
from plugins.image_viewer.tools.ann_prediction.ann_prediction_tool_plugin import AnnPredictionToolPlugin
from plugins.image_viewer.tools.thresholding.thresholding_tool_plugin import ThresholdingToolPlugin

import sys


print('init_app')

plugins = [ImageViewerPlugin, DicomLoaderPlugin]
app = GuiApplication(sys.argv)
app.install_plugins(plugins)


# image_viewer_plugin.image_viewer.drop_file('tests/start_image.png')
app.plugin('ImageViewerPlugin').image_viewer.drop_file('tests/ct.png')
# image_viewer_plugin.image_viewer.drop_file('D:/Projects/Temp/ImReg/Dicoms/Test/O9-P_20111116_001_002_t1_se_tra.hdr')


sys.exit(app.exec_())


'''
main_window_plugin = MainWindowPlugin()
image_viewer_plugin = ImageViewerPlugin(main_window_plugin)
colormap_table_widget_plugin = ColormapTableWidgetPlugin(main_window_plugin, image_viewer_plugin)
dicom_loader_plugin = DicomLoaderPlugin(main_window_plugin)
nifti_loader_plugin = NiftiImageLoaderPlugin()
ann_prediction_plugin = AnnPredictionToolPlugin(image_viewer_plugin, main_window_plugin)

smart_brush_plugin = SmartBrushSegmentationToolPlugin(image_viewer_plugin, main_window_plugin)
clustering_plugin = ClusterSegmentationToolPlugin(image_viewer_plugin, main_window_plugin)
grab_cut_plugin = GrabCutSegmentationToolPlugin(image_viewer_plugin, main_window_plugin)
crop_plugin = CropToolPlugin(image_viewer_plugin, main_window_plugin)
polygon_segmentation_tool_plugin = PolygonSegmentationToolPlugin(image_viewer_plugin, main_window_plugin)
thresholding_tool_plugin = ThresholdingToolPlugin(image_viewer_plugin, main_window_plugin)

exclusive_tool_plugins = [smart_brush_plugin, clustering_plugin, grab_cut_plugin, crop_plugin,
                          polygon_segmentation_tool_plugin, thresholding_tool_plugin]
exclusive_tool_manager_plugin = ImageViewersExclusiveToolManagerPlugin(exclusive_tool_plugins)

plugin_manager = PluginManager()
interactive_console_plugin = InteractiveConsolePlugin(main_window_plugin, locals())

plugins = [main_window_plugin, image_viewer_plugin, colormap_table_widget_plugin, dicom_loader_plugin,
           ann_prediction_plugin, exclusive_tool_manager_plugin, interactive_console_plugin] + exclusive_tool_plugins

for plugin in plugins:
    plugin_manager.install_plugin(plugin)

smart_brush_plugin.activate_tool()
'''
