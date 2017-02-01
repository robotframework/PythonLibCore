import pytest

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
                'all_arguments',
                'class_attribute',
                'defaults',
                'doc_and_tags',
                'function',
                'get_keyword_arguments',
                'get_keyword_documentation',
                'get_keyword_names',
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
                                                 'run_keyword')]
    assert [a for a in dir(HybridLibrary()) if a[0] != '_'] == expected


def test_getattr():
    for lib in [HybridLibrary(), DynamicLibrary()]:
        assert lib.class_attribute == 'not keyword'
        assert lib.instance_attribute == 'not keyword'
        assert lib.function() == 1
        assert lib.method() == 2
        assert getattr(lib, 'Custom name')() == 3
        with pytest.raises(AttributeError) as excinfo:
            lib.attribute
        assert str(excinfo.value) == \
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


def test_tags():
    doc = DynamicLibrary().get_keyword_documentation
    assert doc('tags') == 'Tags: tag, another tag'
    assert doc('doc_and_tags') == 'I got doc!\n\nTags: tag'
