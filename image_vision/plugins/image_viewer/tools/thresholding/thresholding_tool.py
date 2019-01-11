from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool
from core import settings

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QFormLayout
import numpy as np


class ThresholdingTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

        self.tool_settings_widget = None

    def _activation(self):
        super()._activation()

        self.tool_settings_widget = QWidget()

        threshold_value_slider = QSlider(Qt.Horizontal)
        threshold_value_slider.setMinimum(0)
        threshold_value_slider.setMaximum(255)
        threshold_value_slider.valueChanged.connect(self.threshold)

        form_layout = QFormLayout()
        form_layout.addRow(self.tr('Threshold Value:'), threshold_value_slider)
        self.tool_settings_widget.setLayout(form_layout)

        self.tool_settings_widget.show()

    def _deactivation(self):
        super()._deactivation()

    def threshold(self, value):
        print(value)

        image = self.viewer.image().data[:, :, 0]

        self.tool_mask.data.fill(0)
        self.tool_mask.data[np.where(image < value)] = settings.TOOL_BACKGROUND

        self.viewer.update_scaled_combined_image()
