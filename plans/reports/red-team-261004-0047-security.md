# Red-team security review — research/data/visuals/hooks plan

## Scope and verdict

- Review-only, plan-only; no implementation, install, native host, model, network, build or test run.
- Read the six plan documents, the two requested researcher reports, and the requested guards/install/paths/authorization/brief/adapter sources. Narrow `rg` confirmed no current `visual_purpose`, hook runner/codec, or hook ownership implementation.
- Focus: Phase 2 research-only visual enforcement and Phase 3 portable hooks, using a hostile trust-origin, purpose-bypass, privacy, and shared-config lens.
- No Critical finding is evidenced. Five consequential gaps remain; the plan should not claim a fail-closed research-only boundary until the fixes below are explicit and evidenced.

## Findings

### High — F-01: the new `visual_purpose` contract leaves authorization origin unspecified

Evidence: Phase 2 says the guard consumes a brief-supplied `visual_purpose` and `evidence_ids` (`phase-02-scientific-visuals.md:10,14-17,37-41`) and promises every direct/indirect route is guarded (`:49-53`). The current brief makes `authorization_reference` and `private_store` optional (`nckh-kit/core/contracts/brief.schema.json:54-60`); its required set ends at `mode` (`:85-95`). The authorization policy explicitly says model output, JSON approval fields, and source text are not grants (`nckh-kit/core/policies/authorization-policy.md:3-6`). Existing claim checking verifies IDs, hashes, status, locators, and context, but no caller/authorization origin (`nckh-kit/core/guards.py:23-43`).

Failure if the proposal is implemented without an additional local trust-origin rule: a marketing/analytics/provider route, or model-produced brief, could declare a research question/object/role and point at a current evidence record. A structural evidence match could then be mistaken for permission to create a research visual, violating the kit-wide research-only requirement. This is a new-feature contract gap, not evidence of a current `visual_purpose` bug; that field/guard does not exist yet.

Fix direction: make the plan name the authoritative local trust boundary at the artifact edge and define the absent/stale behavior. An owner-approved option is a controller-owned sidecar/capability handle bound to task/session/host, `domain=research`, route identity, and allowed visual purpose; another is an already-authorized host/task context. Do not make a new private service or “non-forgeable” capability mandatory without an approved owner and threat-model decision. In every option, model/source fields remain data, not grants, and the final visual boundary must recheck the selected context for indirect consumers.

### High — F-02: the new hook event contract does not specify how trusted origin is observed

Evidence: Phase 3 feeds host event JSON into codecs and a pure policy (`phase-03-portable-hooks.md:10,31-40`), while its task only says to reject JSON as an authorization/grant (`:38`) and to preserve bounded receipts (`:14-18,41-42`). The same optional authorization fields and structural-only guard are present in the current contracts (`nckh-kit/core/contracts/brief.schema.json:54-60,85-95`; `nckh-kit/core/guards.py:23-43`). All adapters still report hooks `not-installed`, host-permission-only enforcement, and unverified coverage (`nckh-kit/adapters/claude/adapter.json:42-45`, `codex/adapter.json:54-57`, `cursor/adapter.json:51-54`, `agy/adapter.json:48-51`).

Failure if a future codec treats payload fields as its only context: a project/source/model could forge a benign event, artifact hash, rights state, or `research-purpose` field. Without a defined local context binding, the policy could not distinguish a host-delivered event from attacker-controlled JSON and might return `allow` or suppress a required manual gate. This is a proposal contract gap, not a current hook vulnerability: the task already states that JSON is not an authorization/grant, and no hook runner exists today.

Fix direction: specify how the policy receives trusted context using the existing local instruction/host-grant boundary. An owner-approved option is a controller-side record containing host surface/version/session and event identity; a lighter option is an explicitly validated host/task context already available to the runner. A new private controller service or non-forgeable capability is not approved by this review and must not be assumed. Regardless of the selected option, payload grant-like fields stay untrusted, artifact/path hashes are checked against the owned ledger, and missing/stale/mismatched context has an explicit `not-callable/manual` outcome.

### High — F-03: fail-open or unverified host behavior can bypass the promised fail-closed visual boundary

Evidence: Phase 2 requires prohibited visual cases to fail closed (`phase-02-scientific-visuals.md:15-17,40-53`). Phase 3 allows `degraded/failed` or manual outcomes for malformed/timeout/crash events (`phase-03-portable-hooks.md:14-18,44-56`). The native capability report says Claude event/schema, quoting, trust, and tool coverage still require implementation checks (`researcher-261004-0047-native-hook-capabilities.md:11-14`); it documents Cursor crash/timeout and default exit behavior as potentially fail-open unless a supported `failClosed` permission hook is proven (`:15-16`). It also states hooks are not a sandbox and native evidence is absent (`:28-41`). A separate report describes fail-open behavior in upstream ClaudeKit scripts, which is not evidence of a Claude host default (`researcher-261004-0047-hook-resources.md:42-47`).

Failure: a Cursor route can receive a timeout, crash, unsupported event, or missing hook and still let an artifact-producing operation proceed where the documented host default is fail-open. For Claude, Codex, and AGY, the evidence currently establishes coverage/trust/version uncertainty rather than a default fail-open rule; that uncertainty still provides no basis for claiming pre-artifact enforcement. `enabled=false` and “manual fallback” do not by themselves enforce a pre-artifact decision, so the measurable “every route”/“fail closed” claim is not met.

