from PyQt5.QtCore import QObject, pyqtSignal

from inspect import signature


class Plugin(QObject):
    installed = pyqtSignal()
    removed = pyqtSignal()

    def __init__(self):
        self._installed = False

        super().__init__()
        self.print_action('init')

    def __del__(self):
        self.print_action('del')

    def install(self):
        if self._installed:
            return

        self.print_action('install')
        self._install()
        self._installed = True
        self.installed.emit()

    def _install(self):
        pass

    def remove(self):
        if self._installed:
            self.print_action('remove')
            self._remove()
            self._installed = False
            self.removed.emit()

    def _remove(self):
        pass

    def print_action(self, action_str):
        print('{} {} plugin'.format(action_str, self.name()))

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
