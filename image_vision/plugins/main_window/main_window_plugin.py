from core.plugin import Plugin
from plugins.main_window.main_window import MainWindow


class MainWindowPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.main_window = MainWindow()

    def _install(self):
        self.main_window.show()
