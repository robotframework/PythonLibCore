import inspect
from os import path

import pytest
from mockito.matchers import Any

from DynamicLibrary import DynamicLibrary
from DynamicTypesLibrary import DynamicTypesLibrary
from robotlibcore import PY2


@pytest.fixture(scope='module')
def lib():
    return DynamicLibrary()


@pytest.fixture(scope='module')
def lib_types():
    return DynamicTypesLibrary()


@pytest.fixture(scope='module')
def cur_dir():
    return path.dirname(__file__)


@pytest.fixture(scope='module')
def lib_path(cur_dir):
    return path.normpath(path.join(cur_dir, '..', 'atest', 'DynamicLibrary.py'))


@pytest.fixture(scope='module')
def lib_path_components(cur_dir):
    return path.normpath(path.join(cur_dir, '..', 'atest', 'librarycomponents.py'))


@pytest.fixture(scope='module')
def lib_path_types(cur_dir):
    return path.normpath(path.join(cur_dir, '..', 'atest', 'DynamicTypesLibrary.py'))


def test_location_in_main(lib, lib_path):
    source = lib.get_keyword_source('keyword_in_main')
    assert source == '%s:20' % lib_path


def test_location_in_class(lib, lib_path_components):
    source = lib.get_keyword_source('method')
    assert source == '%s:15' % lib_path_components


@pytest.mark.skipif(PY2, reason='Only applicable on Python 3')
def test_decorator_wrapper(lib_types, lib_path_types):
    source = lib_types.get_keyword_source('keyword_wrapped')
    assert source == '%s:72' % lib_path_types


def test_location_in_class_custom_keyword_name(lib, lib_path_components):
    source = lib.get_keyword_source('Custom name')
    assert source == '%s:19' % lib_path_components


def test_no_line_number(lib, lib_path, when):
    when(lib)._DynamicCore__get_keyword_line(Any()).thenReturn(None)
    source = lib.get_keyword_source('keyword_in_main')
    assert source == lib_path


def test_no_path(lib, when):
    when(lib)._DynamicCore__get_keyword_path(Any()).thenReturn(None)
    source = lib.get_keyword_source('keyword_in_main')
    assert source == ':20'


def test_no_path_and_no_line_number(lib, when):
    when(lib)._DynamicCore__get_keyword_path(Any()).thenReturn(None)
    when(lib)._DynamicCore__get_keyword_line(Any()).thenReturn(None)
    source = lib.get_keyword_source('keyword_in_main')
    assert source is None


def test_def_in_decorator(lib_types, lib_path_types):
    source = lib_types.get_keyword_source('keyword_with_def_deco')
    assert source == '%s:66' % lib_path_types


def test_error_in_getfile(lib, when):
    when(inspect).getfile(Any()).thenRaise(TypeError('Some message'))
    source = lib.get_keyword_source('keyword_in_main')
    assert source is None


def test_error_in_line_number(lib, when, lib_path):
    when(inspect).getsourcelines(Any()).thenRaise(IOError('Some message'))
    source = lib.get_keyword_source('keyword_in_main')
    assert source == lib_path
