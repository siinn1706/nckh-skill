---
title: Publish experimental r46 and remove superseded skill copies
status: completed
created: 2026-10-10
branch: main
---

# Experimental r46 publication and skill cleanup

## Outcome and authority

Publish the latest owner-accepted debug/fix candidate and matching packages to
`siinn1706/nckh-skill`, replace the owned project/global installations, and remove
superseded generated skill copies. The direct user request on 10 October 2026 was
“commit skill mới nhất lên github đi, và dọn dẹp các skill phiên bản cũ ở global
và local”. Preparing matching source locks, packages and replacement installations
is part of this delivery.

The accepted instruction bytes and historical failures remain revision-bound.
Experimental publication does not clear stable, native, scientific, model or
process-observability qualification. Keep current ownership state, source-lock
history, active test workspaces, unrelated skills and edited content.

## Phases

| Phase | Status | Dependency |
|---|---|---|
| [1. Freeze and verify](phase-01-freeze-and-verify.md) | completed | Owner-accepted candidate |
| [2. Replace and clean](phase-02-replace-and-clean.md) | replacement and generated cleanup completed; rollback cleanup awaiting authority | Matching verified r46 packages |
| [3. Commit and publish](phase-03-commit-and-publish.md) | completed | Reviewed publication scope |

## Acceptance

- Source lock and all four resource-enabled packages identify revision 46.
- Focused regression checks, reproducible builds and the public verifier pass.
- All owned installed skill and agent destinations match the verified packages.
- Superseded generated copies are removed only after replacement verification.
- Published files pass the privacy/credential audit; remote main equals local HEAD.
- Historical failures and pending qualification retain their original meanings.

## Evidence

Command/process/install records remain in the ignored local state directory.
A privacy-reviewed publication summary is recorded in
[publication evidence](publication-evidence.json). The final result belongs in
[the delivery report](../reports/deploy-261010-1106-r46-publish-and-cleanup.md).
The public publication commit and remote verification are recorded in the
evidence; local private history remains under the retained backup ref.
