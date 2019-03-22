from core import Plugin
from extensions.walkers import ViewerDirDataWalker
from extensions.window import MenuType
from plugins.window import MainWindowPlugin
from plugins.mdi import MdiAreaPlugin
from plugins.loaders import FileLoadingManagerPlugin

from PyQt5.QtCore import Qt


class ViewerDirDataWalkerPlugin(Plugin):
    def __init__(self, main_window_plugin: MainWindowPlugin, mdi_area_plugin: MdiAreaPlugin,
                 loading_manager_plugin: FileLoadingManagerPlugin):
        super().__init__()

        self.main_window = main_window_plugin.main_window
        self.mdi_area = mdi_area_plugin.mdi_area
        self.loading_manager = loading_manager_plugin.loading_manager

        # self.dir_data_walkers = []
        self.viewers_dir_data_walkers = {}  # viewer: dir_data_walker

    def _install(self):
        self.main_window.add_menu_action(MenuType.VIEW, 'Next Image', self._on_next_image_triggered,
                                         Qt.CTRL + Qt.Key_Right)
        self.main_window.add_menu_action(MenuType.VIEW, 'Previous Image', self._on_previous_image_triggered,
                                         Qt.CTRL + Qt.Key_Left)



    def _remove(self):
        raise NotImplementedError

    def _on_next_image_triggered(self):
        active_sub_window = self.mdi_area.activeSubWindow()
        if active_sub_window:
            data_viewer = active_sub_window.widget()
            viewer_dir_data_walker = self.viewers_dir_data_walkers.get(data_viewer)
            if viewer_dir_data_walker is None:
                viewer_dir_data_walker = ViewerDirDataWalker(data_viewer, self.loading_manager)
                self.viewers_dir_data_walkers[data_viewer] = viewer_dir_data_walker
            viewer_dir_data_walker.show_next_image()

    def _on_previous_image_triggered(self):
        print('previous')

    '''
    def _install(self):
        view_menu.addAction('Next Image', self.image_viewer.show_next_image, Qt.CTRL + Qt.Key_Right)
        view_menu.addAction('Previous Image', self.image_viewer.show_previous_image, Qt.CTRL + Qt.Key_Left)
    '''
