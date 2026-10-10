# Review and handoff

Review compares current artifacts to outcome, public contracts, compatibility,
security, regression risk and domain-specific acceptance. Findings include severity,
location/evidence, owner and action; avoid unsupported abstract concerns.
An explicit user decision requires a new decision before reversal. Review-only
requests end with findings rather than unrequested product edits.

Handoff stores scope/mode/authorization reference, plan/input/profile/closure revisions
and hashes, artifacts, exact checks/receipts, unresolved attempts/gates, limitations,
next action and owner. Verify links and current hashes. Preserve history and originals.
Handoff never accepts on behalf of a human or sends/forks/spawns another chat by default.

## Handoff packet

A handoff packet always has these sections: outcome; authority reference (scope,
mode and grant); artifacts with exact path, `sha256` from a recorded command and
attempt status; checks with the exact command and its own exit status; gates as
pass/fail/pending/stale with evidence; next action and owner. An artifact without
a receipt from the current attempt is `existing-before-attempt` (see the
[Attempt ledger](execution.md#attempt-ledger)). Write the packet in the task's
plan directory or the location the user named; with neither, ask once, or return
it inline labelled `not-durable`.

Validator: `check-receipt.py verify --receipt <receipt> --workspace <dir>` rechecks the artifact hashes and command exits the packet cites.
