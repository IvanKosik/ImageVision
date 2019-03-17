from core import Data

from PyQt5.QtCore import QObject, pyqtSignal

import abc
import inspect
from pathlib import Path


class FileLoaderMeta(abc.ABCMeta, type(QObject)):
    _FORMATS = ()

    def __new__(mcls, name, bases, namespace):
        print('Meta new')  #%
        print(type(QObject))  #%
        cls = super().__new__(mcls, name, bases, namespace)

        if not inspect.isabstract(cls) and not cls.formats:
            raise NotImplementedError('Subclass must define formats attribute')

        return cls

    @property
    def formats(cls) -> tuple:
        return cls._FORMATS


class FileLoader(QObject, metaclass=FileLoaderMeta):
    #% _FORMATS = ()

    file_loaded = pyqtSignal(Data)

    @property
    def formats(self):
        return type(self).formats

    def load_file(self, path: Path) -> Data:
        data = self._load_file(path)
        self.file_loaded.emit(data)
        return data

    @abc.abstractmethod
    def _load_file(self, path: Path) -> Data:
        ...
