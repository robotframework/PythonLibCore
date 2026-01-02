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
from pathlib import Path
from typing import Callable, List, Optional

from robotlibcore.keywords import KeywordBuilder
from robotlibcore.utils import _translated_keywords, _translation


class HybridCore:
    def __init__(self, library_components: List, translation: Optional[Path] = None) -> None:
        self.keywords = {}
        self.keywords_spec = {}
        self.attributes = {}
        translation_data = _translation(translation)
        translated_kw_names = _translated_keywords(translation_data)
        self.add_library_components(library_components, translation_data, translated_kw_names)
        self.add_library_components([self], translation_data, translated_kw_names)
        self.__set_library_listeners(library_components)

    def add_library_components(
        self,
        library_components: List,
        translation: Optional[dict] = None,
        translated_kw_names: Optional[list] = None,
    ):
        translation = translation if translation else {}
        translated_kw_names = translated_kw_names if translated_kw_names else []
        self.keywords_spec["__init__"] = KeywordBuilder.build(self.__init__, translation)  # type: ignore
        self.__replace_intro_doc(translation)
        for component in library_components:
            for name, func in self.__get_members(component):
                if callable(func) and hasattr(func, "robot_name"):
                    kw = getattr(component, name)
                    kw_name = self.__get_keyword_name(func, name, translation, translated_kw_names)
                    self.keywords[kw_name] = kw
                    self.keywords_spec[kw_name] = KeywordBuilder.build(kw, translation)
                    # Expose keywords as attributes both using original
                    # method names as well as possible custom names.
                    self.attributes[name] = self.attributes[kw_name] = kw

    def __get_keyword_name(self, func: Callable, name: str, translation: dict, translated_kw_names: list):
        if name in translated_kw_names:
            return name
        if name in translation and translation[name].get("name"):
            return translation[name].get("name")
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
        if type(component) != component.__class__:  # noqa: E721
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
        if name == "attributes":
            return super().__getattribute__(name)
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
