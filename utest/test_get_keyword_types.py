from atest.DynamicLibraryTypes import DynamicLibraryTypes


def test_get_keyword_types():
    lib = DynamicLibraryTypes()
    types = lib.get_keyword_types('keyword_in_main')
    assert types == {'arg1': str}