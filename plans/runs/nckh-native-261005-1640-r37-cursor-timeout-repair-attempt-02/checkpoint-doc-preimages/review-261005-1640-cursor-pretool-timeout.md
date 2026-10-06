# Reviewed Cursor preToolUse timing repair

## Basis và scope

Native failure12 (historical evidence path: `./delivery-261005-1550-r36-cursor-direct-failure-observer.md`; unavailable in the cleaned checkout) records an actual direct5s preToolUse timeout and native failClosed Read denial. Direct20s Read13 (historical evidence path: `./delivery-261005-1610-r36-cursor-direct-timeout-control.md`; unavailable in the cleaned checkout) has Read pre/post receipts with unchanged bytes; mutation14 (historical evidence path: `./delivery-261005-1620-r36-cursor-direct-mutation-control.md`; unavailable in the cleaned checkout) verifies exact public Write and plan-only preventive denial. Earlier receipts/failures remain revision-bound.

Reviewed change: `core/hook_config.py` and `hooks/templates/cursor.json` use timeout20s only for Cursor preToolUse, with failClosed=true. Other events/hosts retain5s. `docs/installation.md` documents the bound and separate native qualification requirement. No codec/output permission change, trust/global write, install or publication.

## Review và verification

Inline review (historical evidence path: `../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/inline-review.json`; unavailable in the cleaned checkout) checks generated config/template agreement, inactive registration/trust state, unchanged other handlers and frozen inventory. Review was performed inline; no independent reviewer was run. Source checkpoint (historical evidence path: `../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/source-checkpoint.json`; unavailable in the cleaned checkout) freezes **r37/281 pins**, three changed pins, canonical hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb`. R36 preimages/history retained.

17 focused config/runner tests passed. Pipeline (historical evidence path: `../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/revalidation-summary.json`; unavailable in the cleaned checkout) runs unchanged full delivery gates against r37 with no overall deadline. Attempt01 setup failure (historical evidence path: `../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/pipeline-setup-failure.json`; unavailable in the cleaned checkout) happened before any suite child started because commands output directory was absent; attempt02 creates it and preserves original files.

## Limits và rollback

The selected bound adds up to15s before native preflight failure in a hung path. FailClosed remains true. This is a bounded reliability repair, not qualification for all Cursor events/surfaces or scientific/stable/release. R36 native controls do not prove fresh r37 package execution; a fresh r37 native observation remains separate.

Rollback restores reviewed source/template/docs from exact r36 preimages, freezes a new source revision and reruns affected gates; never overwrite source-lock history or native failure evidence. Project config cleanup removes only matching owned bytes; installed r25 unchanged.
