from plugins.image_viewer.image_viewer import ImageViewer
from plugins.image_viewer.image_layer import ImageLayer
from core.image import Image
from core import image_utils
from core import settings

from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal
from skimage.io import imread, imsave
import nibabel as nib
import numpy as np
import os

from skimage.morphology import disk
from skimage.filters import rank


class ModelImageViewer(ImageViewer):  #% or rename to ModelSliceViewer
    def __init__(self, main_window, parent=None):
        super().__init__(main_window, parent)

        self.nib_model = None
        self.model = None
        self.slice_number = 0
        self.mask_model = None
        self.nib_mask_model = None

    def dragEnterEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        if not os.path.exists(path):
            e.ignore()
            return

        if os.path.isdir(path) or path.endswith('.nii.gz') or path.endswith('.hdr'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        self.drop_file(path)

    def drop_file(self, path):
        self.actions_before_image_changed()

        if path.endswith('.nii.gz') or path.endswith('.hdr'):
            self.nib_model = nib.load(path)
            self.model = self.nib_model.get_fdata()

            self.mask_path = path.split('.')[0] + '_mask.nii.gz'
            if os.path.exists(self.mask_path):
                nib_mask_model = nib.load(self.mask_path)
                self.mask_model = nib_mask_model.get_fdata()
            else:
                self.mask_model = np.zeros_like(self.model, dtype=np.uint8)
        else:
            return

        self.show_slice(0)

    def has_image(self):
        return self.model is not None

    def show_slice(self, number):
        self.slice_number = number % self.model.shape[2]

        print('--- Show slice:', self.slice_number, '---')
        self.image_layer.image = Image(np.ascontiguousarray(self.model[:, :, self.slice_number]))

        image_utils.print_image_info(self.image().data, 'original')
        self.image().data = image_utils.converted_to_normalized_uint8(self.image().data)

        self.image().data = rank.equalize(self.image().data, selem=disk(40))

        self.image().data = image_utils.converted_to_rgba(self.image().data)
        image_utils.print_image_info(self.image().data, 'converted')

        m = self.mask_model[:, :, self.slice_number]
        m = image_utils.converted_to_normalized_uint8(m)
        m = image_utils.converted_to_rgba_mask(m)
        m[np.where((m != [0, 0, 0, 0]).all(axis=2))] = settings.MASK_COLOR
        self.mask_layer.image = Image(np.ascontiguousarray(m))

        self.initial_mask = Image(np.copy(m))

        self.image_changed.emit()

        self.update_scaled_combined_image()

    def save_current_mask(self):
        if self.mask_model is None:
            return

        mask_data = self.mask().data
        if (mask_data != self.initial_mask.data).any():
            print('save', self.mask_path)

            binary_mask = np.zeros(mask_data.shape[:2], np.uint8)
            binary_mask[np.where((mask_data == settings.MASK_COLOR).all(axis=2))] = 255

            self.mask_model[:, :, self.slice_number] = binary_mask

            self.nib_mask_model = nib.Nifti1Image(self.mask_model, affine=self.nib_model.affine, header=self.nib_model.header)
            self.nib_mask_model.to_filename(self.mask_path)

    def change_slice(self, number):
        self.actions_before_image_changed()
        self.show_slice(number)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            # Load next image and mask in folder
            self.change_slice(self.slice_number + 1)
        elif e.key() == Qt.Key_Left:
            # Load previous image and mask in folder
            self.change_slice(self.slice_number - 1)
