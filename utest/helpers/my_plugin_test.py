from robot.api.deco import keyword


class TestClass:

    @keyword
    def new_keyword(self, arg: int) -> int:
        return arg + self.not_keyword()

    def not_keyword(self):
        return 1


class LibraryBase:

    def __init__(self):
        self.x = 1

    def base(self):
        return 2


class TestClassWithBase(LibraryBase):

    @keyword
    def another_keyword(self) -> int:
        return 2 * 2

    def normal_method(self):
        return "xxx"
