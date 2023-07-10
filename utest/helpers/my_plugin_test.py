from robot.api.deco import keyword


class TestClass:

    @keyword
    def new_keyword(self, arg: int) -> int:
        return arg + self.not_keyword()

    def not_keyword(self):
        return 1


class LibraryBase:

    def __init__(self) -> None:
        self.x = 1

    def base(self):
        return 2


class TestClassWithBase(LibraryBase):

    @keyword
    def another_keyword(self) -> int:
        return 2 * 2

    def normal_method(self):
        return "xxx"


class TestPluginWithPythonArgs(LibraryBase):

    def __init__(self, python_class, rf_arg) -> None:
        self.python_class = python_class
        self.rf_arg = rf_arg
        super().__init__()

    @keyword
    def include_python_object(self):
        return self.python_class.x + self.python_class.y + int(self.rf_arg)
