# Copyright 2017- Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generic test library core for Robot Framework.

Main usage is easing creating larger test libraries. For more information and
examples see the project pages at
https://github.com/robotframework/PythonLibCore
"""

import inspect
import os
import sys

try:
    import typing
except ImportError:
    typing = None

from robot.api.deco import keyword  # noqa F401
from robot import __version__ as robot_version

PY2 = sys.version_info < (3,)
RF31 = robot_version < '3.2'

__version__ = '2.0.3.dev1'


class HybridCore(object):

    def __init__(self, library_components):
        self.keywords = {}
        self.keywords_spec = {}
        self.attributes = {}
        self.add_library_components(library_components)
        self.add_library_components([self])

    def add_library_components(self, library_components):
        for component in library_components:
            for name, func in self.__get_members(component):
                if callable(func) and hasattr(func, 'robot_name'):
                    kw = getattr(component, name)
                    kw_name = func.robot_name or name
                    self.keywords[kw_name] = kw
                    self.keywords_spec[kw_name] = KeywordBuilder.build(kw)
                    # Expose keywords as attributes both using original
                    # method names as well as possible custom names.
                    self.attributes[name] = self.attributes[kw_name] = kw

    def __get_members(self, component):
        if inspect.ismodule(component):
            return inspect.getmembers(component)
        if inspect.isclass(component):
            raise TypeError('Libraries must be modules or instances, got '
                            'class {!r} instead.'.format(component.__name__))
        if type(component) != component.__class__:
            raise TypeError('Libraries must be modules or new-style class '
                            'instances, got old-style class {!r} instead.'
                            .format(component.__class__.__name__))
        return self.__get_members_from_instance(component)

    def __get_members_from_instance(self, instance):
        # Avoid calling properties by getting members from class, not instance.
        cls = type(instance)
        for name in dir(instance):
            owner = cls if hasattr(cls, name) else instance
            yield name, getattr(owner, name)

    def __getattr__(self, name):
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError('{!r} object has no attribute {!r}'
                             .format(type(self).__name__, name))

    def __dir__(self):
        if PY2:
            my_attrs = dir(type(self)) + list(self.__dict__)
        else:
            my_attrs = super().__dir__()
        return sorted(set(my_attrs) | set(self.attributes))

    def get_keyword_names(self):
        return sorted(self.keywords)


class DynamicCore(HybridCore):

    def run_keyword(self, name, args, kwargs=None):
        return self.keywords[name](*args, **(kwargs or {}))

    def get_keyword_arguments(self, name):
        kw_method = self.__get_keyword(name)
        if kw_method is None:
            return None
        spec = ArgumentSpec.from_function(kw_method)
        return spec.get_arguments()

    def get_keyword_tags(self, name):
        return self.keywords[name].robot_tags

    def get_keyword_documentation(self, name):
        if name == '__intro__':
            return inspect.getdoc(self) or ''
        if name == '__init__':
            return inspect.getdoc(self.__init__) or ''
        spec = self.keywords_spec.get(name)
        return spec.documentation

    def get_keyword_types(self, name):
        if name == '__init__':
            spec = KeywordBuilder.build_init(self.__init__)
            return spec.argument_types
        spec = self.keywords_spec.get(name)
        if spec is None:
            raise ValueError('Keyword "%s" not found.' % name)
        return spec.argument_types

    def __get_keyword(self, keyword_name):
        if keyword_name == '__init__':
            return self.__init__
        if keyword_name.startswith('__') and keyword_name.endswith('__'):
            return None
        method = self.keywords.get(keyword_name)
        if not method:
            raise ValueError('Keyword "%s" not found.' % keyword_name)
        return method

    def get_keyword_source(self, keyword_name):
        method = self.__get_keyword(keyword_name)
        path = self.__get_keyword_path(method)
        line_number = self.__get_keyword_line(method)
        if path and line_number:
            return '%s:%s' % (path, line_number)
        if path:
            return path
        if line_number:
            return ':%s' % line_number
        return None

    def __get_keyword_line(self, method):
        try:
            lines, line_number = inspect.getsourcelines(method)
        except (OSError, IOError, TypeError):
            return None
        for increment, line in enumerate(lines):
            if line.strip().startswith('def '):
                return line_number + increment
        return line_number

    def __get_keyword_path(self, method):
        try:
            return os.path.normpath(inspect.getfile(method))
        except TypeError:
            return None


class ArgumentSpec(object):

    _function = None

    def __init__(self, positional=None, defaults=None, varargs=None, kwonlyargs=None,
                 kwonlydefaults=None, kwargs=None):
        self.positional = positional or []
        self.defaults = defaults or []
        self.varargs = varargs
        self.kwonlyargs = kwonlyargs or []
        self.kwonlydefaults = kwonlydefaults or []
        self.kwargs = kwargs

    def __contains__(self, item):
        if item in self.positional:
            return True
        if self.varargs and item in self.varargs:
            return True
        if item in self.kwonlyargs:
            return True
        if self.kwargs and item in self.kwargs:
            return True
        return False

    def get_arguments(self):
        args = self._format_positional(self.positional, self.defaults)
        args += self._format_default(self.defaults)
        if self.varargs:
            args.append('*%s' % self.varargs)
        args += self._format_positional(self.kwonlyargs, self.kwonlydefaults)
        args += self._format_default(self.kwonlydefaults)
        if self.kwargs:
            args.append('**%s' % self.kwargs)
        return args

    def get_typing_hints(self):
        try:
            hints = typing.get_type_hints(self._function)
        except Exception:
            hints = self._function.__annotations__
        for arg in list(hints):
            # remove return and self statements
            if arg not in self:
                hints.pop(arg)
        return hints

    def _format_positional(self, positional, defaults):
        for argument, _ in defaults:
            positional.remove(argument)
        return positional

    def _format_default(self, defaults):
        if not RF31:
            return [default for default in defaults]
        return ['%s=%s' % (argument, default) for argument, default in defaults]

    @classmethod
    def from_function(cls, function):
        cls._function = function
        if PY2:
            spec = inspect.getargspec(function)
        else:
            spec = inspect.getfullargspec(function)
        args = spec.args[1:] if inspect.ismethod(function) else spec.args  # drop self
        defaults = cls._get_defaults(spec)
        kwonlyargs, kwonlydefaults, kwargs = cls._get_kw_args(spec)
        return cls(positional=args,
                   defaults=defaults,
                   varargs=spec.varargs,
                   kwonlyargs=kwonlyargs,
                   kwonlydefaults=kwonlydefaults,
                   kwargs=kwargs)

    @classmethod
    def _get_defaults(cls, spec):
        if not spec.defaults:
            return []
        names = spec.args[-len(spec.defaults):]
        return list(zip(names, spec.defaults))

    @classmethod
    def _get_kw_args(cls, spec):
        if PY2:
            return [], [], spec.keywords
        kwonlyargs = spec.kwonlyargs or []
        defaults = spec.kwonlydefaults or {}
        kwonlydefaults = [(arg, name) for arg, name in defaults.items()]
        return kwonlyargs, kwonlydefaults, spec.varkw


class KeywordBuilder(object):

    @classmethod
    def build(cls, function):
        return KeywordSpecification(
            argument_specification=cls._get_arguments(function),
            documentation=inspect.getdoc(function) or '',
            argument_types=cls._get_types(function)
        )

    @classmethod
    def build_init(cls, init):
        return KeywordSpecification(
            argument_types=cls._get_types(init)
        )

    @classmethod
    def _get_arguments(cls, function):
        arg_spec = cls._get_arg_spec(function)
        argument_specification = cls._get_default_and_named_args(
            arg_spec, function
        )
        argument_specification.extend(cls._get_var_args(arg_spec))
        kw_only_args = cls._get_kw_only(arg_spec)
        if kw_only_args:
            argument_specification.extend(kw_only_args)
        argument_specification.extend(cls._get_kwargs(arg_spec))
        return tuple(argument_specification)

    @classmethod
    def _get_arg_spec(cls, function):
        if PY2:
            return inspect.getargspec(function)
        return inspect.getfullargspec(function)

    @classmethod
    def _get_default_and_named_args(cls, arg_spec, function):
        args = cls._drop_self_from_args(function, arg_spec)
        args.reverse()
        defaults = list(arg_spec.defaults) if arg_spec.defaults else []
        formated_args = []
        for arg in args:
            if defaults:
                formated_args.append(
                    cls._format_defaults(arg, defaults.pop())
                )
            else:
                formated_args.append(arg)
        formated_args.reverse()
        return formated_args

    @classmethod
    def _drop_self_from_args(cls, function, arg_spec):
        return arg_spec.args[1:] if inspect.ismethod(function) else arg_spec.args

    @classmethod
    def _get_var_args(cls, arg_spec):
        if arg_spec.varargs:
            return ['*%s' % arg_spec.varargs]
        return []

    @classmethod
    def _get_kwargs(cls, arg_spec):
        if PY2:
            return ['**%s' % arg_spec.keywords] if arg_spec.keywords else []
        return ['**%s' % arg_spec.varkw] if arg_spec.varkw else []

    @classmethod
    def _get_kw_only(cls, arg_spec):
        kw_only_args = []
        if PY2:
            return kw_only_args
        for arg in arg_spec.kwonlyargs:
            if not arg_spec.kwonlydefaults or arg not in arg_spec.kwonlydefaults:
                kw_only_args.append(arg)
            else:
                value = arg_spec.kwonlydefaults.get(arg, '')
                kw_only_args.append(cls._format_defaults(arg, value))
        return kw_only_args

    @classmethod
    def _format_defaults(cls, arg, value):
        if RF31:
            return '%s=%s' % (arg, value)
        return arg, value

    @classmethod
    def _get_types(cls, function):
        if function is None:
            return function
        types = getattr(function, 'robot_types', ())
        if types is None or types:
            return types
        if not types:
            types = cls._get_typing_hints(function)
        return types

    @classmethod
    def _get_typing_hints(cls, function):
        if PY2:
            return {}
        try:
            hints = typing.get_type_hints(function)
        except Exception:
            hints = function.__annotations__
        all_args = cls._args_as_list(function)
        for arg_with_hint in list(hints):
            # remove return and self statements
            if arg_with_hint not in all_args:
                hints.pop(arg_with_hint)
        return hints

    @classmethod
    def _args_as_list(cls, function):
        arg_spec = cls._get_arg_spec(function)
        function_args = []
        function_args.extend(cls._drop_self_from_args(function, arg_spec))
        if arg_spec.varargs:
            function_args.append(arg_spec.varargs)
        function_args.extend(arg_spec.kwonlyargs or [])
        if arg_spec.varkw:
            function_args.append(arg_spec.varkw)
        return function_args


class KeywordSpecification(object):

    def __init__(self, argument_specification=None, documentation=None, argument_types=None):
        self.argument_specification = argument_specification
        self.documentation = documentation
        self.argument_types = argument_types
