from PyQt5.QtCore import QObject


class Plugin(QObject):
    def __init__(self):
        super().__init__()
        print('init', self.name(), 'plugin')

    def install(self):
        print('install', self.name(), 'plugin')
        self.install_core()
        self.install_gui()

    def install_core(self):
        pass

    def install_gui(self):
        pass

    @classmethod
    def name(cls):
        return cls.__name__
