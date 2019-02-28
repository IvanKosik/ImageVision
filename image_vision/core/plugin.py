from PyQt5.QtCore import QObject, pyqtSignal

from inspect import signature


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

    def remove(self):
        pass

    def _remove(self):
        pass

    @classmethod
    def required_plugin_classes(cls):
        return cls.__init__.__annotations__.values()

    @classmethod
    def init_parameters_number(cls) -> int:
        return len(signature(cls.__init__).parameters)

    @classmethod
    def init_annotated(cls) -> bool:
        return len(cls.required_plugin_classes()) == cls.init_parameters_number() - 1  # minus 1 to ignore |self|

    @classmethod
    def name(cls):
        return cls.__name__
