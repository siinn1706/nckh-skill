# Independent review — authored research resource provenance

Status: DONE_WITH_CONCERNS

Reviewed fingerprint time: 2026-10-06T02:55:53.121490+00:00 (Asia/Saigon: 09:55:53).

## Scope and authority

Review reference: controller delegation `/root/review_owned_provenance`, received 2026-10-06; scope revision 1. The delegation records the existing project-local `--auto` mechanical-work scope and assigns an independent read-only P5/P7 review. This report is the only owned output. The delegation is not a new grant for provider/cloud/native/global installation/publication. No source edits, source-lock freeze, new build, pinned source tests or release tests were performed.

The review covered P5/P7 phase contracts, the four authored packs, contribution ledger, owned/legacy registry and pin dispatch, bundle serializer/schema/verifier, bounded research IO, standalone lookup, declared closure and smoke dispatch. Preserved r38 and r33 Codex bundles were inspected and passed to the current read-only verifier at the controller's explicit request.

Review method: independent fresh task context plus deterministic local reads and in-memory adverse fixtures. Requested/resolved/configured/applied model setting: inherited session; native effective model/effort, usable window and total cost telemetry: unknown. Model independence and human scientific expertise are not established by this review. No nested agents, credentials or network/provider calls were used.

## Findings

| ID | Severity | Finding | Owning surface/action |
| --- | --- | --- | --- |
| F1 | High | Correct authored file records are serialized with `rights=owned-reference` and provenance, but the bundle verifier rejects them; its resource binding gate also requires `copied-upstream`. | `core/build.py`: complete the distinct authored file and resource binding branches without loosening the legacy copied checks. |
| F2 | High | The enlarged current hook inventory is required from historical bundles, so preserved r38/r33 format-2 packages fail unchanged. | `core/build.py`: resolve allowed exact hook closure from the bundle's pinned historical implementation/version, preserving strict original hashes. |
| F3 | Medium | Contribution-to-record membership is checked in only one direction; provenance can claim a source supports a row that no longer cites that source. | `core/owned_resources.py`: compare the exact record-ID set from actual rows for every contribution source. |
| F4 | Medium | The output budget validates compact JSON, while the CLI emits larger indented JSON; domain mismatch also bypasses query/output bounds. | `scripts/search-resource.py`, `core/research_io.py`: bound the actual emitted representation and apply trusted query/result bounds before every return. |
| F5 | Medium | Standalone lookup trusts the selected row's consumer list without checking current catalog identity, allowing an unknown consumer to cause a pack read. | `scripts/search-resource.py` and closure declarations: validate exact catalog identity before source reads and include the catalog dependency in relocated closures. |

### F1 — Serializer/verifier disagreement blocks authored packages

Locations at the reviewed bytes:

- `core/build.py:387`: materialized file records retain the pin's `rights` and `provenance`.
- `core/build.py:510`: only `copied-upstream` receives a provenance branch.
- `core/build.py:518`: any other file with provenance raises `owned artifact cannot relabel copied bytes`.
- `core/build.py:605`: resource binding explicitly requires file rights `copied-upstream`.
- `installer/schemas/bundle-v2.schema.json`: the widened file-row enum/schema already accepts a correctly shaped authored file record.

Deterministic check: formed a manifest file row from the actual statistical pack's source hash and `owned_provenance`, with `rights=owned-reference`, then called `core.schema.validate(row, bundle_schema['properties']['files']['items'])`. Observed: `serializer owned row schema ACCEPTED`. Reading the verifier's unconditional branches establishes that the same valid record cannot pass `verify_bundle`; the resource binding predicate would fail next even after the file branch is repaired.

No candidate was generated to bypass the intentionally stale r38 source lock. This finding is a located serializer/verifier mismatch, not a claimed post-freeze build result. Any repair must additionally verify original authored bytes/provenance against the embedded pin and require each consumer's actual rights/attribution closure.

### F2 — Real historical hook packages fail the current verifier

Locations: `core/build.py:46` adds three hook-shared members; `core/build.py:101`–`116` builds the required hook mapping from current constants for every package.

Read-only reproductions, using `core.build.verify_bundle(Path(...))` from `nckh-kit`:

```text
plans/runs/nckh-upgrade-native-261006-0850-attempt-01/bundle/codex
  embedded revision: 38
  rejected: hook closure requires the exact bounded host inventory

plans/runs/nckh-native-261004-2112-r33-attempt-01/build/on-plugin/codex
  embedded revision: 33
  rejected: hook closure requires the exact bounded host inventory
```

