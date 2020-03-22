import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from robotlibcore import PY2

if not PY2:
    from typing import List, Union
    from DynamicLibraryTypesAnnotations import DynamicLibraryTypesAnnotations

from DynamicTypesLibrary import DynamicTypesLibrary


@pytest.fixture(scope='module')
def lib():
    return DynamicTypesLibrary()


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


def test_not_keyword(lib):
    with pytest.raises(ValueError):
        lib.get_keyword_types('not_keyword')


def test_keyword_booleans(lib):
    types = lib.get_keyword_types('keyword_booleans')
    assert types == {'arg1': bool, 'arg2': bool}


def test_keyword_none(lib):
    types = lib.get_keyword_types('keyword_none')
    assert types == {'arg': type(None)}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_single_annotation(lib_types):
    types = lib_types.get_keyword_types('keyword_with_one_annotation')
    assert types == {'arg': str}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_multiple_annotations(lib_types):
    types = lib_types.get_keyword_types('keyword_with_multiple_annotations')
    assert types == {'arg1': str, 'arg2': List}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_multiple_types(lib_types):
    types = lib_types.get_keyword_types('keyword_multiple_types')
    assert types == {'arg': Union[List, None]}


def test_keyword_with_default_type(lib):
    types = lib.get_keyword_types('keyword_default_types')
    assert types == {'arg': type(None)}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_keyword_new_type(lib_types):
    types = lib_types.get_keyword_types('keyword_new_type')
    assert len(types) == 1
    assert types['arg']


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_keyword_return_type(lib_types):
    types = lib_types.get_keyword_types('keyword_define_return_type')
    assert types == {'arg': str}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_keyword_forward_references(lib_types):
    types = lib_types.get_keyword_types('keyword_forward_references')
    assert types == {'arg': WebDriver}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_keyword_with_annotation_and_default(lib_types):
    types = lib_types.get_keyword_types('keyword_with_annotations_and_default')
    assert types == {'arg': str}


def test_keyword_with_many_defaults(lib):
    types = lib.get_keyword_types('keyword_many_default_types')
    assert types == {}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_keyword_with_annotation_external_class(lib_types):
    types = lib_types.get_keyword_types('keyword_with_webdriver')
    assert types == {'arg': WebDriver}


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_keyword_with_annotation_and_default(lib_types):
    types = lib_types.get_keyword_types('keyword_default_and_annotation')
    assert types == {'arg1': int, 'arg2': bool}
