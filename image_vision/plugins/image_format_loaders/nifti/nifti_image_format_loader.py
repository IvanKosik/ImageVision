from plugins.image_format_loaders.image_format_loader import ImageFormatLoader

from pathlib import Path


class NiftiImageFormatLoader(ImageFormatLoader):
    _FORMATS = ('nii.gz', 'hdr')

    def load_image(self, path: Path):
        print('Load NIfTI')
