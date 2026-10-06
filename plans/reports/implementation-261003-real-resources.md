# Real source integration

Date: 2026-10-03. Project: `C:/Users/USER/Downloads/test-skill`.

## Completed source work

The resource registry now has nine resources: four preserved legacy resources and five compact real-source packs. Twelve consumer skills have task-specific lookup instructions and a linked reference in their skill entrypoint. All 37 identities remain unchanged.

| Pack | Actual packaged content | Scope |
|---|---|---|
| Wikisource | Three actual child passages with parent/revision metadata | Page CC BY-SA; underlying-work jurisdiction separate |
| PMC | Two article excerpts from pinned JATS snapshots | Article-specific CC BY 4.0 |
| World Bank | One series containing 26 non-null observations, 2000–2025 | Source API unit remains blank |
| UCI | Ten actual `bank.csv` rows and column metadata | CC BY 4.0; duration leakage warning |
| Django | One JSONL record with two BSD fixture contents and task locators | Issue/problem/benchmark patch/dataset-row content excluded |

Raw acquisition originals remain in [source staging](../evaluation/personal-use/source-acquisition/derived/manifest.json), outside the package. The package rights summaries are authored metadata; the Django BSD license is copied verbatim. Artifact and upstream hashes have separate meanings. Source/rights/reader details are machine-owned by [the registry](../../nckh-kit/core/registry/catalog/resources.json).

The reader returns actual matching records with provenance, excludes catalog-only rows, preserves no-match/domain/locale/genre/off behavior, and does not execute code examples. JSON duplicates and nonfinite numbers fail. Unrecorded dependencies, private reference-only fields, legacy license/commit drift, reciprocal metadata scope and packaged lineage mismatch fail.

## Actual verification and attempts

- Before registration/freeze, the full resource suite failed with seven errors and one failure because raw copies were unregistered and snapshot registry entries were absent. This was an incomplete source checkpoint, not a passing candidate.
- After registration, three focused checks failed because the authored rights files had changed while registry hashes were still old. The hashes were reconciled against the reviewed actual files.
- Django license lineage was represented twice with incompatible transformations. The license retains its explicit dependency and verbatim provenance; the raw license hash remains in lineage without a redundant packaged path.
- The final focused run `python -B -m unittest tests.resource.test_real_sources tests.resource.test_consumers -v` passed 13 tests. The registry has nine entries; source inventory has 240 members; provenance has 13 third-party file pins at this checkpoint.
- Independent [provenance review](review-261003-resource-provenance.md) verifies the final two extracted-lock guards with a focused regression and ten separate probes.

These checks establish source and reader behavior only. Full frozen-source tests, on/off builds, extracted package checks, project update and candidate native cases are phase 4. No model output, owner score, quality uplift or scientific certification is inferred here.
