from ..image_loader import ImageLoader

from pathlib import Path


class NiftiImageLoader(ImageLoader):
    def __init__(self):
        super().__init__(['nii.gz', 'hdr'])

    def load_image(self, path: Path):
        print('NiftiImageLoader load_image')
