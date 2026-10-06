---
title: NCKH runner journal repair
date: 2026-10-01
summary: 81 local tests pass on revision 18; incomplete journals repaired; full qualification remains pending
---

# NCKH runner journal repair

## Cause and repair

Revision-17 fault injection showed that a lifecycle wait exception and a failed case read after preview could escape the private run handler, leaving its journal running. The reproduction dispatched no driver and is retained with an explicit deterministic-fixture label.

Moved case loading inside the receipt scope and handled lifecycle exceptions. Timeout now records an unknown outcome/exit status and unverified cleanup; subprocess exception summaries omit command arguments. Added two regression tests. The caller must still reconcile actual owned processes before retrying after incomplete cleanup.

## Actual verification

Sixteen focused command-runner tests and four affected existing tests passed. Full discovery passed 81 tests in 345.721 seconds on revision 18, 184 pins, source hash f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d. All four hosts built twice with matching hashes, including optional plugin projections. The retained new build has 2554 checksum entries.

New source-bound records are runner-cleanup-local-checks.json, runner-cleanup-reproducibility.json, runner-cleanup-build.json and candidate-runner-cleanup.json. Artifacts are in dist-runner-cleanup. Revision 14/17 receipt and artifact hashes were rechecked and preserved, as were all 43 installed item hashes, ownership bytes and model-policy hash. No installed update, provider evaluation, Git initialization, commit or publication occurred.

## Completion audit

Reviewed all seven phase requirement/step/success/validation sections. The plan stays in-progress at 28/36 tasks; no phase has full acceptance. Source/fixture/build proof does not close the 148 skill cases, 224 full native cells, ten full installer/OS scenarios, matched baselines, human/domain/native-visual review, cross-run lineage or protected holdout requirements. The owner has no VI/EN corpus/reviewers; provider funding/authority and native environment/effective-model evidence remain absent.

This turn made concrete implementation progress and did not mark the goal complete. Further qualification needs the corresponding human inputs and external state/authority. Cost remains unknown; accepted tasks are zero and stable/public release is NO-GO. See plans/reports/implementation-261001-nckh-runner-journal-repair.md. AgentWiki publish skipped.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
