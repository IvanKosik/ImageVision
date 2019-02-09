from core.plugin import Plugin

from PyQt5.QtCore import pyqtSignal

import importlib


TOOLS_MENU_TITLE = 'Tools'


class ImageViewerToolPlugin(Plugin):
    before_tool_activation = pyqtSignal(object)

    def __init__(self, image_viewer_plugin, main_window_plugin,
                 tool_module_str, tool_cls_str, action_name='', action_shortcut=''):
        super().__init__()

        self.image_viewer_plugin = image_viewer_plugin
        self.main_window_plugin = main_window_plugin
        self.tool_module_str = tool_module_str
        self.tool_cls_str = tool_cls_str
        self.action_name = action_name
        self.action_shortcut = action_shortcut

        self.tool = None
        self.image_viewer = None

    def install_core(self):
        super().install_core()

        self.image_viewer = self.image_viewer_plugin.image_viewer

    def install_gui(self):
        super().install_gui()

        if not self.action_name:
            return

        main_window = self.main_window_plugin.main_window
        menu_bar_actions = main_window.menuBar().actions()
        tools_menu_action = next((action for action in menu_bar_actions if action.text() == TOOLS_MENU_TITLE), None)
        tools_menu = main_window.menuBar().addMenu(TOOLS_MENU_TITLE) if tools_menu_action is None \
            else tools_menu_action.menu()
        tool_action = tools_menu.addAction(self.action_name, self.activate_tool, self.action_shortcut)

    def create_tool(self):
        tool_module = importlib.import_module(self.tool_module_str)
        tool_cls = getattr(tool_module, self.tool_cls_str)
        self.tool = tool_cls(self.image_viewer)
        self.tool.before_activation.connect(self.before_tool_activation)

    def activate_tool(self):
        if self.tool is None:
            self.create_tool()

        self.tool.activate()

    def deactivate_tool(self):
        self.tool.deactivate()
