import pytest
import typing

from robotlibcore import KeywordBuilder, RF32
from moc_library import MockLibrary
from DynamicTypesAnnotationsLibrary import DynamicTypesAnnotationsLibrary


@pytest.fixture
def lib():
    return MockLibrary()


@pytest.fixture
def dyn_types():
    return DynamicTypesAnnotationsLibrary(1)


def test_documentation(lib):
    spec = KeywordBuilder.build(lib.positional_args)
    assert spec.documentation == 'Some documentation\n\nMulti line docs'
    spec = KeywordBuilder.build(lib.positional_and_default)
    assert spec.documentation == ''


def test_no_args(lib):
    spec = KeywordBuilder.build(lib.no_args)
    assert spec.argument_specification == []


def test_positional_args(lib):
    spec = KeywordBuilder.build(lib.positional_args)
    assert spec.argument_specification == ['arg1', 'arg2']


def test_positional_and_named(lib):
    spec = KeywordBuilder.build(lib.positional_and_default)
    assert spec.argument_specification == ['arg1', 'arg2', ('named1', 'string1'), ('named2', 123)]


def test_named_only(lib):
    spec = KeywordBuilder.build(lib.default_only)
    assert spec.argument_specification == [('named1', 'string1'), ('named2', 123)]


def test_varargs_and_kwargs(lib):
    spec = KeywordBuilder.build(lib.varargs_kwargs)
    assert spec.argument_specification == ['*vargs', '**kwargs']


def test_named_only_part2(lib):
    spec = KeywordBuilder.build(lib.named_only)
    assert spec.argument_specification == ['*varargs', 'key1', 'key2']


def test_named_only(lib):
    spec = KeywordBuilder.build(lib.named_only_with_defaults)
    assert spec.argument_specification == ['*varargs', 'key1', 'key2', ('key3', 'default1'), ('key4', True)]


def test_types_in_keyword_deco(lib):
    spec = KeywordBuilder.build(lib.positional_args)
    assert spec.argument_types == {'arg1': str, 'arg2': int}


def test_types_disabled_in_keyword_deco(lib):
    spec = KeywordBuilder.build(lib.types_disabled)
    assert spec.argument_types is None


def test_types_(lib):
    spec = KeywordBuilder.build(lib.args_with_type_hints)
    assert spec.argument_types == {'arg3': str, 'arg4': type(None)}


def test_types(lib):
    spec = KeywordBuilder.build(lib.self_and_keyword_only_types)
    assert spec.argument_types == {'varargs': int, 'other': bool, 'kwargs': int}


@pytest.mark.skipif(not RF32, reason='Only for RF3.2+')
def test_optional_none_rf32(lib):
    spec = KeywordBuilder.build(lib.optional_none)
    assert spec.argument_types == {'arg1': str, 'arg2': str}


@pytest.mark.skipif(RF32, reason='Only for RF4')
def test_optional_none_rf4(lib):
    spec = KeywordBuilder.build(lib.optional_none)
    assert spec.argument_types == {'arg1': typing.Union[str, None], 'arg2': typing.Union[str, None]}


def test_complex_deco(dyn_types):
    spec = KeywordBuilder.build(dyn_types.keyword_with_deco_and_signature)
    assert spec.argument_types == {'arg1': bool, 'arg2': bool}
    assert spec.argument_specification == [('arg1', False), ('arg2', False)]
    assert spec.documentation == "Test me doc here"
