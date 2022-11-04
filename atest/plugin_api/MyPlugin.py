from robot.api.deco import keyword  # noqa F401


class MyPlugin:

    @keyword
    def plugin_keyword(self):
        return 2
