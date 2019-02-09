from core.plugin import Plugin
from plugins.main_window.main_window import MainWindow


class MainWindowPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.main_window = None

    def install_gui(self):
        super().install_gui()

        self.main_window = MainWindow()
        self.main_window.show()
