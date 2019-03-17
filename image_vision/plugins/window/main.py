from core.plugin import Plugin
from extensions.window.main import MainWindow


class MainWindowPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.main_window = MainWindow()

    def _install(self):
        self.main_window.show()

    def _remove(self):
        self.main_window.hide()
