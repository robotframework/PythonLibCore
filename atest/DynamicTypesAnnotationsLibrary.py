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

    @keyword
    def keyword_only_arguments(self, *varargs, some=111):
        return f'{varargs}: {type(varargs)}, {some}: {type(some)}'

    @keyword
    def keyword_only_arguments_no_default(self, *varargs, other):
        return f'{varargs}, {other}'

    @keyword
    def keyword_only_arguments_no_vararg(self, *, other):
        return f'{other}: {type(other)}'

    @keyword
    def keyword_only_arguments_many_positional_and_default(self, *varargs, one, two, three, four=True, five=None, six=False):
        return f'{varargs}, {one}, {two}, {three}, {four}, {five}, {six}'

    @keyword
    def keyword_only_arguments_default_and_no_default(self, *varargs, other, value=False):
        return f'{varargs}, {other}, {value}'

    @keyword
    def keyword_only_arguments_many(self, *varargs, some='value', other=None):
        return f'{some}: {type(some)}, {other}: {type(other)}, {varargs}: {type(varargs)}'

    @keyword
    def keyword_mandatory_and_keyword_only_arguments(self, arg: int, *vararg, some=True):
        return f'{arg}, {vararg}, {some}'

    @keyword
    def keyword_all_args(self, mandatory, positional=1, *varargs, other, value=False, **kwargs):
        return True
