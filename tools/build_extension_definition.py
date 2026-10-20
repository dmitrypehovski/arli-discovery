"""Определение расширения по адресу его имени, собранное из нормативного текста.

Зачем. Имя расширения указывает на наш домен: `https://arliwork.com/a2a/extensions/arli.discovery.v1`.
Имя обещает место, и до сих пор места за ним не было: тот, кто открывал адрес, получал ничего.
Определение закрывает обещание и делает его проверяемым: по адресу лежит машиночитаемая
выжимка из текста, а не пересказ руками.

Собирается из `SPEC.en.md`, поэтому отстать от текста не может: тест сверяет записанный
файл с собранным, а прогон сверяет номер версии и перечни кодов с самим текстом.

Запуск: python -m tools.build_extension_definition [путь]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "SPEC.en.md"
DEFAULT_TARGET = ROOT / "docs" / "extension-definition.json"

EXTENSION_URI = "https://arliwork.com/a2a/extensions/arli.discovery.v1"
CONFORMANCE_COMMAND = "python -m arli_engine.conformance --target <url> [--holder <url>]"

# Какие пункты текста несут какие перечни. Список задан номерами осознанно: если пункт
# переедет, сборка обязана сломаться, а не тихо отдать пустой перечень.
LISTS = {
    "1.2": "intent_types",
    "1.3": "intent_statuses",
    "1.4": "provenance",
    "2.5": "operation_availability_codes",
    "4.11": "matching_refusals",
    "5.5": "confidence_values",
    "6.2": "negotiation_actions",
    "6.6": "turn_refusals",
    "6.7": "opening_refusals",
    "6.9": "intent_refusals",
    "8.5": "retention_refusals",
    "12.2": "binding_naming_rule_has_no_codes",
    "13.1": "claim_levels",
    "12.6": "call_refusals",
    "13.4": "claim_refusals",
}

# В этих пунктах за обратными кавычками стоят и обычные слова. Поэтому берём только те,
# что похожи на код: строчные латинские буквы, цифры и подчёркивания.
CODE = re.compile(r"`([a-z][a-z0-9_]*)`")


def read_clauses(markdown: str) -> dict[str, str]:
    """Собрать пункты текста: номер к его тексту, включая переносы строк."""
    clauses: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        match = re.match(r"^(\d+\.\d+)\.\s*(.*)$", stripped)
        if match:
            if current is not None:
                clauses[current] = " ".join(buffer)
            current, buffer = match.group(1), [match.group(2)]
            continue
        if current is not None and stripped:
            buffer.append(stripped)
    if current is not None:
        clauses[current] = " ".join(buffer)
    return clauses


def list_part(clause: str) -> str:
    """Вырезать ту часть пункта, где перечислены коды.

    Перечень стоит после последнего двоеточия и кончается концом предложения. Иначе в него
    попадают имена полей, стоящие перед перечислением, и коды, упомянутые дальше по тексту
    в другом смысле. Проверка на пустой перечень стоит выше: молча отдать пустое нельзя.
    """
    tail = clause.rsplit(":", 1)[-1]
    for stop in (". ", ". The ", ")"):
        position = tail.find(stop)
        if position > 0:
            tail = tail[:position]
    return tail


def codes_in(text: str) -> list[str]:
    seen: list[str] = []
    for code in CODE.findall(text):
        if code not in seen:
            seen.append(code)
    return seen


def build_definition(markdown: str) -> dict:
    version = re.search(r"^# ARLI Discovery Extension v(\d+\.\d+\.\d+)", markdown, re.M)
    if version is None:
        raise ValueError("the text does not carry a version line")
    clauses = read_clauses(markdown)
    lists: dict[str, list[str]] = {}
    for number, name in LISTS.items():
        if number not in clauses:
            raise ValueError(f"clause {number} is missing from the text; the definition would be stale")
        if name.endswith("has_no_codes"):
            continue
        found = codes_in(list_part(clauses[number]))
        if not found:
            raise ValueError(f"clause {number} carries no codes; expected the list {name}")
        lists[name] = found
    return {
        "extension": "arli.discovery",
        "uri": EXTENSION_URI,
        "version": version.group(1),
        "status": "published",
        "description": (
            "Discovery and matching for independent agents by declared intent, with verifiable "
            "evidence and no index holder. An extension to A2A 1.0."
        ),
        "normative_text": "https://github.com/dmitrypehovski/arli-discovery",
        "reference_implementation": "https://github.com/dmitrypehovski/arli-discovery-engine",
        "readable_text": "https://arliwork.com/spec/",
        "conformance": {
            "command": CONFORMANCE_COMMAND,
            "result": "conforms, or the exact list of divergences with check codes",
        },
        "licence": "Apache-2.0 for the text and the implementation; the name ARLI and the "
                   "conformance mark are reserved",
        "lists": lists,
        "notes": [
            "Every list here is generated from the normative text, never written by hand.",
            "A refusal must reach the caller as a code from these lists, not as a generic error.",
            "A level from claim_levels is not evidence of the identity of a person and does not "
            "transfer between networks.",
        ],
    }


def build_from_disk() -> str:
    return json.dumps(build_definition(SOURCE.read_text(encoding="utf-8")), ensure_ascii=False, indent=2) + "\n"


def write_definition(target: Path | None = None) -> Path:
    destination = target or DEFAULT_TARGET
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_from_disk(), encoding="utf-8")
    return destination


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    written = write_definition(Path(argv[0]) if argv else None)
    definition = build_definition(SOURCE.read_text(encoding="utf-8"))
    print(json.dumps({
        "written": str(written),
        "version": definition["version"],
        "lists": {name: len(codes) for name, codes in definition["lists"].items()},
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
