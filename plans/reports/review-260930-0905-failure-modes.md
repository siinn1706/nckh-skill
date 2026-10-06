# Failure-mode review: Vietnamese research skill kit

## Scope and limits

- Reviewed `plan.md`, `phase-01` through `phase-05`, and the requested
  brainstorm/synthesis reports; trace: `research-plan`/approval → P1 resolve/
  execute/critic → P2 evidence → P3 writing → P4 visuals → P5 package/handoff.
- Plan-only: `CREATE` files are future proposals, not failures; no runtime,
  provider, human review, or test result was available.
- `VERIFIED` means explicitly/consistently specified by documents, not runtime
  proof; `FAILED` is a concrete missing transition/recovery; `UNVERIFIED` needs
  runtime/user/human evidence; `PROPOSED` is a future check only.

## Verification tier

Fifteen controls were sampled per phase across flow, recovery, dependency and
acceptance sections (75 total).

| Phase | Sampled | VERIFIED | FAILED | UNVERIFIED | PROPOSED |
|---|---:|---:|---:|---:|---:|
| P1 foundation/adapter | 15 | 10 | 2 | 1 | 2 |
| P2 evidence/research | 15 | 10 | 2 | 1 | 2 |
| P3 VI/EN writing | 15 | 11 | 1 | 1 | 2 |
| P4 visuals | 15 | 11 | 1 | 1 | 2 |
| P5 evaluation/package | 15 | 9 | 2 | 2 | 2 |
| **Total** | **75** | **51** | **8** | **6** | **10** |

Counts measure plan-flow consistency only; they do not demonstrate any adapter,
worker, visual format, reviewer, holdout, or quality gate exists.

## Findings

### F-01 — High — P1 execute/critic: no recoverable partial-execution commit protocol
- **Flaw:** Timeout and side effect are named, but there is no durable attempt
  state, idempotency key, artifact commit boundary, or reconciliation/adoption
  path for a worker that timed out after writing or acting.
- **Failure scenario:** A native worker creates an artifact (or performs an
  allowed side effect), then the adapter times out before its receipt arrives.
  A resume cannot distinguish “not started”, “completed but receipt lost”, and
  “side effect unknown”; retry can duplicate work or discard a usable artifact.
- **Evidence:** `phase-01-start.md:47-49,111-112,128-140`; `brainstorm-260930-0905-skill-kit-contract.md:73`.
- **Suggested fix:** Add attempt/operation IDs and durable states such as
  `started`, `staged`, `committed`, `timeout-unknown`, and `reconcile-required`.
  Require hash-based artifact adoption or explicit user approval before retrying
  an operation whose side-effect status is unknown.

### F-02 — High — P1 lifecycle: approval/authorization drift is not a resume guard
- **Flaw:** The lifecycle explicitly invalidates profile/input/dependency drift,
  but the resume matrix does not require a current approval/consent revision for
  egress, sample rights, provider, license, or reviewer/API permission.
- **Failure scenario:** A paused cook is resumed after the user withdraws a
  sample license or changes egress policy. Inputs remain identical, so the only
  explicit resume check can pass while the old authorization is reused.
- **Evidence:** `phase-01-start.md:46-48,57-64,102-112,128-135`; `phase-05-evaluation-and-packaging.md:66-69`.
- **Suggested fix:** Version the approval/consent record and bind its hash to
  plan, cook, receipt, and handoff. Any rights, egress, provider, venue, or
  human-gate change must invalidate approval and require a fresh authorization.

### F-03 — High — P1→P5 contracts: no transitive revision invalidation evidence
- **Flaw:** P1 says a reviewed contract revision invalidates “affected receipts”,
  but receipts/handoffs do not explicitly carry a contract revision/hash and no
  dependency graph defines how invalidation reaches downstream artifacts.
- **Failure scenario:** P1 changes an evidence field after P2 produced a package;
  P3/P4 continue consuming the old package and P5 sees valid-looking worker and
  output hashes without a stale-contract marker.
- **Evidence:** `phase-01-start.md:35-37,57-60,92-94`; `phase-02-evidence-and-research.md:91-97`; `phase-05-evaluation-and-packaging.md:88-92`.
- **Suggested fix:** Include contract revision/hash in every plan, approval,
  receipt, artifact manifest, and phase handoff. Define a transitive invalidation
  graph and make each downstream gate reject artifacts on inactive revisions.

### F-04 — High — P2 claim ledger→P3 writer: no executable verdict policy
- **Flaw:** P2 defines `supported`, `contradicted`, `insufficient`, and
  `unverified`, while P3 can merely mark output `UNVERIFIED`; no rule maps each
  verdict to omission, qualification, blocking, or allowed assertion.
- **Failure scenario:** A contradicted claim is rendered as an asserted sentence
  with an `UNVERIFIED` marker and proceeds as a draft to P4/P5. A visible status
  is not the same as preventing the sentence from being accepted in scope.
- **Evidence:** `phase-02-evidence-and-research.md:52-58,102-103`; `phase-03-vietnamese-and-english-writing.md:50-54,100-106,129-135`.
- **Suggested fix:** Define a claim-to-sentence matrix: supported may assert;
  insufficient/unverified must be qualified or omitted; contradicted blocks the
  sentence until resolved. Enforce the mapping at P3 handoff and P5 acceptance.

