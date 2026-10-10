# Scoped acceptance

Required gates are independent pass/fail/pending/stale records bound to revision,
artifact/input hashes and actual evidence. No required fail or pending can become
accepted-for-scope. Human-reviewed records an event, not aggregate approval.
No gates means pending. Unknown cost/model/window stays unknown, never zero.

Separate static, deterministic behavior, agent behavior, host integration and
human/scientific evidence. Tests and synthetic fault fixtures cannot certify prose
quality, claim entailment, native editability or cross-host compatibility.

Stable eligibility is per skill + host/surface/version + mode/profile with positive,
negative, outcome and failure cases, rights and appropriate acceptance evidence.
Experimental routes remain useful without a stable badge. Do not narrow approved
deliverables, OS or runtime scope to close a gate.

## Shared personal-use profile

The repository-wide default is the [personal-use acceptance profile](../profiles/acceptance/personal-use.json).
It contains the five common gates, one skill-specific criteria row per approved
skill ID (the loader rejects a missing or extra row), the official
source URLs with applicability/limitations, and the `pass | fail | pending |
not-applicable` vocabulary. Resolve a row by exact skill ID; do not copy a
partial row into a skill or treat the profile as a quality guarantee. The
repository reader is `core.acceptance.load_profile(root)` and
`core.acceptance.lookup(root, skill_id)`; it validates the profile against the
current catalog before returning a row. A package consumer must retain the
profile JSON in the skill closure when packaging the acceptance policy. The
Python reader is repository-side validation support; a projected/native package
must include that reader and its dependency closure explicitly if it invokes the
reader, otherwise it should consume the self-contained JSON profile directly.

For the personal-use lane, the project owner may perform the final score and
request revisions. An external reviewer, blind holdout or human-gold corpus is
not a prerequisite for this lane. Missing owner feedback is
`pending-personal-review`; feedback must bind the exact artifact hash, input
hashes and revision. A feedback mismatch fails closed, and no helper or policy
path may fabricate a `pass` verdict.

This lane does not change the catalog's `experimental` status or the historical
stable/scientific protocol. Native, provider, rights, venue, domain and
scientific evidence remain separate gates and keep their actual pending or
unverified state.

The historical stable/scientific lane freezes sample rights, protocol, human
reviewers, thresholds and economics before its human/paid qualification runs.
Personal-use delivery preserves source rights, authorized provider scope and
actual receipts; final owner review follows usable delivery. At most three
development rounds apply to the historical protocol; holdout exposure moves a
set to development. A protected holdout cannot become blind by renaming it.
