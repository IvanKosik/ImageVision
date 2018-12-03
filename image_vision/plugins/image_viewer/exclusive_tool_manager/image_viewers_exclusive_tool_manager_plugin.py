from plugin import Plugin


class ImageViewersExclusiveToolManagerPlugin(Plugin):
    def __init__(self, exclusive_tool_plugins):
        super().__init__()

        self.exclusive_tool_plugins = exclusive_tool_plugins

        self.active_tool = None

    def install_core(self, plugin_manager):
        super().install_core(plugin_manager)

        for tool_plugin in self.exclusive_tool_plugins:
            tool_plugin.before_tool_activation.connect(self.on_before_tool_activation)

    def on_before_tool_activation(self, tool):
        if self.active_tool is not None:
            self.active_tool.deactivate()

        self.active_tool = tool
