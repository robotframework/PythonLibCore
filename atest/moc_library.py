from typing import Optional

from robot.api.deco import keyword


class MockLibrary:

    def no_args(self):
        pass

    @keyword(types={'arg1': str, 'arg2': int})
    def positional_args(self, arg1, arg2):
        """Some documentation

        Multi line docs
        """
        pass

    @keyword(types=None)
    def types_disabled(self, arg=False):
        pass

    @keyword
    def positional_and_default(self, arg1, arg2, named1='string1', named2=123):
        pass

    def default_only(self, named1='string1', named2=123):
        pass

    def varargs_kwargs(self, *vargs, **kwargs):
        pass

    def named_only(self, *varargs, key1, key2):
        pass

    def named_only_with_defaults(self, *varargs, key1, key2, key3='default1', key4=True):
        pass

    def args_with_type_hints(self, arg1, arg2, arg3: str, arg4: None) -> bool:
        pass

    def self_and_keyword_only_types(
            x: 'MockLibrary',  # noqa: N805
            mandatory,
            *varargs: int,
            other: bool,
            **kwargs: int
    ):
        pass

    def optional_none(self, xxx, arg1: Optional[str] = None, arg2: Optional[str] = None, arg3=False):
        pass
