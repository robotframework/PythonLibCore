from typing import List, Union, NewType

from robot.api import logger

from robotlibcore import DynamicCore, keyword

UserId = NewType('UserId', int)


class CustomObject(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class DynamicTypesAnnotationsLibrary(DynamicCore):

    def __init__(self, arg: str):
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
    def keyword_forward_references(self, arg: 'CustomObject'):
        return arg

    @keyword
    def keyword_with_annotations_and_default(self, arg: str = 'Foobar'):
        return arg

    @keyword
    def keyword_with_webdriver(self, arg: CustomObject):
        return arg

    @keyword
    def keyword_default_and_annotation(self, arg1: int, arg2=False) -> str:
        return '%s: %s, %s: %s' % (arg1, type(arg1), arg2, type(arg2))

    @keyword(types={'arg': str})
    def keyword_robot_types_and_annotations(self, arg: int):
        return '%s: %s' % (arg, type(arg))

    @keyword(types=None)
    def keyword_robot_types_disabled_and_annotations(self, arg: int):
        return '%s: %s' % (arg, type(arg))

    @keyword(types={'arg1': str})
    def keyword_robot_types_and_bool_defaults(self, arg1, arg2=False):
        return '%s: %s, %s: %s' % (arg1, type(arg1), arg2, type(arg2))

    @keyword
    def keyword_exception_annotations(self, arg: 'NotHere'):
        return arg
