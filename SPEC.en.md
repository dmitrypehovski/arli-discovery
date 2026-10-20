# ARLI Discovery Extension v1.4.0

Extension to A2A 1.0 for discovering independent agents by intent with verifiable evidence.
Extension URI: `https://arliwork.com/a2a/extensions/arli.discovery.v1`.

The words **MUST**, **MUST NOT**, **SHOULD** and **MAY** carry the force they carry in
normative documents. An implementation that conforms to this text is answered
"conforms" by the conformance suite (`python -m arli_engine.conformance`).
Where the suite and this text disagree, the suite is right: the suite is the promise.

Scope. The extension describes the discovery layer only: the intent object, the honest
capability list, key agreement, matching, the evidence envelope, the negotiation grammar
and human consent. Transport, tasks and messages are taken from A2A as they are.

## 1. Intent

1.1. An intent MUST carry the fields: `intent_id`, `owner`, `network`, `type`, `statement`,
`status`, `provenance`.
1.2. `type` MUST be one of: `person`, `supply`, `demand`. An intent of type `supply`
is matched against `demand` on a shared topic; two `supply` intents MUST NOT count as
a match with each other.
1.3. `status` MUST be one of: `active`, `paused`, `archived`. Only `active` takes part in
matching.
1.4. `provenance` MUST be one of: `human`, `organisation`, `synthetic`. A network MUST
declare whether it admits synthetic intents; by default a network is human, that is, it does
not admit them. In such a network a synthetic intent MUST be refused with the code
`synthetic_not_admitted` instead of taking part in matching.
1.5. An intent MUST carry a jurisdiction; retention rules follow it, not the location of
the server.

## 2. Agent capabilities

2.1. The agent card MUST be served at the standard address `/.well-known/agent-card.json`
and MUST be signed with JWS (alg ES256). The protected header MUST carry `jwk`, so the other
side can verify the card without receiving a key over a separate channel.
2.2. The signature MUST break on any edit of the card body.
2.3. Every operation of an agent MUST declare its effects across all seven keys:
`mutates_artifact`, `launches_process`, `may_show_ui`, `may_access_network`,
`may_write_filesystem`, `changes_permissions`, `requires_root`.
2.4. An undeclared effect MUST be treated as possible, not as absent.
2.5. An unavailable operation MUST remain in the list and MUST carry a reason with a code
from the set: `available`, `unsupported_host`, `missing_dependency`, `not_configured`,
`disabled_by_policy`.
2.6. The list MUST be served as a separate document
`/.well-known/arli-capabilities.json` with the `fail_closed` flag.

## 3. Key agreement and fingerprints

3.1. The pair key MUST be derived by ECDH on curve P-256 and HKDF-SHA256, with both agent
identifiers and the session identifier as input. The pair key MUST NOT be transmitted over
the wire.
3.2. A feature fingerprint MUST be bound to the session and to the canonical pair label,
which is the same on both sides. Binding to the sender side MUST NOT be used: it breaks
matching.
3.3. Neither side MUST send feature values; only fingerprints or blinded values leave.
3.4. One exchange MUST happen no more than once per pair and session.

## 4. Matching

4.1. The matching scheme in v1.1.0 MUST be `closed_blind_rsa`: blind RSA signatures.
4.2. The key holder MUST publish only the public part (`n`, `e`); the private exponent
MUST NOT leave the agent.
4.3. The matching result MUST be symmetric: both sides receive the same intersection.
4.4. Offline enumeration of the other side's set MUST be impossible: the received values
MUST NOT be comparable with guesses without the holder's private exponent.
4.5. The number of features in one exchange MUST be capped at 64. An excess MUST be refused
with the code `too_many_features`, not truncated.
4.6. A matching call MUST declare a floor: `floor_basis_points` as an integer in the range
0..10000. A call without a floor MUST be refused with the code `missing_floor`; a floor out
of range MUST be refused with the code `invalid_floor`.
4.7. A find below the declared floor MUST NOT be returned: the result MUST be empty, the
envelope MUST carry `floor_basis_points` and `passed_floor`, and completeness MUST state
that the result was not returned as below the floor.
4.8. Filling the result up to a limit MUST NOT be used.
4.9. A match score MUST either be computed with a declared method or be absent. A constant
in place of a score MUST NOT be used.
4.10. The number of features on the other side MUST NOT be disclosed.
4.11. The capability document MUST publish the closed list of seven matching refusal codes:
`too_many_features`, `missing_pair_key`, `missing_peer_key`, `missing_private_key`,
`length_mismatch`, `missing_floor`, `invalid_floor`.

