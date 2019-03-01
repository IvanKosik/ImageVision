from .plugin import Plugin

from typing import Type, List, Union


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def plugin(self, plugin_name: Union[Type[Plugin], str]):
        return self.plugins[plugin_name if isinstance(plugin_name, str) else plugin_name.name()]

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

        plugin.removed.connect(lambda: self.remove_plugin(plugin_cls))

        # Remove plugin if any required plugin was removed
        for required_plugin in required_plugins:
            required_plugin.removed.connect(plugin.remove)

        return plugin

    def install_plugins(self, plugin_classes: List[Type[Plugin]]):
        for plugin_cls in plugin_classes:
            self.install_plugin(plugin_cls)

    def remove_plugin(self, plugin_name: Union[Type[Plugin], str]):
        if not isinstance(plugin_name, str):
            plugin_name = plugin_name.name()

        # Do nothing if plugin already removed
        if plugin_name not in self.plugins:
            return

        plugin = self.plugins[plugin_name]
        del self.plugins[plugin_name]
        plugin.remove()
