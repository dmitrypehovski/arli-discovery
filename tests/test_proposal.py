"""Предложение про якорь доверия: черновик для юриста, а не обещание.

Главная проверка здесь защищает от самой опасной ошибки в этом месте: обещать уровень
доверия раньше, чем юрист ответил. Нормативный текст обязан оставаться чистым, а черновик
обязан быть помечен как необязательный. Иначе мы либо публикуем обещание, которого не
выполним, либо тихо вводим его через документ, который никто не считает нормативным.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = "PROPOSAL-trust-anchor.md"

# Обещания, которых в нормативном тексте не должно быть никогда: они читаются как гарантия
# личности, а гарантию личности мы не выдаём ни при каком ответе юриста.
FORBIDDEN_PROMISES = (
    "identity guarantee",
    "guarantees identity",
    "proves identity",
    "trust anchor",
    "verify identity",
)


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_the_normative_text_never_promises_identity():
    english = _read("SPEC.en.md")
    russian = _read("SPEC.md")
    for promise in FORBIDDEN_PROMISES:
        assert promise not in english, f"the normative text promises {promise!r}"
        assert promise not in russian


def test_the_normative_text_carries_the_two_prohibitions():
    """Уровни описаны, но с двумя запретами: не личность и не переносимость."""
    english = _read("SPEC.en.md")
    assert "13.6" in english
    assert "MUST NOT be presented as evidence of the identity" in english
    assert "MUST NOT be treated as transferable between networks" in english


def test_the_normative_text_keeps_the_issuance_question_out():
    """Кто вправе выдавать подтверждения, спецификация не решает."""
    english = _read("SPEC.en.md")
    assert "relays and verifies statements made by others" in english
    for overreach in ("MUST issue", "certifies that the person"):
        assert overreach not in english


def test_the_proposal_says_loudly_that_it_is_not_normative():
    proposal = _read(PROPOSAL)
    assert "Not normative, not implemented" in proposal
    assert "No clause of this\nproposal is part of" in proposal or "not part of `SPEC.en.md`" in proposal
    assert "draft for legal review" in proposal


def test_the_proposal_states_the_levels_and_their_limits():
    proposal = _read(PROPOSAL)
    for level in ("Level 0, declared", "Level 1", "Level 2"):
        assert level in proposal, level
    # ограничения уровня обязаны быть сказаны прямо: иначе уровень прочтут как гарантию
    assert "never a property of a person" in proposal
    assert "must never be written as if it did" in proposal


def test_the_proposal_names_what_we_will_not_do_whatever_the_answer():
    proposal = _read(PROPOSAL)
    assert "will not buy external databases of people" in proposal
    assert "without their separate, recorded consent" in proposal
    assert "will not sell the level as a guarantee of identity" in proposal


def test_the_proposal_carries_the_questions_for_counsel():
    proposal = _read(PROPOSAL)
    questions = re.findall(r"^\d+\. ", proposal, re.M)
    assert len(questions) >= 6, "the legal review needs concrete questions"
    assert "regulated activity" in proposal
    assert "retention period" in proposal


def test_every_legal_answer_has_a_named_cost():
    """Ответ юриста без цены ответа бесполезен: нужны варианты и их последствия."""
    proposal = _read(PROPOSAL)
    for branch in ("Yes, we may issue", "No, we may not issue, but may relay", "No, and no relay either"):
        assert branch in proposal, branch


def test_the_publication_plan_names_both_addresses_honestly():
    """Переносы строк не должны прятать смысл: сверяем текст с приведёнными пробелами."""
    plan = " ".join(_read("PUBLISHING.md").split())
    assert "https://github.com/dmitrypehovski/arli-discovery" in plan
    assert "https://github.com/dmitrypehovski/arli-discovery-engine" in plan
    assert "personal account" in plan
    # перенос в организацию обязан быть назван как сохраняющий историю и ссылки
    assert "a transfer keeps the history and the links" in plan


def test_the_house_readme_points_at_the_draft():
    readme = _read("README.md")
    assert PROPOSAL in readme
    assert "not normative" in readme.lower()
