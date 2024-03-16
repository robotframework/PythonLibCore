import json

import pytest
from approvaltests.approvals import verify
from DynamicLibrary import DynamicLibrary
from DynamicTypesAnnotationsLibrary import DynamicTypesAnnotationsLibrary
from HybridLibrary import HybridLibrary
from robotlibcore import HybridCore, NoKeywordFound


@pytest.fixture(scope="module")
def dyn_lib():
    return DynamicLibrary()


def test_keyword_names_hybrid():
    verify(json.dumps(HybridLibrary().get_keyword_names(), indent=4))


def test_keyword_names_dynamic():
    verify(json.dumps(DynamicLibrary().get_keyword_names(), indent=4))


def test_dir_dyn_lib():
    result = [a for a in dir(DynamicLibrary()) if a[:2] != "__"]
    result = json.dumps(result, indent=4)
    verify(result)


def test_dir_hubrid_lib():
    result = [a for a in dir(HybridLibrary()) if a[:2] != "__"]
    result = json.dumps(result, indent=4)
    verify(result)


def test_getattr():
    for lib in [HybridLibrary(), DynamicLibrary()]:
        assert lib.class_attribute == "not keyword"
        assert lib.instance_attribute == "not keyword"
        assert lib.function() == 1
        assert lib.method() == 2
        assert lib._other_name_here() == 3
        assert getattr(lib, "Custom name")() == 3
        with pytest.raises(AttributeError) as exc_info:
            lib.non_existing
        assert str(exc_info.value) == "'%s' object has no attribute 'non_existing'" % type(lib).__name__


def test_get_keyword_arguments():
    args = DynamicLibrary().get_keyword_arguments
    assert args("mandatory") == ["arg1", "arg2"]
    assert args("defaults") == ["arg1", ("arg2", "default"), ("arg3", 3)]
    assert args("varargs_and_kwargs") == ["*args", "**kws"]
    assert args("kwargs_only") == ["**kws"]
    assert args("all_arguments") == ["mandatory", ("default", "value"), "*varargs", "**kwargs"]
    assert args("__init__") == [("arg", None)]
    with pytest.raises(NoKeywordFound):
        args("__foobar__")


def test_keyword_only_arguments_for_get_keyword_arguments():
    args = DynamicTypesAnnotationsLibrary(1).get_keyword_arguments
    assert args("keyword_only_arguments") == ["*varargs", ("some", 111)]
    assert args("keyword_only_arguments_many") == ["*varargs", ("some", "value"), ("other", None)]
    assert args("keyword_only_arguments_no_default") == ["*varargs", "other"]
    assert args("keyword_only_arguments_default_and_no_default") == ["*varargs", "other", ("value", False)]
    all_args = ["mandatory", ("positional", 1), "*varargs", "other", ("value", False), "**kwargs"]
    assert args("keyword_all_args") == all_args
    assert args("keyword_with_deco_and_signature") == [("arg1", False), ("arg2", False)]


def test_named_only_argumens():
    args = DynamicTypesAnnotationsLibrary(1).get_keyword_arguments
    assert args("kw_with_named_arguments") == ["*", "arg"]
    assert args("kw_with_many_named_arguments") == ["*", "arg1", "arg2"]
    assert args("kw_with_named_arguments_and_variable_number_args") == ["*varargs", "arg"]
    assert args("kw_with_many_named_arguments_with_default") == ["*", "arg1", "arg2"]
    assert args("kw_with_positional_and_named_arguments") == ["arg1", "*", "arg2"]
    assert args("kw_with_positional_and_named_arguments_with_defaults") == [("arg1", 1), "*", ("arg2", "foobar")]


def test_get_keyword_documentation():
    doc = DynamicLibrary().get_keyword_documentation
    assert doc("function") == ""
    assert doc("method") == ""
    assert doc("one_line_doc") == "I got doc!"
    assert doc("multi_line_doc") == "I got doc!\n\nWith multiple lines!!\nYeah!!!!"
    assert doc("__intro__") == "General library documentation."
    assert doc("__init__") == "Library init doc."


def test_get_keyword_tags():
    lib = DynamicLibrary()
    tags = lib.get_keyword_tags
    doc = lib.get_keyword_documentation
    assert tags("tags") == ["tag", "another tag"]
    assert tags("doc_and_tags") == ["tag"]
    assert doc("tags") == ""
    assert doc("doc_and_tags") == "I got doc!"


def test_library_cannot_be_class():
    with pytest.raises(TypeError) as exc_info:
        HybridCore([HybridLibrary])
    assert str(exc_info.value) == "Libraries must be modules or instances, got class 'HybridLibrary' instead."
