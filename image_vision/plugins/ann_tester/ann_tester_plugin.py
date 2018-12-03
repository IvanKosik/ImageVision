from plugin import Plugin
from plugins.ann_tester.ann_tester import AnnTester
from plugins.main_window.main_window_plugin import MainWindowPlugin


class AnnTesterPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.ann_tester = None

    def install_core(self, plugin_manager):
        super().install_core(plugin_manager)

        self.ann_tester = AnnTester()

    def install_gui(self, plugin_manager):
        super().install_gui(plugin_manager)

        main_window = plugin_manager.plugin(MainWindowPlugin.name()).main_window

        view_menu = main_window.menuBar().addMenu('Test')
        self.test_model_action = view_menu.addAction(
            'Model', self.ann_tester.test_model)
