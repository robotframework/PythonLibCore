import sys

import pytest

from robotlibcore import HybridCore

from HybridLibrary import HybridLibrary
from DynamicLibrary import DynamicLibrary
from DynamicLibraryAnnotations import DynamicLibraryAnnotations
if sys.version_info[0] == 3:
    from DynamicLibraryAnnotationPY3 import DynamicLibraryAnnotationsPY3
else:
    DynamicLibraryAnnotationsPY3 = object


@pytest.fixture()
def annotation_lib():
    return DynamicLibraryAnnotations()


@pytest.fixture()
def annotation_lib_py3():
    return DynamicLibraryAnnotationsPY3()


def test_keyword_names():
    expected = ['Custom name',
                'Embedded arguments "${here}"',
                'all_arguments',
                'defaults',
                'doc_and_tags',
                'function',
                'keyword_in_main',
                'mandatory',
                'method',
                'multi_line_doc',
                'one_line_doc',
                'tags',
                'varargs_and_kwargs']
    assert HybridLibrary().get_keyword_names() == expected
    assert DynamicLibrary().get_keyword_names() == expected


def test_dir():
    expected = ['Custom name',
                'Embedded arguments "${here}"',
                '_custom_name',
                '_get_arg_spec',
                '_get_default_types',
                '_get_keyword_tags_supported',
                '_get_members',
                '_get_members_from_instance',
                'add_library_components',
                'all_arguments',
                'attributes',
                'class_attribute',
                'defaults',
                'doc_and_tags',
                'embedded',
                'function',
                'get_keyword_arguments',
                'get_keyword_documentation',
                'get_keyword_names',
                'get_keyword_tags',
                'get_keyword_types',
                'instance_attribute',
                'keyword_in_main',
                'keywords',
                'mandatory',
                'method',
                'multi_line_doc',
                'not_keyword_in_main',
                'one_line_doc',
                'run_keyword',
                'tags',
                'varargs_and_kwargs']
    assert [a for a in dir(DynamicLibrary()) if a[:2] != '__'] == expected
    expected = [e for e in expected if e not in ('_get_arg_spec',
                                                 '_get_keyword_tags_supported',
                                                 'get_keyword_arguments',
                                                 'get_keyword_documentation',
                                                 'get_keyword_tags',
                                                 'run_keyword')]
    expected.remove('get_keyword_types')
    expected.remove('_get_default_types')
    assert [a for a in dir(HybridLibrary()) if a[:2] != '__'] == expected


def test_getattr():
    for lib in [HybridLibrary(), DynamicLibrary()]:
        assert lib.class_attribute == 'not keyword'
        assert lib.instance_attribute == 'not keyword'
        assert lib.function() == 1
        assert lib.method() == 2
        assert lib._custom_name() == 3
        assert getattr(lib, 'Custom name')() == 3
        with pytest.raises(AttributeError) as exc_info:
            lib.non_existing
        assert str(exc_info.value) == \
            "'%s' object has no attribute 'non_existing'" % type(lib).__name__


def test_get_keyword_arguments():
    args = DynamicLibrary().get_keyword_arguments
    assert args('mandatory') == ['arg1', 'arg2']
    assert args('defaults') == ['arg1', 'arg2=default', 'arg3=3']
    assert args('varargs_and_kwargs') == ['*args', '**kws']
    assert args('all_arguments') == ['mandatory', 'default=value', '*varargs', '**kwargs']
    assert args('__init__') == ['arg=None']


def test_get_keyword_documentation():
    doc = DynamicLibrary().get_keyword_documentation
    assert doc('function') == ''
    assert doc('method') == ''
    assert doc('one_line_doc') == 'I got doc!'
    assert doc('multi_line_doc') == 'I got doc!\n\nWith multiple lines!!\nYeah!!!!'
    assert doc('__intro__') == 'General library documentation.'
    assert doc('__init__') == 'Library init doc.'


def test_embed_tags_to_doc_when_get_keyword_tags_is_not_called():
    doc = DynamicLibrary().get_keyword_documentation
    assert doc('tags') == 'Tags: tag, another tag'
    assert doc('doc_and_tags') == 'I got doc!\n\nTags: tag'


def test_get_keyword_tags():
    lib = DynamicLibrary()
    tags = lib.get_keyword_tags
    doc = lib.get_keyword_documentation
    assert tags('tags') == ['tag', 'another tag']
    assert tags('doc_and_tags') == ['tag']
    assert doc('tags') == ''
    assert doc('doc_and_tags') == 'I got doc!'


def test_library_cannot_be_class():
    with pytest.raises(TypeError) as exc_info:
        HybridCore([HybridLibrary])
    assert str(exc_info.value) == \
        "Libraries must be modules or instances, got class 'HybridLibrary' instead."


@pytest.mark.skipif(sys.version_info[0] == 2, reason='Only applicable on Py 3')
def test_get_keyword_types_typing(annotation_lib_py3):
    types = annotation_lib_py3.get_keyword_types('kw_annotated_type')
    assert types == {'arg': int}


def test_get_keyword_types_no_args(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_no_args')
    assert types == {}


def test_get_keyword_types_no_type(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_no_type')
    assert types == {}


def test_get_keyword_types_from_deco_as_list(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_types_from_deco_as_list')
    assert types == [int, list]


def test_get_keyword_types_from_deco_as_dict(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_types_from_deco_as_dict')
    assert types == {'arg1': int, 'arg2': bool}


def test_get_keyword_types_from_default_type(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_types_from_default_type')
    assert types == {'arg1': bool, 'arg2': type(None)}


def test_get_keyword_types_from_default_varargs(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_types_from_varargs')
    assert types == {'arg': bool, 'varargs': list}
    assert False, 'Talk with Pekka about the correct type.'

def test_get_keyword_types_from_default_kwargs(annotation_lib):
    types = annotation_lib.get_keyword_types('kw_types_from_kwargs')
    assert types == {'kwargs': dict}
    assert False, 'Talk with Pekka about the correct type.'


@pytest.mark.skipif(sys.version_info[0] == 2, reason='Only applicable on Py 3')
def test_get_keyword_types_deco_and_typing(annotation_lib_py3):
    types = annotation_lib_py3.get_keyword_types('kw_types_from_deco_and_annotation')
    assert types == {'arg1': bool, 'arg2': bool}


@pytest.mark.skipif(sys.version_info[0] == 2, reason='Only applicable on Py 3')
def test_get_keyword_types_typing_and_default(annotation_lib_py3):
    types = annotation_lib_py3.get_keyword_types('kw_annotated_type_with_default')
    assert types == {'arg': str}


@pytest.mark.skipif(sys.version_info[0] > 2, reason='Only applicable on Py 2')
def test_library_cannot_be_old_style_class_instance():
    class OldStyle:
        pass
    with pytest.raises(TypeError) as exc_info:
        HybridCore([OldStyle()])
    assert str(exc_info.value) == \
           "Libraries must be modules or new-style class instances, got old-style class 'OldStyle' instead."
