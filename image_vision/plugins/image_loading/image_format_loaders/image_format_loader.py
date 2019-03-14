from core.image import Image

from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path
import abc
import inspect


class ImageFormatLoaderMeta(abc.ABCMeta, type(QObject)):
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


class ImageFormatLoader(QObject, metaclass=ImageFormatLoaderMeta):
    # _FORMATS = ()

    image_loaded = pyqtSignal(Image)

    @property
    def formats(self):
        return type(self).formats

    def load_image(self, path: Path):
        image = self._load_image(path)
        self.image_loaded.emit(image)
        return image

    @abc.abstractmethod
    def _load_image(self, path: Path):
        ...
