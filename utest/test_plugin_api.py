import pytest

from robotlibcore import Module, PluginParser


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
