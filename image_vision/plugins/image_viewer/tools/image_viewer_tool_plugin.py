from core.plugin import Plugin
from ..image_viewer_plugin import ImageViewerPlugin
from plugins.window.main import MainWindowPlugin

from PyQt5.QtCore import pyqtSignal

import importlib


TOOLS_MENU_TITLE = 'Tools'


class ImageViewerToolPlugin(Plugin):
    before_tool_activation = pyqtSignal(object)

    def __init__(self, image_viewer_plugin: ImageViewerPlugin, main_window_plugin: MainWindowPlugin,
                 tool_module_str, tool_cls_str, action_name='', action_shortcut=''):
        super().__init__()

        self.image_viewer = image_viewer_plugin.image_viewer
        self.main_window = main_window_plugin.main_window
        self.tool_module_str = tool_module_str
        self.tool_cls_str = tool_cls_str
        self.action_name = action_name
        self.action_shortcut = action_shortcut

        self.tool = None

    def _install(self):
        if not self.action_name:
            return

        menu_bar_actions = self.main_window.menuBar().actions()
        tools_menu_action = next((action for action in menu_bar_actions if action.text() == TOOLS_MENU_TITLE), None)
        tools_menu = self.main_window.menuBar().addMenu(TOOLS_MENU_TITLE) if tools_menu_action is None \
            else tools_menu_action.menu()
        tool_action = tools_menu.addAction(self.action_name, self.activate_tool, self.action_shortcut)

    def _remove(self):
        assert False, 'Not implemented'

    def create_tool(self):
        tool_module = importlib.import_module(self.tool_module_str)
        tool_cls = getattr(tool_module, self.tool_cls_str)
        self.tool = tool_cls(self.image_viewer)
        self.tool.before_activation.connect(self.before_tool_activation)

    def activate_tool(self):
        if self.tool is None:
            self.create_tool()

        self.tool.mask_class = self.image_viewer.colormap.active_color_class
        self.tool.activate()

    def deactivate_tool(self):
        self.tool.deactivate()