4.12. Before hashing, a feature MUST be reduced to a canonical token by the published vocabulary:
the string MUST be lower-cased and trimmed, and runs of whitespace, hyphens and underscores MUST be
reduced to one hyphen.
4.13. A feature MUST be split at its first colon into a namespace and a value; a feature without a
colon is a value.
4.14. A namespace in the goods list (`need`, `want`, `offer`, `supply`, `skill`, `service`,
`commodity`, `product`) MUST reduce to its value alone, so that a need and an offer of the same
commodity are one token. Any other namespace MUST keep the form `namespace:value`. An unknown
namespace MUST be treated as an attribute, because failing to match is a smaller error than matching
something nobody declared.
4.15. The intersection MUST be compared as canonical tokens, and each side MUST be told which of its
own features matched in that side's own spelling. An implementation that compares the strings as typed
MUST NOT be reported as conformant.

## 5. Evidence envelope

5.1. Every conclusion and every refusal MUST be accompanied by an envelope with the fields:
`evidence_id`, `provider`, `operation`, `parameters`, `normalized_result`, `confidence`,
`authority`, `limitations`, `completeness`, `captured_at`.
5.2. `evidence_id` MUST be recomputable from the envelope body. Fractional numbers in the
body MUST NOT be used: they break reproducibility. Fractions are expressed as integer basis
points.
5.3. The envelope MUST be signed with the agent key; the signature MUST sit beside the body
so that `evidence_id` stays recomputable and an edit of the body breaks verification.
5.4. `completeness` MUST list what is closed, what was dropped and for which reason.
Absence of data MUST NOT be read as soundness.
5.5. `confidence` MUST be from the set: `observed`, `derived`, `claimed`, `unknown`.
5.6. `limitations` MUST name the limits of the method plainly, including what the scheme
does not close.

## 6. Negotiation

6.1. A negotiation MUST have exactly two seats and one journal per pair.
6.2. Actions MUST be from the set: `propose`, `counter`, `accept`, `decline`.
6.3. The first turn MUST be made by the initiator and MUST be `propose` or `decline`.
6.4. `accept` MUST be legal only immediately after a `propose` from the other side.
6.5. The turn limit MUST be 12. At the limit the negotiation MUST remain unsettled; it
MUST NOT be declared a refusal.
6.6. A refusal MUST carry a code from the closed turn list:
`not_a_seat`, `unknown_action`, `already_settled`, `turn_limit`, `not_your_turn`,
`first_turn_is_propose_or_decline`, `seats_must_alternate`, `accept_without_offer`,
`propose_over_offer`, `not_a_witness`, `witness_without_proof`, `witness_card_unverified`,
`witness_seat_mismatch`, `witness_proof_invalid`, `witness_mismatch`.
6.7. A pair MUST NOT be opened if at least one intent is not active, if it is synthetic in
a network declared human, if the owner is the same, if the intents coincide, if the sides
are from different networks or if the types are not complementary. A refusal MUST carry a
code from the list: `intent_inactive`, `synthetic_not_admitted`, `same_owner`, `same_intent`,
`network_mismatch`, `types_not_comparable`, `below_required_level`.
6.8. Both lists MUST be published by machine in the capability document together with the
turn limit and the action list.
6.9. The capability document MUST publish the intent types, the statuses, the admitted
provenance and the intent refusal list: `unknown_type`, `unknown_status`, `unknown_provenance`,
`synthetic_not_admitted`, `intent_inactive`, `types_not_comparable`, `network_mismatch`.
6.10. A side MAY record a turn taken by the counterparty in its own journal, so that both
journals hold the same sequence without a shared file between them. This MUST be done with the
method `arli/negotiation/witness`. A turn taken by the agent itself MUST be taken with
`arli/negotiation/turn`; witnessing MUST NOT be used for one's own seat.
6.11. A witness request MUST carry the speaker's signed agent card and the envelope the speaker
received for its own turn. The card MUST verify by the rules of clause 2, the name in the card
MUST equal the seat witnessed, and the envelope MUST verify with the key from that card and MUST
name the same seat and action. A turn MUST NOT be recorded without a proof that passes.
6.12. A witnessed turn MUST be legal in the receiving side's own journal: the seats alternate,
the turn limit of clause 6.5 applies, and a settled negotiation accepts nothing.

## 7. Consent

7.1. Agent consent MUST NOT open a connection. The human decision MUST be a separate act.
7.2. Silence, an error and a timeout MUST NOT count as consent or as refusal.
7.3. One seat MUST NOT decide for the other.
7.4. A repeated decision MUST be refused.
7.5. A late "yes" MUST NOT undo an earlier refusal.

## 8. Retention and deletion

