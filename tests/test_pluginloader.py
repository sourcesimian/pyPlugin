from unittest import TestCase

import os


class ParserBaseVirtual(object):
    def visit(self, bar):
        pass


class TestPluginLoader(TestCase):
    def test_static_module(self):
        from pyplugin import PluginLoader
        from base import Parser1

        plugin_dir = os.path.dirname(__file__)

        path = os.path.join(plugin_dir, 'plugins1.py')
        plugins = PluginLoader(Parser1, path)

        parsers = [cls() for cls in plugins]
        self.assertEqual(1, len(parsers))

        for p in parsers:
            self.assertEqual('bar', p.visit('tea?'))

    def test_virtual_module(self):
        from pyplugin import PluginLoader

        plugin_dir = os.path.dirname(__file__)

        import types
        vmodule = types.ModuleType('VModule')
        vmodule.Parser2 = ParserBaseVirtual

        path = os.path.join(plugin_dir, 'plugins2.py')
        plugins = PluginLoader(ParserBaseVirtual, path, vmodule)

        parsers = [cls() for cls in plugins]
        self.assertEqual(1, len(parsers))

        for p in parsers:
            p.handle('door?')

    def test_common_name(self):
        from pyplugin import PluginLoader
        from base import Parser1

        plugin_dir = os.path.dirname(__file__)

        path = os.path.join(plugin_dir, 'time.py')
        plugins = PluginLoader(Parser1, path)

        parsers = [cls() for cls in plugins]
        self.assertEqual(1, len(parsers))

        for p in parsers:
            self.assertEqual('tock', p.tick())
