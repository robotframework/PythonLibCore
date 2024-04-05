from pathlib import Path

import pytest
from SmallLibrary import SmallLibrary


@pytest.fixture(scope="module")
def lib():
    translation = Path(__file__).parent.parent / "atest" / "translation.json"
    return SmallLibrary(translation=translation)


def test_invalid_translation():
    translation = Path(__file__)
    assert SmallLibrary(translation=translation)


def test_translations_names(lib: SmallLibrary):
    keywords = lib.keywords_spec
    assert "other_name" in keywords
    assert "name_changed_again" in keywords


def test_translations_docs(lib: SmallLibrary):
    keywords = lib.keywords_spec
    kw = keywords["other_name"]
    assert kw.documentation == "This is new doc"
    kw = keywords["name_changed_again"]
    assert kw.documentation == "This is also replaced.\n\nnew line."


def test_init_and_lib_docs(lib: SmallLibrary):
    keywords = lib.keywords_spec
    init = keywords["__init__"]
    assert init.documentation == "Replaces init docs with this one."
    doc = lib.get_keyword_documentation("__intro__")
    assert doc == "New __intro__ documentation is here."


def test_not_translated(lib: SmallLibrary):
    keywords = lib.keywords_spec
    assert "not_translated" in keywords
    doc = lib.get_keyword_documentation("not_translated")
    assert doc == "This is not replaced."


def test_doc_not_translated(lib: SmallLibrary):
    keywords = lib.keywords_spec
    assert "doc_not_translated" not in keywords
    assert "this_is_replaced" in keywords
    doc = lib.get_keyword_documentation("this_is_replaced")
    assert doc == "This is not replaced also."


def test_kw_not_translated_but_doc_is(lib: SmallLibrary):
    keywords = lib.keywords_spec
    assert "kw_not_translated" in keywords
    doc = lib.get_keyword_documentation("kw_not_translated")
    assert doc == "Here is new doc"


def test_rf_name_not_in_keywords():
    translation = Path(__file__).parent.parent / "atest" / "translation.json"
    lib = SmallLibrary(translation=translation)
    kw = lib.keywords
    assert "Execute SomeThing" not in kw, f"Execute SomeThing should not be present: {kw}"
    assert len(kw) == 6, f"Too many keywords: {kw}"
