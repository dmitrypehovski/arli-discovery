# PROPOSAL: an exchange opened directly between two agents

Status: **draft. Not normative, not implemented.** This document moves no version and changes no
behaviour. It exists because the next question after a room is what two agents can do without one.

## What this would add

Today every exchange in the product runs through the room: the service holds a list on behalf of a
caller, reaches a connected agent at its own address, and the two sides meet. The room is not a witness
to anybody's data, but it is still a party: it chooses the session, and it is the only place an
exchange starts.

This proposal is the other shape. One agent opens an exchange **directly** at another agent's address,
with no service in between:

1. The initiator fetches the counterparty's card at `GET /.well-known/agent-card.json` and verifies it.
2. It calls `arli/negotiation/open` at the counterparty with both seats named, then takes turns by the
   grammar already published, each side witnessing the other's turns in its own journal (clauses
   6.10-6.12 exist exactly for this: two machines do not share a journal).
3. Both principals approve separately, as they already do.
4. The intersection runs with the same method and the same vocabulary.

Nothing new is needed from the cryptography. What is missing is a surface: how an agent tells another
"here is my address, open with me", and how a person sees the result.

## Why it is worth having

- **The room becomes optional.** Two parties who already know each other's addresses can compare with
  no third party at all: useful where a listing is itself a disclosure.
- **The engine stops being the only initiator.** A participant can drive their own agent instead of
  filling a box on our page, which is what "any harness can join" should mean at the level of who
  starts.
- **It makes the honest claim stronger.** Today "nothing is in the middle" is true of the data and not
  of the session. Directly, it is true of both.

## What has to be decided before it is written into the text

1. **How the two addresses are exchanged.** Out of band (a message, a business card), or by an
   invitation link issued by one side? An invitation link is a product feature, not a protocol
   requirement, and should be decided as product.
2. **Whether a third party may relay the exchange.** A relay that carries signed calls cannot read
   them, but it can drop or reorder them. The text should say whether that is allowed and what the
   evidence shows when it happens.
3. **What the refusal vocabulary needs.** Expect no new codes: an unwelcome opening is refused by
   `intent_inactive`, `same_intent`, `network_mismatch` or `types_not_comparable`, all published.
4. **What a person sees.** The room prints a result page. Without a room there is a trace on two
   machines, and each side's own envelope is the record. That is enough to be checkable and not enough
   to be convenient.

## Consequences if adopted

- Version 1.5.0: a clause stating that an exchange MAY be opened directly by one side at another's
  address, that the initiating side MUST verify the card before the first call, and that the room MUST
  NOT be required for an exchange to be valid.
- Both implementations: the capability is already present in the engine's own client, so the work is
  the documentation, a surface to start it, and tests that a direct exchange settles.
- The product page gains one section: "or connect two agents to each other, without us".
- The measurement suite gains a direct exchange beside the room exchange, so the performance of both
  is reported.

## Not claimed

Direct exchange does not remove the limits the product already states: the other side learns how many
items you submitted, an online single guess is still answerable inside the feature cap, and a signed
card proves which key published an agent, not who is behind it.