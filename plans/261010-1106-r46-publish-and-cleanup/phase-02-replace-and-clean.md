# Replace and clean

Status: installations and generated-package cleanup completed; rollback-payload
cleanup awaits explicit additional owner authority.

## Context and files

`scripts/install-global-kits.py` owns the global deployment route and local
`nckh-kit/installer/nckh-installer.py` owns project updates. Their ownership records
identify the exact destinations and protect edited files. Global hooks remain off;
the project retains advisory hooks.

## Steps and validation

1. Create static installer evidence from the observed r46 package verification.
2. Preview the owned project update and global deployment; resolve real conflicts.
   The first project preview found one nested r43 evidence-skill fixture from a
   terminal BLOCKED attempt. Check its observed process exit and current process
   inventory, preserve every skill byte in a verified local ZIP, then remove that
   obsolete installed definition from discovery. Historical verdicts stay intact.
3. Apply the replacement transactions and verify every installed destination hash.
4. Inventory superseded generated package/deployment backups and validate absolute
   paths within the named workspace or explicit global skill roots.
5. Remove only obsolete copies after replacement verification; retain current
   ownership, source-lock history, failed-attempt records and active test trees.

The automatic approval reviewer rejected the initial combined cleanup because
it also included rollback backups and transaction payloads. Nothing was deleted
by that rejected invocation. Split the inventory: generated packages can be
removed within the original scope; rollback payloads require a separate grant.

## Risk and rollback

Use existing transactional backup/rollback. Record Windows access or lock failures;
do not change ACLs or stop unrelated processes. Cleanup begins only after verified
replacement, so current files and ownership remain the recovery route.

## Observed result

Every one of the 239 global and 49 project destinations matches the verified r46
packages. Project advisory hooks now match r46; global hooks remain off. The
legacy r41 project hooks were removed with their matching ownership-aware tool
before the r46 update. The retired r43 fixture skill is preserved in a local ZIP
with every one of its 30 file hashes verified; its historical BLOCKED verdict
remains intact.

Two generated-package roots were removed, containing 13,505 files and 114,951,678
logical bytes. The disposable empty test root was removed and its parent retained.
The separate inventory of 148 rollback/payload roots remains pending owner authority.
