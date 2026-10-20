"""Сборка страницы спецификации из нормативного текста.

Страница не пишется руками. Рукописная страница расходится с текстом на первой правке, и
расходится молча: люди читают страницу, а проверяют по тексту, и обе стороны уверены в
своём. Поэтому страница собирается из `SPEC.en.md`, а тест сверяет записанный файл с
собранным.

Запуск: python -m tools.build_spec_page [путь]
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "SPEC.en.md"
DEFAULT_TARGET = ROOT / "docs" / "spec.html"

ACCENT = "#c4a97d"
TITLE = "ARLI Discovery Extension v1.0.0"
CONFORMANCE_COMMAND = (
    "python -m arli_engine.conformance --target <url> [--holder <url>]"
)

STATUS_NOTICE = (
    "Status: not published. This page is generated from SPEC.en.md and is the same text "
    "the conformance suite is bound to. Publication waits for the legal check described in "
    "PUBLISHING.md."
)


def _inline(text: str) -> str:
    """Разметка внутри строки: код в обратных кавычках и жирное."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_sections(markdown: str) -> tuple[dict, list[tuple[str, list[dict]]]]:
    """Разобрать текст на шапку и разделы. Разбор простой и честный: только то, что есть.

    Пункт начинается со своего номера в начале строки и может переноситься на следующую.
    Поэтому блок текста режется не по пустым строкам, а по началам пунктов: иначе несколько
    пунктов склеиваются в один и на странице остаётся первый.
    """
    lines = markdown.splitlines()
    header = {"title": "", "paragraphs": []}
    sections: list[tuple[str, list[dict]]] = []
    current: tuple[str, list[dict]] | None = None
    buffer: list[str] = []

    def target() -> list[dict]:
        return header["paragraphs"] if current is None else current[1]

    def flush() -> None:
        if not buffer:
            return
        text = " ".join(part.strip() for part in buffer if part.strip())
        if text:
            clause = re.match(r"^(\d+\.\d+)\.\s*(.+)$", text, re.S)
            if clause:
                target().append({"clause": clause.group(1), "text": clause.group(2)})
            else:
                target().append({"paragraph": text})
        buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            flush()
            header["title"] = stripped[2:].strip()
            continue
        if stripped.startswith("## "):
            flush()
            current = (stripped[3:].strip(), [])
            sections.append(current)
            continue
        if not stripped:
            flush()
            continue
        if re.match(r"^\d+\.\d+\.\s", stripped):
            # начало нового пункта: закрываем предыдущий, даже если пустой строки не было
            flush()
        buffer.append(stripped)
    flush()
    return header, sections


def build_html(markdown: str, *, source_name: str = "SPEC.en.md") -> str:
    header, sections = parse_sections(markdown)
    title = header["title"] or TITLE
    clause_count = sum(1 for _, items in sections for item in items if "clause" in item)
    toc = "\n".join(
        f'      <li><a href="#{_slug(name)}">{html.escape(name)}</a></li>' for name, _ in sections
    )
    header_html = "\n".join(
        f"    <p>{_inline(item['paragraph'])}</p>" for item in header["paragraphs"]
    )
    body = []
    for name, items in sections:
        body.append(f'  <section id="{_slug(name)}">')
        body.append(f"    <h2>{html.escape(name)}</h2>")
        for item in items:
            if "clause" in item:
                body.append(
                    f'      <p class="clause"><span class="id">{item["clause"]}</span>'
                    f'{_inline(item["text"])}</p>'
                )
            else:
                body.append(f"      <p>{_inline(item['paragraph'])}</p>")
        body.append("  </section>")
    body_html = "\n".join(body)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ --accent: {ACCENT}; --ink: #1c1c1a; --muted: #6f6b62; --rule: #e6e1d6; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #fbfaf7; color: var(--ink);
      font: 16px/1.65 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    .wrap {{ max-width: 820px; margin: 0 auto; padding: 48px 20px 96px; }}
    header h1 {{ font-size: 30px; line-height: 1.25; margin: 0 0 12px; }}
    .status {{ border-left: 3px solid var(--accent); background: #fff; padding: 12px 14px;
      color: var(--muted); font-size: 14.5px; margin: 18px 0 28px; }}
    nav {{ border: 1px solid var(--rule); background: #fff; padding: 14px 18px; border-radius: 6px; }}
    nav h2 {{ font-size: 13px; text-transform: uppercase; letter-spacing: .08em;
      color: var(--muted); margin: 0 0 10px; }}
    nav ol {{ margin: 0; padding-left: 20px; columns: 2; }}
    nav a {{ color: var(--ink); text-decoration: none; }}
    nav a:hover {{ color: var(--accent); }}
    section {{ margin-top: 40px; }}
    section h2 {{ font-size: 20px; margin: 0 0 6px; padding-bottom: 8px;
      border-bottom: 1px solid var(--rule); }}
    .clause {{ margin: 14px 0; }}
    .clause .id {{ display: inline-block; min-width: 48px; color: var(--accent);
      font-weight: 600; }}
    code {{ background: #f2efe7; padding: 1px 5px; border-radius: 3px;
      font: 13.5px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .plain-intro {{ margin: 18px 0 6px; padding: 16px 18px; background: var(--card, #fff);
      border: 1px solid var(--rule); border-radius: 10px; font-size: 15.5px; }}
    .plain-intro p {{ margin: 0 0 8px; }}
    .plain-intro p:last-child {{ margin-bottom: 0; }}
    footer {{ margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--rule);
      color: var(--muted); font-size: 14px; }}
    @media (max-width: 560px) {{ nav ol {{ columns: 1; }} .wrap {{ padding: 32px 16px 64px; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>{html.escape(title)}</h1>
      <div class="plain-intro">
        <p><b>What this is.</b> The rules of the discovery extension, written so two independent teams
        can build it and agree on the result. It is the text implementations are measured against.</p>
        <p><b>Who has to read it.</b> Only those building or auditing an implementation. To use the
        product, open <a href="https://match.arliwork.com">ARLI Match</a> and press one button. Nothing
        here is needed for that.</p>
        <p><b>Where the machine-readable copy lives.</b>
        <a href="https://arliwork.com/a2a/extensions/arli.discovery.v1">arli.discovery.v1</a>, built from
        this text rather than written by hand.</p>
      </div>
{header_html}
      <p class="status">{html.escape(STATUS_NOTICE)}</p>
    </header>
    <nav>
      <h2>Sections</h2>
      <ol>
{toc}
      </ol>
    </nav>
{body_html}
    <footer>
      <p>{clause_count} clauses in {len(sections)} sections. Source: <code>{html.escape(source_name)}</code>.
      Licence: Apache-2.0. The name ARLI and the conformance mark are reserved, see TRADEMARK.md.</p>
      <p>Conformance suite:<br><code>{html.escape(CONFORMANCE_COMMAND)}</code></p>
    </footer>
  </div>
</body>
</html>
"""


def build_from_disk(*, source: Path | None = None) -> str:
    text = (source or SOURCE).read_text(encoding="utf-8")
    name = str((source or SOURCE).relative_to(ROOT))
    return build_html(text, source_name=name)


def write_page(target: Path | None = None) -> Path:
    destination = target or DEFAULT_TARGET
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_from_disk(), encoding="utf-8")
    return destination


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    target = Path(argv[0]) if argv else None
    written = write_page(target)
    header, sections = parse_sections(SOURCE.read_text(encoding="utf-8"))
    clauses = sum(1 for _, items in sections for item in items if "clause" in item)
    print(json.dumps({"written": str(written), "sections": len(sections), "clauses": clauses}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
