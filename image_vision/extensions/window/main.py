from PyQt5.QtWidgets import QMainWindow, QMenuBar

from enum import Enum


class MenuType(Enum):
    FILE = 1
    VIEW = 2
    HELP = 3


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self._menus = {}

        self.add_menu(MenuType.FILE)
        self.add_menu(MenuType.VIEW)
        self.add_menu(MenuType.HELP)
        # TODO: It's better to add menus at runtime (if they needed), but we have to keep correct menus order,
        #  using self.insertMenu instead of self.addMenu

    def add_menu(self, menu_type: MenuType):
        menu = self.addMenu(menu_type.name.title())
        # menu.menuAction().setVisible(False) # to hide menu (while no actions)
        self._menus[menu_type] = menu
        return menu

    def menu(self, menu_type: MenuType):
        return self._menus[menu_type]

    def add_menu_action(self, menu_type: MenuType, action_name, method, shortcut):
        return self.menu(menu_type).addAction(action_name, method, shortcut)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.move(300, 300)
        self.setWindowTitle('Image Vision')

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

    def add_menu_action(self, menu_type: MenuType, action_name, method, shortcut):
        return self.menu_bar.add_menu_action(menu_type, action_name, method, shortcut)
