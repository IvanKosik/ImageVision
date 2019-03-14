from core.image import Image

from PyQt5.QtCore import QObject, pyqtSignal

from pathlib import Path
import abc
import inspect


class ImageFormatLoaderRegistry(abc.ABCMeta):
    _registry = {}

    def __new__(mcls, name, bases, namespace):
        print('Meta new')
        cls = super().__new__(mcls, name, bases, namespace)

        if not inspect.isabstract(cls):
            if not cls.formats:
                raise NotImplementedError('Subclass must define formats attribute')

            for image_format in cls.formats:
                mcls._registry[image_format] = cls

        return cls

    @property
    def formats(cls) -> tuple:
        return cls._FORMATS

    @classmethod
    def registry(mcls):
        return mcls._registry.copy()

    @classmethod
    def image_format_loader_cls(mcls, image_format):
        return mcls._registry[image_format]

    @classmethod
    def image_format_loader(mcls, image_format):
        return mcls.image_format_loader_cls(image_format)()


class ImageFormatLoader(metaclass=ImageFormatLoaderRegistry):
    _FORMATS = ()

    # image_loaded = pyqtSignal(Image)

    @property
    def formats(self):
        return type(self).formats

    @abc.abstractmethod
    def load_image(self, path: Path):
        ...
