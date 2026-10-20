"""Определение расширения: выжимка по адресу имени собирается из текста, а не пишется руками.

Проверяется связка, ради которой это сделано. Адрес имени расширения обещает место, и место
теперь есть: машиночитаемая выжимка. Если определение устареет относительно текста, обещание
снова станет пустым, поэтому тест сверяет записанный файл с собранным, а перечни кодов с
самим текстом.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.build_extension_definition import (  # noqa: E402
    EXTENSION_URI,
    build_definition,
    build_from_disk,
    read_clauses,
)

DEFINITION = ROOT / "docs" / "extension-definition.json"
CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def _definition() -> dict:
    return json.loads(DEFINITION.read_text(encoding="utf-8"))


def test_the_recorded_definition_matches_the_generated_one():
    assert DEFINITION.read_text(encoding="utf-8") == build_from_disk(), \
        "docs/extension-definition.json drifted from SPEC.en.md"


def test_the_definition_carries_the_version_of_the_text():
    markdown = (ROOT / "SPEC.en.md").read_text(encoding="utf-8")
    version = re.search(r"^# ARLI Discovery Extension v(\d+\.\d+\.\d+)", markdown, re.M).group(1)
    assert _definition()["version"] == version


def test_the_extension_uri_in_the_definition_is_the_one_in_the_text():
    markdown = (ROOT / "SPEC.en.md").read_text(encoding="utf-8")
    assert EXTENSION_URI in markdown
    assert _definition()["uri"] == EXTENSION_URI


def test_every_published_list_matches_the_text_it_comes_from():
    markdown = (ROOT / "SPEC.en.md").read_text(encoding="utf-8")
    expected = build_definition(markdown)["lists"]
    published = _definition()["lists"]
    assert published == expected
    # перечни не пустые и не выродились в один код
    for name, codes in published.items():
        assert len(codes) >= 3, f"{name} looks broken: {codes}"


def test_the_pair_level_refusals_include_the_code_from_clause_13_5():
    """Найдено при сборке: в 6.7 не хватало кода, введённого в 13.5. Теперь списки сходятся."""
    openings = _definition()["lists"]["opening_refusals"]
    assert "below_required_level" in openings
    assert len(openings) == 7


def test_the_definition_names_the_two_prohibitions_and_the_licence():
    definition = _definition()
    joined = " ".join(definition["notes"])
    assert "not evidence of the identity" in joined
    assert "does not\ntransfer" in joined or "transfer between networks" in joined
    assert "reserved" in definition["licence"]


def test_the_definition_is_english_only():
    assert not CYRILLIC.search(DEFINITION.read_text(encoding="utf-8"))


def test_the_clause_reader_finds_the_lists_where_they_live():
    clauses = read_clauses((ROOT / "SPEC.en.md").read_text(encoding="utf-8"))
    for number in ("1.2", "4.11", "6.6", "6.7", "6.9", "8.5", "13.1", "13.4"):
        assert number in clauses, number
