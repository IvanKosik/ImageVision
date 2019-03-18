from core import Image

from .base import DataVisualizer
from extensions.mdi.windows import ImageSubWindow
from extensions.viewers import ImageViewer


class ImageDataVisualizer(DataVisualizer):
    _DATA_TYPES = (Image, )

    def _visualize_data(self, data: Image):
        print('visualize image')
        sub_window = ImageSubWindow()
        sub_window.setWidget(ImageViewer(data))
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
