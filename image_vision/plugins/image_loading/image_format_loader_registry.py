class ImageFormatLoaderRegistry:
    def __init__(self):
        super().__init__()

        self._registry = {}

    def register_loader_cls(self, loader_cls):
        for image_format in loader_cls.formats:
            assert image_format not in self._registry, 'Duplicate format of image loader'
            self._registry[image_format] = loader_cls

    def unregister_loader_cls(self, loader_cls):
        for image_format in loader_cls.formats:
            assert self._registry[image_format] == loader_cls, 'Format registered for other image loader'
            del self._registry[image_format]

    def loader_cls(self, image_format):
        return self._registry[image_format]

    def contains_format(self, image_format) -> bool:
        return image_format in self._registry
