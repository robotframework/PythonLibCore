import typing

from DynamicLibraryTypes import DynamicLibraryTypes


def test_using_keyword_types():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_with_types')
    assert types == {'arg1': str}


def test_types_disabled():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_with_disabled_types')
    assert types == {}


def test_one_keyword_type_defined():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_with_one_type')
    assert types == {'arg1': str}


def test_keyword_no_args():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_with_no_args')
    assert types == {}


def test_single_annotation():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_with_one_annotation')
    assert types == {'arg': str}


def test_multiple_annotations():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_with_multiple_annotations')
    assert types == {'arg1': str, 'arg2': typing.List}
