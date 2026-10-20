# ARLI Discovery Extension

The normative text of the extension, kept apart from the code on purpose.

This directory is a separate artefact. The engine implements what is written here, and the
two version independently: the text is at 1.0.0, and the code is at 0.1.0 and walks there in
steps. The text is the promise; a test in this directory keeps the promise internally
consistent, and a test in the engine repository checks that the engine depends on this text
and not on some copy of it.

Status: **the text is published**. Sources: https://github.com/dmitrypehovski/arli-discovery.
Readable page: https://arliwork.com/spec/. Mirror of the repository on our own domain:
https://arliwork.com/plugin/arli-spec.git.

Two honest notes. The repository sits under a personal account today, because we have no
company organisation on that platform yet; the move is one command and the history comes with
it. And no announcement has been made, so this is publication to whoever looks, not a launch.
The reference implementation is not published yet: see `PUBLISHING.md`.

## What is here

- `SPEC.en.md`: the normative text, English. This is the published artefact.
- `SPEC.md`: the Russian working translation. Clause numbers are identical to the English
  text, and a test fails if they diverge.
- `CHANGELOG.md`: the extension version history and the transition rules.
- `PUBLISHING.md`: what is published, what stays ours, and the legal checklist.
- `PROPOSAL-trust-anchor.md`: the draft for legal review about verifying features. Marked
  as not normative and not implemented: the normative text makes no promise about trust
  levels, and a test fails if it ever does before the legal answer.
- `docs/spec.html`: the readable page, generated from `SPEC.en.md`, never hand-written.
- `tools/build_page.py`: the generator.
- `LICENSE`, `NOTICE`, `TRADEMARK.md`: the licence terms of the text itself.

Licence of the text and of the reference implementation: Apache-2.0. The name ARLI and the
conformance mark are reserved, see `TRADEMARK.md`.

Copyright 2026 Shenzhen Capernaum Technology Co., Ltd. (ARLI).

## Checks in this directory

```
python -m pytest tests -q
python -m tools.build_page
```

The second command regenerates `docs/spec.html`. A test fails if the recorded page does not
match the generated one, so the page cannot drift from the text.

The page is not served anywhere yet. Serving it is a publication step.
