from core import FlatImage

from .base import ImageVisualizer
from extensions.mdi.windows import ImageViewerSubWindow
from extensions.viewers import FlatImageViewer


class FlatImageVisualizer(ImageVisualizer):
    _DATA_TYPES = (FlatImage, )

    def _visualize_data(self, data: FlatImage):
        print('visualize flat image')

        image_viewer = FlatImageViewer(data)
        sub_window = ImageViewerSubWindow(image_viewer)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        return sub_window
