from robot.api.deco import keyword  # noqa F401

from robotlibcore import DynamicCore, PluginParser


class PluginLib(DynamicCore):

    def __init__(self, plugins) -> None:
        plugin_parser = PluginParser()
        parsed_plugins = plugin_parser.parse_plugins(plugins)
        self._plugin_keywords = plugin_parser.get_plugin_keywords(plugins)
        DynamicCore.__init__(self, parsed_plugins)

    @keyword
    def foo(self):
        return 1
