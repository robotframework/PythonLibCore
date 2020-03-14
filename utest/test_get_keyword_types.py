import pytest

from robotlibcore import PY2

if not PY2:
    from typing import List
    from DynamicLibraryTypesAnnotations import DynamicLibraryTypesAnnotations

from DynamicLibraryTypes import DynamicLibraryTypes


@pytest.fixture(scope='module')
def lib():
    return DynamicLibraryTypes()


@pytest.fixture(scope='module')
def lib_types():
    return DynamicLibraryTypesAnnotations()


def test_using_keyword_types(lib):
    types = lib.get_keyword_types('keyword_with_types')
    assert types == {'arg1': str}


def test_types_disabled(lib):
    types = lib.get_keyword_types('keyword_with_disabled_types')
    assert types == {}


def test_one_keyword_type_defined(lib):
    types = lib.get_keyword_types('keyword_with_one_type')
    assert types == {'arg1': str}


def test_keyword_no_args(lib):
    types = lib.get_keyword_types('keyword_with_no_args')
    assert types == {}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_single_annotation(lib_types):
    types = lib_types.get_keyword_types('keyword_with_one_annotation')
    assert types == {'arg': str}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_multiple_annotations(lib_types):
    types = lib_types.get_keyword_types('keyword_with_multiple_annotations')
    assert types == {'arg1': str, 'arg2': List}
