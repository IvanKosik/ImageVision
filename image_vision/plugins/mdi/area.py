from core import Plugin
from plugins.window import MainWindowPlugin
from extensions.mdi import MdiArea


class MdiAreaPlugin(Plugin):
    def __init__(self, main_window_plugin: MainWindowPlugin):
        super().__init__()

        self.main_window = main_window_plugin.main_window

        self.mdi_area = MdiArea()

    def _install(self):
        self.main_window.setCentralWidget(self.mdi_area)

    def _remove(self):
        self.main_window.setCentralWidget(None)
