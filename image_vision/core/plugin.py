from PyQt5.QtCore import QObject, pyqtSignal


class Plugin(QObject):
    installed = pyqtSignal()

    def __init__(self):
        super().__init__()
        print('init', self.name(), 'plugin')

    def install(self):
        print('install', self.name(), 'plugin')
        self._install()
        self.installed.emit()

    def _install(self):
        pass

    @classmethod
    def required_plugins(cls):
        import inspect
        return inspect.getfullargspec(cls.__init__)

    @classmethod
    def name(cls):
        return cls.__name__