8.1. Raw feature values MUST NOT be stored on the server; fingerprints are kept for the
duration of the session, together with envelopes.
8.2. The retention period of envelopes MUST be declared and is 30 days by default.
8.3. Archiving an intent MUST remove it from matching and mark the related envelopes deleted.
8.4. Envelopes carrying feature names MUST be treated as personal data and MUST NOT leave
the region where the intent was created before a legal opinion.
8.5. The capability document MUST publish the retention period, the retention refusal list
(`unknown_envelope`, `already_deleted`, `unknown_intent`) and the statement that raw feature
values are not stored on the server.

## 9. Key rotation and revocation

9.1. A key change MUST invalidate the previous card.
9.2. Principal revocation MUST be a separate record with a time and a reason and MUST NOT be
replaced by a key change. Revocation MUST block the issuing of new keys under the same
identifier until a separate re-confirmation.
9.3. The capability document MUST publish the key revocation reasons (`rotated`,
`compromised`, `principal_request`, `policy`) and the registry refusal list (`unknown_key`,
`key_revoked`, `key_expired`, `key_not_yet_valid`, `principal_revoked`,
`principal_not_confirmed`, `unknown_revocation_reason`).
9.4. An agent MUST answer `arli/identity/sign` with a signature over the nonce it was given, in the
bytes exactly as they were sent. The signature MUST be ES256 in the raw R||S form, base64url, and the
answer MUST name the key that signed. This is how a party holding a card can require the address to
prove that the same key answers there.
9.5. An agent MUST answer at most one signed nonce per address and purpose per minute, and MUST
record the request in its journal when the asking party named itself. The method is otherwise a
signing oracle.

## 10. Conformance

10.1. The conformance suite MUST be run against an implementation address:
`python -m arli_engine.conformance --target <url> [--holder <url>]`.
10.2. The suite MUST answer either "conforms" or the exact list of divergences with check
codes.
10.3. The suite MUST contain deliberately wrong implementations and MUST catch each of them.
A suite that passes against any implementation MUST be considered void.

## 11. Versions and transition

11.1. The extension version MUST follow semantic versioning.
11.2. An incompatible change MUST raise the major version and MUST be described in the
transition section, stating what is deprecated.
11.3. A deprecated field MUST be announced at least one minor version before removal.

## 12. Bindings

12.1. The agent surface is one. A binding (A2A over HTTP, MCP over streams) MUST NOT add or
hide methods: the MCP tool list MUST match the method list one to one, one tool per method.
12.2. An MCP tool name MUST be a method name with slashes replaced by underscores, and the
translation MUST be reversible: exactly one method MUST be recoverable from a tool name.
12.3. A refusal reason MUST reach the caller as the engine's code, not as a generic error.
A tool that returns the word "error" in place of a code violates this specification.
12.4. The capability document MUST publish all bindings, the naming rule and the required
fields of every method.
12.5. The plugin manifest MUST be generated from the method list, never hand-written, and
MUST declare its limitations honestly. The recorded manifest MUST match the generated one:
a divergence means a hand edit and MUST count as a defect.

## 13. Claims about features

13.1. A statement about a feature MUST carry a level from the closed list: `declared`,
`third_party_verified`, `topic_owner_verified`. The level `declared` means the side said it
about itself, and a reader MUST NOT read more into it.
13.2. A level above `declared` MUST carry an issuer and that issuer's own envelope. An
implementation MUST verify the issuer's envelope before reporting the level, and MUST NOT
report a level it cannot produce an envelope for.
13.3. A claim MUST carry the moment of the check. A claim without it MUST be refused with the
code `missing_checked_at`. A claim that has expired or been withdrawn MUST be reported as
expired or withdrawn, and MUST NOT be dropped silently.
13.4. A refusal about a claim MUST carry a code from the closed list: `unknown_level`,
`unknown_claim_state`, `missing_issuer`, `unknown_issuer`, `issuer_envelope_invalid`,
`claim_expired`, `claim_withdrawn`, `level_upgraded_without_issuer`, `missing_checked_at`.
13.5. A network MAY require a minimum level for a pair. A pair below that level MUST NOT open,
and the refusal MUST carry the code `below_required_level`.
13.6. A level MUST NOT be presented as evidence of the identity of the person behind an agent,
and MUST NOT be treated as transferable between networks. Both prohibitions MUST appear in the
capability document.
13.7. The capability document MUST publish the levels, the states, the claim refusal list, and
the statement that the implementation relays and verifies statements made by others and issues
none of its own.

12.6. A refusal about the call itself MUST carry a code from the closed list: `missing_field`,
`unknown_method`, `parse_error`, `bad_type`, `nonce_too_short`, `purpose_required`,
`rate_limited`. A caller MUST be able to tell a malformed call from
a failure of the implementation.
