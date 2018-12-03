from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool
import settings

from PyQt5.QtCore import Qt, QEvent
from skimage.draw import line, rectangle, polygon_perimeter
import numpy as np
import cv2


class GrabCutSegmentationTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

        self.bgd_model = None
        self.fgd_model = None

        self.last_mouse_pos = ()

        self.foreground_pixels = set()
        self.rect_rr = []
        self.rect_cc = []

        self.image_data = None

        self.temp_counter = 0

    def recreate_tool_mask(self):
        super().recreate_tool_mask()

        if not self.viewer.has_image():
            return

        self.image_data = self.viewer.image().data[:, :, :3]

        self.bgd_model = np.zeros((1, 65), np.float64)
        self.fgd_model = np.zeros((1, 65), np.float64)

        mask_pixels = np.where((self.viewer.mask().data == settings.MASK_COLOR).all(axis=2))
        self.tool_mask.data[mask_pixels] = settings.TOOL_FOREGROUND

        self.foreground_pixels.clear()
        for i in range(len(mask_pixels[0])):
            self.foreground_pixels.add((mask_pixels[0][i], mask_pixels[1][i]))

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
        self.last_mouse_pos = (image_coords[0], image_coords[1])

        if e.buttons() == Qt.LeftButton:
            self.tool_mask.data[image_coords[0], image_coords[1]] = settings.TOOL_FOREGROUND
            self.foreground_pixels.add((image_coords[0], image_coords[1]))
        elif e.buttons() == Qt.RightButton:
            self.tool_mask.data[image_coords[0], image_coords[1]] = settings.TOOL_BACKGROUND
            self.foreground_pixels.discard((image_coords[0], image_coords[1]))

    def on_mouse_moved(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())

        rr, cc = line(self.last_mouse_pos[0], self.last_mouse_pos[1], image_coords[0], image_coords[1])
        if e.buttons() == Qt.LeftButton:
            self.tool_mask.data[rr, cc] = settings.TOOL_FOREGROUND
            for i in range(len(rr)):
                self.foreground_pixels.add((rr[i], cc[i]))
        elif e.buttons() == Qt.RightButton:
            self.tool_mask.data[rr, cc] = settings.TOOL_BACKGROUND
            for i in range(len(rr)):
                self.foreground_pixels.discard((rr[i], cc[i]))
        self.last_mouse_pos = (image_coords[0], image_coords[1])

        if self.temp_counter % 5 == 0:
            self.mask_grab_cut()
        self.temp_counter += 1

        self.viewer.update_scaled_combined_image()

    def on_mouse_released(self, e):
        if not (self.viewer.has_image() and self.viewer.is_over_image(e.pos())):
            return

        image_coords = self.viewer.pos_to_image_coords(e.pos())

        self.mask_grab_cut()

        self.viewer.update_scaled_combined_image()

    def mask_grab_cut(self):
        # Erase old rectangle around foreground
        self.tool_mask.data[self.rect_rr, self.rect_cc] = settings.TOOL_NO_COLOR

        mask = np.zeros(self.viewer.image().data.shape[:2], np.uint8)

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
            self.tool_mask.data[self.rect_rr, self.rect_cc] = settings.TOOL_BACKGROUND

            # wherever it is marked white (sure foreground), change mask=1
            # wherever it is marked black (sure background), change mask=0
            rect_pad = pad - 1
            p_foreground_rect_rr, p_foreground_rect_cc = rectangle((min_r - rect_pad, min_c - rect_pad),
                                                                   end=(max_r + rect_pad, max_c + rect_pad),
                                                                   shape=self.tool_mask.data.shape[:2])
            mask[p_foreground_rect_rr, p_foreground_rect_cc] = 3

        # mask.fill(2)

        # print('before', mask.shape)
        # aaa = (self.viewer.tool_mask == [0, 128, 255, 255]).all(axis=2)
        # print(aaa.shape)
        # print(aaa)
        # print('bbb')
        mask[np.where((self.tool_mask.data == settings.TOOL_FOREGROUND).all(axis=2))] = 1
        mask[np.where((self.tool_mask.data == settings.TOOL_BACKGROUND).all(axis=2))] = 0
        # print('after')

        try:
            mask, self.bgd_model, self.fgd_model = cv2.grabCut(self.image_data, mask, None, self.bgd_model, self.fgd_model, 1, cv2.GC_INIT_WITH_MASK)
            # mask, self.bgd_model, self.fgd_model = cv2.grabCut(self.viewer.image, mask, None, self.bgd_model,
            #                                                    self.fgd_model, 5, cv2.GC_INIT_WITH_MASK)
        except:
            print('cv2.grabCut exception')

        self.viewer.mask().data[np.where(((mask == 1) | (mask == 3)))] = settings.MASK_COLOR
        self.viewer.mask().data[np.where(((mask == 0) | (mask == 2)))] = settings.NO_MASK_COLOR
        # cv2.GC_PR_BGD
        # cv2.GC_FGD
