from .plugin import Plugin

from typing import Type, List


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def plugin(self, name):
        return self.plugins[name]

    '''
    def plugin(self, cls):
        if type(cls) is str:
            return self.plugins[cls]
        if type(cls) is Plugin:
            return self.plugins[cls.name()]
    '''

    def install_plugin(self, plugin_cls: Type[Plugin]):
        # Do nothing if plugin already installed
        if plugin_cls.name() in self.plugins:
            return self.plugins[plugin_cls.name()]

        assert plugin_cls.init_annotated(), 'Add annotations for plugin {}'.format(plugin_cls)

        # Install all required plugins
        required_plugins = []
        for required_plugin_cls in plugin_cls.required_plugin_classes():
            required_plugin = self.install_plugin(required_plugin_cls)
            required_plugins.append(required_plugin)

        # Create plugin instance with required plugins as parameters
        plugin = plugin_cls(*required_plugins)

        self.plugins[plugin.name()] = plugin
        plugin.install()

        # Remove plugin if any required plugin was removed
        '''
        for required_plugin in required_plugins:
            required_plugin.removed.connect(self.remove_plugin)              ####
        '''

        return plugin

    def install_plugins(self, plugin_classes: List[Type[Plugin]]):
        for plugin_cls in plugin_classes:
            self.install_plugin(plugin_cls)

    def remove_plugin(self, plugin_cls: Type[Plugin]):
        assert False
        pass
