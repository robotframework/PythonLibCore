from robot.api import logger

from calculator import Calculator
from stringtools import StringTools
from waiter import Waiter


class HybridLibrary(Calculator, StringTools, Waiter):
    def __init__(self, separator: str = ";"):
        self.separator = separator

    def get_keyword_names(self):
        keywords = []
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, "robot_name"):
                keywords.append(name)
        return keywords
