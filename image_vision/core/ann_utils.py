import nibabel as nib
import keras
import numpy as np
from core import image_utils
from pathlib import Path


def predict_on_nifti_model_slices(nifti_model_path: Path, keras_model_path: Path, nifti_predicted_model_path: Path):
    nifti_model = nib.load(str(nifti_model_path))

    try:
        keras_model = keras.models.load_model(str(keras_model_path), compile=False)
    except Exception as exception:
        print('Keras model loading exception: {}\n{}'.format(type(exception).__name__, exception))
        return

    model = nifti_model.get_fdata()
    predicted_model = np.zeros_like(model, np.uint8)
    for slice_number in range(model.shape[2]):
        cur_slice = model[:, :, slice_number]
        predicted_slice = predict_on_image(keras_model, cur_slice)
        predicted_model[:, :, slice_number] = predicted_slice * 255

    predicted_nifti_model = nib.Nifti1Image(predicted_model, affine=nifti_model.affine, header=nifti_model.header)
    predicted_nifti_model.to_filename(str(nifti_predicted_model_path))


def predict_on_image(keras_model, image):
    resized_rect_image = image_utils.resized_padded_to_rect_image(image, 512)  #! 512 get from model layers input shape

    images = np.zeros((1, 512, 512, 1), dtype=np.float32)
    images[0, :, :, 0] = resized_rect_image / resized_rect_image.max()

    try:
        predictions = keras_model.predict(images)
    except Exception as exception:
        print('Keras prediction exception: {}\n{}'.format(type(exception).__name__, exception))
        return

    predicted_image = predictions[0, :, :, 0]

    # Resize |predicted_image| to size of original |image|
    original_nrows, original_ncols = image.shape
    original_max_size = max(original_nrows, original_ncols)
    predicted_image = image_utils.resized_image(predicted_image, original_max_size)
    predicted_image = predicted_image[0: original_nrows, 0: original_ncols]

    predicted_image[predicted_image < 0] = 0
    predicted_image[predicted_image > 1] = 1
    return predicted_image
