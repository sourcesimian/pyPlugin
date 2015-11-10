import glob
import inspect
import sys
import os


class PluginLoader(object):
    """
    Simple framework-less plugin loader for Python

        https://github.com/sourcesimian/pyPlugin

    A flexible, framework-less form of Python plugins. You write a base class
    of whatever shape you wish and then derive your plugins from that class.
    PluginLoader() simply returns references to all such classes found in the
    one or more files which you specified. The rest is up to you.


    So a plugin module would look as follows, e.g.:
        from MyModule import Parser

        class Whatever(Parser):
            ...

        class Another(Parser):
            ...

    And the usage would be, e.g.:
        from pyplugin import PluginLoader
        ...

        class ParserBase(object):
            # whatever base class you wish to define
            def visit(self, bar):
                pass
        ...

        # Build myself a virtual module
        import types
        vmodule = types.ModuleType('MyModule')
        vmodule.Parser = ParserBase

        # Get all of my Parser plugin classes from my plugin_dir
        path = os.path.join(plugin_dir, '*.py')
        plugins = PluginLoader(ParserBase, [path], [vmodule])

        # Initialise my Parser classes, if that is what I want to do
        parsers = [cls(foo) for cls in plugins]
        ...

        # Visit all of my plugins, for example
        for p in parsers:
            p.visit(bar)
    """
    def __init__(self, base_class, filespecs, import_modules=None):
        """
        base_class     : all classes that are derived from <base_class> will be found
        filespecs      : path or file glob expressions to select files to scan
        import_modules : list of references to additional modules that will be
                         available for import when the plugin module is loaded.
        """
        import_modules = import_modules or []

        import_modules = import_modules if isinstance(import_modules, (list, tuple)) else (import_modules,)
        filespecs = filespecs if isinstance(filespecs, (list, tuple)) else (filespecs,)

        self.__base_class = base_class
        self.__import_modules = import_modules

        from itertools import chain
        files = list(chain(*[glob.glob(f) for f in filespecs]))

        self.__plugins = self.__load_child_classes(files)

    def __iter__(self):
        """
        Iterate references to the classes found when the class was initialised
        """
        for plugin_cls in self.__plugins:
            yield plugin_cls

    def __load_child_classes(self, files):
        try:
            self.__push_import_modules()
            child_classes = []
            for file in files:
                child_classes.extend(self.__find_child_classes(file))
        finally:
            self.__pop_import_modules()

        return child_classes

    def __push_import_modules(self):
        """
        Add custom <import_modules> to the import namespace under its own __name__.
        """
        for module in self.__import_modules:
            sys.modules[module.__name__] = module

    def __pop_import_modules(self):
        for module in self.__import_modules:
            del sys.modules[module.__name__]

    def __find_child_classes(self, file):
        """
        Return a list of all <__base_class> based classes found in <file>
        """

        child_classes = []
        folder, name = os.path.split(file)
        name = os.path.splitext(name)[0]

        import imp
        module = imp.load_source(name, file)

        def filter_classes(m):
            if inspect.isclass(m):
                if inspect.getmro(m)[1] == self.__base_class:
                    return True
            return False

        for name, obj in inspect.getmembers(module, filter_classes):
            child_classes.append(obj)

        return child_classes
