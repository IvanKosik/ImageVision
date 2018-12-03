from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.move(300, 300)
        self.setWindowTitle('Data Editor')