Fix direction: make proven host capability a prerequisite for claiming hook enforcement at the artifact boundary. For Cursor, and for any other host if later evidence shows fail-open behavior, require a receipt proving deny behavior for malformed, timeout, crash, and unsupported cases; otherwise mark the hook `not-callable` and require a synchronous local/manual preflight before generation. Do not treat an exit code or post-delivery receipt as protection against a side effect that already occurred.

### High — F-04: shared-config preservation is promised but not backed by an ownership/merge contract

Evidence: Phase 3/4 require preserving shared Codex/AGY `.agents`, invalid JSON, later edits, and only owned hook blocks (`phase-03-portable-hooks.md:41,50-52`; `phase-04-integration-and-personal-acceptance.md:42,53-55`). Current ownership validation only admits top-level `items`, `installs`, and `policies` (`nckh-kit/core/install.py:49-58`); installation projects skills/native agents, not hook blocks or JSON pointers (`:149-229`). Commit writes whole staged owned paths and the ownership index (`:554-635`), while `atomic_json` replaces a complete target file (`nckh-kit/core/paths.py:97-108`). Adapter roots show shared `.agents` paths for Codex and AGY (`nckh-kit/adapters/codex/adapter.json:8-30`; `agy/adapter.json:8-24`).

Failure: a future hook merge can neither prove which JSON members it owns nor safely rebase a concurrent user edit. A stale preview, duplicate shared definition, or malformed/partially edited config can overwrite user policy or leave a hook enabled outside the intended namespace—contrary to the no-overwrite and default-off claims.

Fix: specify per-target owned JSON pointers/blocks, preimage and parent-file hashes, lock scope, and a three-way merge rule. Any unknown member, changed preimage, invalid JSON, duplicate visible definition, or concurrent edit must stop in preview with no write. Register hook ownership separately from skill ownership and require a post-merge assertion that no host registration/trust state changed.

### Medium — F-05: locator and receipt fields can leak private paths or sensitive context

Evidence: Phase 2 requires source locators, rights, and artifact/render hashes in the source-to-mark record (`phase-02-scientific-visuals.md:37-41`); Phase 3 permits owned receipts (`phase-03-portable-hooks.md:16,41`). The current visual receipt checker accepts arbitrary file paths and references, hashes them, and returns status without a privacy classification or redaction (`nckh-kit/core/guards.py:61-69`). The authorization policy requires private manuscripts/corpora/raw transcripts outside source/dist and opaque evidence references in public receipts (`nckh-kit/core/policies/authorization-policy.md:17-20`).

Failure: an absolute private dataset path, transcript-derived locator, command, or credential-bearing reference can enter a QA manifest, hook receipt, package, or shared config even when the file bytes are not copied. Content hashing does not make the locator itself safe.

Fix: split public manifests from a private sidecar; constrain public fields to opaque evidence IDs, approved relative locators, access class, and content hashes. Reject absolute paths, environment/credential material, commands, transcript text, and unapproved URLs at schema validation; add negative cases for leakage before packaging or hook receipt write.

## Verified / failed / unverified claims

### Verified from current source

- This turn is plan-only and explicitly leaves implementation/install/native/provider/trust work pending (`plan.md:16,41-43`).
- The existing brief has optional authorization/private-store fields, structural guards have no trust-origin check, current adapters have no installed/enforced hook state, and current installer ownership covers skills/agents rather than hook JSON blocks (citations above).
- The source/resource delta is intentionally recorded as r26 versus installed r25; this review does not treat that as a defect (`plan.md:18`; `phase-04-integration-and-personal-acceptance.md:14-16`).
- The plan and hook-resource report reject copying proprietary ClaudeKit code and retain the rights conflict as a no-copy boundary (`source-adoption-map.md:19,24-28`; `researcher-261004-0047-hook-resources.md:8-16,60-66,84-93`).

### Failed or insufficient for the security contract

- “Research-only through all direct/indirect routes” is not yet contract-verifiable from the proposed brief fields because trusted authorization origin and route binding are unspecified; this is a new-feature plan gap, not a current implementation violation (F-01).
- “Reject JSON as grant” is an explicit existing boundary, but the new event contract does not say how a future codec observes trusted host/task context or handles stale/missing context (F-02).
- “Fail closed” is not established for Cursor’s documented fail-open/default behavior or for the other hosts whose coverage/trust/version remain unverified; no implementation/native receipt exists yet (F-03).
- Shared-config preservation/default-off claims lack a block-level ownership and concurrent-merge contract in the current installer model (F-04).
- No-path/secret privacy claims are not schema-enforced for planned locator/receipt fields (F-05).

### Unverified by design (no run authorized)

- Exact host event/output schemas, supported `failClosed` surfaces, trust prompts, event coverage, and deny semantics for each version.
- Any new `visual_purpose`, source-to-mark, hook schema/runner/codec, indirect-route fixture, or native receipt; none exists in the current tree.
- Owner-selected hard-block classes and the final private-store/sidecar location.

## Unresolved questions

1. What controller-owned capability/sidecar is the authoritative source for visual purpose and hook authorization, and how is it bound to task/session/host?
2. Which exact host/version/event combinations are permitted to claim pre-artifact fail-closed enforcement?
3. What JSON block namespace and three-way merge/lock protocol owns hook configuration without touching shared `.agents` policy?

Status: DONE_WITH_CONCERNS
Summary: The plan has strong no-copy, off-by-default, and evidence-boundary intent, but Phase 2/3 still need explicit trusted-origin, host-fail-closed, shared-config ownership, and receipt-privacy contracts before its security claims are verifiable.
Concerns/Blockers: No implementation or native receipt exists; the findings are plan-level blockers, not evidence that the requested new scope already violated the old specification.
