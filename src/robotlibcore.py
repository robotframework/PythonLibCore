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

__version__ = '1.0.1.dev1'


class HybridCore(object):

    def __init__(self, library_components):
        self.keywords = {}
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
    __get_keyword_tags_supported = False  # get_keyword_tags is new in RF 3.0.2

    def run_keyword(self, name, args, kwargs=None):
        return self.keywords[name](*args, **(kwargs or {}))

    def get_keyword_arguments(self, name):
        kw_method = self.__get_keyword(name)
        if kw_method is None:
            return None
        args, defaults, varargs, kwargs, kwonlydefaults = self.__get_arg_spec(kw_method)
        if self.__rf_31:
            args += self.__old_default_spec(defaults)
        else:
            args += self.__new_default_spec(defaults)
        if varargs:
            args.append('*%s' % varargs)
        if kwargs:
            args.append('**%s' % kwargs)
        if kwonlydefaults:
            args += self.__kwonlydefaults_spec(kwonlydefaults)
        return args

    @property
    def __rf_31(self):
        return robot_version < '3.2'

    def __new_default_spec(self, defaults):
        return [(name, value) for name, value in defaults]

    def __old_default_spec(self, defaults):
        return ['{}={}'.format(name, value) for name, value in defaults]

    def __kwonlydefaults_spec(self, kwonlydefaults):
        args = []
        for argument, default_value in kwonlydefaults.items():
            if self.__rf_31:
                args.append(self.__old_kwonlydefaults_spec(argument, default_value))
            else:
                args.append(self.__new_kwonlydefaults_spec(argument, default_value))
        return args

    def __new_kwonlydefaults_spec(self, argument, default_value):
        return (argument, default_value)

    def __old_kwonlydefaults_spec(self, argument, default_value):
        return '%s=%s' % (argument, default_value)

    def __get_arg_spec(self, kw):
        if PY2:
            spec = inspect.getargspec(kw)
            keywords = spec.keywords
            kwonlydefaults = {}
        else:
            spec = inspect.getfullargspec(kw)
            keywords = spec.varkw
            kwonlydefaults = spec.kwonlydefaults
        args = spec.args[1:] if inspect.ismethod(kw) else spec.args  # drop self
        defaults = spec.defaults or ()
        nargs = len(args) - len(defaults)
        mandatory = args[:nargs]
        defaults = zip(args[nargs:], defaults)
        return mandatory, defaults, spec.varargs, keywords, kwonlydefaults

    def get_keyword_tags(self, name):
        self.__get_keyword_tags_supported = True
        return self.keywords[name].robot_tags

    def get_keyword_documentation(self, name):
        if name == '__intro__':
            return inspect.getdoc(self) or ''
        if name == '__init__':
            return inspect.getdoc(self.__init__) or ''
        kw = self.keywords[name]
        doc = inspect.getdoc(kw) or ''
        if kw.robot_tags and not self.__get_keyword_tags_supported:
            tags = 'Tags: {}'.format(', '.join(kw.robot_tags))
            doc = '{}\n\n{}'.format(doc, tags) if doc else tags
        return doc

    def get_keyword_types(self, keyword_name):
        method = self.__get_keyword(keyword_name)
        if method is None:
            return method
        types = getattr(method, 'robot_types', ())
        if types is None:
            return types
        if not types:
            types = self.__get_typing_hints(method)
        types = self.__join_defaults_with_types(method, types)
        return types

    def __get_keyword(self, keyword_name):
        if keyword_name == '__init__':
            return self.__init__
        if keyword_name.startswith('__') and keyword_name.endswith('__'):
            return None
        method = self.keywords.get(keyword_name)
        if not method:
            raise ValueError('Keyword "%s" not found.' % keyword_name)
        return method

    def __get_typing_hints(self, method):
        if PY2:
            return {}
        try:
            hints = typing.get_type_hints(method)
        except Exception:
            hints = method.__annotations__
        hints.pop('return', None)
        return hints

    def __join_defaults_with_types(self, method, types):
        _, defaults, _, _, kwonlydefaults = self.__get_arg_spec(method)
        for name, value in defaults:
            if name not in types and isinstance(value, (bool, type(None))):
                types[name] = type(value)
        if kwonlydefaults:
            for name, value in kwonlydefaults.items():
                if name not in types and isinstance(value, (bool, type(None))):
                    types[name] = type(value)
        return types

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


class StaticCore(HybridCore):

    def __init__(self):
        HybridCore.__init__(self, [])


class ArgumentSpec(object):

    def __init__(self, positional=None,  varargs=None, kwonlyargs=None, kwargs=None, defaults=None):
            self.positional = positional or []
            self.varargs = varargs
            self.kwonlyargs = kwonlyargs or []
            self.kwargs = kwargs
            self.defaults = defaults or {}

    @classmethod
    def from_function(cls, function):
        spec = inspect.getfullargspec(function)
        args = spec.args[1:] if inspect.ismethod(function) else spec.args  # drop self
        defaults = cls._get_defaults(spec)
        positional = cls._remove_defaults_from_positional(args, defaults)
        return cls(positional=positional,
                   defaults=defaults,
                   varargs=spec.varargs,
                   kwargs=spec.varkw)

    @classmethod
    def _get_defaults(cls, spec):
        if not spec.defaults:
            return {}
        names = spec.args[-len(spec.defaults):]
        return dict(zip(names, spec.defaults))

    @classmethod
    def _remove_defaults_from_positional(cls, args, defaults):
        positional = []
        for argument in args:
            if argument not in defaults:
                positional.append(argument)
        return positional
