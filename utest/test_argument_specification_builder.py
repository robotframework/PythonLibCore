from robotlibcore import ArgumentBuilder, PY2

from DynamicLibrary import DynamicLibrary

if not PY2:
    from DynamicTypesLibrary import DynamicTypesLibrary


def test_documentation():
    spec = ArgumentBuilder.build(DynamicLibrary().one_line_doc)
    assert spec.documentation == 'I got doc!'
    spec = ArgumentBuilder.build(DynamicLibrary().multi_line_doc)
    assert spec.documentation == 'I got doc!\n\nWith multiple lines!!\nYeah!!!!'
    spec = ArgumentBuilder.build(DynamicLibrary().__init__)
    assert spec.documentation == 'Library init doc.'


def test_positional_argument():
    spec = ArgumentBuilder.build(DynamicTypesLibrary().keyword_with_types)
    assert spec.get_arguments() == ('arg1', )


def test_varargs_and_kwargs_argument():
    spec = ArgumentBuilder.build(DynamicTypesLibrary().varargs_and_kwargs)
    assert spec.get_arguments() == ('*args', '**kwargs')

