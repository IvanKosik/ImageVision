from core import FlatImage
from .base import ImageFileLoader

from pathlib import Path

from skimage.io import imread


class SimpleImageFileLoader(ImageFileLoader):
    _FORMATS = ('png', 'jpg')

    def _load_file(self, path: Path):
        print('Load Simple Image')
        return FlatImage(imread(str(path)), path)
