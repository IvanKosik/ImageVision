from core import settings

from core.image import Image
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class ImageViewerTool(QObject):
    before_activation = pyqtSignal(object)
    activated = pyqtSignal(object)
    deactivated = pyqtSignal(object)

    def __init__(self, viewer, parent=None):
        super().__init__(parent)

        # self.type = tool_type

        self.viewer = viewer

        self.tool_mask = None
        self.tool_mask_layer = None

    @classmethod
    def name(cls):
        return cls.__name__

    def activate(self):
        self.before_activation.emit(self)

        print('activate tool', self.name())

        self._activation()

        self.activated.emit(self)

    def _activation(self):
        self.tool_mask_layer = self.viewer.add_layer('Tool Mask')
        self.recreate_tool_mask()
        self.viewer.update_scaled_combined_image()

        self.viewer.installEventFilter(self)

        self.viewer.before_image_changed.connect(self.on_before_viewer_image_changed)
        self.viewer.image_changed.connect(self.on_viewer_image_changed)

    def deactivate(self):
        print('deactivate tool', self.name())

        self._deactivation()

        self.deactivated.emit(self)

    def _deactivation(self):
        self.viewer.image_changed.disconnect(self.on_viewer_image_changed)
        self.viewer.before_image_changed.disconnect(self.on_before_viewer_image_changed)

        self.viewer.removeEventFilter(self)

        self.tool_mask = None
        self.viewer.remove_layer(self.tool_mask_layer)
        self.tool_mask_layer = None

    def on_before_viewer_image_changed(self):
        pass

    def on_viewer_image_changed(self):
        self.recreate_tool_mask()

    def recreate_tool_mask(self):
        if not self.viewer.has_image():
            return

        tool_mask_data = np.full((self.viewer.image().data.shape[0], self.viewer.image().data.shape[1]),
                                 settings.TOOL_NO_COLOR_CLASS, np.uint8)
        if self.tool_mask is None:
            self.tool_mask = Image(tool_mask_data)
            self.tool_mask_layer.image = self.tool_mask
        else:
            self.tool_mask.data = tool_mask_data
