from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool

import numpy as np
from PyQt5.QtCore import Qt, QEvent


class CropTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

    def eventFilter(self, watched_obj, e):
        if e.type() == QEvent.MouseButtonPress:
            self.on_mouse_pressed(e)
            return True
        else:
            return super().eventFilter(watched_obj, e)

    def on_mouse_pressed(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        if e.buttons() == Qt.LeftButton:
            image_coords = self.viewer.pos_to_image_coords(e.pos())
            self.crop_around(image_coords[0], image_coords[1])

    def crop_around(self, row, col):
        # x_center = self.viewer.image().data.shape[0] // 2
        # y_center = self.viewer.image().data.shape[1] // 2
        crop_row_center = row
        crop_col_center = col
        self.viewer.image().data = np.ascontiguousarray(self.viewer.image().data[
                                                        :,
                                                        crop_col_center - 1560:crop_col_center + 1560,
                                                        :])
        print('ssss', self.viewer.image().data.shape, self.viewer.image().data.dtype)
        self.viewer.mask().data = np.ascontiguousarray(self.viewer.mask().data[
                                                       :,
                                                       crop_col_center - 1560:crop_col_center + 1560,
                                                       :])
        self.viewer.update_scaled_combined_image()
