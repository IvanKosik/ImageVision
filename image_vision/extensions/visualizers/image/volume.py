from core import VolumeImage

from .base import ImageVisualizer
from extensions.mdi.windows import ImageViewerSubWindow
from extensions.viewers import SliceImageViewer


class VolumeImageVisualizer(ImageVisualizer):
    _DATA_TYPES = (VolumeImage, )

    def _visualize_data(self, data: VolumeImage):
        print('visualize flat image')

        image_viewer = SliceImageViewer(data)
        sub_window = ImageViewerSubWindow(image_viewer)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        return sub_window
