from robot.api.deco import keyword  # noqa F401

from PluginWithBaseLib import BaseClass


class MyPluginBase(BaseClass):

    def __init__(self, arg) -> None:
        self.arg = int(arg)

    @keyword
    def base_plugin_keyword(self):
        return 40 + self.arg
