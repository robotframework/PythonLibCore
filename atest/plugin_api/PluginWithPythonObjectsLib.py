from robot.api.deco import keyword  # noqa F401

from robotlibcore import DynamicCore, PluginParser


class BaseWithPython:
    def __init__(self, py1, py2):
        self.py1 = py1
        self.py2 = py2


class PluginWithPythonObjectsLib(DynamicCore):

    def __init__(self, plugins):
        plugin_parser = PluginParser(BaseWithPython, [8, 9])
        parsed_plugins = plugin_parser.parse_plugins(plugins)
        self._plugin_keywords = plugin_parser.get_plugin_keywords(plugins)
        DynamicCore.__init__(self, parsed_plugins)

    @keyword
    def keyword_with_python(self):
        return "123"
