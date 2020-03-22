from typing import List, Union, NewType

from robot.api import logger
from selenium.webdriver.chrome.webdriver import WebDriver

from robotlibcore import DynamicCore, keyword

UserId = NewType('UserId', int)


class DynamicTypesAnnotationsLibrary(DynamicCore):

    def __init__(self, arg=None):
        DynamicCore.__init__(self, [])
        self.instance_attribute = 'not keyword'
        self.arg = arg

    @keyword
    def keyword_with_one_annotation(self, arg: str):
        return arg

    @keyword
    def keyword_with_multiple_annotations(self, arg1: str, arg2: List):
        return arg1, arg2

    @keyword
    def keyword_multiple_types(self, arg: Union[List, None]):
        return arg

    @keyword
    def keyword_new_type(self, arg: UserId):
        return arg

    @keyword
    def keyword_define_return_type(self, arg: str) -> None:
        logger.info(arg)
        return None

    @keyword
    def keyword_forward_references(self, arg: 'WebDriver'):
        return arg

    @keyword
    def keyword_with_annotations_and_default(self, arg: str = 'Foobar'):
        return arg

    @keyword
    def keyword_with_webdriver(self, arg: WebDriver):
        return arg

    @keyword
    def keyword_default_and_annotation(self, arg1: int, arg2=False) -> str:
        return '%s: %s, %s: %s' % (arg1, type(arg1), arg2, type(arg2))
