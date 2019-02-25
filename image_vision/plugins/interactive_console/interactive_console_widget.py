from PyQt5.Qt import QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout, QLabel, QFormLayout


class InteractiveConsoleWidget(QWidget):
    command_entered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont('Lucida Console', 10)

        self.input_prompt_label = QLabel()
        self.input_prompt_label.setFont(font)
        self.set_continue_input_prompt(False)

        self.command_line = QLineEdit()
        self.command_line.setFont(font)
        self.command_line.returnPressed.connect(self.on_command_line_return_pressed)

        self.output_widget = QTextEdit()
        self.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.output_widget)

        command_line_layout = QFormLayout()
        command_line_layout.addRow(self.input_prompt_label, self.command_line)
        layout.addLayout(command_line_layout)

        self.setLayout(layout)

    def on_command_line_return_pressed(self):
        command_text = self.command_line.text()
        output = '{} {}'.format(self.input_prompt_label.text(), command_text)
        self.append_output(output)
        self.command_line.clear()
        self.command_entered.emit(command_text)

    def append_output(self, text):
        self.output_widget.append(text)

    def set_continue_input_prompt(self, continue_input: bool = True):
        self.input_prompt_label.setText('...' if continue_input else '>>>')

    def focus_command_line(self):
        self.command_line.setFocus()
