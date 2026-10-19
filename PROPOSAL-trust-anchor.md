# Proposal: trust anchor for features

Status: **draft for legal review. Not normative, not implemented.** No clause of this
proposal is part of `SPEC.en.md`, and no promise in it is made to anyone yet. It exists so
that the legal review has something concrete to answer, instead of a paragraph of
intentions.

## The hole this addresses

Today an envelope can say: the other side declared these features about itself. That
sentence is true and useless. Nothing checks whether the declaration is true, with two
consequences.

A liar wins matches it should not win. And a person can be matched to a counterpart that was
fabricated by whoever runs the other agent.

The engine already refuses synthetic intents inside human networks (clause 1.4). That
refusal is a declaration too: it says "this network does not admit synthetic intents", and
nothing verifies it. Closing that hole is the point of this proposal.

## Three levels, and nothing more

- **Level 0, declared.** A side says a feature about itself. This is what happens today. The
  envelope says so, and no reader should read more into it.
- **Level 1, verified by a third party.** Somebody other than the two sides states that the
  feature held at a moment in time, and their statement is itself an envelope: who, when,
  what was checked, and how. The two sides do not have to trust each other; they can check
  the issuer.
- **Level 2, confirmed by the owner of the topic.** The party whose competence or authority
  covers the feature states it. For a skill this is the certification body, for a licence the
  registry, for a membership the network itself.

A level is a claim with an issuer, never a property of a person. What it does not mean, and
must never be written as if it did: that a level proves who is behind an agent, or that a
level earned in one network transfers to another. Both sentences must be forbidden in the
wording, because both would be read as a guarantee.

## What the envelope would carry

- the level, one of the three, or `unknown`
- the issuer, with a key that verifies the statement
- the moment of the check, and the moment the statement stops being valid
- what was actually checked, in one sentence a human can dispute
- the identifier of the issuer's own envelope, so the claim is inspectable rather than
  repeated

A forged level must be caught by the conformance suite: a side that upgrades its own level
without an issuer's envelope is a deliberately wrong implementation, and the suite fails it.
That check goes into the suite only after this proposal becomes normative.

## What we will not do, whatever the legal answer

- We will not state a level we cannot produce an envelope for.
- We will not verify a person without their separate, recorded consent.
- We will not buy external databases of people. The plan forbids it, and a network built that
  way is the thing we claim to replace.
- We will not sell the level as a guarantee of identity. That is a different service with a
  different regulator, and we are not entering it by accident through wording.

## Questions for counsel

1. May we issue a level 1 statement ourselves, or is issuing it a regulated activity where we
   are established and where the principal is?
2. If we issue a statement that later proves wrong, what is our exposure, and what wording in
   the participant terms keeps the statement a report rather than a warranty?
3. A level links a feature to an identifiable person, and the link is more sensitive than the
   feature alone. What retention period applies to it, and may it cross the border of the
   region where the intent was created (clause 8.4 already forbids the crossing before a
   legal opinion)?
4. May a Chinese entity issue these statements to principals in other jurisdictions, and does
   the answer change if the statement concerns a regulated competence, such as a licence?
5. What must the participant terms say about the fact that we record a verification event,
   and about the participant's right to withdraw it without losing past matches?
6. If we choose not to issue statements ourselves and only relay others' statements, does
   that relay change our legal position, and what must the envelope say to make the relay
   honest?

## Three answers and what each costs us

- **Yes, we may issue.** We build the issuer registry and the checks. The level becomes part
  of what we sell, and the mark follows the level.
- **No, we may not issue, but may relay.** The envelope carries somebody else's statement and
  our role is transport plus verification of the statement's shape. Cheaper, weaker, honest.
- **No, and no relay either.** Only level 0 remains. The wording of the envelope then says
  plainly that nothing is verified, and the pricing must reflect that. This is survivable:
  a matching layer with no verification still beats an index holder reading both intents.

## Size of the work, so the answer is informed

Small on the code side and large on the process side. Code: one envelope field, one registry
of issuers, two conformance checks. Process: an agreement with each issuer, a dispute path
for a wrong statement, and a decision about who pays for a check.
