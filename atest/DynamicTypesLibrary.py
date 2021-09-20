import functools
import sys

from robot import version as rf_version

from robotlibcore import DynamicCore, keyword


def def_deco(func):
    return func


def deco_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class DynamicTypesLibrary(DynamicCore):

    def __init__(self, arg=False):
        DynamicCore.__init__(self, [])
        self.instance_attribute = 'not keyword'
        self.arg = arg

    @keyword(types={'arg1': str})
    def keyword_with_types(self, arg1):
        return arg1

    @keyword(types={'arg1': str})
    def keyword_robot_types_and_bool_default(self, arg1, arg2=False):
        return arg1, arg2

    @keyword(types=None)
    def keyword_with_disabled_types(self, arg1):
        return arg1

    @keyword(types={'arg1': str})
    def keyword_with_one_type(self, arg1, arg2):
        return arg1, arg2

    @keyword
    def keyword_with_no_args(self):
        return False

    def not_keyword(self):
        return False

    @keyword
    def keyword_default_types(self, arg=None):
        return arg

    @keyword
    def keyword_many_default_types(self, arg1=1, arg2='Foobar'):
        return arg1, arg2

    @keyword
    def keyword_none(self, arg=None):
        return '{}: {}'.format(arg, type(arg))

    @keyword
    def is_python_3_10(self):
        return sys.version_info >= (3, 10)

    @keyword
    def is_rf_401(self):
        return "4.0." in rf_version.VERSION

    @keyword
    @def_deco
    def keyword_with_def_deco(self):
        return 1

    @deco_wraps
    @keyword
    @deco_wraps
    def keyword_wrapped(self, number=1, arg=''):
        return number, arg

    @keyword
    def varargs_and_kwargs(self, *args, **kwargs):
        return '{}, {}'.format(args, kwargs)

    @keyword
    def keyword_booleans(self, arg1=True, arg2=False):
        return '{}: {}, {}: {}'.format(arg1, type(arg1), arg2, type(arg2))
