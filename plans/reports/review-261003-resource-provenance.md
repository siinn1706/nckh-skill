# Resource provenance and standalone reader review

Status: DONE

## Final recheck of the two findings

Both findings below are resolved in the rechecked snapshot. This follow-up was limited to the requested reciprocal metadata scope and packaged lineage pin/hash/rights/bytes invariants; it did not broaden the review to newly imported source files.

| File, relative to `nckh-kit/` | SHA-256 at final recheck |
|---|---|
| `core/resources.py` | `b0555d150a79f654f3112d92589a33d5632fa79dca8ebf2750b06de591962bb7` |
| `core/contracts/resource-provenance.schema.json` | `ea7bcd2bcb20ae9cf693e236e5ae1966ec97453a2324e60d8f59948ecb2d24f2` |
| `core/contracts/resource-registry.schema.json` | `fa85ed77c5a367f4e7100ad02fcbe1b955b77c7d4891d0e8f39713c54811154f` |
| `scripts/search-resource.py` | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` |
| `tests/resource/test_real_sources.py` | `ba1ad9fcc1632f56310de47952bbdaf81322bd2783316f2359519312ebf10af8` |
| `core/profiles/resources/k-dense-license.md` (existing actual-byte fixture) | `09b02a3c9df3053c55531d503357a9c7cde275970e6c3ceaa1ddf5f0e90b40c1` |

**Metadata scope repair:** `verify_provenance` now checks both directions between reference-only scope and metadata-only mode, including redistribution pairing (`core/resources.py:177`–`186`). A valid metadata-only reference passes; metadata-only with redistributable scope and normalized source content with reference-only scope both reject.

**Packaged lineage repair:** The verifier now checks path containment, a matching file pin/hash, copied upstream rights and a matching upstream hash for packaged source-response/archive members, and actual file bytes when `check_files=True` (`core/resources.py:202`–`216`). Pathless external staging lineage remains accepted.

**Focused regression:** `python -B -m unittest tests.resource.test_real_sources.RealSourceTests.test_extracted_metadata_scope_and_packaged_lineage_are_bound -v` passed: one test, 0.045 seconds. The test exercises scope rejection, mismatched raw pins, owned relabeling, a valid matching pin and byte drift in an isolated temporary fixture. It does not build, freeze, install or invoke a provider.

**Independent captured-source checks:** Ten cases matched their expected outcomes. Source/contract/reader/test hashes remained unchanged during these probes.

| Case | Observed outcome |
|---|---|
| Valid normalized record with pathless external lineage | Accepted |
| Metadata-only mode with redistributable scope | Rejected |
| Valid metadata-only record with reference-only scope/redistribution | Accepted |
| Reference-only scope with normalized source-content mode | Rejected |
| Packaged lineage with no file pin | Rejected |
| Packaged lineage hash differs from file pin | Rejected |
| Packaged upstream lineage relabeled owned | Rejected |
| Packaged lineage upstream hash differs from copied provenance | Rejected |
| Valid packaged lineage with existing file bytes, `check_files=True` | Accepted |
| Matching synthetic pin/lineage hashes differ from actual existing bytes | Rejected: `packaged lineage bytes changed` |

Concerns/Blockers: None remain for these two findings in the rechecked snapshot. Subsequent source revisions, imported corpus content and freeze/build acceptance remain outside this follow-up's scope.

## Original review scope and snapshot

Read-only review of source rights, raw/artifact bindings, resource dependency ownership and the standalone reader. Source was being edited concurrently; findings below apply only to the recorded SHA-256 snapshots. The reviewer changed only this report, ran six existing reader tests and pure in-memory fault probes, and did not build, freeze, install or invoke a native model/provider. Snapshots and deterministic fixtures do not establish human gold, semantic support, model benefit or release clearance.

| Read file, relative to `nckh-kit/` unless stated | SHA-256 at original probe capture |
|---|---|
| `core/resources.py` | `80694fb3012e9662cbfa618a397d45fa6adc958f636b6f63d2e25893b0531be5` |
| `core/contracts/resource-provenance.schema.json` | `ea7bcd2bcb20ae9cf693e236e5ae1966ec97453a2324e60d8f59948ecb2d24f2` |
| `core/contracts/resource-registry.schema.json` | `fa85ed77c5a367f4e7100ad02fcbe1b955b77c7d4891d0e8f39713c54811154f` |
| `scripts/search-resource.py` | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` |
| `core/build.py` (callers and bundle binding) | `f9ffefa298d731a8eb8393e25215922879595d3e2852ccc4876f5efcea70395b` |
| `core/schema.py` (validator) | `6d0d60c0ec5d9a1741bf498ee2bf06a63ac688045d35317ba77e03705874edac` |
| `core/registry/catalog/resources.json` (four legacy rows at capture) | `d908a7a0eea4bcbe7a565dc2417b3f6861e971b35b231d6957bca2319279d27f` |
| `tests/resource/test_consumers.py` | `1adaea4b9651bdf9c2e6285c4ec9b51b918c29f4617402aab3c302180fe795e1` |
| Workspace `plans/evaluation/personal-use/source-acquisition/derived/manifest.json` | `48d6b7ca16d777a7248197c5271f697fdcd05cc99e0f15aec6600d273ade5998` |

