# Proposal: proving who holds an address

Status: **draft. Not normative, not implemented.** No clause of this proposal is part of
`SPEC.en.md`, and no promise in it is made to anyone yet. It follows the same route as the witness
clause: written where the promise would live, marked as a draft, and left there until it is accepted.

## The hole this addresses

Connecting an agent checks two things: the card's signature verifies, and the address answers this
extension. Both can be true while the address belongs to somebody else. A stranger can host a copy
of your agent's card and a thin proxy that answers `agent/card` and `arli/capabilities`, and the
service will list it with your name, your claim level and your feature count.

The matching service says so in its own answer rather than implying more, but a directory with such
an entry is still wrong: it publishes somebody else's identity as if it were the entry's.

## The clause to add, in the words it would enter the text

> **Method: `arli/identity/sign`.** An agent signs bytes chosen by the asker, so that a party who
> holds the agent's card can prove the address answers with the same key.
>
> Parameters: `nonce` (a string, at least 16 characters), `purpose` (a short label for the record).
> The answer carries `signature`, the ES256 signature over the nonce bytes exactly as sent, raw R||S,
> base64url, and `kid`, the key that signed.
>
> A refusal MUST carry a code from the closed list: `nonce_too_short`, `purpose_required`.
>
> An agent MUST answer at most one signed nonce per address per purpose per minute, and MUST record
> the request in its own journal with the asking party's name when one was given. This bounds the
> method's use as a signing oracle.

Connecting then becomes three checks in one call: the card verifies, the address answers, and the
address signs a nonce that this service chose. Only then is the agent listed as connected.

## What it still does not prove, said out loud

A proxy that forwards the nonce to the real agent and returns its signature will pass. That is
accepted on purpose: passing means the proxy holds a live, working path to the agent and is
answerable for what it forwards, which is the same trust a relay has. What the check eliminates is
the cheap case, where a card is copied and answered by a script that holds no key at all.

It also does not prove anything about the human behind the agent: a card names a key, and this
method adds only that the key is reachable at the address.

## Ripple, before any of this becomes a promise

1. Extension version moves 1.2.0 to 1.3.0; `CHANGELOG.md` records the method, the two refusals and
   the rate rule, and states what an older implementation is expected to answer (a refusal of an
   unknown method, not silence).
2. Both texts gain the clause with identical numbering; the page and the definition are rebuilt; the
   definition's refusal list count changes and the published copy follows.
3. The surface list, the MCP binding and the plugin manifest gain the method, and the conformance
   suite gains a check that a signing request is refused for a short nonce.
4. Both implementations gain the method; the second implementation in Rust needs it for the
   cross-implementation proof to hold with the stronger check.
5. The matching service changes one step: after the liveness probe it sends a nonce and requires a
   signature before the agent enters the directory.
6. The rate rule needs somewhere to live: a per-address, per-purpose counter with a one-minute
   window, and a test that the second call inside the window is refused.

## Where the text is not touched

Nothing in the published normative text changes until this proposal is accepted. Until then, a
connected agent is listed after two checks, and the service says which two.
