from core import Data
from .registry import FileLoaderRegistry

from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path


class FileLoadingManager(QObject):
    file_loaded = pyqtSignal(Data)

    def __init__(self, loaders_registry: FileLoaderRegistry):
        super().__init__()

        self.loaders_registry = loaders_registry

    def can_load_file(self, path: Path) -> bool:
        file_format = path.suffix[1:]  # remove dot
        return self.loaders_registry.contains_format(file_format)

    def load_file(self, path: Path) -> Data:
        print('File loader: load_file')
        file_format = path.suffix[1:]  # remove dot
        format_loader_cls = self.loaders_registry.loader_cls(file_format)
        format_loader = format_loader_cls()
        data = format_loader.load_file(path)
        self.file_loaded.emit(data)
        return data
