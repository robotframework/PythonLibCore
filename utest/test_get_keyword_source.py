from os import path

import pytest
from DynamicLibrary import DynamicLibrary
from mockito.matchers import Any


@pytest.fixture(scope='module')
def lib():
    return DynamicLibrary()


@pytest.fixture(scope='module')
def lib_path():
    cur_dir = path.dirname(__file__)
    return path.normpath(path.join(cur_dir, '..', 'atest', 'DynamicLibrary.py'))


@pytest.fixture(scope='module')
def lib_path_components():
    cur_dir = path.dirname(__file__)
    return path.normpath(path.join(cur_dir, '..', 'atest', 'librarycomponents.py'))


def test_location_in_main(lib, lib_path):
    source = lib.get_keyword_source('keyword_in_main')
    assert source == '%s:20' % lib_path


def test_location_in_class(lib, lib_path_components):
    source = lib.get_keyword_source('method')
    assert source == '%s:15' % lib_path_components


def test_location_in_class_custom_keyword_name(lib, lib_path_components):
    source = lib.get_keyword_source('Custom name')
    assert source == '%s:19' % lib_path_components


def test_no_line_number(lib, lib_path, when):
    when(lib)._DynamicCore__get_keyword_line(Any()).thenReturn('')
    source = lib.get_keyword_source('keyword_in_main')
    assert source == lib_path


def test_no_path(lib, when):
    when(lib)._DynamicCore__get_keyword_path(Any()).thenReturn('')
    source = lib.get_keyword_source('keyword_in_main')
    assert source == ':20'


def test_no_path_and_no_line_number(lib, when):
    when(lib)._DynamicCore__get_keyword_path(Any()).thenReturn('')
    when(lib)._DynamicCore__get_keyword_line(Any()).thenReturn('')
    source = lib.get_keyword_source('keyword_in_main')
    assert source is None
