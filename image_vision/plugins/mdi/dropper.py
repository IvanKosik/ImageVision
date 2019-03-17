from core import Plugin
from extensions.mdi import MdiAreaFileDropper
from .area import MdiAreaPlugin
from plugins.loaders import FileLoadingManagerPlugin
from plugins.visualizers import DataVisualizationManagerPlugin


class MdiAreaFileDropperPlugin(Plugin):
    def __init__(self, mdi_area_plugin: MdiAreaPlugin, loading_manager_plugin: FileLoadingManagerPlugin,
                 visualization_manager_plugin: DataVisualizationManagerPlugin):
        super().__init__()

        self.mdi_area = mdi_area_plugin.mdi_area

        self.file_dropper = MdiAreaFileDropper(loading_manager_plugin.loading_manager,
                                               visualization_manager_plugin.visualization_manager)

    def _install(self):
        self.mdi_area.setAcceptDrops(True)
        self.mdi_area.installEventFilter(self.file_dropper)

    def _remove(self):
        self.mdi_area.removeEventFilter(self.file_dropper)
