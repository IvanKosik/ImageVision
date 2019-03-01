from core.plugin import Plugin
from ..main_window.main_window_plugin import MainWindowPlugin
from .interactive_console import InteractiveConsole
from .interactive_console_widget import InteractiveConsoleWidget

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDockWidget, QShortcut

import io
from contextlib import redirect_stdout


class InteractiveConsolePlugin(Plugin):
    locals = None

    def __init__(self, main_window_plugin: MainWindowPlugin):
        super().__init__()

        self.main_window = main_window_plugin.main_window

        self.console_widget = InteractiveConsoleWidget()
        self.console_widget.command_entered.connect(self.on_command_entered)
        self.interactive_console = self.create_console()

        self.dock_widget = QDockWidget('Interactive Console')
        self.dock_widget.setWidget(self.console_widget)
        self.dock_widget.hide()

        self.shortcut = QShortcut(Qt.CTRL + Qt.Key_Greater, self.main_window)

    def _install(self):
        self.main_window.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)
        self.shortcut.activated.connect(self.on_shortcut_activated)

    def _remove(self):
        self.shortcut.activated.disconnect(self.on_shortcut_activated)
        self.main_window.removeDockWidget(self.dock_widget)

        # Remove all created references (otherwise some plugins may not be deleted)
        self.interactive_console.reset_locals()

    def create_console(self):
        return InteractiveConsole(self.locals.copy(), self.console_widget.append_output)

    def reset_console(self):
        self.interactive_console = self.create_console()

    def on_command_entered(self, command_text):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            more_input_required = self.interactive_console.push(command_text)

        output_text = stdout.getvalue()
        if output_text.endswith('\n'):  # enter was redirected to stdout too, so we need to remove it
            output_text = output_text[:-1]
        if output_text:
            self.console_widget.append_output(output_text)
            print('InteractiveConsole >', output_text)

        self.console_widget.set_continue_input_prompt(more_input_required)

    def on_shortcut_activated(self):
        self.dock_widget.show()
        self.console_widget.focus_command_line()
