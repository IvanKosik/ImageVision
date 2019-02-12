from core import settings

from PyQt5.Qt import QColor
from PyQt5.QtCore import QObject, pyqtSignal

import numpy as np


class Colormap(QObject):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.lut = np.zeros((11, 4), np.uint8)
        self.lut[settings.NO_MASK_CLASS] = settings.NO_MASK_COLOR
        self.lut[settings.MASK_CLASS] = settings.MASK_COLOR
        self.lut[settings.TOOL_BACKGROUND_CLASS] = settings.TOOL_BACKGROUND
        self.lut[settings.TOOL_FOREGROUND_CLASS] = settings.TOOL_FOREGROUND
        self.lut[settings.TOOL_ERASER_CLASS] = settings.TOOL_ERASER
        self.lut[settings.TOOL_NO_COLOR_CLASS] = settings.TOOL_NO_COLOR

        self.lut[6] = [255, 90, 90, 80]
        self.lut[7] = [90, 90, 255, 80]
        self.lut[8] = [120, 180, 255, 80]
        self.lut[9] = [255, 120, 180, 80]
        self.lut[10] = [120, 255, 180, 80]

        '''
        self.lut = np.array([settings.NO_MASK_COLOR,
                             settings.MASK_COLOR,
                             settings.TOOL_BACKGROUND,
                             settings.TOOL_FOREGROUND,
                             settings.TOOL_ERASER,
                             settings.TOOL_NO_COLOR])
        '''

    def set_class_color(self, class_number: int, color: QColor):
        color_array = [color.red(), color.green(), color.blue(), color.alpha()]
        if (self.lut[class_number] != color_array).any():
            self.lut[class_number] = color_array
            self.changed.emit()

    def colored_image(self, image):
        return self.lut[image]
