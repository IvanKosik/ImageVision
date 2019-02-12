from core.image import Image


class ImageLayer:
    max_id = 0

    def __init__(self, name='', image: Image = None, visible=True, opacity=1):
        self.id = ImageLayer.max_id
        ImageLayer.max_id += 1

        self.name = name if name else 'Layer ' + str(self.id)
        self.image = image #if image is not None else Image()
        self.visible = visible
        self.opacity = opacity
