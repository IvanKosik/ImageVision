from core import Data
from .registry import FileLoaderRegistry
from .base import FileLoader

from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path
from typing import Type, Optional


class FileLoadingManager(QObject):
    file_loaded = pyqtSignal(Data)

    def __init__(self, loaders_registry: FileLoaderRegistry):
        super().__init__()

        self.loaders_registry = loaders_registry

    def can_load_file(self, path: Path) -> bool:
        return self._loader_cls(path) is not None

    def load_file(self, path: Path) -> Optional[Data]:
        print('File loader: load_file')
        format_loader_cls = self._loader_cls(path)
        if format_loader_cls is None:
            return None
        format_loader = format_loader_cls()
        data = format_loader.load_file(path)
        self.file_loaded.emit(data)
        return data

    def _loader_cls(self, path: Path) -> Optional[Type[FileLoader]]:
        """Return FileLoader for a file with this path.

        Start to check file format from biggest part after first dot,
        e.g. for NiftiFile.nii.gz
        at first check 'nii.gz', then check 'gz'
        """
        file_format = path.name
        while True:
            loader_cls = self.loaders_registry.loader_cls(file_format)
            if loader_cls is not None:
                return loader_cls

            dot_index = file_format.find('.')
            if dot_index == -1:
                return None

            file_format = file_format[dot_index + 1:]  # dot_index + 1 to remove dot
