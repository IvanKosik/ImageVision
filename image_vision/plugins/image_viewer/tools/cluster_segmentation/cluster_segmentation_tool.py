from plugins.image_viewer.tools.image_viewer_tool import ImageViewerTool
from core import settings

from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from enum import Enum
import cv2
import numpy as np


class ClusterSegmentationTool(ImageViewerTool):
    def __init__(self, viewer, parent=None):
        super().__init__(viewer, parent)

        self.number_of_clusters = 3

        self.cluster_clusses = [settings.TOOL_BACKGROUND_CLASS,
                                settings.TOOL_FOREGROUND_CLASS,
                                settings.TOOL_ERASER_CLASS,
                                settings.TOOL_BACKGROUND_2_CLASS]

    def eventFilter(self, watched_obj, event):
        if event.type() == QEvent.MouseButtonPress:
            self.on_mouse_pressed(event)
            return True
        else:
            return super().eventFilter(watched_obj, event)

    def on_mouse_pressed(self, event):
        self.clustering(event)

    def clustering(self, event):
        clustered_indexes = self.viewer.mask().data == self.mask_class
        samples = self.viewer.image().data[clustered_indexes][:, 0]  # use only first channel
        samples = samples.astype(np.float32)

        if self.number_of_clusters > samples.size:
            return

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, centers = cv2.kmeans(samples, self.number_of_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        label = label.ravel()  # 2D array (one column) to 1D array without copy
        centers = centers.ravel()
        print(label)

        pixels = self.tool_mask.data[clustered_indexes]
        for l in label:
            pixels[label == l] = self.cluster_clusses[l]

        self.tool_mask.data[clustered_indexes] = pixels

        self.viewer.update_scaled_combined_image()
