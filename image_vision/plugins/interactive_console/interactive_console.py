import code


class InteractiveConsole(code.InteractiveConsole):
    def __init__(self, namespace, error_callback=None):
        super().__init__(namespace)

        self.error_callback = error_callback

    def write(self, data: str):
        if self.error_callback:
            self.error_callback(data)
        else:
            super().write(data)
