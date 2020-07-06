import pytest

from robotlibcore import PY2, RF31, KeywordBuilder
from moc_library import MockLibrary
if not PY2:
    from moc_library_py3 import MockLibraryPy3


@pytest.fixture
def lib():
    return MockLibrary()


@pytest.fixture
def lib_py3():
    return MockLibraryPy3()


def test_documentation(lib):
    spec = KeywordBuilder.build(lib.positional_args)
    assert spec.documentation == 'Some documentation\n\nMulti line docs'
    spec = KeywordBuilder.build(lib.positional_and_default)
    assert spec.documentation == ''


def test_no_args(lib):
    spec = KeywordBuilder.build(lib.no_args)
    assert spec.argument_specification == ()


def test_positional_args(lib):
    spec = KeywordBuilder.build(lib.positional_args)
    assert spec.argument_specification == ('arg1', 'arg2')


@pytest.mark.skipif(RF31, reason='Only for RF3.2+')
def test_positional_and_named_rf32(lib):
    spec = KeywordBuilder.build(lib.positional_and_default)
    assert spec.argument_specification == ('arg1', 'arg2', ('named1', 'string1'), ('named2', 123))


@pytest.mark.skipif(not RF31, reason='Only for RF3.1')
def test_positional_and_named_rf31(lib):
    spec = KeywordBuilder.build(lib.positional_and_default)
    assert spec.argument_specification == ('arg1', 'arg2', 'named1=string1', 'named2=123')


@pytest.mark.skipif(RF31, reason='Only for RF3.2+')
def test_named_only_rf32(lib):
    spec = KeywordBuilder.build(lib.default_only)
    assert spec.argument_specification == (('named1', 'string1'), ('named2', 123))


@pytest.mark.skipif(not RF31, reason='Only for RF3.1')
def test_named_only_rf31(lib):
    spec = KeywordBuilder.build(lib.default_only)
    assert spec.argument_specification == ('named1=string1', 'named2=123')


def test_varargs_and_kwargs(lib):
    spec = KeywordBuilder.build(lib.varargs_kwargs)
    assert spec.argument_specification == ('*vargs', '**kwargs')


@pytest.mark.skipif(PY2, reason='Only for Python 3')
def test_named_only(lib_py3):
    spec = KeywordBuilder.build(lib_py3.named_only)
    assert spec.argument_specification == ('*varargs', 'key1', 'key2')


@pytest.mark.skipif(PY2, reason='Only for Python 3')
@pytest.mark.skipif(RF31, reason='Only for RF3.2+')
def test_named_only_rf32(lib_py3):
    spec = KeywordBuilder.build(lib_py3.named_only_with_defaults)
    assert spec.argument_specification == ('*varargs', 'key1', 'key2', ('key3', 'default1'), ('key4', True))


@pytest.mark.skipif(PY2, reason='Only for Python 3')
@pytest.mark.skipif(not RF31, reason='Only for RF3.1')
def test_named_only_rf31(lib_py3):
    spec = KeywordBuilder.build(lib_py3.named_only_with_defaults)
    assert spec.argument_specification == ('*varargs', 'key1', 'key2', 'key3=default1', 'key4=True')


def test_types_in_keyword_deco(lib):
    spec = KeywordBuilder.build(lib.positional_args)
    assert spec.argument_types == {'arg1': str, 'arg2': int}


def test_types_disabled_in_keyword_deco(lib):
    spec = KeywordBuilder.build(lib.types_disabled)
    assert spec.argument_types is None


@pytest.mark.skipif(PY2, reason='Only for Python 3')
def test_types_(lib_py3):
    spec = KeywordBuilder.build(lib_py3.args_with_type_hints)
    assert spec.argument_types == {'arg3': str, 'arg4': type(None)}
