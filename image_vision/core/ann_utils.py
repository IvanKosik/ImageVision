import nibabel as nib
import keras
from core import image_utils

from pahtlib import Path


def predict_on_nifti_model_slices(nifti_model_path: Path, keras_model_path: Path, nifti_predicted_model_path):
    nifti_model = nib.load(nifti_model_path)

    try:
        keras_model = keras.models.load_model(keras_model_path, compile=False)
    except Exception as exception:
        print('Keras model loading exception: {}\n{}'.format(type(exception).__name__, exception))
        return

    model = nifti_model.get_fdata()
    for slice_number in model.shape[2]:
        slice = model[:, :, slice_number]
        predict_on_image(slice)


def predict_on_image(image):
    pass
    '''
    image_utils.resized_image(image, max_size):

    row_pad = max(image.shape[1] - image.shape[0], 0)
    col_pad = max(image.shape[0] - image.shape[1], 0)
    image = np.pad(image, ((0, row_pad), (0, col_pad)), 'constant')
    image = cv2.resize(image, (512, 512), cv2.INTER_LANCZOS4)

    images = np.zeros((1, 512, 512, 1), dtype=np.float32)
    images[0, :, :, 0] = image / image.max()

    try:
        preds = self.model.predict(images)
    except Exception as exception:
        print('predict exception: ', type(exception).__name__)
        print(exception)
        return

    pred = preds[0, :, :, 0]
    # pred[pred < 0] = 0
    # pred[pred > 1] = 1
    # cv2.imwrite('pred.png', pred * 255)
    # print_image_info(pred)

    src_image_width = self.viewer.image().data.shape[0]
    src_image_height = self.viewer.image().data.shape[1]
    src_image_max_size = max(src_image_width, src_image_height)
    pred = cv2.resize(pred, (src_image_max_size, src_image_max_size), cv2.INTER_LANCZOS4)
    pred = pred[0: src_image_width, 0: src_image_height]

    print('s1', self.viewer.image().data.shape)
    print('s2', pred.shape)

    self.tool_mask.data = np.zeros(self.viewer.image().data.shape, np.uint8)
    self.tool_mask.data[np.where((pred > 0.5))] = settings.TOOL_FOREGROUND

    self.viewer.update_scaled_combined_image()
    '''