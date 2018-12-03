import settings

from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtCore import Qt

import cv2
import numpy as np
from skimage.draw import rectangle, polygon_perimeter, line


class GrabCutBrushToolInteractor(QObject):

    def __init__(self, viewer, parent=None):
        super().__init__(parent)

        self.viewer = viewer
        # self.mode = Mode.SHOW

        self.rect_start = ()
        self.rect_end = ()

        self.c = 0
        self.bgd_model = np.zeros((1, 65), np.float64)
        self.fgd_model = np.zeros((1, 65), np.float64)
        self.m_pos = ()

        self.foreground_pixels = set()
        self.rect_rr = []
        self.rect_cc = []

        ### self.viewer.tool_mask_cleared.connect(self.on_tool_mask_cleared)

    def on_tool_mask_cleared(self):
        self.foreground_pixels = set()
        self.rect_rr = []
        self.rect_cc = []

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
        else:
            return super().eventFilter(watched_obj, e)

    def on_mouse_pressed(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())
        self.rect_start = (image_coords[0], image_coords[1])
        self.m_pos = (image_coords[0], image_coords[1])

        if e.buttons() == Qt.LeftButton:
            self.viewer.tool_mask[image_coords[0], image_coords[1]] = [0, 128, 255, 255]
            self.foreground_pixels.add((image_coords[0], image_coords[1]))
        elif e.buttons() == Qt.RightButton:
            self.viewer.tool_mask[image_coords[0], image_coords[1]] = [255, 0, 0, 255]
            self.foreground_pixels.discard((image_coords[0], image_coords[1]))

    def on_mouse_moved(self, e):
        if not self.rect_start:
            return

        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())
        # self.draw_rect(image_coords[0], image_coords[1])

        rr, cc = line(self.m_pos[0], self.m_pos[1], image_coords[0], image_coords[1])
        if e.buttons() == Qt.LeftButton:
            self.viewer.tool_mask[rr, cc] = [0, 128, 255, 255]
            for i in range(len(rr)):
                self.foreground_pixels.add((rr[i], cc[i]))
        elif e.buttons() == Qt.RightButton:
            self.viewer.tool_mask[rr, cc] = [255, 0, 0, 255]
            for i in range(len(rr)):
                self.foreground_pixels.discard((rr[i], cc[i]))
        self.m_pos = (image_coords[0], image_coords[1])

        self.mask_grab_cut()

        self.viewer.update_scaled_combined_image()

    def draw_rect(self, row, col):
        rr, cc = rectangle(self.rect_start, end=(row, col), shape=self.viewer.tool_mask.shape[:2])
        self.viewer.tool_mask[rr, cc] = [255, 0, 0, 255]

    def on_mouse_released(self, e):
        if not self.rect_start:
            return

        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())
        self.rect_end = (image_coords[0], image_coords[1])

        # self.grab_cut()
        # if self.c == 1:

        self.mask_grab_cut()

        # self.grab_cut()
        # self.c = 1

        self.rect_start = ()
        # self.draw_brush_event(e)

        # Erase tool mask
        # self.viewer.tool_mask.fill(0)

        self.viewer.update_scaled_combined_image()

    def mask_grab_cut(self):
        print('mask_grab_cut')

        # Erase old rectangle around foreground
        self.viewer.tool_mask[self.rect_rr, self.rect_cc] = [0, 0, 0, 0]

        mask = np.zeros(self.viewer.image.shape[:2], np.uint8)

        # Draw rectangle around foreground lines
        if self.foreground_pixels:
            min_r = min(self.foreground_pixels, key=lambda p: p[0])[0]
            min_c = min(self.foreground_pixels, key=lambda p: p[1])[1]
            max_r = max(self.foreground_pixels, key=lambda p: p[0])[0]
            max_c = max(self.foreground_pixels, key=lambda p: p[1])[1]
            # rr, cc = rectangle((min_x, min_y), end=(max_x, max_y), shape=self.viewer.tool_mask.shape[:2])
            pad = 2
            self.rect_rr, self.rect_cc = polygon_perimeter([min_r - pad, min_r - pad, max_r + pad, max_r + pad],
                                                           [min_c - pad, max_c + pad, max_c + pad, min_c - pad])
            self.viewer.tool_mask[self.rect_rr, self.rect_cc] = settings.TOOL_BACKGROUND

            # wherever it is marked white (sure foreground), change mask=1
            # wherever it is marked black (sure background), change mask=0
            rect_pad = pad - 1
            p_foreground_rect_rr, p_foreground_rect_cc = rectangle((min_r - rect_pad, min_c - rect_pad),
                                                                   end=(max_r + rect_pad, max_c + rect_pad),
                                                                   shape=self.viewer.tool_mask.shape[:2])
            mask[p_foreground_rect_rr, p_foreground_rect_cc] = 3

        # mask.fill(2)

        # print('before', mask.shape)
        # aaa = (self.viewer.tool_mask == [0, 128, 255, 255]).all(axis=2)
        # print(aaa.shape)
        # print(aaa)
        # print('bbb')
        mask[np.where((self.viewer.tool_mask == settings.TOOL_FOREGROUND).all(axis=2))] = 1
        mask[np.where((self.viewer.tool_mask == settings.TOOL_BACKGROUND).all(axis=2))] = 0
        print(np.unique(mask))
        # print('after')
        try:
            mask, self.bgd_model, self.fgd_model = cv2.grabCut(self.viewer.image, mask, None, self.bgd_model, self.fgd_model, 1, cv2.GC_INIT_WITH_MASK)
            # mask, self.bgd_model, self.fgd_model = cv2.grabCut(self.viewer.image, mask, None, self.bgd_model,
            #                                                    self.fgd_model, 5, cv2.GC_INIT_WITH_MASK)
        except:
            print('exception')
        print(np.unique(mask))

        self.viewer.mask[np.where(((mask == 1) | (mask == 3)))] = settings.MASK_COLOR
        self.viewer.mask[np.where(((mask == 0) | (mask == 2)))] = settings.NO_MASK_COLOR

    def grab_cut(self):
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        mask = np.zeros(self.viewer.image.shape[:2], np.uint8)
        print(mask.shape)
        rect_width = self.rect_end[1] - self.rect_start[1]
        rect_height = self.rect_end[0] - self.rect_start[0]
        rect = (self.rect_start[1], self.rect_start[0], rect_width, rect_height)
        print(rect)
        try:
            cv2.grabCut(self.viewer.image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        except:
            print('exception grabCut')
        # cv2.GC_PR_BGD
        # cv2.GC_FGD
        # print(np.where((mask == 2) | (mask == 0)))
        # self.viewer.mask = np.where((mask == 2) | (mask == 0), settings.MASK_COLOR)
        #
        # print(mask)
        # print(mask.shape)

        # mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
        self.viewer.mask[np.where(((mask == 1) | (mask == 3)))] = settings.MASK_COLOR
        self.viewer.mask[np.where(((mask == 0) | (mask == 2)))] = settings.NO_MASK_COLOR

        # self.viewer.mask = np.where((mask == 1) | (mask == 3), settings.MASK_COLOR, settings.NO_MASK_COLOR)

        # mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        # img = img * mask2[:, :, np.newaxis]

    def draw_brush_event(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())
        self.update_mode(e)
        self.draw_brush(image_coords[0], image_coords[1])
        self.viewer.update_scaled_combined_image()

    def draw_brush(self, row, col):
        # Erase old tool mask
        self.viewer.tool_mask.fill(0)

        rr, cc = circle(row, col, 22, self.viewer.tool_mask.shape)
        # self.tool_mask[rr, cc] = [0, 255, 0, 255]

        samples = self.viewer.image[rr, cc][:, 0]  # use only first channel
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
            self.viewer.tool_mask[rr, cc] = [0, 0, 255, 255]
        else:
            brush_circle = self.viewer.tool_mask[rr, cc]
            brush_circle[label == center_pixel_label] = [0, 128, 255, 255]
            brush_circle[label != center_pixel_label] = [255, 0, 0, 255]
            self.viewer.tool_mask[rr, cc] = brush_circle

        if self.mode == Mode.DRAW:
            brush_circle = self.viewer.mask[rr, cc]
            brush_circle[label == center_pixel_label] = settings.MASK_COLOR
            self.viewer.mask[rr, cc] = brush_circle
        elif self.mode == Mode.ERASE:
            self.viewer.mask[rr, cc] = [0, 0, 0, 0]