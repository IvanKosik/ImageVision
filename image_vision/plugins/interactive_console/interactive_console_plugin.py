from core.plugin import Plugin
from .interactive_console import InteractiveConsole
from .interactive_console_widget import InteractiveConsoleWidget

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDockWidget, QShortcut

import io
from contextlib import redirect_stdout


class InteractiveConsolePlugin(Plugin):
    def __init__(self, main_window_plugin, namespace):
        super().__init__()

        self.main_window_plugin = main_window_plugin
        self.namespace = namespace

        self.interactive_console = None
        self.dock_widget = None
        self.console_widget = None

    def install_gui(self):
        super().install_gui()

        self.console_widget = InteractiveConsoleWidget()
        self.console_widget.command_entered.connect(self.on_command_entered)

        self.interactive_console = InteractiveConsole(self.namespace, self.console_widget.append_output)

        self.dock_widget = QDockWidget('Interactive Console')
        self.dock_widget.setWidget(self.console_widget)
        self.dock_widget.hide()
        QShortcut(Qt.CTRL + Qt.Key_Greater, self.main_window_plugin.main_window, self.on_shortcut_activated)

        self.main_window_plugin.main_window.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)

    def on_command_entered(self, command_text):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            more_input_required = self.interactive_console.push(command_text)

        output_text = stdout.getvalue()
        if output_text.endswith('\n'):  # enter was redirected to stdout too, so we need to remove it
            output_text = output_text[:-1]
        if output_text:
            self.console_widget.append_output(output_text)

        self.console_widget.set_continue_input_prompt(more_input_required)

    def on_shortcut_activated(self):
        self.dock_widget.show()
        self.console_widget.focus_command_line()
