import sys

import pytest
from robot import __version__ as robot__version

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
                '_DynamicCore__get_arg_spec',
                '_DynamicCore__get_keyword',
                '_DynamicCore__get_keyword_line',
                '_DynamicCore__get_keyword_path',
                '_DynamicCore__get_keyword_tags_supported',
                '_DynamicCore__get_typing_hints',
                '_DynamicCore__join_defaults_with_types',
                '_DynamicCore__new_arg_spec',
                '_DynamicCore__old_arg_spec',
                '_HybridCore__get_members',
                '_HybridCore__get_members_from_instance',
                '_custom_name',
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
                'get_keyword_source',
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
    expected = [e for e in expected if e not in ('_DynamicCore__get_typing_hints',
                                                 '_DynamicCore__get_arg_spec',
                                                 '_DynamicCore__get_keyword',
                                                 '_DynamicCore__get_keyword_line',
                                                 '_DynamicCore__get_keyword_path',
                                                 '_DynamicCore__get_keyword_tags_supported',
                                                 '_DynamicCore__join_defaults_with_types',
                                                 '_DynamicCore__new_arg_spec',
                                                 '_DynamicCore__old_arg_spec',
                                                 'get_keyword_arguments',
                                                 'get_keyword_documentation',
                                                 'get_keyword_source',
                                                 'get_keyword_tags',
                                                 'run_keyword',
                                                 'get_keyword_types')]
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

@pytest.mark.skipif(robot__version >= '3.2', reason='For RF 3.1')
def test_get_keyword_arguments_rf31():
    args = DynamicLibrary().get_keyword_arguments
    assert args('mandatory') == ['arg1', 'arg2']
    assert args('defaults') == ['arg1', 'arg2=default', 'arg3=3']
    assert args('varargs_and_kwargs') == ['*args', '**kws']
    assert args('all_arguments') == ['mandatory', 'default=value', '*varargs', '**kwargs']
    assert args('__init__') == ['arg=None']
    assert args('__foobar__') == []


@pytest.mark.skipif(robot__version < '3.2', reason='For RF 3.2 or greater')
def test_get_keyword_arguments_rf32():
    args = DynamicLibrary().get_keyword_arguments
    assert args('mandatory') == [('arg1', ), ('arg2', )]
    assert args('defaults') == [('arg1', ), ('arg2', 'default'), ('arg3', 3)]
    assert args('varargs_and_kwargs') == [('*args', ), ('**kws', )]
    assert args('all_arguments') == [('mandatory', ), ('default', 'value'), ('*varargs', ), ('**kwargs', )]
    assert args('__init__') == [('arg', None)]
    assert args('__foobar__') == [()]


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