For both actual manifests, subtracting their `hooks.members` from `hook_source_mapping('codex')` returned exactly:

```text
hooks/_shared/core/contracts/owned-resource-provenance.schema.json
hooks/_shared/core/owned_resources.py
hooks/_shared/core/research_io.py
```

Calling `_verify_hooks(manifest, embedded_lock, manifest['files'])` separately produced the same rejection. Thus this is a current verifier compatibility regression on preserved artifacts, independent of the stale live source lock. Historical format-1 dist manifests r14/r17 contain no hook declaration; no new format-1 delivery result is claimed.

### F3 — Reverse source bindings can drift

Locations: `core/owned_resources.py:71`–`97`, especially line 90. Every row's selected source must contain its ID in that contribution; no check requires every contribution's `record_ids` to equal the rows actually selecting that source.

Minimal reproduction, entirely in memory:

```python
from pathlib import Path
from core.resources import registry
from core.owned_resources import read_pack, validate_pack_rows

root = Path.cwd()
resource = next(row for row in registry(root)['resources']
                if row['resource_id'] == 'R-telemetry-dictionary')
rows = read_pack(resource, root)
rows[0]['source_ids'].remove('otel-conventions')
validate_pack_rows(resource, rows)
```

Observed: accepted, although the `otel-conventions` contribution still includes `log-event-observation-time`. The current unmodified records and ledger agree; this mutation demonstrates a missing invariant, not current ledger drift.

### F4 — Actual output can exceed its trusted budget

Locations: `scripts/search-resource.py:247` returns early on domain mismatch; query checks occur only at line 258 for authored selection; line 303 calls `reader.output(result)` using its compact encoder; line 328 prints a separate indented serialization.

Two deterministic observations:

1. For the actual statistical lookup, compact JSON contained 12,879 bytes and the CLI's indented representation contained 16,165 bytes before the final newline. These are distinct sizes.
2. An in-memory authored fixture enlarged only the first row's `title`, recomputed its artifact/source hash and retained the existing row/contribution identities. `ArtifactReader.read` was temporarily replaced with a function supplying those registry/pack bytes and otherwise calling the real reader. The normal `lookup` with default limits accepted the result, while measuring the exact CLI serialization exceeded its default output cap:

```text
DEFAULT CAP                 2097152
compact accepted            2096152
CLI emitted bytes           2099439
status                      matched
```

No input file was modified. The injected pack remains below the normal 8 MiB per-file budget. The monkeypatch is solely an adverse review fixture, not product behavior or a real execution receipt.

Calling the actual lookup with the correct resource/consumer/locale/genre, a mismatched domain and a query of `ResearchLimits().output_bytes + 1` ASCII characters returned before either query or output checks:

```text
status                      no-applicable-record
resource_read               False
CLI serialized bytes        2097734
```

Resource no-read behavior is preserved in that case; its returned/emitted payload is still not bounded by the declared output contract.

### F5 — Standalone consumer validation omits catalog identity

Location: `scripts/search-resource.py:240` checks only membership in the selected registry row; it never reads `core/registry/catalog/skills.json`. `core.resources.registry` does enforce catalog identity, so the two validators disagree.

In-memory reproduction: append `nckh-not-in-catalog` to the statistical resource's registered `consumers`, supply the changed registry bytes through `ArtifactReader.read`, and invoke the standalone module's `lookup` for that consumer. Observed:

```text
resource_read               True
status                      no-applicable-record
```

The row-level typed filter prevents returning records because the actual row consumers exclude the new identity. The pack has already been opened, however. The equivalent core registry rejects an unknown consumer. Adding catalog validation requires adding its JSON dependency to the standalone reader/package closure, since current `SCRIPT_REQUIREMENTS` does not declare that file.

## Positive checks and practical limits

Actual current registry reads passed for all eight authored bindings:

| Resource | Consumer | Status | Records |
| --- | --- | --- | ---: |
| R-statistical-recipes | nckh-statistics | matched/read | 3 |
| R-statistical-recipes | nckh-method | matched/read | 3 |
| R-telemetry-dictionary | nckh-telemetry | matched/read | 3 |
| R-aiops-benchmark-cards | nckh-aiops | matched/read | 3 |
| R-aiops-benchmark-cards | nckh-dataset | matched/read | 3 |
| R-aiops-evaluation-recipes | nckh-aiops | matched/read | 5 |
| R-aiops-evaluation-recipes | nckh-statistics | matched/read | 5 |
| R-aiops-evaluation-recipes | nckh-method | matched/read | 5 |

Additional observed checks:

