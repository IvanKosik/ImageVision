from plugins.image_loading.image_format_loaders.image_format_loader import ImageFormatLoader

from pathlib import Path


class SimpleImageFormatLoader(ImageFormatLoader):
    _FORMATS = ('png', 'jpg')

    def _load_image(self, path: Path):
        print('Load Simple Image')
