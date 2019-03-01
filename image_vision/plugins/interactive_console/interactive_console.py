import code


class InteractiveConsole(code.InteractiveConsole):
    def __init__(self, console_locals, error_callback=None):
        super().__init__(console_locals)

        self.console_locals = console_locals

        self.error_callback = error_callback

    def write(self, data: str):
        if self.error_callback:
            self.error_callback(data)
        super().write(data)

    def reset_locals(self):
        self.console_locals.clear()
