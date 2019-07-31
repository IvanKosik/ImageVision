from core import VolumeImage
from .base import ImageFileLoader

import nibabel
import numpy as np

from pathlib import Path


class NiftiImageFileLoader(ImageFileLoader):
    _FORMATS = ('nii.gz', 'hdr')

    def _load_file(self, path: Path):
        print('Load NIfTI')
        nifti = nibabel.load(str(path))
        array = np.asarray(nifti.dataobj)
        return VolumeImage(array, path)
