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

from robot.api.deco import keyword

from robotlibcore.core import DynamicCore, HybridCore
from robotlibcore.keywords import KeywordBuilder, KeywordSpecification
from robotlibcore.plugin import PluginParser
from robotlibcore.utils import Module, NoKeywordFound, PluginError, PythonLibCoreException

__version__ = "4.5.0"

__all__ = [
    "DynamicCore",
    "HybridCore",
    "KeywordBuilder",
    "KeywordSpecification",
    "Module",
    "NoKeywordFound",
    "PluginError",
    "PluginParser",
    "PythonLibCoreException",
    "keyword",
]
