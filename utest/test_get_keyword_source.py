import inspect
from pathlib import Path

import pytest
from DynamicLibrary import DynamicLibrary
from DynamicTypesLibrary import DynamicTypesLibrary
from mockito.matchers import Any


@pytest.fixture(scope="module")
def lib():
    return DynamicLibrary()


@pytest.fixture(scope="module")
def lib_types():
    return DynamicTypesLibrary()


@pytest.fixture(scope="module")
def cur_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="module")
def lib_path(cur_dir) -> Path:
    path = cur_dir / ".." / "atest" / "DynamicLibrary.py"
    return path.resolve()


@pytest.fixture(scope="module")
def lib_path_components(cur_dir) -> Path:
    path = cur_dir / ".." / "atest" / "librarycomponents.py"
    return path.resolve()


@pytest.fixture(scope="module")
def lib_path_types(cur_dir) -> Path:
    path = cur_dir / ".." / "atest" / "DynamicTypesLibrary.py"
    return path.resolve()


def test_location_in_main(lib, lib_path):
    source = lib.get_keyword_source("keyword_in_main")
    assert source == f"{lib_path}:19"


def test_location_in_class(lib, lib_path_components):
    source = lib.get_keyword_source("method")
    assert source == f"{lib_path_components}:14"


def test_decorator_wrapper(lib_types, lib_path_types):
    source = lib_types.get_keyword_source("keyword_wrapped")
    assert source == f"{lib_path_types}:73"


def test_location_in_class_custom_keyword_name(lib, lib_path_components):
    source = lib.get_keyword_source("Custom name")
    assert source == f"{lib_path_components}:19"


def test_no_line_number(lib, lib_path, when):
    when(lib)._DynamicCore__get_keyword_line(Any()).thenReturn(None)
    source = lib.get_keyword_source("keyword_in_main")
    assert Path(source) == lib_path


def test_no_path(lib, when):
    when(lib)._DynamicCore__get_keyword_path(Any()).thenReturn(None)
    source = lib.get_keyword_source("keyword_in_main")
    assert source == ":19"


def test_no_path_and_no_line_number(lib, when):
    when(lib)._DynamicCore__get_keyword_path(Any()).thenReturn(None)
    when(lib)._DynamicCore__get_keyword_line(Any()).thenReturn(None)
    source = lib.get_keyword_source("keyword_in_main")
    assert source is None


def test_def_in_decorator(lib_types, lib_path_types):
    source = lib_types.get_keyword_source("keyword_with_def_deco")
    assert source == f"{lib_path_types}:67"


def test_error_in_getfile(lib, when):
    when(inspect).getfile(Any()).thenRaise(TypeError("Some message"))
    source = lib.get_keyword_source("keyword_in_main")
    assert source is None


def test_error_in_line_number(lib, when, lib_path):
    when(inspect).getsourcelines(Any()).thenRaise(IOError("Some message"))
    source = lib.get_keyword_source("keyword_in_main")
    assert Path(source) == lib_path
