from enum import Enum
from functools import wraps
from typing import Dict, List, NewType, Optional, Tuple, Union

from robot.api import logger
from robotlibcore import DynamicCore, keyword

UserId = NewType('UserId', int)

penum = Enum("penum", "ok")


def _my_deco(old_args: Tuple[str, str], new_args: Tuple[str, str]):
    def actual_decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            for index, old_arg in enumerate(old_args):
                logger.warn(
                    f"{old_arg} has deprecated, use {new_args[index]}",
                )
            return method(*args, **kwargs)

        return wrapper

    return actual_decorator


class CustomObject:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class DynamicTypesAnnotationsLibrary(DynamicCore):

    def __init__(self, arg: str) -> None:
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
    def keyword_define_return_type(self, arg: str) -> Union[List[str], str]:
        logger.info(arg)
        return None

    @keyword
    def keyword_forward_references(self: 'DynamicTypesAnnotationsLibrary', arg: 'CustomObject'):
        return arg

    @keyword
    def keyword_with_annotations_and_default(self: 'DynamicTypesAnnotationsLibrary', arg: str = 'Foobar'):
        return arg

    @keyword
    def keyword_with_webdriver(self, arg: CustomObject):
        return arg

    @keyword
    def keyword_default_and_annotation(
            self: 'DynamicTypesAnnotationsLibrary',
            arg1: int,
            arg2: Union[bool, str] = False
    ) -> str:
        return '{}: {}, {}: {}'.format(arg1, type(arg1), arg2, type(arg2))

    @keyword(types={'arg': str})
    def keyword_robot_types_and_annotations(self: 'DynamicTypesAnnotationsLibrary', arg: int):
        return '{}: {}'.format(arg, type(arg))

    @keyword(types=None)
    def keyword_robot_types_disabled_and_annotations(self, arg: int):
        return '{}: {}'.format(arg, type(arg))

    @keyword(types={'arg1': str})
    def keyword_robot_types_and_bool_hint(self, arg1, arg2: bool):
        return '{}: {}, {}: {}'.format(arg1, type(arg1), arg2, type(arg2))

    @keyword
    def keyword_exception_annotations(
            self: 'DynamicTypesAnnotationsLibrary',
            arg: 'NotHere'  # noqa F821
    ):
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
    def keyword_only_arguments_many_positional_and_default(self: 'DynamicTypesAnnotationsLibrary', *varargs, one, two,
                                                           three, four: Union[int, str] = 1, five=None,
                                                           six: Union[bool, str] = False):
        return f'{varargs}, {one}, {two}, {three}, {four}, {five}, {six}'

    @keyword
    def keyword_only_arguments_default_and_no_default(self, *varargs, other, value=False):
        return f'{varargs}, {other}, {value}'

    @keyword
    def keyword_only_arguments_many(self, *varargs, some='value', other=None):
        return f'{some}: {type(some)}, {other}: {type(other)}, {varargs}: {type(varargs)}'

    @keyword
    def keyword_mandatory_and_keyword_only_arguments(self, arg: int, *vararg, some: bool):
        return f'{arg}, {vararg}, {some}'

    @keyword
    def keyword_all_args(
            self: 'DynamicTypesAnnotationsLibrary',
            mandatory,
            positional=1,
            *varargs,
            other,
            value=False,
            **kwargs
    ):
        return True

    @keyword
    def keyword_self_and_types(self: 'DynamicTypesAnnotationsLibrary', mandatory: str, *varargs, other: bool, **kwargs):
        return True

    @keyword
    def keyword_self_and_keyword_only_types(
            x: 'DynamicTypesAnnotationsLibrary',  # noqa: N805
            mandatory,
            *varargs: int,
            other: bool,
            **kwargs: int
        ):
        return (f'{mandatory}: {type(mandatory)}, {varargs}: {type(varargs)}, '
                f'{other}: {type(other)}, {kwargs}: {type(kwargs)}')

    @keyword
    def enum_conversion(self, param: Optional[penum] = None):
        logger.info(f'OK {param}')
        logger.info(param.ok)
        return f'OK {param}'

    @keyword
    @_my_deco(old_args=("arg1", ), new_args=("arg2", ))
    def keyword_with_deco_and_signature(self, arg1: bool = False, arg2: bool = False):
        """Test me doc here"""
        return f"{arg1}: {type(arg1)}, {arg2}: {type(arg2)}"

    @keyword
    def keyword_optional_with_none(self, arg: Optional[str] = None):
        return f"arg: {arg}, type: {type(arg)}"

    @keyword
    def keyword_union_with_none(self, arg: Union[None, Dict, str] = None):
        return f"arg: {arg}, type: {type(arg)}"

    @keyword
    def kw_with_named_arguments(self, *, arg):
        print(arg)
        return f"arg: {arg}, type: {type(arg)}"

    @keyword
    def kw_with_many_named_arguments(self, *, arg1, arg2):
        print(arg1)
        print(arg2)
        return f"arg1: {arg1}, type: {type(arg1)}, arg2: {arg2}, type: {type(arg2)}"

    @keyword
    def kw_with_named_arguments_and_variable_number_args(self, *varargs, arg):
        print(arg)
        return f"arg: {arg}, type: {type(arg)}"

    @keyword
    def kw_with_many_named_arguments_with_default(self, *, arg1, arg2: int):
        print(arg1)
        print(arg2)
        return f"arg1: {arg1}, type: {type(arg1)}, arg2: {arg2}, type: {type(arg2)}"

    @keyword
    def kw_with_positional_and_named_arguments(self, arg1, *, arg2: int):
        return f"arg1: {arg1}, type: {type(arg1)}, arg2: {arg2}, type: {type(arg2)}"

    @keyword
    def kw_with_positional_and_named_arguments_with_defaults(self, arg1: int = 1, *, arg2: str = "foobar"):
        return f"arg1: {arg1}, type: {type(arg1)}, arg2: {arg2}, type: {type(arg2)}"

