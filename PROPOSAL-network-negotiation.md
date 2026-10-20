# Proposal: negotiation between two machines

Status: **draft. Not normative, not implemented.** No clause of this proposal is part of
`SPEC.en.md`, and no promise in it is made to anyone yet. It exists because building a real network
found a hole in the current text, and the hole has to be written down where somebody can check it
rather than fixed quietly in one implementation.

## The hole this addresses

Clause 6 describes the negotiation log as one log for two seats, and the reference implementation
says the same in a comment: *the negotiation log: two seats, one log, no wire between the agents*.

That assumption holds when both agents are raised inside one process. It is false the moment two
implementations live on two machines, which is the entire point of a network. Each side keeps its
own log, so a turn taken by one side is invisible to the other, and the other side refuses the
counterparty's next turn with `first_turn_is_propose_or_decline`, or refuses a turn whose seat it
cannot place.

This is not a theory. It was found by connecting a real agent: the second implementation, in Rust,
running on its own port, was connected to the matching service (its card verified, its extension
answering), and its exchange was refused by exactly those codes.

## The clause to add, in the words it would enter the text

> **Method: `arli/negotiation/witness`.** A side records a turn taken by the counterparty in its own
> log, so that both logs hold the same sequence without a shared file between them.
>
> Parameters: `negotiation_id`, `seat`, `action`, `message`, `proof`, `card`.
> - `seat` must be a seat of this negotiation and must not be the receiving agent's own seat.
>   A side takes its own turns with `arli/negotiation/turn`; witnessing is for the other side's.
> - `card` is the speaker's signed agent card. It must verify by its own rules, and its `name` must
>   equal `seat`, so the key in the card is bound to the seat it claims.
> - `proof` is the envelope the speaker received for its own turn. It must verify with the key from
>   the presented card, and its recorded parameters must name the same seat and action. Without a
>   valid proof the turn is not recorded, because an unsigned turn could be written by anyone.
> - The turn must be legal in the receiving side's own log: seats alternate, the turn limit applies,
>   and a settled negotiation accepts nothing.
> - The answer carries an envelope like every other mutating call.

Closed rejections, added to clause 6's list: `not_a_witness`, `witness_without_proof`,
`witness_card_unverified`, `witness_seat_mismatch`, `witness_proof_invalid`, `witness_mismatch`.

The exchange then reads: the initiator takes its turn and sends the turn and its envelope to the
counterparty as a witness; the counterparty records it, takes its own turn, and witnesses back.

## What is still not proven, and is said out loud

Connecting an agent proves that a signed card exists and that the address answers this text. It does
**not** prove that the address is run by the owner of the key: a proxy would pass both checks. The
same limit applies to witnessing, because the proof only shows that some agent holding the key
signed the turn.

Closing that needs one more method, `arli/identity/sign`, where an agent signs bytes chosen by the
asker. Then the address itself can be challenged. This proposal deliberately stops short of it and
records it as a second step, so that neither limit is presented as closed.

## Ripple, before any of this becomes a promise

1. Extension version moves 1.1.0 to 1.2.0, and `CHANGELOG.md` records what changed and how an older
   implementation is expected to answer.
2. Both texts gain the clause, with identical clause numbering; the generator rebuilds the page;
   the definition served at `arliwork.com/a2a/extensions/arli.discovery.v1` follows.
3. The MCP binding and the plugin manifest are derived from the surface list: a new method without
   them is a broken promise, and a test fails today if they drift.
4. The conformance suite gains a check: a pair settles when the two sides are two separate
   processes. The current record, `test_matching_across_two_processes_is_a_recorded_gap`, fails at
   that moment and gets rewritten.
5. The second implementation in Rust gains the method. Until it does, cross-implementation matching
   stays refused by code, which the network service shows honestly instead of pretending.
6. The matching service switches from direct turns to witnessing in `app/network.py`.

## Where the text is not touched

Nothing in the published normative text changes until this proposal is accepted. Until then, an
implementation that follows `SPEC.en.md` exactly is conforming, and matching across two machines is
a known limit rather than a promise.
