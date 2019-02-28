from .plugin import Plugin

from typing import Type, List, get_type_hints


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def plugin(self, name):
        return self.plugins[name]

    '''
    def plugin(self, cls):
        if type(cls) is str:
            return self.plugins[cls]
        if type(cls) is Plugin:
            return self.plugins[cls.name()]
    '''

    def install_plugin(self, plugin_cls: Type[Plugin]):
        # Do nothing if plugin already installed
        if plugin_cls.name() in self.plugins:
            return self.plugins[plugin_cls.name()]

        print('before install required', plugin_cls)

        print('PLUGIN Req:', plugin_cls.required_plugins())

        import inspect
        signature = inspect.signature(plugin_cls.__init__)
        print('INSpect:', signature.parameters)
        fullargs = inspect.getfullargspec(plugin_cls.__init__)
        print('full', fullargs)
        print('args', fullargs.args)
        print('annot', fullargs.annotations)

        assert len(fullargs.annotations) == len(fullargs.args) - 1, 'Add annotations for plugin {}'.format(plugin_cls)  # minus 1 for |self| parameter

        '''
        
        print('INIT TYPES', plugin_cls.__init__.__annotations__)
        '''

        required_plugins = []

        # Install all required plugins
        # print('get_type_hints', get_type_hints(plugin_cls.__init__))
        annotations = plugin_cls.__init__.__annotations__
        # issubclass()

        for par_name, par_annotation in plugin_cls.__init__.__annotations__.items():
            print('CLS:', par_annotation)
            required_plugin = self.install_plugin(par_annotation)
            required_plugins.append(required_plugin)
        '''
        # Install all required plugins
        for required_plugin_cls in plugin_cls.required_plugin_classes:
            print('CLS:', required_plugin_cls)
            required_plugin = self.install_plugin(required_plugin_cls)
            required_plugins.append(required_plugin)
        '''

        print('before Create plugin instance', plugin_cls)
        # Create plugin instance
        plugin = plugin_cls(*required_plugins)
        print('after Create plugin instance', plugin_cls)

        '''
        # Install all required plugins
        for required_plugin_cls in plugin.required_plugin_classes():
            required_plugin = self.install_plugin(required_plugin_cls)

            # Remove plugin if any required plugin was removed
            # dep_plugin.removed.connect(plugin.remove)
        '''

        self.plugins[plugin.name()] = plugin
        print('befor install', plugin)
        plugin.install()
        print('return plugin', plugin)
        return plugin

    def install_plugins(self, plugin_classes: List[Type[Plugin]]):
        for plugin_cls in plugin_classes:
            self.install_plugin(plugin_cls)

    def remove_plugin(self, plugin_cls: Type[Plugin]):
        assert False
        pass
