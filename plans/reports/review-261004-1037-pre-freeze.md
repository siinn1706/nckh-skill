# Rà soát source trước freeze

Status: local source review complete; package/runtime gates pending execution.

Scope: accepted P1–P4 under `/goal ak-cook --auto`. Controller `/root` reviewed
the local candidate against the phase contracts with `ak-code-review`; there is
no Git checkout, so the r26 source archive supplies the preimage comparison.
The independent writer trial is recorded separately, without native/human labels.

## Evidence

- [Pre-freeze state](../runs/nckh-writing-hooks-261004-1037-attempt-01/pre-freeze-state.json): exact baseline identities and case IDs retained; candidate 39 identities/156 base cases; 509 protected hashes unchanged; 281 current source members, 72 Python files parse, 25 schemas use the supported subset, and 469 Markdown links resolve.
- Focused suite (historical evidence path: `tests-261004-1037-pre-freeze.log`; unavailable in the cleaned checkout): 46 actual tests passed. Final affected suites (historical evidence path: `tests-261004-1037-phase-03-surface-binding.log`; unavailable in the cleaned checkout): 22 tests passed after the surface-binding amendment.
- [Independent writer forward test](reviewer-261004-1037-writer-forward-test.md): four bounded agent trials with actual prose/outline/conflict/clarification outputs. No external resource lookup, native telemetry, human taste or scientific verdict. Writer entrypoint bytes are unchanged since that trial; the later guard changes affect visual integrity and do not alter the writer normalization functions.
- [Xia source/schema comparison](researcher-261004-1037-hook-schemas-visual-source.md): selected K-Dense paths/hashes/license and official host schemas; AGY failure behavior and native coverage remain unverified.

## Confirmed repairs

1. Malformed JSON and encoding errors now return the local contract error. Initial failed logs remain available; successful retries do not replace them.
2. Hook transactions retain durable config/ownership preimages and planned postimage hashes before mutation. Interrupted journals block fresh previews; recovery checks matching hashes and preserves later edits.
3. Payload removal checks references in all four known host configs. A malformed config preserves the payload conservatively.
4. Concurrent successful receipts suppress duplicates under kernel locks; failed attempts remain separate. Stop codecs do not submit a continuation.
5. Delivery checks bind final artifact bytes. Computation receipts bind source, code, transform and output; the diagnostic calculation actually reads its transform input and reports a subprocess exit, without inventing process-group evidence.
6. New bundle closure has an exact per-host inventory, source pins and unchanged bytes; dependencies are relocated under `hooks/_shared/`. The plugin projection is inactive. Legacy bundles without hook source remain readable.
7. Activation preview binds host, version and exact surface. CLI summaries omit unowned config values; full config preimages remain in the explicitly saved private preview.

No unresolved implementation defect was found in the inspected local paths.
The mandatory packaged closure suite has deliberately not run before freeze.
This review does not certify a host's timeout/crash/deny behavior, semantic fidelity,
source truth, real research results, native editability or human acceptance.

## Freeze and next checkpoint

Source lock r26 remains unchanged and stale against these edits. `/root` owns the
next freeze under the user's current cook authorization. After freezing, run the
full static/deterministic checks, four-host reproducibility and 16 persistent
bundles; archive/extract outside the repository, inspect actual packaged reads,
and preview installation/configuration with explicit packages. Retain every
failure and freeze a later revision if any pinned bytes require repair.
