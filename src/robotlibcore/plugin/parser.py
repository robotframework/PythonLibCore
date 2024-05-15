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
from typing import Any, List, Optional, Union

from robot.errors import DataError
from robot.utils import Importer

from robotlibcore.core import DynamicCore
from robotlibcore.utils import Module, PluginError


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
