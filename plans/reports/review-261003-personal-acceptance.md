# Technical review: personal-use acceptance

Date: 2026-10-03, Asia/Saigon. Work context: `C:/Users/USER/Downloads/test-skill`.

## Scope and authority

- Live reference: controller `/root` delegation to `/root/technical_review`, current task on 2026-10-03; the controller records the user's research → plan → cook grant for personal delivery and owner scoring after use. This reference documents scope; it does not create permission.
- Owned outputs: this report and deterministic review evidence under `plans/evaluation/personal-use/technical-review/`. No product, installer, source lock, historical protocol or other owner's edits were changed by the reviewer.
- Review: implementation contracts and minimal complexity; independent fresh context. This is internal technical verification. External review, protected holdout and owner feedback are not new prerequisites to personal-use delivery.
- Model/control record: requested `inherit`; logical review tier `worker`; configured/applied/effective vendor model and effort, usable window and usage telemetry are unknown in this evidence. No provider trial, paid evaluation or credential inspection was performed.

The assigned plan/phase, implementation report, profile, reader, policy, workflow, cook skill, tests, state/build helpers, personal-use guide and historical qualification protocol were read. Additional bounded reads covered the existing strict JSON loader/schema, native maker/reviewer role instructions and model/context contract.

## Findings resolved during review

No actionable finding remains in the final reviewed source. The two initial low-severity failures and their correction evidence are retained below.

### Low — duplicate keys silently select a different acceptance contract

- Initial location: `nckh-kit/core/acceptance.py:35`–`40`, compared with `nckh-kit/core/build.py:25`–`38`.
- Reproduction: the preserved fixture declares `"schema_version": 999` followed by `"schema_version": 1`. `_load_json` plus `validate_profile` accepts the fixture, while the existing repository loader raises `ContractError: duplicate JSON key: schema_version`.
- Effect: malformed local acceptance/catalog JSON can silently replace a declaration through last-key-wins parsing. The new reader has weaker parse behavior than the existing repository reader. No duplicate exists in the reviewed actual profile, and no authorization bypass was observed.
- Smallest correction: reuse the existing strict JSON parse behavior, preserving the acceptance reader's located error reporting. No new validation framework or schema is necessary.
- Owner: controller/implementation owner. Status: resolved. Current `acceptance.py:13`/`33`–`37` reuses `core.build.load_json`; the final probe rejects the preserved fixture with `ContractError: duplicate JSON key: schema_version`.

### Low — boolean schema version passes as integer version 1

- Initial location: `nckh-kit/core/acceptance.py:123`.
- Reproduction: copying the current profile and setting `schema_version = True` is accepted by `validate_profile`, because Python compares `True == 1`. The existing contract validator and state tests explicitly distinguish booleans from integer versions.
- Effect: the declared version contract is not enforced for malformed input. The current actual profile uses integer `1` and is unaffected.
- Smallest correction: require `type(profile.get("schema_version")) is int` before comparing the value to `1`.
- Owner: controller/implementation owner. Status: resolved. Current `acceptance.py:122`–`124` checks exact integer type; the final probe rejects the boolean version with `ContractError: unsupported acceptance profile schema`. Regression coverage is in `tests/acceptance/test_profile.py:61`–`70`.

No critical security, data-loss or outage issue was found in the reviewed scope.

## Instruction conflicts corrected during review

The initial source still proposed an interactive default when the caller omitted a mode and said auto waits at taste. That contradicted the approved personal delivery followed by owner scoring. The controller repaired the instructions; this reviewer reread the repaired files.

- `nckh-kit/core/workflows/execution.md:8`–`13` and `nckh-kit/skills/core/nckh-cook/SKILL.md:35` now continue already-authorized implementation/checks/delivery without a mode flag, preserving an explicit approved mode and actual scope boundaries.
- `execution.md:46`–`51` and cook `SKILL.md:39`/`46`–`48` now permit usable personal delivery while owner/taste feedback remains pending.
- `nckh-kit/core/policies/acceptance-policy.md:44`–`49` now scopes the reviewer/threshold/development-round freeze to historical stable/scientific qualification. Final personal owner review follows usable delivery.

These corrections are verified instructions, not observations of an agent obeying them in a native runtime.

## Verified contracts and complexity

