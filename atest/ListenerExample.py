from robot.running.model import TestCase
from robot.result.model import TestCase as TestCaseResult

from robotlibcore import DynamicCore, keyword


class ListenerExample(DynamicCore):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        components = [KeywordsWithListener()]
        super().__init__(components)



class KeywordsWithListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.test = None


    def start_test(self, data: TestCase, result: TestCaseResult):
        self.test = data.name
        self.passed = result.passed

    @keyword
    def keyword_with_listener(self, name: str, status: bool):
        assert name == self.test, f"Test case name {name} does not match expected {self.test}"
        assert status == self.passed, f"Test case status {status} does not match expected {self.passed} {type(self.passed)}"
