from plugins.image_viewer.image_layer import ImageLayer
from core.image import Image
from core.colormap import Colormap
from core import image_utils
from core import settings

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal
from skimage.io import imread, imsave
import numpy as np
import os


class ImageViewer(QLabel):
    before_image_changed = pyqtSignal()
    image_changed = pyqtSignal()

    def __init__(self, main_window, parent=None):
        super().__init__(parent)

        self.main_window = main_window  #%! Temp

        self.image_layer = ImageLayer('Image')
        self.mask_layer = ImageLayer('Mask')
        self.layers = [self.image_layer, self.mask_layer]
        # self.layers = {self.image_layer.id: self.image_layer,
        #                self.mask_layer.id: self.mask_layer}

        self.initial_mask = None

        self.colormap = Colormap()
        self.colormap.changed.connect(self.update_scaled_combined_image)

        self.combined_qimage = None
        self.scaled_combined_qimage = None
        self.scale = None

        self.setMinimumSize(100, 100)
        self.setAlignment(Qt.AlignTop)

        self.setAcceptDrops(True)

        # self.view_mode = ViewMode.FILE
        self.image_path = '' #tests/start_image.png'
        self.mask_path = ''
        self.view_path = ''
        self.images_path = ''
        self.masks_path = ''
        self.dir_image_index = 0
        self.dir_images = []

        self.image_view = False

        #self.drop_file('test_data/test_image.png')
        # self.tool_interactor = SmartBrushToolInteractor(self)
        # self.tool_interactor = GrabCutToolInteractor(self)
        # self.tool_interactor = GrabCutBrushToolInteractor(self)
        # self.installEventFilter(self.tool_interactor)

        self.setFocusPolicy(Qt.StrongFocus)  # for key events

    def add_layer(self, name, image: Image = None):
        layer = ImageLayer(name, image)
        self.layers.append(layer)
        return layer

    def remove_layer(self, layer):
        self.layers.remove(layer)

    def toogle_mask_visibility(self):
        self.mask_layer.visible = not self.mask_layer.visible
        self.update_scaled_combined_image()

    def toogle_image_view(self):
        self.image_view = not self.image_view
        self.update_scaled_combined_image()

    def image(self):
        return self.image_layer.image

    def mask(self):
        return self.mask_layer.image

    def has_image(self):
        return self.image() is not None

    def is_over_image(self, pos):
        return pos.x() <= self.scaled_combined_qimage.width() and pos.y() <= self.scaled_combined_qimage.height()

    def pos_to_image_coords(self, pos):
        return [round(pos.y() / self.scale), round(pos.x() / self.scale)]

    def dragEnterEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        if not os.path.exists(path):
            e.ignore()
            return

        if os.path.isdir(path) or path.endswith('.png') or path.endswith('.jpg'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        self.drop_file(path)

    def drop_file(self, path):
        self.actions_before_image_changed()

        if os.path.isdir(path) and os.path.exists(os.path.join(path, 'image')):
            self.view_path = path
            self.images_path = os.path.join(self.view_path, 'image')
            self.masks_path = os.path.join(self.view_path, 'mask')

            self.dir_images = sorted(os.listdir(self.images_path))
            self.dir_image_index = 0

        elif path.endswith('.png') or path.endswith('.jpg'):
            self.images_path = os.path.dirname(path)
            self.view_path = os.path.dirname(self.images_path)
            self.masks_path = os.path.join(self.view_path, 'mask')

            self.dir_images = sorted(os.listdir(self.images_path))
            self.dir_image_index = self.dir_images.index(os.path.basename(path))

        else:
            return

        if not self.dir_images:
            return

        self.load_image_in_dir_by_index(self.dir_image_index)

    def save_current_mask(self):
        if self.mask() is None or not os.path.exists(self.masks_path):
            return

        mask_data = self.mask().data
        if (mask_data != self.initial_mask.data).any():
            print('save', self.mask_path)

            binary_mask = np.zeros(mask_data.shape[:2], np.uint8)
            binary_mask[np.where((mask_data == settings.MASK_COLOR).all(axis=2))] = 255

            # cv2.imwrite(self.mask_path, binary_mask)
            imsave(self.mask_path, binary_mask)

    def save_current_image(self):
        if self.image() is None:
            return

        save_folder = os.path.join(self.view_path, 'image-edited')
        if not os.path.exists(save_folder):
            return

        save_path = os.path.join(save_folder, os.path.basename(self.image_path))
        imsave(save_path, self.image().data[:, :, :3])

    def actions_before_image_changed(self):
        self.save_current_mask()
        # self.save_current_image()
        self.before_image_changed.emit()

    def change_image_in_dir_by_index(self, index):
        self.actions_before_image_changed()
        self.load_image_in_dir_by_index(index)

    def load_image_in_dir_by_index(self, index):
        self.dir_image_index = index % len(self.dir_images)
        file_name = self.dir_images[self.dir_image_index]
        image_path = os.path.join(self.images_path, file_name)
        mask_path = os.path.join(self.masks_path, file_name)
        self.load_image(image_path, mask_path)

    def show_next_image(self):
        # Load next image and mask in folder
        self.change_image_in_dir_by_index(self.dir_image_index + 1)

    def show_previous_image(self):
        # Load previous image and mask in folder
        self.change_image_in_dir_by_index(self.dir_image_index - 1)

    def load_image(self, image_path, mask_path=None):
        if not (os.path.exists(image_path) and (image_path.endswith('.png') or image_path.endswith('.jpg'))):
            return
        print('--- Load:', image_path, '---')
        self.image_path = image_path
        self.main_window.setWindowTitle(os.path.basename(self.image_path))
        self.mask_path = mask_path

        self.image_layer.image = Image(imread(self.image_path))
        # self.image_layer.image.data = resize(self.image_layer.image.data, (512, 512), anti_aliasing=True)
        # print('s', self.image().data.shape)
        image_utils.print_image_info(self.image().data, 'original')
        self.image().data = image_utils.converted_to_normalized_uint8(self.image().data)
        self.image().data = image_utils.converted_to_rgba(self.image().data)
        image_utils.print_image_info(self.image().data, 'converted')

        if os.path.exists(mask_path):
            print('mask', mask_path)
            mask = imread(mask_path)
            image_utils.print_image_info(mask, 'mask original')
            # If mask is greyscale then convert to binary
            if len(np.unique(mask)) > 2:
                mask[mask >= 127] = 255
                mask[mask < 127] = 0
            mask = image_utils.converted_to_normalized_uint8(mask)
            mask = image_utils.converted_to_rgba_mask(mask)
            # Paint the mask (change color)
            mask[np.where((mask != [0, 0, 0, 0]).all(axis=2))] = settings.MASK_COLOR
            image_utils.print_image_info(mask, 'mask converted')
        else:
#            mask = np.zeros(self.image().data.shape, np.uint8)
            mask = np.full((self.image().data.shape[0], self.image().data.shape[1]), settings.NO_MASK_CLASS, np.uint8)
        self.mask_layer.image = Image(mask)
        self.initial_mask = Image(np.copy(mask))
        self.image_changed.emit()

        self.update_scaled_combined_image()

    def update_scaled_combined_image(self):
        if not self.has_image():
            return

        self.combined_qimage = image_utils.numpy_rgba_image_to_qimage(self.layers[0].image.data)
        if not self.image_view:
            painter = QPainter(self.combined_qimage)
            for i in range(1, len(self.layers)):
                layer = self.layers[i]
                if layer.image is not None and layer.visible:
                    painter.setOpacity(layer.opacity)
                    rgba_layer_image_data = self.colormap.colored_premultiplied_image(layer.image.data)
                    painter.drawImage(0, 0, image_utils.numpy_rgba_image_to_qimage(rgba_layer_image_data))
            painter.end()

        self.scaled_combined_qimage = self.combined_qimage.scaled(self.width(), self.height(),
                                                                  Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.scale = self.scaled_combined_qimage.width() / self.combined_qimage.width()

        self.setPixmap(QPixmap(self.scaled_combined_qimage))

    def resizeEvent(self, e):
        self.update_scaled_combined_image()
        super().resizeEvent(e)
