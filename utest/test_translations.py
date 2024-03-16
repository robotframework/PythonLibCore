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