| Check | Result and evidence |
|---|---|
| Exact identity coverage | 37 profile identities equal the 37 catalog identities; kit/status/eval IDs are checked. |
| Sources and references | 35 source records; 53 URL entries representing 51 unique URLs; no undefined source IDs. The implementation report's 51 URL count is consistent with distinct URLs. |
| Substantive applicability | Applicability contains conditions and exclusions: PRISMA only for the applicable systematic-review type; ICMJE primarily medical publishing; IEEE policy only for the applicable venue; CAN-SPAM US commercial email; PECR UK; platform-specific GA4; WCAG/full-page level and web-only performance guidance. This is more than a list of source titles. |
| Applicability limitation | The validator checks nonempty fields and references. It does not semantically establish source support or freshness. Source-specific applicability was inspected locally; no duplicate web audit was performed. The repeated generic limitation sentence is not a new substantive limitation for each source, but the applicability statements carry concrete scope. |
| Owner feedback | Missing feedback produces `pending-personal-review`; revision, artifact and input hash mismatches raise `ContractError`. A recorded owner verdict remains evidence, without stable/scientific aggregation. |
| Skill reachability | All 37 source skill closures contain the profile. A deterministic simulation of the existing materialization mapping found zero broken remapped local Markdown links. This is closure/projection evidence, not a built bundle or runtime claim. |
| Native role transport | Six existing optional role closures contain authorization and model/context, not the profile; build flattening removes Markdown link targets, leaving no unresolved native-role href. Under the assigned same-agent/default scope, roles receive their task/skill/profile contract from the controller packet. These roles are not 37 extra skill identities or a new delivery gate. |
| Reader availability | Policy explicitly distinguishes repository Python lookup from direct self-contained JSON consumption. A native package must package Python dependencies only if it invokes that reader. The current skill closure does not promise an installed Python API. |
| Existing state behavior | Existing state lifecycle/aggregate/interactive contracts remain separate; the new feedback helper neither creates a competing execution state machine nor accepts on behalf of the owner. Existing state/evidence tests pass, and state/build/schema hashes equal the initial review snapshot. |
| Historical boundary | Profile keeps `experimental`, forbids protocol mutation and does not certify stable/scientific/native/provider/venue. The protocol was read only; its hash matches both the initial review snapshot and the current lock pin. Its SHA-256 at review was `8219a98f78073263105ae8e035a4701a98c5d0b3e270f40070f7a9b3a5f344f4`. |
| Minimal complexity | A single shared profile and a repository lookup/binding helper are proportionate. Common checks are declared once; per-skill rows carry distinct criteria. The worthwhile DRY correction is strict JSON parsing above. Rewriting state, adding a provider, adding mandatory role discovery or splitting into 37 manifests is unnecessary. |

## Checks and raw evidence

From `nckh-kit`:

```text
python -m unittest tests.acceptance.test_profile -v
python -m unittest tests.acceptance.test_profile tests.contracts.test_state tests.evidence.test_guards -v
```

Initial reviewer results: 6/6 acceptance tests and 23/23 acceptance/state/evidence tests passed, exit 0. After the controller's correction, the final combined run passed 24/24 tests (7 acceptance tests plus the unchanged state/evidence checks), exit 0. `PYTHONDONTWRITEBYTECODE=1` was set for reviewer runs.

From the workspace:

```text
python plans/evaluation/personal-use/technical-review/verify-profile.py
python plans/evaluation/personal-use/technical-review/verify-profile.py final
```

The probe is read-only over product source. It creates a clearly labelled malformed synthetic configuration fixture and preserves its actual parser results; that fixture is not user/domain gold or live acceptance.

- Acceptance stdout (historical evidence path: `../evaluation/personal-use/technical-review/acceptance-tests.txt`; unavailable in the cleaned checkout)
- Regression stdout (historical evidence path: `../evaluation/personal-use/technical-review/regression-tests.txt`; unavailable in the cleaned checkout)
- [Deterministic probe](../evaluation/personal-use/technical-review/verify-profile.py)
- [Initial probe receipt and source hashes](../evaluation/personal-use/technical-review/profile-review.json)
- Initial probe stdout (historical evidence path: `../evaluation/personal-use/technical-review/profile-review.txt`; unavailable in the cleaned checkout)
- [Final probe receipt and source hashes](../evaluation/personal-use/technical-review/profile-review-final.json)
- Final probe stdout (historical evidence path: `../evaluation/personal-use/technical-review/profile-review-final.txt`; unavailable in the cleaned checkout)
- Final 24-test stdout (historical evidence path: `../evaluation/personal-use/technical-review/regression-tests-final.txt`; unavailable in the cleaned checkout)
- [Duplicate-key fixture](../evaluation/personal-use/technical-review/duplicate-profile.fixture.json)
- [Controller's first repair attempt](../evaluation/personal-use/technical-review/controller-repair-attempt-01.json)
- [Report links, shared-file preservation and final source match audit](../evaluation/personal-use/technical-review/report-audit.json)

The controller's first added regression run failed on a Windows temporary-directory ACL. That failed attempt is retained. The current test uses the existing `core.paths.temporary_tree`; the final reviewer run passed it. No failing assertion was removed or weakened.

A Git diff command was unavailable because `nckh-kit` is not a Git repository. No Git-backed unchanged-history claim is made. Product file hashes are preserved in the probe receipt.

## Scoped gate matrix and recommendation

| Gate | State | Scope |
|---|---|---|
| Valid current profile, references, feedback binding | Verified | Local current source and focused tests. |
| Authorized default delivery and deferred owner/taste feedback | Verified instructions | Controller corrections reread; native behavior remains a separate runtime observation. |
| Rejection of malformed duplicate/boolean versions | Verified | Both initial failures are now rejected; preserved probe results and the new regression case verify the repair. |
| Source freeze and actual generated bundle | Controller phase 4 | Source lock at inspection was revision 22; this review does not perform or certify the pending freeze/build. |
| Selected native/application smoke | Controller runtime phase | This review adds no discovery/certification gate or paid run. |
| Owner score after use | Pending owner action | Does not block usable personal delivery; do not fabricate an owner verdict. |
| Stable/scientific eligibility | Separate historical lane | Does not block this approved personal-use lane. |

Recommendation: continue the authorized personal delivery and selected runtime work. The two parser inconsistencies were repaired with the existing loader and an exact-type check; no additional architecture, external reviewer, protected holdout or universal threshold is justified by this review.

Status: DONE
Summary: 37 identities, substantive source scope, closure links and feedback binding are verified. The controller resolved default-mode/taste/freeze wording and both malformed-input failures; the final 24-test regression and deterministic probes pass.
Concerns/Blockers: no remaining technical finding in this review scope. Controller owns source freeze/build and selected runtime observations; owner personal scoring follows use.
