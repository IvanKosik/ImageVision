import nibabel as nib
import keras
import numpy as np
from core import image_utils

from pahtlib import Path


def predict_on_nifti_model_slices(nifti_model_path: Path, keras_model_path: Path, nifti_predicted_model_path: Path):
    nifti_model = nib.load(nifti_model_path)

    try:
        keras_model = keras.models.load_model(keras_model_path, compile=False)
    except Exception as exception:
        print('Keras model loading exception: {}\n{}'.format(type(exception).__name__, exception))
        return

    model = nifti_model.get_fdata()
    for slice_number in model.shape[2]:
        slice = model[:, :, slice_number]
        predict_on_image(keras_model, slice)


def predict_on_image(keras_model, image):
    resized_rect_image = image_utils.resized_padded_to_rect_image(image, 512)  #! 512 get from model layers input shape

    images = np.zeros((1, 512, 512, 1), dtype=np.float32)
    images[0, :, :, 0] = resized_rect_image / image.max()

    try:
        predictions = keras_model.predict(images)
    except Exception as exception:
        print('Keras prediction exception: {}\n{}'.format(type(exception).__name__, exception))
        return

    predicted_image = predictions[0, :, :, 0]

    # Resize |predicted_image| to size of original |image|
    original_width =

    src_image_width = self.viewer.image().data.shape[0]
    src_image_height = self.viewer.image().data.shape[1]
    src_image_max_size = max(src_image_width, src_image_height)
    predicted_image = cv2.resize(predicted_image, (src_image_max_size, src_image_max_size), cv2.INTER_LANCZOS4)
    predicted_image = predicted_image[0: src_image_width, 0: src_image_height]

    # pred[pred < 0] = 0
    # pred[pred > 1] = 1
    # cv2.imwrite('pred.png', pred * 255)
    # print_image_info(pred)



    print('s1', self.viewer.image().data.shape)
    print('s2', predicted_image.shape)

    self.tool_mask.data = np.zeros(self.viewer.image().data.shape, np.uint8)
    self.tool_mask.data[np.where((predicted_image > 0.5))] = settings.TOOL_FOREGROUND

    self.viewer.update_scaled_combined_image()
