# Reviewed Cursor preToolUse timing repair

## Basis và scope

[Native failure12](./delivery-261005-1550-r36-cursor-direct-failure-observer.md) records an actual direct5s preToolUse timeout and native failClosed Read denial. [Direct20s Read13](./delivery-261005-1610-r36-cursor-direct-timeout-control.md) has Read pre/post receipts with unchanged bytes; [mutation14](./delivery-261005-1620-r36-cursor-direct-mutation-control.md) verifies exact public Write and plan-only preventive denial. Earlier receipts/failures remain revision-bound.

Reviewed change: `core/hook_config.py` and `hooks/templates/cursor.json` use timeout20s only for Cursor preToolUse, with failClosed=true. Other events/hosts retain5s. `docs/installation.md` documents the bound and separate native qualification requirement. No codec/output permission change, trust/global write, install or publication.

## Review và verification

[Inline review](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/inline-review.json) checks generated config/template agreement, inactive registration/trust state, unchanged other handlers and frozen inventory. Review was performed inline; no independent reviewer was run. [Source checkpoint](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/source-checkpoint.json) freezes **r37/281 pins**, three changed pins, canonical hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb`. R36 preimages/history retained.

17 focused config/runner tests passed. [Verified checkpoint](./delivery-261005-1640-r37-local-native-checkpoint.md) binds all six completed pipeline stages/exit0,192 tests successful (one Windows symlink skip),16 archives/extractions,216 resource reads,48 internal OFF/no-read observations,24 hook projections,eight previews,509 protected hashes and four legacy bundles. [Pipeline](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/revalidation-summary.json) retains original native-pending status. [Attempt01 setup failure](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/pipeline-setup-failure.json) happened before any suite child started. Original audit self-match and failed verifier are retained; corrected executable/run-path/PID-creation audit has zero matching/tracked-live processes. Review remains inline.

## Limits và rollback

The selected bound adds up to15s before native preflight failure in a hung path. FailClosed remains true. [Fresh packaged r37 controls15](./delivery-261005-1700-r37-cursor-packaged-controls.md) now verify exact public Write effect and native plan-only preventive Write denial at producer-default timing. This scoped result leaves the full Cursor event/failure/private-mutation/surface matrix and scientific/stable/release gates open.

Rollback restores reviewed source/template/docs from exact r36 preimages, freezes a new source revision and reruns affected gates; never overwrite source-lock history or native failure evidence. Project config cleanup removes only matching owned bytes; installed r25 unchanged.
