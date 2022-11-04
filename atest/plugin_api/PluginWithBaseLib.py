from robot.api.deco import keyword  # noqa F401

from robotlibcore import DynamicCore, PluginParser


class BaseClass:
    def method(self):
        return 1


class PluginWithBaseLib(DynamicCore):

    def __init__(self, plugins):
        plugin_parser = PluginParser(BaseClass)
        parsed_plugins = plugin_parser.parse_plugins(plugins)
        self._plugin_keywords = plugin_parser.get_plugin_keywords(plugins)
        DynamicCore.__init__(self, parsed_plugins)

    @keyword
    def base_keyword(self):
        return "42"
