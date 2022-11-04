from robot.api.deco import keyword  # noqa F401

from PluginWithBaseLib import BaseClass


class MyPluginBase(BaseClass):

    @keyword
    def base_plugin_keyword(self):
        return "40"
