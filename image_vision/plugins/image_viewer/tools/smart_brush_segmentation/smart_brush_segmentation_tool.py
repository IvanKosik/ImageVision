from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool
from core import settings

from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from enum import Enum
import cv2
import numpy as np
from skimage.draw import circle


RADIUS = 22


class Mode(Enum):
    SHOW = 1
    DRAW = 2
    ERASE = 3


class SmartBrushSegmentationTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

        self.mode = Mode.SHOW

        self.radius = RADIUS

    def _activation(self):
        super()._activation()

        self.viewer.setMouseTracking(True)

    def _deactivation(self):
        super()._deactivation()

        self.viewer.setMouseTracking(False)

    def eventFilter(self, watched_obj, e):
        if e.type() == QEvent.MouseButtonPress:
            self.on_mouse_pressed(e)
            return True
        elif e.type() == QEvent.MouseMove:
            self.on_mouse_moved(e)
            return True
        elif e.type() == QEvent.MouseButtonRelease:
            self.on_mouse_released(e)
            return True
        elif e.type() == QEvent.Wheel and e.modifiers() == Qt.ControlModifier:
            self.on_cntrl_wheel_scrolled(e)
            return True
        else:
            return super().eventFilter(watched_obj, e)

    def update_mode(self, e):
        if e.buttons() == Qt.LeftButton:
            self.mode = Mode.DRAW
        elif e.buttons() == Qt.RightButton:
            self.mode = Mode.ERASE
        else:
            self.mode = Mode.SHOW

    def on_cntrl_wheel_scrolled(self, e):
        self.radius += e.angleDelta().y() / 10
        self.draw_brush_event(e)

    def on_mouse_pressed(self, e):
        self.draw_brush_event(e)

    def on_mouse_moved(self, e):
        self.draw_brush_event(e)

    def on_mouse_released(self, e):
        self.draw_brush_event(e)

    def draw_brush_event(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())
        self.update_mode(e)
        self.draw_brush(image_coords[0], image_coords[1])
        self.viewer.update_scaled_combined_image()

    def draw_brush(self, row, col):
        # Erase old tool mask
        self.tool_mask.data.fill(0)

        rr, cc = circle(row, col, self.radius, self.tool_mask.data.shape[:2])
        # self.tool_mask.data[rr, cc] = [0, 255, 0, 255]

        samples = self.viewer.image().data[rr, cc][:, 0]  # use only first channel
        samples = samples.astype(np.float32)
        number_of_clusters = 2
        if number_of_clusters > samples.size:
            return

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(samples, number_of_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        label = label.ravel()  # 2D array (one column) to 1D array without copy

        center_pixel_indexes = np.where(np.logical_and(rr == row, cc == col))[0]
        if center_pixel_indexes.size != 1:  # there are situations, when the center pixel is out of image
            return
        center_pixel_index = center_pixel_indexes[0]
        center_pixel_label = label[center_pixel_index]

        if self.mode == Mode.ERASE:
            self.tool_mask.data[rr, cc] = [255, 0, 0, 255]
        else:
            brush_circle = self.tool_mask.data[rr, cc]
            brush_circle[label == center_pixel_label] = settings.TOOL_FOREGROUND
            brush_circle[label != center_pixel_label] = settings.TOOL_BACKGROUND
            self.tool_mask.data[rr, cc] = brush_circle

        if self.mode == Mode.DRAW:
            brush_circle = self.viewer.mask().data[rr, cc]
            brush_circle[label == center_pixel_label] = settings.MASK_COLOR
            self.viewer.mask().data[rr, cc] = brush_circle
        elif self.mode == Mode.ERASE:
            self.viewer.mask().data[rr, cc] = settings.NO_MASK_COLOR
