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
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, Optional, Union, get_type_hints

from robot.api import logger
from robot.api.deco import keyword  # noqa: F401
from robot.errors import DataError
from robot.utils import Importer

__version__ = "4.4.0"


class PythonLibCoreException(Exception):  # noqa: N818
    pass


class PluginError(PythonLibCoreException):
    pass


class NoKeywordFound(PythonLibCoreException):
    pass


def _translation(translation: Optional[Path] = None):
    if translation and isinstance(translation, Path) and translation.is_file():
        with translation.open("r") as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                logger.warn(f"Could not convert json file {translation} to dictionary.")
                return {}
    else:
        return {}


class HybridCore:
    def __init__(self, library_components: List, translation: Optional[Path] = None) -> None:
        self.keywords = {}
        self.keywords_spec = {}
        self.attributes = {}
        translation_data = _translation(translation)
        self.add_library_components(library_components, translation_data)
        self.add_library_components([self], translation_data)
        self.__set_library_listeners(library_components)

    def add_library_components(self, library_components: List, translation: Optional[dict] = None):
        translation = translation if translation else {}
        self.keywords_spec["__init__"] = KeywordBuilder.build(self.__init__, translation)  # type: ignore
        self.__replace_intro_doc(translation)
        for component in library_components:
            for name, func in self.__get_members(component):
                if callable(func) and hasattr(func, "robot_name"):
                    kw = getattr(component, name)
                    kw_name = self.__get_keyword_name(func, name, translation)
                    self.keywords[kw_name] = kw
                    self.keywords_spec[kw_name] = KeywordBuilder.build(kw, translation)
                    # Expose keywords as attributes both using original
                    # method names as well as possible custom names.
                    self.attributes[name] = self.attributes[kw_name] = kw

    def __get_keyword_name(self, func: Callable, name: str, translation: dict):
        if name in translation:  # noqa: SIM102
            if new_name := translation[name].get("name"):
                return new_name
        return func.robot_name or name

    def __replace_intro_doc(self, translation: dict):
        if "__intro__" in translation:
            self.__doc__ = translation["__intro__"].get("doc", "")

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
            msg = f"Libraries must be modules or instances, got class '{component.__name__}' instead."
            raise TypeError(
                msg,
            )
        if type(component) != component.__class__:
            msg = (
                "Libraries must be modules or new-style class instances, "
                f"got old-style class {component.__class__.__name__} instead."
            )
            raise TypeError(
                msg,
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
        msg = "{!r} object has no attribute {!r}".format(type(self).__name__, name)
        raise AttributeError(
            msg,
        )

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
        if not spec:
            msg = f"Could not find keyword: {name}"
            raise NoKeywordFound(msg)
        return spec.argument_specification

    def get_keyword_tags(self, name):
        return self.keywords[name].robot_tags

    def get_keyword_documentation(self, name):
        if name == "__intro__":
            return inspect.getdoc(self) or ""
        spec = self.keywords_spec.get(name)
        if not spec:
            msg = f"Could not find keyword: {name}"
            raise NoKeywordFound(msg)
        return spec.documentation

    def get_keyword_types(self, name):
        spec = self.keywords_spec.get(name)
        if spec is None:
            raise ValueError('Keyword "%s" not found.' % name)
        return spec.argument_types

    def __get_keyword(self, keyword_name):
        if keyword_name == "__init__":
            return self.__init__  # type: ignore
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
    def build(cls, function, translation: Optional[dict] = None):
        translation = translation if translation else {}
        return KeywordSpecification(
            argument_specification=cls._get_arguments(function),
            documentation=cls.get_doc(function, translation),
            argument_types=cls._get_types(function),
        )

    @classmethod
    def get_doc(cls, function, translation: dict):
        if kw := cls._get_kw_transtation(function, translation):  # noqa: SIM102
            if "doc" in kw:
                return kw["doc"]
        return inspect.getdoc(function) or ""

    @classmethod
    def _get_kw_transtation(cls, function, translation: dict):
        return translation.get(function.__name__, {})

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
    def _get_arg_spec(cls, function: Callable) -> inspect.FullArgSpec:
        return inspect.getfullargspec(function)

    @classmethod
    def _get_type_hint(cls, function: Callable):
        try:
            hints = get_type_hints(function)
        except Exception:  # noqa: BLE001
            hints = function.__annotations__
        return hints

    @classmethod
    def _get_args(cls, arg_spec: inspect.FullArgSpec, function: Callable) -> list:
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
    def _drop_self_from_args(
        cls,
        function: Callable,
        arg_spec: inspect.FullArgSpec,
    ) -> list:
        return arg_spec.args[1:] if inspect.ismethod(function) else arg_spec.args

    @classmethod
    def _get_varargs(cls, arg_spec: inspect.FullArgSpec) -> list:
        return [f"*{arg_spec.varargs}"] if arg_spec.varargs else []

    @classmethod
    def _get_kwargs(cls, arg_spec: inspect.FullArgSpec) -> list:
        return [f"**{arg_spec.varkw}"] if arg_spec.varkw else []

    @classmethod
    def _get_named_only_args(cls, arg_spec: inspect.FullArgSpec) -> list:
        rf_spec: list = []
        kw_only_args = arg_spec.kwonlyargs if arg_spec.kwonlyargs else []
        if not arg_spec.varargs and kw_only_args:
            rf_spec.append("*")
        kw_only_defaults = arg_spec.kwonlydefaults if arg_spec.kwonlydefaults else {}
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
        hints = cls._get_type_hint(function)
        arg_spec = cls._get_arg_spec(function)
        all_args = cls._args_as_list(function, arg_spec)
        for arg_with_hint in list(hints):
            # remove self statements
            if arg_with_hint not in [*all_args, "return"]:
                hints.pop(arg_with_hint)
        return hints

    @classmethod
    def _args_as_list(cls, function, arg_spec) -> list:
        function_args = cls._drop_self_from_args(function, arg_spec)
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
    def __init__(
        self,
        argument_specification=None,
        documentation=None,
        argument_types=None,
    ) -> None:
        self.argument_specification = argument_specification
        self.documentation = documentation
        self.argument_types = argument_types


class PluginParser:
    def __init__(self, base_class: Optional[Any] = None, python_object=None) -> None:
        self._base_class = base_class
        self._python_object = python_object if python_object else []

    def parse_plugins(self, plugins: Union[str, List[str]]) -> List:
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

    def _string_to_modules(self, modules: Union[str, List[str]]):
        parsed_modules: list = []
        if not modules:
            return parsed_modules
        for module in self._modules_splitter(modules):
            module_and_args = module.strip().split(";")
            module_name = module_and_args.pop(0)
            kw_args = {}
            args = []
            for argument in module_and_args:
                if "=" in argument:
                    key, value = argument.split("=")
                    kw_args[key] = value
                else:
                    args.append(argument)
            parsed_modules.append(Module(module=module_name, args=args, kw_args=kw_args))
        return parsed_modules

    def _modules_splitter(self, modules: Union[str, List[str]]):
        if isinstance(modules, str):
            for module in modules.split(","):
                yield module
        else:
            for module in modules:
                yield module
