from PyQt5.QtGui import QImage
import numpy as np
from skimage.color import gray2rgb
from skimage.transform import rescale


def converted_to_normalized_uint8(image):
    if image.dtype != np.uint8 or image.max() != 255:
        if image.max() != 0:
            image = image / image.max() * 255
        image = image.astype(np.uint8)
    return image


def converted_to_n_channels(image, n):
    if image.ndim == 2:  # one channel
        image = np.stack((image,) * n, -1)
    return image


def converted_to_rgba(image):
    if image.ndim == 2:  # one channel (grayscale image)
        image = gray2rgb(image, True)
    elif image.ndim == 3 and image.shape[2] == 3:  # 3-channel image
        # Add alpha-channel
        image = np.dstack((image, np.full(image.shape[:2], 255, np.uint8)))
    return image


def converted_to_rgba_mask(mask):
    if mask.ndim == 2:  # one channel (grayscale mask)
        mask = np.stack((mask,) * 4, -1)
    elif mask.ndim == 3 and mask.shape[2] == 3:  # 3-channel mask
        # Add alpha-channel
        mask = np.dstack((mask, np.full(mask.shape[:2], 0, np.uint8)))
        mask[np.where((mask != [0, 0, 0, 0]).any(axis=2))][3] = 255  # set full opacity for masked regions
    return mask


def numpy_rgb_image_to_qimage(numpy_image):
    height, width, channel = numpy_image.shape
    bytes_per_line = 3 * width
    return QImage(numpy_image.data, width, height, bytes_per_line, QImage.Format_RGB888)


def numpy_bgr_image_to_qimage(numpy_image):
    return numpy_rgb_image_to_qimage(numpy_image).rgbSwapped()


def numpy_rgba_image_to_qimage(numpy_image, image_format: QImage.Format = QImage.Format_RGBA8888_Premultiplied):
    # print("STRIDES", numpy_image.strides[0])
    # print(numpy_image.flags['C_CONTIGUOUS'])

    height, width, channel = numpy_image.shape
    bytes_per_line = width * channel
    return QImage(numpy_image.data, width, height, bytes_per_line, image_format)


def numpy_bgra_image_to_qimage(numpy_image):
    return numpy_rgba_image_to_qimage(numpy_image).rgbSwapped()


def numpy_gray_image_to_qimage(numpy_image):
    height, width = numpy_image.shape
    bytes_per_line = numpy_image.strides[0]
    return QImage(numpy_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)


# Returns resized image keeping aspect ratio
def resized_image(image, max_size, multichannel=False, anti_aliasing=True):
    bigger_side = max(image.shape[0], image.shape[1])
    scale_factor = max_size / bigger_side
    # mode='constant' is used just to hide warning in scikit-image 0.14.1
    return rescale(image, scale_factor, mode='constant', multichannel=multichannel, anti_aliasing=anti_aliasing)


# Returns resized image keeping aspect ration and padded to rectangular
def resized_padded_to_rect_image(image, max_size, multichannel=False, anti_aliasing=True):
    resized = resized_image(image, max_size, multichannel, anti_aliasing)
    return np.pad(resized, ((0, max_size - resized.shape[0]), (0, max_size - resized.shape[1])), 'constant')


def print_image_info(image, prefix=''):
    if prefix:
        prefix += '\t'
    print(prefix + 'type:', image.dtype, '\tshape:', image.shape, '\tmin:', image.min(), '\tmax:', image.max())
