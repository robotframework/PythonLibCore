import sys

import pytest

from robotlibcore import HybridCore

from HybridLibrary import HybridLibrary
from DynamicLibrary import DynamicLibrary


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
                'add_library_components',
                'all_arguments',
                'class_attribute',
                'defaults',
                'doc_and_tags',
                'function',
                'get_keyword_arguments',
                'get_keyword_documentation',
                'get_keyword_names',
                'get_keyword_tags',
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
    assert [a for a in dir(DynamicLibrary()) if a[0] != '_'] == expected
    expected = [e for e in expected if e not in ('get_keyword_arguments',
                                                 'get_keyword_documentation',
                                                 'get_keyword_tags',
                                                 'run_keyword')]
    assert [a for a in dir(HybridLibrary()) if a[0] != '_'] == expected


def test_getattr():
    for lib in [HybridLibrary(), DynamicLibrary()]:
        assert lib.class_attribute == 'not keyword'
        assert lib.instance_attribute == 'not keyword'
        assert lib.function() == 1
        assert lib.method() == 2
        assert getattr(lib, 'Custom name')() == 3
        with pytest.raises(AttributeError) as exc_info:
            lib.attribute
        assert str(exc_info.value) == \
            "'%s' object has no attribute 'attribute'" % type(lib).__name__


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


@pytest.mark.skipif(sys.version_info[0] > 2, reason='Only applicable on Py 2')
def test_library_cannot_be_old_style_class_instance():
    class OldStyle:
        pass
    with pytest.raises(TypeError) as exc_info:
        HybridCore([OldStyle()])
    assert str(exc_info.value) == \
           "Libraries must be modules or new-style class instances, got old-style class 'OldStyle' instead."
