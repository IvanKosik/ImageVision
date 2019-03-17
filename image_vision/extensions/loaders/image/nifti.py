from .base import ImageFileLoader

from pathlib import Path


class NiftiImageFileLoader(ImageFileLoader):
    _FORMATS = ('nii.gz', 'hdr')

    def _load_file(self, path: Path):
        print('Load NIfTI')
