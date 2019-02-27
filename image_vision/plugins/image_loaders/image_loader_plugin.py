from core.plugin import Plugin


class ImageLoaderPlugin(Plugin):
    def __init__(self, loader_cls):
        super().__init__()

        self.loader_cls = loader_cls

        self.image_loader = None

    def install_core(self):
        super().install_core()

        self.image_loader = self.loader_cls()
