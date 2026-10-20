"""Проверки самого нормативного текста: он живёт отдельно и держит себя сам.

Здесь проверяется то, за что отвечает текст, а не код. Две версии одного обещания обязаны
совпадать по номерам пунктов, английский текст обязан быть английским, страница обязана
совпадать с текстом, лицензия обязана быть официальной. Проверка соответствия движка этому
тексту живёт в движке: он зависит от нас, а не мы от него.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
EXTENSION_VERSION = "1.2.0"
CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_the_text_is_at_the_declared_extension_version():
    english = _read("SPEC.en.md")
    assert english.startswith(f"# ARLI Discovery Extension v{EXTENSION_VERSION}")
    assert "https://arliwork.com/a2a/extensions/arli.discovery.v1" in english


def test_the_published_text_contains_no_cyrillic():
    assert not CYRILLIC.search(_read("SPEC.en.md"))


def test_the_two_texts_agree_on_sections_and_clause_numbers():
    russian = _read("SPEC.md")
    english = _read("SPEC.en.md")
    clause = re.compile(r"^(\d+\.\d+)\.", re.M)
    section = re.compile(r"^## (.+)$", re.M)
    assert clause.findall(russian) == clause.findall(english), "clause numbers diverged"
    assert len(section.findall(russian)) == len(section.findall(english))
    assert len(clause.findall(english)) >= 60


def test_the_page_matches_the_text_it_is_generated_from():
    import sys

    sys.path.insert(0, str(ROOT))
    from tools.build_page import build_from_disk

    recorded = (ROOT / "docs" / "spec.html").read_text(encoding="utf-8")
    assert recorded == build_from_disk(), "docs/spec.html drifted from SPEC.en.md"


def test_the_page_carries_every_clause_and_the_conformance_command():
    page = (ROOT / "docs" / "spec.html").read_text(encoding="utf-8")
    english = _read("SPEC.en.md")
    for number in re.findall(r"^(\d+\.\d+)\.", english, re.M):
        assert f'<span class="id">{number}</span>' in page, number
    assert "arli_engine.conformance" in page
    assert not CYRILLIC.search(page)


def test_license_and_notice_are_in_place_and_official():
    license_text = _read("LICENSE")
    assert hashlib.sha256(license_text.encode()).hexdigest() == CANONICAL_LICENSE_SHA256
    notice = _read("NOTICE")
    assert "Shenzhen Capernaum Technology Co., Ltd." in notice
    assert "NOT licensed under" in notice


def test_the_house_rules_are_stated():
    readme = _read("README.md")
    assert "the text is published" in readme
    assert "https://arliwork.com/spec/" in readme
    # адрес площадки и наш зеркальный адрес обязаны быть названы оба: читатель смотрит в разные места
    assert "https://github.com/dmitrypehovski/arli-discovery" in readme
    assert "https://arliwork.com/plugin/arli-spec.git" in readme
    assert "separate artefact" in readme
    plan = _read("PUBLISHING.md")
    for kept in ("network and the service", "conformance mark"):
        assert kept in plan
    # состояние публикации обязано быть названо точно: вышли и текст, и код
    assert "Status: **published.**" in plan
    assert "went out unanswered" in plan
    policy = _read("TRADEMARK.md")
    assert "ARLI verified" in policy


def test_the_history_speaks_about_the_extension_only():
    history = _read("CHANGELOG.md")
    assert "Закрытые перечни" in history or "Bindings" in history or "привязки" in history.lower()
    # история расширения не должна выдавать себя за историю пакета
    assert "Package version" not in history
