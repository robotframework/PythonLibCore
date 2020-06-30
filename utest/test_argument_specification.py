import pytest
from robot import __version__ as robot_version

from robotlibcore import ArgumentSpecification


def test_no_args():
    spec = ArgumentSpecification()
    assert spec.get_arguments() == ()


def test_positional_args():
    spec = ArgumentSpecification(positional=[])
    assert spec.get_arguments() == ()
    spec = ArgumentSpecification(positional=['arg'])
    assert spec.get_arguments() == ('arg', )
    spec = ArgumentSpecification(positional=['mandatory1', 'mandatory2'])
    assert spec.get_arguments() == ('mandatory1', 'mandatory2')


@pytest.mark.skipif(robot_version < '3.2', reason='For RF 3.2 or greater')
def test_default_args_rf32():
    spec = ArgumentSpecification(positional=[], defaults=[('arg', False)])
    assert spec.get_arguments() == (('arg', False), )
    spec = ArgumentSpecification(positional=['mandatory'], defaults=[('arg1', False), ('arg2', None)])
    assert spec.get_arguments() == ('mandatory', ('arg1', False), ('arg2', None))


@pytest.mark.skipif(robot_version >= '3.2', reason='For RF 3.1')
def test_default_args_rf31():
    spec = ArgumentSpecification(positional=[], defaults=[('arg', False)])
    assert spec.get_arguments() == ('arg=False', )
    spec = ArgumentSpecification(positional=['mandatory'], defaults=[('arg1', False), ('arg2', None)])
    assert spec.get_arguments() == ('mandatory', 'arg1=False', 'arg2=None')


def test_varargs():
    spec = ArgumentSpecification(varargs='*varargs')
    assert spec.get_arguments() == ('*varargs', )


@pytest.mark.skipif(robot_version < '3.2', reason='For RF 3.2 or greater')
def test_varargs_rf32():
    spec = ArgumentSpecification(positional=['mandatory'], defaults=[('arg', 'str')], varargs='*varargs')
    assert spec.get_arguments() == ('mandatory', ('arg', 'str'), '*varargs')


@pytest.mark.skipif(robot_version >= '3.2', reason='For RF 3.1')
def test_varargs_rf31():
    spec = ArgumentSpecification(positional=['mandatory'], defaults=[('arg', 'str')], varargs='*varargs')
    assert spec.get_arguments() == ('mandatory', 'arg=str', '*varargs')


def test_keyword_args():
    spec = ArgumentSpecification(kwargs='**kwargs')
    assert spec.get_arguments() == ('**kwargs', )


@pytest.mark.skipif(robot_version < '3.2', reason='For RF 3.2 or greater')
def test_keyword_args_rf32():
    spec = ArgumentSpecification(
        positional=['mandatory'],
        defaults=[('arg', 'str')],
        varargs='*varargs',
        kwargs='**kwargs'
    )
    assert spec.get_arguments() == ('mandatory', ('arg', 'str'), '*varargs', '**kwargs')


@pytest.mark.skipif(robot_version >= '3.2', reason='For RF 3.1')
def test_keyword_args_rf31():
    spec = ArgumentSpecification(
        positional=['mandatory'],
        defaults=[('arg', 'str')],
        varargs='*varargs',
        kwargs='**kwargs'
    )
    assert spec.get_arguments() == ('mandatory', 'arg=str', '*varargs', '**kwargs')


def test_kw_only_args():
    spec = ArgumentSpecification(kwonlyargs=['kw_only_arg'])
    assert spec.get_arguments() == ('kw_only_arg', )
    spec = ArgumentSpecification(varargs='*varargs', kwonlyargs=['kw_only_arg'])
    assert spec.get_arguments() == ('*varargs', 'kw_only_arg')


@pytest.mark.skipif(robot_version < '3.2', reason='For RF 3.2 or greater')
def test_kw_only_args_rf32():
    spec = ArgumentSpecification(defaults=[('kw_only_arg', None)], kwonlyargs=['kw_only_arg'])
    assert spec.get_arguments() == (('kw_only_arg', None), 'kw_only_arg')
    spec = ArgumentSpecification(
        positional=['mandatory'],
        defaults=[('arg', str), ('kw_only_arg', None)],
        varargs='*varargs',
        kwonlyargs=['kw_only_arg', 'kw_only'],
        kwargs='**kwargs'
    )
    assert spec.get_arguments() == (
        'mandatory',
        ('arg', str),
        ('kw_only_arg', None),
        '*varargs',
        'kw_only_arg',
        'kw_only',
        '**kwargs'
    )


@pytest.mark.skipif(robot_version >= '3.2', reason='For RF 3.1')
def test_kw_only_args_rf31():
    spec = ArgumentSpecification(defaults=[('kw_only_arg', None)], kwonlyargs=['kw_only_arg'])
    assert spec.get_arguments() == ('kw_only_arg=None', 'kw_only_arg')
    spec = ArgumentSpecification(
        positional=['mandatory'],
        defaults=[('arg', 'str'), ('kw_only_arg', None)],
        varargs='*varargs',
        kwonlyargs=['kw_only_arg', 'kw_only'],
        kwargs='**kwargs'
    )
    assert spec.get_arguments() == (
        'mandatory',
        'arg=str',
        'kw_only_arg=None',
        '*varargs',
        'kw_only_arg',
        'kw_only',
        '**kwargs'
    )
