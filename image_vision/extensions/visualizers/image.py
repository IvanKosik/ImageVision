from core import Image

from .base import DataVisualizer
from extensions.mdi.windows import ImageSubWindow
from plugins.image_viewer.image_viewer import ImageViewer    #%% transfer to extensions


class ImageDataVisualizer(DataVisualizer):
    _DATA_TYPES = (Image, )

    def _visualize_data(self, data: Image):
        print('visualize image')
        sub_window = ImageSubWindow()
        sub_window.setWidget(ImageViewer(None))
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
