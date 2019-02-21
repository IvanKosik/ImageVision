from core.plugin import Plugin
from plugins.interactive_console.interactive_console import InteractiveConsole

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDockWidget, QTextEdit, QLineEdit, QWidget, QVBoxLayout

import io
import sys
from contextlib import redirect_stdout, redirect_stderr


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class InteractiveConsolePlugin(Plugin):
    def __init__(self, main_window_plugin, namespace):
        super().__init__()

        self.main_window_plugin = main_window_plugin
        self.namespace = namespace

        self.interactive_console = None
        self.interpreter_line = None
        self.interpreter_output = None

    def install_gui(self):
        super().install_gui()

        self.interactive_console = InteractiveConsole(self.namespace)

        dock_widget = QDockWidget('Interactive Console')

        self.interpreter_line = QLineEdit('print("Hello")')
        self.interpreter_line.returnPressed.connect(self.on_interpreter_line_return_pressed)
        self.interpreter_output = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.interpreter_output)
        layout.addWidget(self.interpreter_line)

        interpreter_widget = QWidget()
        interpreter_widget.setLayout(layout)

        dock_widget.setWidget(interpreter_widget)

        self.main_window_plugin.main_window.addDockWidget(Qt.BottomDockWidgetArea, dock_widget)

    def on_interpreter_line_return_pressed(self):
        '''
        with Capturing() as output:
            result = self.interactive_console.push(self.interpreter_line.text())
        print('myOut:', output)
        '''

        fff = io.StringIO()
        with redirect_stdout(fff):
            result = self.interactive_console.push(self.interpreter_line.text())
        print('---interpreter result', result)
        out = fff.getvalue()
        print('out:', out)
        if out:
            self.interpreter_output.append(out)
