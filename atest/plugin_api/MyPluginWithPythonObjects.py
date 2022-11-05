from robot.api.deco import keyword  # noqa F401

from PluginWithPythonObjectsLib import BaseWithPython


class MyPluginWithPythonObjects(BaseWithPython):

    def __init__(self, py1, py2, rf1, rf2):
        self.rf1 = int(rf1)
        self.rf2 = int(rf2)
        super().__init__(py1, py2)

    @keyword
    def plugin_keyword_with_python(self):
        return self.rf1 + self.rf2 + self.py1 + self.py2
