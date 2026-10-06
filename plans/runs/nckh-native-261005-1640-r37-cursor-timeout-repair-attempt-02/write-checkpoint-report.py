"""Write a factual checkpoint only after terminal local/native verification."""

import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
record = json.loads((RUN / "verified-checkpoint.json").read_text(encoding="utf8"))
assert record["status"] == "verified-r37-local-and-scoped-packaged-native-checkpoint"
target = WORK / "plans/reports/delivery-261005-1640-r37-local-native-checkpoint.md"
assert not target.exists()
body = f"""# R37 verified local and scoped native checkpoint

## Current candidate

[Verified bindings](./delivery-261005-1640-r37-local-native-checkpoint.json) freeze source **r37/{record['pins']} pins**, canonical hash `{record['source_lock_hash']}`. [Reviewed repair](./review-261005-1640-cursor-pretool-timeout.md) changes three pins: config producer, Cursor template and installation docs. Cursor preToolUse is bounded20s with failClosed=true; other selected handlers5s, package registration/activation/trust inactive by default.

The repair follows [actual direct5s native timeout12](./delivery-261005-1550-r36-cursor-direct-failure-observer.md), [direct20s Read control13](./delivery-261005-1610-r36-cursor-direct-timeout-control.md) and [Write allow/plan-only prevention14](./delivery-261005-1620-r36-cursor-direct-mutation-control.md). Prior failures and revision-bound receipts remain unchanged. Local synthetic timing does not establish native scheduling/process overhead cause.

## Local delivery

| Gate | Verified r37 result |
|---|---|
| Focused config/runner | {record['focused_config_runner_tests']} tests passed |
| Deterministic suite | {record['deterministic_tests']} tests successful; one Windows symlink skip |
| Reproducibility/build/archive/extraction | Four variants; {record['archives_extractions']} archives/extracted bundles |
| Actual resource readers | {record['resource_reads']} observations |
| Internal OFF comparison | {record['off_no_read_observations']} explicit no-read observations |
| Extracted hook/manual/config projections | {record['hook_projections']} |
| Installer previews | {record['installer_previews']}, no project writes |
| Protected bytes and legacy verifier | {record['protected_hashes']} hashes and {record['legacy_bundles']} legacy bundles preserved |

All six stages exit0, source hash unchanged; [pipeline](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/revalidation-summary.json) has no overall deadline and owned child-process cleanup. Original native-pending pipeline status is retained; this separate checkpoint reconciles fresh native evidence. [Attempt01 setup failure](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01/pipeline-setup-failure.json) happened before any test child started and remains historical. Harness exit0. [Corrected process audit](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/final-process-audit-corrected.json) verifies absent root and zero matching/tracked-live processes by executable, owned run path and PID/creation identity. [Original audit](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/final-process-audit.json) matched its own audit shell PID5144; [failed verifier attempt](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/checkpoint-verifier-attempt-01-failure.json) and helper preimages are retained. No process was stopped for this correction.

## Fresh packaged native r37

[Cursor controls15](./delivery-261005-1700-r37-cursor-packaged-controls.md) / [bindings](./delivery-261005-1700-r37-cursor-packaged-controls.json) bind two actual model turns on CLI2026.09.15-d2fe57e using Grok4.7/context500k/reasoning_effortxhigh/fast=false and freshly built r37 packaged defaults. Public Read→Write produces exact requested bytes; plan-only Write has actual selected-path permission_denied/plan-only-mutation, file unchanged. Read/Write policy event hashes and native denial ID/version/tool/path are bound. Both final markers/Stop observed; artifact QA pending.

Matching cleanup removes26 owned config/payload members and preserves{record['native_historical_preserved']} historical project members. Native/graceful exit requests then exact-identity force-stop leave zero matching/zero tracked-live; harness exit1 retained. Protected global hook/MCP/plugin configs unchanged; CLI-owned state hashes differ and controller direct-write=false. Terminal chunks are bounded/truncated, raw model frames/tool-return content not retained; earlier running deny observation is preserved before final continuation. No model retry conceals failure.

## Remaining acceptance and owner actions

Plan remains **in-progress44/45**, phase3 active, full native event/surface/version task unchecked. [Remaining gate ledger](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/remaining-native-gates.json) keeps private mutation/unsupported routes/full failure matrix and Desktop/IDE surfaces explicit. Local checks and scoped native controls do not close those gates.

- Claude Code CLI2.1.272 has live model/effort options; owner selection remains pending. Existing granted GPT/Grok/Gemini choices do not select a Claude model.
- AGY access and unlock are granted. [Current Computer Use observation](../runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02/agy-window-final-observation.json) returns zero windows under AGY app IDs and attributes the Antigravity-titled window to Codex. No input is sent to that window; recovery needs an identifiable AGY-owned work surface.

Exact r29 VI/EN owner samples remain accepted. Installed r25 stays in place; scientific/stable/release/publication gates remain separate. Controller direct writes to global config/trust stores and publication are not performed; native-owned CLI state has separate before/after hashes, which do not identify changed fields. Rollback restores reviewed source preimages under a new freeze and removes only matching owned project definitions; never overwrite historical source-lock/native evidence or user edits.
"""
with target.open("x", encoding="utf8") as stream:
    stream.write(body)
print(json.dumps({"status": "checkpoint-report-written", "path": str(target)}))
