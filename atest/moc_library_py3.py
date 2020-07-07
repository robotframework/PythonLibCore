from typing import Optional


class MockLibraryPy3:

    def named_only(self, *varargs, key1, key2):
        pass

    def named_only_with_defaults(self, *varargs, key1, key2, key3='default1', key4=True):
        pass

    def args_with_type_hints(self, arg1, arg2, arg3: str, arg4: None) -> bool:
        pass

    def self_and_keyword_only_types(x: 'MockLibraryPy3', mandatory, *varargs: int, other: bool, **kwargs: int):
        pass

    def optional_none(self, arg: Optional[str] = None):
        pass
