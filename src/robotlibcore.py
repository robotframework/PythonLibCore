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
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, get_type_hints

from robot.api.deco import keyword  # noqa F401
from robot.errors import DataError
from robot.utils import Importer  # noqa F401

__version__ = "4.1.2"


class PythonLibCoreException(Exception):
    pass


class PluginError(PythonLibCoreException):
    pass


class HybridCore:
    def __init__(self, library_components):
        self.keywords = {}
        self.keywords_spec = {}
        self.attributes = {}
        self.add_library_components(library_components)
        self.add_library_components([self])
        self.__set_library_listeners(library_components)

    def add_library_components(self, library_components):
        self.keywords_spec["__init__"] = KeywordBuilder.build(self.__init__)
        for component in library_components:
            for name, func in self.__get_members(component):
                if callable(func) and hasattr(func, "robot_name"):
                    kw = getattr(component, name)
                    kw_name = func.robot_name or name
                    self.keywords[kw_name] = kw
                    self.keywords_spec[kw_name] = KeywordBuilder.build(kw)
                    # Expose keywords as attributes both using original
                    # method names as well as possible custom names.
                    self.attributes[name] = self.attributes[kw_name] = kw

    def __set_library_listeners(self, library_components: list):
        listeners = self.__get_manually_registered_listeners()
        listeners.extend(self.__get_component_listeners([self, *library_components]))
        if listeners:
            self.ROBOT_LIBRARY_LISTENER = list(dict.fromkeys(listeners))

    def __get_manually_registered_listeners(self) -> list:
        manually_registered_listener = getattr(self, "ROBOT_LIBRARY_LISTENER", [])
        try:
            return [*manually_registered_listener]
        except TypeError:
            return [manually_registered_listener]

    def __get_component_listeners(self, library_listeners: list) -> list:
        return [component for component in library_listeners if hasattr(component, "ROBOT_LISTENER_API_VERSION")]

    def __get_members(self, component):
        if inspect.ismodule(component):
            return inspect.getmembers(component)
        if inspect.isclass(component):
            raise TypeError(
                "Libraries must be modules or instances, got " "class {!r} instead.".format(component.__name__)
            )
        if type(component) != component.__class__:
            raise TypeError(
                "Libraries must be modules or new-style class "
                "instances, got old-style class {!r} instead.".format(component.__class__.__name__)
            )
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
        raise AttributeError("{!r} object has no attribute {!r}".format(type(self).__name__, name))

    def __dir__(self):
        my_attrs = super().__dir__()
        return sorted(set(my_attrs) | set(self.attributes))

    def get_keyword_names(self):
        return sorted(self.keywords)


@dataclass
class Module:
    module: str
    args: list
    kw_args: dict


class DynamicCore(HybridCore):
    def run_keyword(self, name, args, kwargs=None):
        return self.keywords[name](*args, **(kwargs or {}))

    def get_keyword_arguments(self, name):
        spec = self.keywords_spec.get(name)
        return spec.argument_specification

    def get_keyword_tags(self, name):
        return self.keywords[name].robot_tags

    def get_keyword_documentation(self, name):
        if name == "__intro__":
            return inspect.getdoc(self) or ""
        spec = self.keywords_spec.get(name)
        return spec.documentation

    def get_keyword_types(self, name):
        spec = self.keywords_spec.get(name)
        if spec is None:
            raise ValueError('Keyword "%s" not found.' % name)
        return spec.argument_types

    def __get_keyword(self, keyword_name):
        if keyword_name == "__init__":
            return self.__init__
        if keyword_name.startswith("__") and keyword_name.endswith("__"):
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
            return "{}:{}".format(path, line_number)
        if path:
            return path
        if line_number:
            return ":%s" % line_number
        return None

    def __get_keyword_line(self, method):
        try:
            lines, line_number = inspect.getsourcelines(method)
        except (OSError, TypeError):
            return None
        for increment, line in enumerate(lines):
            if line.strip().startswith("def "):
                return line_number + increment
        return line_number

    def __get_keyword_path(self, method):
        try:
            return os.path.normpath(inspect.getfile(inspect.unwrap(method)))
        except TypeError:
            return None


