from .base import FileLoader

from typing import Type


class FileLoaderRegistry:
    def __init__(self):
        super().__init__()

        self._registry = {}

    def register_loader_cls(self, loader_cls: Type[FileLoader]):
        for file_format in loader_cls.formats:
            assert file_format not in self._registry, 'Duplicate format of file loader'
            self._registry[file_format] = loader_cls

    def unregister_loader_cls(self, loader_cls: Type[FileLoader]):
        for file_format in loader_cls.formats:
            assert self._registry[file_format] == loader_cls, 'Format registered for other file loader'
            del self._registry[file_format]

    def loader_cls(self, file_format: str) -> Type[FileLoader]:
        return self._registry[file_format]

    def contains_format(self, file_format: str) -> bool:
        return file_format in self._registry
