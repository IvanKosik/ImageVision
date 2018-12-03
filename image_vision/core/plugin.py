from PyQt5.QtCore import QObject


class Plugin(QObject):
    def __init__(self):
        super().__init__()
        print('init', self.name(), 'plugin')

    def install(self, plugin_manager):
        print('install', self.name(), 'plugin')
        self.install_core(plugin_manager)
        self.install_gui(plugin_manager)

    def install_core(self, plugin_manager):
        pass

    def install_gui(self, plugin_manager):
        pass

    @classmethod
    def name(cls):
        return cls.__name__