- Four actual pack byte hashes match their registry hashes; 14 total authored records.
- Every packaged contribution's fields excluding `record_ids` match the corresponding current contribution-ledger source. No current source/rights-ledger drift was observed.
- The two authored rights/attribution file hashes match their explicit source/provenance bindings. Rights remain `local-package-only`; metadata source licenses do not become release grants.
- `resource-registry.schema.json` embeds the exact current owned-provenance schema.
- Each pack's declared `closure` contained all seven entries in the current `SCRIPT_REQUIREMENTS['scripts/search-resource.py']`, with 12 total declared members. This establishes static declared helper closure, not extracted runtime qualification.
- Legacy copied/retrieved validation remains a distinct source branch; no raw snapshots, data, gold labels or measured-result artifacts were found among the four reviewed packs.
- Installer consumers route through `core.build.verify_bundle` (`core/install.py:69`, `:284`), so F1/F2 affect package consumption as well as direct verification. No install preview or activation occurred.

## Gate matrix and recommendation

| Gate | State | Evidence/limit |
| --- | --- | --- |
| Actual local authored records and eight valid bindings | Pass for observed scope | Current registry and actual byte-bound reads. |
| Current ledger/artifact/notice bindings | Pass for observed scope | Hash and exact contribution-field comparison. |
| Exact authored contribution membership | Fail | F3 adverse fixture accepted. |
| Standalone exact consumer identity | Fail | F5 unknown consumer caused a pack read. |
| Query and actual emitted output bounds | Fail | F4 default-cap and mismatch reproductions. |
| Static standalone helper closure | Pass for current declaration | All declared helpers present; catalog validation dependency not yet declared. |
| New authored bundle serialization/verification | Fail by located contract mismatch | F1; no new build claimed. |
| Historical format-2 compatibility | Fail | Real r38/r33 unchanged package verifier failures. |
| Candidate freeze/build/relocated four-host smoke | Pending P7 | Intentionally not run against stale r38 source pins. |
| Scientific usefulness/semantic support/human acceptance | Not evaluated | Local hashes, reader outputs and this model review do not establish them. |
| Provider/native/global install/publication | Outside review scope | No such operation performed. |

Recommendation: repair F1–F5, then perform one focused re-review of changed owners and affected assertions. Preserve this pre-fix evidence. Proceed to the P7 freeze and descendant packaging checks only after those deterministic/public-contract findings are resolved. This report does not accept scientific, native or public release gates.

## Reviewed fingerprints

Paths below are relative to `nckh-kit/` unless prefixed with `plans/`.

```text
core/owned_resources.py
  2cf160cfbdd34dec588e10764dfbdf938ee3c138887c5e84368af85f4a2275f9
core/resources.py
  2b1ce1b0941f904777230eae88293392615fcbffd4dff7417b6b59fc0efd98eb
core/build.py
  511516bbf78f6efcbd322c7554f72e5b78787daca4660b3217b728ab705539f8
core/research_io.py
  43ab446703f010509abdfc721d1e0d6057498de3361248002de3ce40614b91c7
core/contracts/owned-resource-provenance.schema.json
  c6c9b214388ca804ca8eb46f85d6bd0a636f7cbdc37bbf23a55e8cb45f6dbd60
core/contracts/resource-registry.schema.json
  fe6a99d3600c801c5a9c312f8d619bd181620a6ad1a6318b59d03196be1c862c
installer/schemas/bundle-v2.schema.json
  2d1d5f68f394d923ab6e72583bc4f59196367423d25592e9bd0dea3ab708f899
scripts/search-resource.py
  4a4d0c60613f1dcdc42e8215ea74d0dfd58d90cbcdc125123f9638385c4fe3a5
scripts/resource-smoke.py
  9e1747c242e5e20a174e4ea015ff898b66743cdc8b4d3f1602a015e628c2849a
core/registry/catalog/resources.json
  f84eed69a8ffcf1789c66e55b6a388081fdce9275e2b1034e82df77e92a5eac2
core/profiles/resources/statistical-recipes.jsonl
  f009560f2fb6eed8628a214a6a09ff9e9fc11b8be03f00d3a647a0c1f266f29b
core/profiles/resources/telemetry-dictionary.jsonl
  532dfc7427d0dc1349a3c3c2134bd9de4076a741e5950c854c0527331d9bdb34
core/profiles/resources/aiops-benchmark-cards.jsonl
  712960f5a1b1ed86457180a463a083e7c9eb0c89305b32b2c5e7923905310859
core/profiles/resources/aiops-evaluation-recipes.jsonl
  8858fb0b7a8500404469c4138c7de299605e69c567fd36b6c676cf6831f6dfb4
core/profiles/resources/research-packs-rights.md
  2dbc882e1497b4ad242b62f4e54e79795c38b85c5c9f9e5e185c2e566a7f41d9
core/profiles/resources/research-packs-attribution.md
  7f3d6036faa5ed1bc0fdcdd90b8b35460a12d3f432880d1fe2208825d9ae2375
plans/runs/nckh-upgrade-261006-0850-attempt-01/p5-contribution-ledger.json
  dbf58a34a90b04707313a9ec1dff90c7b4c7c098a659dfe4eb7c4f6025beb12e
```

