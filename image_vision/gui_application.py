from core.plugin_manager import PluginManager
from core.plugin import Plugin

from PyQt5.QtWidgets import QApplication

from typing import Type, List


class GuiApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.plugin_manager = PluginManager()

    def plugin(self, name):
        return self.plugin_manager.plugin(name)

    def install_plugin(self, plugin_cls: Type[Plugin]):
        self.plugin_manager.install_plugin(plugin_cls)

    def install_plugins(self, plugin_classes: List[Type[Plugin]]):
        self.plugin_manager.install_plugins(plugin_classes)

    def remove_plugin(self, plugin_cls: Type[Plugin]):
        self.plugin_manager.remove_plugin(plugin_cls)