New registry entries/resource files introduced after this capture are outside the reviewed snapshot.

## Original findings, now resolved

The failures below preserve their original evidence and repair direction. Their open status is superseded by the final recheck above.

### [P2] Metadata-only pins can claim redistribution

**Owner/location:** `nckh-kit/core/resources.py:177`–`185`, `verify_provenance`.

**Mechanism:** Snapshot pin validation enforces `rights_scope=reference-only -> copied_vs_reauthored=metadata-only-reference`, but does not enforce the inverse. An otherwise valid `retrieved-snapshot` pin with `copied_vs_reauthored=metadata-only-reference`, `rights_scope=redistributable`, `redistribution=permitted-with-notices`, valid retrieval metadata and normalized raw/artifact hashes is accepted. The source registry validator rejects the same combination. The bundle verifier calls `verify_lock_structure -> verify_provenance`, so the extracted lock gate does not preserve the source validator's rights invariant.

**Observed probe:** `pin-metadata-only-claims-redistribution: ACCEPTED`; no product artifact was generated.

**Minimal repair:** Require metadata-only pins to keep `rights_scope=reference-only` and `redistribution=reference-only`, alongside the existing reciprocal rule.

**Regression test:** A complete normalized metadata-only pin with redistributable scope must raise `ContractError`; the same pin with reference-only scope/redistribution must pass.

### [P2] Packaged lineage is not bound to its file pin

**Owner/location:** `nckh-kit/core/resources.py:189`–`198`, `verify_provenance`.

**Mechanism:** The verifier checks that every declared upstream hash appears in lineage, but ignores a lineage member's packaged `path`. An otherwise valid normalized pin with lineage `path=core/profiles/resources/raw.json`, lineage `sha256=b*64` and a source-lock file pin at that path with `sha256=c*64` and `rights=owned-local-package` is accepted. The license/notice paths already receive pin/hash checks; packaged raw lineage paths do not. Source registry validation checks actual lineage bytes before freeze, but extracted-lock validation does not retain that binding.

**Observed probe:** `pin-packaged-lineage-hash-mismatch: ACCEPTED`; the synthetic source-lock map existed only in memory.

**Minimal repair:** For every lineage member with a packaged path, validate containment, require the matching file pin/hash and an appropriate explicit rights record; verify actual bytes when `check_files=True`. Keep pathless external staging lineage usable.

**Regression tests:** Reject missing lineage file pins, mismatched lineage/file hashes and copied raw paths relabeled owned; preserve valid pathless external references and valid packaged lineage.

## Verified repairs and retained behavior

The following initial findings were communicated during implementation and are resolved in the captured snapshot or verified by the cited source changes:

- Legacy source validation and pin validation preserve MIT/Apache-2.0, a 40-character lowercase hexadecimal commit, verbatim mode and notices.
- Declared dependencies without a main resource, reader, registry, license/notice or lineage role are rejected regardless of extension/path prefix.
- Legacy `source.license_kind=owned-rights-record` is rejected, preserving copied provenance for original upstream LICENSE bytes. Authored snapshot rights metadata can retain its declared owned role.
- Strict registry/reader JSON parsing rejects duplicate keys, `NaN` and overflowing `1e999` numeric tokens. The latter was independently reproduced after repair.
- The unused raw API/XML/ZIP/SWE reader routes, including issue-body emission under `issue_text_reference`, were removed. The current metadata-only engineering JSONL gate rejects an actual GitHub `body` field; the pure probe now raises `ValueError: metadata-only reference contains unreviewed/private fields`.
- The snapshot bundle binding compares file ownership to `copied-upstream` and provenance source kind to the declared `retrieved-snapshot`, fixing the earlier direct source-kind/ownership mismatch. This conclusion is source inspection only; bundle materialization was outside reviewer scope.
- Consumer/locale/genre mismatches reject. A wrong domain returns no applicable records without reading source bytes. `resource_access=off` returns before file access, including when the root does not exist.
- Composed Vietnamese Unicode and decomposed combining characters are preserved by JSONL decoding/record selection; no spelling or Unicode normalization was introduced.
- The staged SWE rights boundary remains explicit in the acquisition manifest at lines 232–244: upstream code rights do not clear issue text, benchmark patches or dataset rows. The manifest's source access/status is not public-release acceptance.

## Verification

`python -B -m unittest tests.resource.test_consumers -v`: six tests passed; latest observed run completed in 0.064 seconds. No bytecode writes, build, freeze or native/provider execution were used by this review.

The final in-memory probe compiled captured source bytes and validated against captured contract JSON, so later mutations cannot change those recorded outcomes. It confirmed rejection of legacy owned LICENSE and metadata-only issue body, and acceptance of the two remaining malformed pin cases above.

Original disposition: These two extracted-lock invariants were open at the original snapshot. Both are resolved by the final recheck recorded above. Future registry/resource changes require their own bounded verification; this report does not cover future source bytes.