Concerns/Blockers: F1–F5 require owning repairs and focused re-review before candidate packaging acceptance. No missing user decision is needed for the reported mechanical corrections. Unresolved questions: none.

---

## Focused re-review — corrected source

Current review status: DONE.

Re-review fingerprint time: 2026-10-06T03:00:50.145976+00:00 (Asia/Saigon: 10:00:50).

Scope revision 2: controller requested a read-only re-review of the five repaired findings, actual preserved r38/r33 package verification and directly affected regressions, with this same report as the only owned output. The original pre-fix findings and evidence above are retained. No source-lock freeze, new build, pinned-source/release test, installation or provider call occurred in this re-review; live source-lock revision remains 38.

### Resolution evidence

| Finding | Current result | Independently observed evidence |
| --- | --- | --- |
| F1 | Resolved for inspected pre-freeze contract; new bundle execution pending P7 | Current authored verifier branch accepts the valid actual statistical-pack record and rejects altered artifact hash, altered provenance and absent attribution. Expected rights now dispatch by source kind; registry/source and typed pack checks are explicit. Corrected projected pack root matches materializer mapping. |
| F2 | Resolved for preserved Codex r38/r33 artifacts | Current complete `verify_bundle` accepts both preserved packages. Adding only one of the three new helper pins in memory is rejected as `partial authored-resource hook helper inventory`. |
| F3 | Resolved | Previous reverse-source fixture now raises `authored row source IDs differ from contribution bindings`. A registered consumer with no applicable authored rows raises `every registered authored consumer requires applicable records`. |
| F4 | Resolved | Global query byte/token checks reject the previous mismatched-domain inputs; a one-byte result budget rejects the mismatch response. Exact output encoder bounds indentation and final newline. Current CLI emits bounded compact bytes. |
| F5 | Resolved | Previous unknown-consumer fixture raises `resource consumer is absent from current exact catalog`; the only observed read before rejection is `core/registry/catalog/skills.json`. Catalog JSON and schema are now present in the declared helper closure. |

F1 source-branch check used the actual `verify_bundle` AST branch, compiled and executed in memory with the actual authored provenance/pin and projected notice records. It did not substitute product behavior, produce a bundle or claim a post-freeze result. Observed output:

```text
F1 ACTUAL BRANCH VALID ACCEPTED
F1 ACTUAL BRANCH ALTERED ARTIFACT REJECTED
  authored reference provenance/bytes differ from their original pin
F1 ACTUAL BRANCH ALTERED PROVENANCE REJECTED
  authored reference provenance/bytes differ from their original pin
F1 ACTUAL BRANCH MISSING ATTRIBUTION REJECTED
  authored reference lacks its original packaged notice for this consumer
```

The first repaired draft called `read_pack` from `skills/<consumer>`, which omitted the shared projection segment. This was located during re-review and corrected by the controller before the final fingerprint. Current `core/build.py:625` uses `skills/<consumer>/references/_shared`. For each of all four current authored packs, reproducing the actual `_materialize_host` mapping gives exactly:

```text
skills/<consumer>/references/_shared/<row.path>
```

The verifier's corrected root plus `row.path` equals that mapping. Static closure now contains 14 members per reviewed pack, including all nine declared standalone script requirements, the catalog JSON and its schema. This resolves the located path error; execution from a newly extracted authored package remains a P7 gate.

F2 actual complete read-only results:

```text
nckh-upgrade-native-261006-0850-attempt-01/bundle/codex
  embedded revision 38: ACCEPTED
nckh-native-261004-2112-r33-attempt-01/build/on-plugin/codex
  embedded revision 33: ACCEPTED
partial authored helper inventory for either preserved manifest: REJECTED
```

F4 repeated the near-cap fixture through the current actual `main()` function with captured stdout/stderr and only in-memory input substitution. Observed:

```text
exit status                 0
actual emitted bytes        2096153
default cap                 2097152
stderr                      empty
```

