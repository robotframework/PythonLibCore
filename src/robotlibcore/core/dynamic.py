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
import os

from robotlibcore.utils import NoKeywordFound

from .hybrid import HybridCore


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
