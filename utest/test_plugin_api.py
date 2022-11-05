import pytest

from robotlibcore import Module, PluginParser, PluginError
import my_plugin_test


@pytest.fixture(scope="module")
def plugin_parser() -> PluginParser:
    return PluginParser()


def test_no_plugins_parsing(plugin_parser):
    for item in [None, ""]:
        assert plugin_parser._string_to_modules(item) == []


def test_plugins_string_to_modules(plugin_parser):
    result = plugin_parser._string_to_modules("foo/bar.by")
    assert result == [Module("foo/bar.by", [], {})]
    result = plugin_parser._string_to_modules("path.to.MyLibrary,path.to.OtherLibrary")
    assert result == [
        Module("path.to.MyLibrary", [], {}),
        Module("path.to.OtherLibrary", [], {})
    ]
    result = plugin_parser._string_to_modules("path.to.MyLibrary , path.to.OtherLibrary")
    assert result == [
        Module("path.to.MyLibrary", [], {}),
        Module("path.to.OtherLibrary", [], {})
    ]
    result = plugin_parser._string_to_modules("path.to.MyLibrary;foo;bar , path.to.OtherLibrary;1")
    assert result == [
        Module("path.to.MyLibrary", ["foo", "bar"], {}),
        Module("path.to.OtherLibrary", ["1"], {})
    ]
    result = plugin_parser._string_to_modules("PluginWithKwArgs.py;kw1=Text1;kw2=Text2")
    assert result == [
        Module("PluginWithKwArgs.py", [], {"kw1": "Text1", "kw2": "Text2"}),
    ]


def test_parse_plugins(plugin_parser):
    plugins = plugin_parser.parse_plugins("my_plugin_test.TestClass")
    assert len(plugins) == 1
    assert isinstance(plugins[0], my_plugin_test.TestClass)
    plugins = plugin_parser.parse_plugins("my_plugin_test.TestClass,my_plugin_test.TestClassWithBase")
    assert len(plugins) == 2
    assert isinstance(plugins[0], my_plugin_test.TestClass)
    assert isinstance(plugins[1], my_plugin_test.TestClassWithBase)


def test_parse_plugins_with_base():
    parser = PluginParser(my_plugin_test.LibraryBase)
    plugins = parser.parse_plugins("my_plugin_test.TestClassWithBase")
    assert len(plugins) == 1
    assert isinstance(plugins[0], my_plugin_test.TestClassWithBase)
    with pytest.raises(PluginError) as excinfo:
        parser.parse_plugins("my_plugin_test.TestClass")
    assert "Plugin does not inherit <class 'my_plugin_test.LibraryBase'>" in str(excinfo.value)


def test_plugin_keywords(plugin_parser):
    plugins = plugin_parser.parse_plugins("my_plugin_test.TestClass,my_plugin_test.TestClassWithBase")
    keywords = plugin_parser.get_plugin_keywords(plugins)
    assert len(keywords) == 2
    assert keywords[0] == "another_keyword"
    assert keywords[1] == "new_keyword"


def test_plugin_python_objects():
    class PythonObject:
        x = 1
        y = 2
    python_object = PythonObject()
    parser = PluginParser(my_plugin_test.LibraryBase, [python_object])
    plugins = parser.parse_plugins("my_plugin_test.TestPluginWithPythonArgs;4")
    assert len(plugins) == 1
    plugin = plugins[0]
    assert plugin.python_class.x == 1
    assert plugin.python_class.y == 2