The emitted output includes its final newline and remains within the cap. Separate boundary checks of `ArtifactReader.output(..., newline=True)` rejected a compact representation at the cap whose final newline would exceed it; the indented equivalent was also rejected. Oversized byte/token queries on domain mismatch and a one-byte mismatch output budget were independently rejected.

All eight unmodified local authored lookup bindings again returned `matched` and their expected 3/3/3/5 record counts. The controller's current-source CLI receipt was read: eight bindings, all exit 0, every recorded reader hash equal to the current `scripts/search-resource.py` hash. Its OFF observation records an absent root, `resource-disabled`, empty records and `resource_read=false`. The receipt explicitly identifies local source reads and defers relocated bundle checks; that distinction is retained here.

The controller's text receipts show 89 passing tests in attempt 03 and 19 passing pack tests in attempt 04. These test logs were inspected rather than re-executed by the reviewer, and they contain no self-contained source-hash snapshot. They are recorded as controller test evidence, separate from this review's current hash-bound source checks and direct reproductions.

### Current gate state

| Gate | Current state |
| --- | --- |
| Current local authored bindings and ledger/notice checks | Pass for observed scope; resource/registry bytes unchanged from initial review. |
| Exact reverse contribution and consumer coverage invariants | Pass for reproduced adverse fixtures. |
| Standalone unknown-consumer no-read boundary | Pass; rejected after catalog read, before registry/pack reads. |
| Query and exact emitted output bounds | Pass for reproduced boundaries and actual CLI serialization fixture. |
| Authored file/source-kind dispatch and projected root | Pass for isolated current branches and actual mapping comparison. |
| Preserved r38/r33 Codex package verification | Pass, directly observed with current verifier. |
| New authored bundle build, four-host extraction and isolated reader smoke | Pending P7 after the sole candidate freeze. |
| Scientific, human, native and publication acceptance | Not evaluated; no promotion from this review. |

No concrete new low-impact gap remains from this bounded re-review. The remaining P7 gates require their planned actual candidate execution and are not waived by the resolved findings.

### Current fingerprints

```text
core/build.py
  1c9f03583397190938cd55fd3e2646dfb1b35c363edf5240bc1456b393100645
core/owned_resources.py
  5bb3e7051cd9298c68a34675c0963aac3f89e46c3b4b361a6cb951e0b6d2bc40
core/research_io.py
  824742c52ea0a92432abe6c6669e2fca27adb350da19697f6d5141df209ef96b
scripts/search-resource.py
  60c9770390c4779ec94dcec70afa1869baebd69485cb27a056239ae79741a6fd
core/resources.py
  2b1ce1b0941f904777230eae88293392615fcbffd4dff7417b6b59fc0efd98eb
core/contracts/owned-resource-provenance.schema.json
  c6c9b214388ca804ca8eb46f85d6bd0a636f7cbdc37bbf23a55e8cb45f6dbd60
core/contracts/resource-registry.schema.json
  fe6a99d3600c801c5a9c312f8d619bd181620a6ad1a6318b59d03196be1c862c
installer/schemas/bundle-v2.schema.json
  2d1d5f68f394d923ab6e72583bc4f59196367423d25592e9bd0dea3ab708f899
core/registry/catalog/resources.json
  f84eed69a8ffcf1789c66e55b6a388081fdce9275e2b1034e82df77e92a5eac2
tests/resource/test_research_packs.py
  09f93e9eab08972173f6eb54fb15d2a87d215e84128991bd8a37825eedccbc32
core/registry/source-lock/source-lock.json (revision 38; intentionally stale)
  5616070c7027b0e9f25ae897dc60e51c0830a6c0ae62779708936e62c2b9ce47
plans/runs/nckh-upgrade-261006-0850-attempt-01/p5-contract-tests-attempt-03.txt
  514f06384b945c316151bd86dcb13269f5bef3baa726682d83d39ecb1f5133ed
plans/runs/nckh-upgrade-261006-0850-attempt-01/p5-contract-tests-attempt-04.txt
  7f519015ecdfb54a048851fc371c65715d5d24b3bd55304353e364874132fcd7
plans/runs/nckh-upgrade-261006-0850-attempt-01/p5-local-reader-receipt.json
  53b919b4ce3eefd0cb79f8933d81b8650ce2bde9c870ae39412d154c59466195
```

Summary: all five original findings are resolved for the bounded pre-freeze review, including the corrected projection path and real preserved Codex bundle compatibility. Concerns/Blockers: none within this review scope; P7 candidate build/extraction/runtime gates remain pending as planned. Unresolved questions: none.
