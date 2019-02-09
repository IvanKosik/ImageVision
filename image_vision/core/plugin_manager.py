class PluginManager:
    def __init__(self):
        self.plugins = {}

    def plugin(self, name):
        return self.plugins[name]

    def install_plugin(self, plugin):
        plugin.install()
        self.plugins[plugin.name()] = plugin
