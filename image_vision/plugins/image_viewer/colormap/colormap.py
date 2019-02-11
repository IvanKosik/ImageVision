from core import settings

from PyQt5.Qt import QColor

import numpy as np


class Colormap:
    def __init__(self):
        self.lut = np.zeros((10, 4), np.uint8)
        self.lut[settings.NO_MASK_CLASS] = settings.NO_MASK_COLOR
        self.lut[settings.MASK_CLASS] = settings.MASK_COLOR
        self.lut[settings.TOOL_BACKGROUND_CLASS] = settings.TOOL_BACKGROUND
        self.lut[settings.TOOL_FOREGROUND_CLASS] = settings.TOOL_FOREGROUND
        self.lut[settings.TOOL_ERASER_CLASS] = settings.TOOL_ERASER
        self.lut[settings.TOOL_NO_COLOR_CLASS] = settings.TOOL_NO_COLOR

    def set_class_color(self, class_number: int, color: QColor):
        self.lut[class_number] = [color.red(), color.green(), color.blue(), color.alpha()]
