from core.plugin import Plugin
from plugins.main_window.main_window import MainWindow


class MainWindowPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.main_window = None

    def install_gui(self, plugin_manager):
        super().install_gui(plugin_manager)

        self.main_window = MainWindow()
        self.main_window.show()