class KeywordBuilder:
    @classmethod
    def build(cls, function):
        return KeywordSpecification(
            argument_specification=cls._get_arguments(function),
            documentation=inspect.getdoc(function) or "",
            argument_types=cls._get_types(function),
        )

    @classmethod
    def unwrap(cls, function):
        return inspect.unwrap(function)

    @classmethod
    def _get_arguments(cls, function):
        unwrap_function = cls.unwrap(function)
        arg_spec = cls._get_arg_spec(unwrap_function)
        argument_specification = cls._get_args(arg_spec, function)
        argument_specification.extend(cls._get_varargs(arg_spec))
        argument_specification.extend(cls._get_named_only_args(arg_spec))
        argument_specification.extend(cls._get_kwargs(arg_spec))
        return argument_specification

    @classmethod
    def _get_arg_spec(cls, function: Callable):
        return inspect.getfullargspec(function)

    @classmethod
    def _get_args(cls, arg_spec: inspect.FullArgSpec, function: Callable):
        args = cls._drop_self_from_args(function, arg_spec)
        args.reverse()
        defaults = list(arg_spec.defaults) if arg_spec.defaults else []
        formated_args = []
        for arg in args:
            if defaults:
                formated_args.append((arg, defaults.pop()))
            else:
                formated_args.append(arg)
        formated_args.reverse()
        return formated_args

    @classmethod
    def _drop_self_from_args(cls, function: Callable, arg_spec: inspect.FullArgSpec):
        return arg_spec.args[1:] if inspect.ismethod(function) else arg_spec.args

    @classmethod
    def _get_varargs(cls, arg_spec: inspect.FullArgSpec) -> list:
        return [f"*{arg_spec.varargs}"] if arg_spec.varargs else []

    @classmethod
    def _get_kwargs(cls, arg_spec: inspect.FullArgSpec) -> list:
        return [f"**{arg_spec.varkw}"] if arg_spec.varkw else []

    @classmethod
    def _get_named_only_args(cls, arg_spec: inspect.FullArgSpec) -> list:
        rf_spec = []
        kw_only_args = arg_spec.kwonlyargs if arg_spec.kwonlyargs else []
        if not arg_spec.varargs and kw_only_args:
            rf_spec.append("*")
        kw_only_defaults = arg_spec.kwonlydefaults if arg_spec.kwonlydefaults else []
        for kw_only_arg in kw_only_args:
            if kw_only_arg in kw_only_defaults:
                rf_spec.append((kw_only_arg, kw_only_defaults[kw_only_arg]))
            else:
                rf_spec.append(kw_only_arg)
        return rf_spec

    @classmethod
    def _get_types(cls, function):
        if function is None:
            return function
        types = getattr(function, "robot_types", ())
        if types is None or types:
            return types
        return cls._get_typing_hints(function)

    @classmethod
    def _get_typing_hints(cls, function):
        function = cls.unwrap(function)
        try:
            hints = get_type_hints(function)
        except Exception:
            hints = function.__annotations__
        arg_spec = cls._get_arg_spec(function)
        all_args = cls._args_as_list(function, arg_spec)
        for arg_with_hint in list(hints):
            # remove return and self statements
            if arg_with_hint not in all_args:
                hints.pop(arg_with_hint)
        return hints

    @classmethod
    def _args_as_list(cls, function, arg_spec):
        function_args = []
        function_args.extend(cls._drop_self_from_args(function, arg_spec))
        if arg_spec.varargs:
            function_args.append(arg_spec.varargs)
        function_args.extend(arg_spec.kwonlyargs or [])
        if arg_spec.varkw:
            function_args.append(arg_spec.varkw)
        return function_args

    @classmethod
    def _get_defaults(cls, arg_spec):
        if not arg_spec.defaults:
            return {}
        names = arg_spec.args[-len(arg_spec.defaults) :]
        return zip(names, arg_spec.defaults)


class KeywordSpecification:
    def __init__(self, argument_specification=None, documentation=None, argument_types=None):
        self.argument_specification = argument_specification
        self.documentation = documentation
        self.argument_types = argument_types


class PluginParser:
    def __init__(self, base_class: Optional[Any] = None, python_object: List[Any] = []):
        self._base_class = base_class
        self._python_object = python_object

    def parse_plugins(self, plugins: str) -> List:
        imported_plugins = []
        importer = Importer("test library")
        for parsed_plugin in self._string_to_modules(plugins):
            plugin = importer.import_class_or_module(parsed_plugin.module)
            if not inspect.isclass(plugin):
                message = f"Importing test library: '{parsed_plugin.module}' failed."
                raise DataError(message)
            args = self._python_object + parsed_plugin.args
            plugin = plugin(*args, **parsed_plugin.kw_args)
            if self._base_class and not isinstance(plugin, self._base_class):
                message = f"Plugin does not inherit {self._base_class}"
                raise PluginError(message)
            imported_plugins.append(plugin)
        return imported_plugins

    def get_plugin_keywords(self, plugins: List):
        return DynamicCore(plugins).get_keyword_names()

    def _string_to_modules(self, modules):
        parsed_modules = []
        if not modules:
            return parsed_modules
        for module in modules.split(","):
            module = module.strip()
            module_and_args = module.split(";")
            module_name = module_and_args.pop(0)
            kw_args = {}
            args = []
            for argument in module_and_args:
                if "=" in argument:
                    key, value = argument.split("=")
                    kw_args[key] = value
                else:
                    args.append(argument)
            module = Module(module=module_name, args=args, kw_args=kw_args)
            parsed_modules.append(module)
        return parsed_modules
