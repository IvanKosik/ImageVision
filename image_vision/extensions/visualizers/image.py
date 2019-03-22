from core import Image

from .base import DataVisualizer
from extensions.mdi.windows import ImageViewerSubWindow
from extensions.viewers import ImageViewer


class ImageDataVisualizer(DataVisualizer):
    _DATA_TYPES = (Image, )

    def _visualize_data(self, data: Image):
        print('visualize image')

        image_viewer = ImageViewer(data)
        sub_window = ImageViewerSubWindow(image_viewer)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        return sub_window
