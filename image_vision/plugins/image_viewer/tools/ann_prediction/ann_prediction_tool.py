from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool
from core import settings

import keras
import tensorflow as tf
from keras.backend import flatten, sum, sigmoid
import numpy as np
import cv2
from tensorflow.python.tools import freeze_graph


SMOOTH = 1.


# or just 0.9 and 0.1
def binary_loss(y_true, y_pred):
    y = y_true
    pred = y_pred

    loss_map = tf.nn.sigmoid_cross_entropy_with_logits(logits=pred, labels=y)

    ones = tf.count_nonzero(y) / tf.reduce_prod(tf.shape(y, out_type=tf.int64))
    ones = tf.cast(ones, tf.float32)

    weight_map = (1 - ones) * y + (tf.ones_like(y) - y) * ones

    loss_map = tf.multiply(weight_map, loss_map)

    return tf.reduce_mean(loss_map)


def dice_coef_with_sigmoid(y_true, y_pred):
    y_true_f = flatten(y_true)
    y_pred_f = sigmoid(flatten(y_pred))
    intersection = sum(y_true_f * y_pred_f)
    return (2. * intersection + SMOOTH) / (sum(y_true_f) + sum(y_pred_f) + SMOOTH)


def dice_coef_loss(y_true, y_pred):
    return 1 - dice_coef_with_sigmoid(y_true, y_pred)


def bce_dice_loss(y_true, y_pred):
    return binary_loss(y_true, y_pred) + (dice_coef_loss(y_true, y_pred))


class AnnPredictionTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

        try:
            # self.model = keras.models.load_model('D:/Projects/MandibularNerve/Models/2018.11.16.Model_Los014_64size.h5',
            #                                      custom_objects={'bce_dice_loss': bce_dice_loss,
            #                                                      'dice_coef_with_sigmoid': dice_coef_with_sigmoid
            #                                                      }
            #                                 )  # DO it only ONE time
            self.model = keras.models.load_model('D:/Projects/BsAnn/Models/2018.11.26.Model_Loss025.h5', #2018.11.14.Model_594EditedSlices3_loss027.h5',
                                                 custom_objects={'bce_dice_loss': bce_dice_loss,
                                                                 'dice_coef_with_sigmoid': dice_coef_with_sigmoid
                                                                 }
                                            )  # DO it only ONE time

        except Exception as exception:
            print('model exception: ', type(exception).__name__)
            print(exception)
            return


        '''
        print('model name:', self.model.output.op.name)
        saver = tf.train.Saver()
        save_res = saver.save(keras.backend.get_session(), 'tmp/keras_model.ckpt')
        print('save_res', save_res)

        input_saver_def_path = ""
        input_binary = True
        output_node_names = self.model.output.op.name # [out.op.name for out in self.model.outputs]   #"'conv2d_19/BiasAdd'  #"output_node"
        restore_op_name = "save/restore_all"
        filename_tensor_name = "save/Const:0"
        clear_devices = False
        checkpoint_path = save_res #'tmp/keras_model.ckpt'
        input_meta_graph = checkpoint_path + ".meta"
        output_graph = 'tmp/out/keras_frozen.pb'

        # see example: https://github.com/tensorflow/tensorflow/blob/v1.12.0/tensorflow/python/tools/freeze_graph_test.py
        res = freeze_graph.freeze_graph(
            "", input_saver_def_path, input_binary, checkpoint_path,
            output_node_names, restore_op_name, filename_tensor_name,
            output_graph, clear_devices, "", "", "", input_meta_graph)

        # res = freeze_graph.freeze_graph(input_meta_graph='tmp/keras_model.ckpt.meta',
        #                                 input_checkpoint='tpm/keras_model.ckpt',
        #                                 output_graph='tmp/out/keras_frozen.pb',
        #                                 output_node_names='conv2d_19/BiasAdd',
        #                                 input_binary=True)
        print('res:', res)
        
        '''

    def recreate_tool_mask(self):
        super().recreate_tool_mask()

        if not self.viewer.has_image():
            return

        # self.predict_64()
        self.predict_lesions()

    def predict_64(self):
        print('Predict')

        image = self.viewer.image().data[:, :, 0]
        x_center = image.shape[0] // 2
        y_center = image.shape[1] // 2
        image = image[x_center - 32: x_center + 32, y_center - 32: y_center + 32]

        images = np.zeros((1, 64, 64, 1), dtype=np.float32)
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
        pred_empty = np.zeros((src_image_width, src_image_height), dtype=np.float32)
        pred_empty[x_center - 32: x_center + 32:, y_center - 32: y_center + 32:] = pred
        pred = pred_empty

        print('s1', self.viewer.image().data.shape)
        print('s2', pred.shape)

        self.tool_mask.data = np.zeros(self.viewer.image().data.shape, np.uint8)
        self.tool_mask.data[np.where((pred > 0.5))] = settings.TOOL_FOREGROUND

        self.viewer.update_scaled_combined_image()

    def predict_128(self):
        print('Predict')

        image = self.viewer.image().data[:, :, 0]
        row_pad = max(image.shape[1] - image.shape[0], 0)
        col_pad = max(image.shape[0] - image.shape[1], 0)
        image = np.pad(image, ((0, row_pad), (0, col_pad)), 'constant')
        image = cv2.resize(image, (128, 128), cv2.INTER_LANCZOS4)

        images = np.zeros((1, 128, 128, 1), dtype=np.float32)
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

    def predict_lesions(self):
        print('Predict Lesions')

        image = self.viewer.image().data[:, :, 0]
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
