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


import inspect
from typing import Callable, Optional, get_type_hints

from .specification import KeywordSpecification


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
