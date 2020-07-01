from DynamicLibrary import DynamicLibrary
from robotlibcore import ArgumentBuilder


def test_documentation():
    spec = ArgumentBuilder.build(DynamicLibrary().one_line_doc)
    assert spec.documentation == 'I got doc!'
    spec = ArgumentBuilder.build(DynamicLibrary().multi_line_doc)
    assert spec.documentation == 'I got doc!\n\nWith multiple lines!!\nYeah!!!!'
    spec = ArgumentBuilder.build(DynamicLibrary().__init__)
    assert spec.documentation == 'Library init doc.'

