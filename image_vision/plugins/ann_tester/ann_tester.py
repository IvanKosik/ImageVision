from PyQt5.QtCore import QObject
import cv2
from pathlib import Path
import numpy as np
from skimage.io import imsave
from timeit import default_timer as timer


class AnnTester(QObject):
    def __init__(self):
        super().__init__()

        self.model = None
        self.load_model_start_time = None

    def test_model(self):
        self.load_model_start_time = timer()
        self.model = cv2.dnn.readNetFromTensorflow('tmp/out/keras_frozen.pb')
        print('load model time:', timer() - self.load_model_start_time)

        self.predict_dir_images()

    def predict_dir_images(self):
        images_path = Path('test_data/nerv_series')

        images_len = sum(1 for _ in images_path.iterdir())
        images = np.zeros((images_len, 64, 64, 1), dtype=np.float32)

        # Read all images in dir
        for index, image_path in enumerate(images_path.iterdir()):
            image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
            x_center = image.shape[0] // 2
            y_center = image.shape[1] // 2
            image = image[x_center - 32: x_center + 32, y_center - 32: y_center + 32]

            images[index, :, :, 0] = image / image.max()

        print('images shape:', images.shape)
        prediction_start_time = timer()
        self.model.setInput(cv2.dnn.blobFromImages(images))
        result_blob = self.model.forward()
        print('prediction time:', timer() - prediction_start_time)
        print('result_blob:', result_blob.shape)

        masks = np.zeros((images_len, 64, 64, 1), dtype=np.float32)
        # Loop through all result masks
        for i in range(result_blob.shape[0]):
            mask = result_blob[i, 0, :, :]
            mask[mask >= 0.5] = 255
            mask[mask < 0.5] = 0
            masks[i, :, :, 0] = mask

        print('common time (not considering time to save data to disk):', timer() - self.load_model_start_time)

        # Create all masks with original image sizes and save them to masks dir
        masks_path = Path('test_data/mask')

        for index, image_path in enumerate(images_path.iterdir()):
            image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
            x_center = image.shape[0] // 2
            y_center = image.shape[1] // 2

            mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            mask[x_center - 32: x_center + 32, y_center - 32: y_center + 32] = masks[index, :, :, 0]
            mask = mask.astype(np.uint8)

            imsave(str(masks_path / image_path.name), mask)
