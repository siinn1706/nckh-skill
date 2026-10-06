# Phase 3 implementation: personal-use acceptance

**Date:** 2026-10-03 (Asia/Saigon)  
**Scope:** implement the approved shared personal-use acceptance profile and
owner-feedback binding for the 37 experimental NCKH skills.  
**Lane:** `personal-use`; catalog status remains `experimental`.

## Delivered

- Added one self-contained JSON profile with the five common gates, 37 exact
  skill rows, 35 source definitions, 51 authoritative URLs, applicability and
  limitations.
- Kept the profile progressive: common checks are declared once, while each
  skill row adds its positive/negative/output/authority criteria and source IDs.
- Added a repository reader that validates the profile against the current
  catalog before lookup. It fails closed for unknown identities, missing source
  definitions, changed catalog metadata, changed eval IDs or missing
  applicability.
- Added owner feedback binding to `revision`, `artifact_hash` and
  `input_hashes`. Missing feedback returns `pending-personal-review`; a
  mismatch raises an error. The reader never aggregates a `pass` or grants
  stable/scientific acceptance.
- Kept external reviewer, protected holdout and human-gold evidence out of the
  personal-use prerequisite. Existing human, rights, provider, paid and
  irreversible boundaries remain in force.
- Linked the profile from the acceptance policy and preserved the existing
  policy links in all 37 skill instructions. The closure check confirms that
  every skill resolves the profile file.
- Preserved `evals/protocols/qualification.json` and its historical stable/
  scientific gates. The test reads the protocol and verifies its round limit,
  split axes and forbidden human-label/holdout rule.

## Exact modified paths

Implementation paths:

- `nckh-kit/core/profiles/acceptance/personal-use.json`
- `nckh-kit/core/acceptance.py`
- `nckh-kit/core/policies/acceptance-policy.md`
- `nckh-kit/core/workflows/execution.md`
- `nckh-kit/skills/core/nckh-cook/SKILL.md`
- `nckh-kit/tests/acceptance/__init__.py`
- `nckh-kit/tests/acceptance/test_profile.py`

Rollback snapshots:

- `plans/evaluation/personal-use/acceptance/before/acceptance-policy.md`
- `plans/evaluation/personal-use/acceptance/before/execution.md`
- `plans/evaluation/personal-use/acceptance/before/nckh-cook.SKILL.md`
- `plans/evaluation/personal-use/acceptance/before/snapshot.json`

The source lock, installer, resource registry/reader, historical receipts and
qualification protocol were not modified.

## Checks run

Command:

```text
cd nckh-kit
python -m unittest tests.acceptance.test_profile -v
```

Result: **6 tests passed**.

The tests verify:

1. exact 37 identity mapping and catalog eval IDs;
2. 35 defined source IDs, URL presence and nonempty applicability/limitations;
3. scoped lookup returns common gates, skill criteria and source records;
4. an unknown source reference or missing applicability fails closed;
5. the profile is reachable through the acceptance policy from all 37 skill
   closures;
6. absent owner feedback is `pending-personal-review`, current feedback is
   recorded, and revision/artifact/input mismatches are rejected;
7. the historical qualification split, development limit and forbidden
   human-label rule remain unchanged.

An additional regression run passed the six acceptance tests plus the existing
state and evidence guard suites: **23 tests passed** in the final run.

## Limitations and pending gates

- The current source lock predates these Phase 3 files. It was intentionally not
  edited under the ownership boundary. Controller-owned source freeze/build
  receipts must pin the new profile, reader, policy, workflow, cook skill and
  tests before the candidate can claim reproducible build closure.
- No provider/native model run, external publication, paid evaluation, human
  reviewer, protected holdout or scientific/domain review was performed.
- The profile maps official source URLs and applicability; it does not prove
  source freshness, legal applicability, venue acceptance, native editability,
  model quality or scientific validity at runtime.
- Owner personal-use scoring remains an owner action after an actual artifact
  is produced. A structural profile read or a successful local test cannot
  create that owner verdict.

**Status:** DONE_WITH_CONCERNS  
**Summary:** Shared personal-use criteria now cover all 37 catalog identities,
resolve 35 official source records, remain reachable through every skill
closure, and bind owner feedback to exact revision/artifact/input evidence.  
**Concerns:** Source-lock/build freeze, native/provider observations and owner
artifact scoring remain pending by design.
