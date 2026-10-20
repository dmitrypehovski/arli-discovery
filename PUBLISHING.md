# Publication plan for the extension

Status: **published.** As of 20.10.2026 the normative text, its history and the reference
implementation are public. Nothing is listed in a public index and no announcement has been
made, so this is publication to whoever looks rather than a launch.

Addresses, and which one is which:

- https://github.com/dmitrypehovski/arli-discovery, the normative text and its history
- https://github.com/dmitrypehovski/arli-discovery-engine, the reference implementation
- https://arliwork.com/spec/, the readable page, generated from the text
- https://arliwork.com/plugin/arli-spec.git and .../arli-engine.git, mirrors on our own domain

The code platform is where contributions arrive and where a reader looks first, so it is the
canonical source. Our own domain is the readable page and the mirror we control. Both mirrors
carry the same commit as the platform, checked by fingerprint.

Two things said plainly rather than discovered later. Both repositories sit under a personal
account, because the company has no organisation on that platform yet; a transfer keeps the
history and the links, so this is a starting position. And the comments inside the code are in
Russian while the documentation and the specification are in English.

One item went out unanswered, by the decision of the holder on 20.10.2026: the export-control
review of publishing an implementation of ECDH and blind RSA signatures, with the key rotation
described in the text. The item is recorded here as an open risk, not as a settled question,
and it belongs in front of counsel. If counsel narrows it, the narrowing applies to later
versions; it cannot un-publish what is already readable.

## What we publish, and what we keep

Published under Apache-2.0:

- the normative specification text, English (`spec/SPEC.en.md`)
- the version history and the transition rules (`spec/CHANGELOG.md`)
- the conformance suite (`arli_engine/conformance`)
- the reference implementation of the engine (`arli_engine`)
- the plugin manifest (`arli_engine/adapters/plugin/arli-discovery.json`)

Kept as ours, not published:

- the network and the service: live intents, liquidity, reputation
- the conformance mark and the right to use it (`TRADEMARK.md`)
- pricing, commercial terms, certification agreements
- client integrations
- internal funnel metrics and operational data

The reason for this split is in the licence decision itself: the text is worth nothing and
buys adoption, while the network and the mark are what can be sold. A closed specification
would leave the conformance suite with nobody to run it.

## Language

The published normative text is English. Written English text is the normative one; the
Russian file `spec/SPEC.md` is a working translation and is not the published artefact.
A third language can follow later; the English text stays the reference.

## Legal check before publishing

This is a checklist for counsel, not a settled question. The publisher is a Chinese entity
(Shenzhen Capernaum Technology Co., Ltd.).

1. Encryption law review. The Cryptography Law places export control on commercial
   cryptography products that affect national security or the public interest, and exempts
   products for mass consumption. A specification text that names public algorithms
   (ECDH P-256, HKDF-SHA256, blind RSA signatures) is not itself a product, but the
   reference implementation and the conformance suite are software. Confirm that publishing
   them as open source needs no licence, and confirm the position on the export list
   entry for key management products, since the extension describes key rotation.
2. Outbound licence consistency. Confirm that a Chinese entity may grant Apache-2.0,
   including the patent grant, over this code.
3. Personal data. Confirm the wording of clause 8.4, that envelopes carrying feature names
   count as personal data, before any cross-border publication of examples that contain
   feature names. Examples must use synthetic features only.
4. Mark registration. Confirm the filing position for the conformance mark before it is
   used in public material.
5. Contribution terms. Confirm that the contributor terms in `CONTRIBUTING.md` are
   acceptable for the entity.

## Order of steps

1. Legal check above, answered in writing.
2. Repo hygiene: `LICENSE`, `NOTICE`, `TRADEMARK.md`, `CONTRIBUTING.md`, `README.md`,
   English specification.
3. Publication of the text and the reference implementation under Apache-2.0.
4. Conformance service and the mark, as a separate commercial step.

Steps 1 and 2 are done for the text, and the text part of step 3 is done. The code part of
step 3 is held. Step 4 is not started.

What publishing changed in practice: the legal check is no longer a gate on the text, and the
checklist items that concerned the text only are now settled by the fact of publication. Item
1 of the checklist still governs the code, and item 3 still governs any example carrying real
feature names.

## State of the houses

The text lives in its own repository with its own history, on branch `main`, one commit so
far. It is not nested inside the engine repository: the engine changes more often and for
other reasons, and a shared history would entangle the promise with the implementation.
The engine references this directory through the `ARLI_SPEC_DIR` setting and keeps no copy.

What an outsider can do today with a copy of this directory: read the normative text, rebuild
the page, run the eight checks that keep the two texts aligned. What an outsider cannot do yet:
there is no public address, and the reference implementation is not published either.

Python is required for the checks and for the page build:

```
python -m pytest tests -q
python -m tools.build_page
```
