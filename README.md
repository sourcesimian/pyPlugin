pyPlugin <!-- omit in toc -->
===
***Simple framework-less plugin loader for Python***

A flexible, framework-less form of Python plugins. You write a base class
of whatever shape you wish and then derive your plugins from that class.
PluginLoader() simply returns references to all such classes found in the
one or more files which you specified. The rest is up to you.

- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)

# Installation
```
pip install pyPlugin
```

# Usage

A plugin module could look as follows, e.g.:
```
from MyModule import Parser

class Whatever(Parser):
    ...

class Another(Parser):
    ...
```

And the usage would be, e.g.:
```
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
```

# Contribution
Yes sure! And please. I built **mqtt-gpio** because I couldn't find an solution to with the same capabilities. I want it to be a project that is quick and easy to get up and running, and helps open up MQTT to anyone.

Before pushing a PR please ensure that `make check` and `make test` are clean and please consider adding unit tests.