### F-05 — High — P1–P5 handoffs: no aggregate dependency status gate
- **Flaw:** Each phase uses different statuses (`accepted`, `pending`,
  `evidence-pending`, `human-review-required`, `accepted-for-scope`), but no
  shared lattice or precondition says how a downstream status is computed.
- **Failure scenario:** P4 marks visuals `accepted` while P3 remains
  `evidence-pending`; P5 can then produce an `accepted-for-scope` package without
  an explicit rule that an open mandatory dependency forces `pending`/`blocked`.
- **Evidence:** `phase-01-start.md:49`; `phase-02-evidence-and-research.md:52-54`; `phase-03-vietnamese-and-english-writing.md:54`; `phase-04-slides-and-scientific-visuals.md:49-50`; `phase-05-evaluation-and-packaging.md:41-52,127-139`.
- **Suggested fix:** Define one status algebra and dependency precondition table.
  Aggregate status must remain `pending`/`blocked` when any required input is
  open; allow `accepted-for-scope` only when explicitly excluding open outputs.

### F-06 — High — P4 authoring→QA: repair can leave a stale passing receipt
- **Flaw:** The plan allows repair after clipping/collision, but does not bind QA
  to immutable source, data, render, manifest, and viewer hashes or invalidate a
  prior audit when any of them changes.
- **Failure scenario:** An author edits the source to fix a render failure, then
  hands off the changed source with the old passing report/manifest. The prior
  truth mapping and editability inspection no longer prove the delivered file.
- **Evidence:** `phase-04-slides-and-scientific-visuals.md:48-50,68-70,103-106,120-129,156-162`.
- **Suggested fix:** Record a source/data/render/manifest hash tuple and QA run
  ID. Any repair, data/font/viewer change invalidates prior QA and requires
  truth-map, semantic, native-object, and render checks again.

### F-07 — High — P5 holdout: exposure/rotation is not enforceable
- **Flaw:** The plan says an exposed holdout becomes development and a new one is
  needed, but does not define label isolation, access roles, exposure logging,
  replacement lineage/hash, or invalidation of the exposed result.
- **Failure scenario:** A local evaluator/worker can read the holdout answer in
  the case inventory, tune against it, and still submit the original result or a
  replacement with no auditable relation to the exposed set.
- **Evidence:** `brainstorm-260930-0905-skill-kit-contract.md:94`; `phase-05-evaluation-and-packaging.md:32-36,76-83,96-105,127-138,148-150`.
- **Suggested fix:** Keep labels outside worker/evaluator context, log every
  reveal, mark the result invalid on exposure, and create a hashed replacement
  with parent/exposure lineage before any new comparison.

### F-08 — Medium — P5 review/evaluation: no terminal adjudication/iteration rule
- **Flaw:** Reviewer roles, raw counts, uncertainty, and user-owned thresholds
  are required, but there is no minimum reviewer/coverage rule, disagreement
  adjudication, maximum development rounds, or terminal state for unresolved
  thresholds/budget.
- **Failure scenario:** A reviewer disagreement or missing subjective threshold
  can be repeatedly re-run, or comments can be “consolidated” into an acceptance
  state without a recorded adjudicator; the candidate never reaches a principled
  stop.
- **Evidence:** `phase-05-evaluation-and-packaging.md:48-69,104-115,127-142,164-177`; `brainstorm-260930-0905-skill-kit-contract.md:94`.
- **Suggested fix:** Add `UNRESOLVED_REVIEW`, `PENDING_USER_THRESHOLD`, and
  `BUDGET_EXHAUSTED` non-accepting states; specify reviewer quorum/adjudication,
  max rounds/attempts, and a hard stop before any `accepted-for-scope` result.

### F-09 — High — P2→P5 source checks: correction/retraction can stale evidence
- **Flaw:** Source version/hash and check date are recorded and retraction checks
  are planned, but no freshness/recheck trigger at P2→P3/P4/P5 invalidates claims
  when the external source status changes after the initial audit.
- **Failure scenario:** A paper is checked as eligible, then corrected/retracted
  before writing or packaging. The immutable P2 package remains usable because
  its old verdict is preserved, and downstream stages have no stale-status gate.
- **Evidence:** `phase-02-evidence-and-research.md:50-56,106-107,123-130,152-156`; `phase-03-vietnamese-and-english-writing.md:100-106`; `phase-05-evaluation-and-packaging.md:101-108,127-139`.
- **Suggested fix:** Pin a permitted source snapshot or define status freshness
  and recheck at every downstream handoff. A changed correction/retraction
  revision must invalidate dependent claims, text, visuals, and package review.

## Unresolved questions

1. Should an allowed local/native worker be treated as potentially side-effecting
   even when no provider is configured, or can P1 guarantee a pure artifact route?
2. What exact user action/version is the authoritative approval revocation event?
3. What reviewer quorum, maximum evaluation rounds, and subjective thresholds are
   intended for the first accepted-for-scope package?

Status: DONE_WITH_CONCERNS
Summary: Plan-only failure-mode review completed with 9 findings: 8 High and 1 Medium. The proposed flow is internally traceable in documents, but timeout recovery, authorization/contract invalidation, cross-phase status gating, source freshness, visual repair provenance, and evaluation termination need explicit contracts before implementation.
