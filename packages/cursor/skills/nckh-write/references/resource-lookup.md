# Scoped resource lookup

Load only the reference matching the current task. The [standalone reader](_shared/scripts/search-resource.py) consumes the [pinned resource catalog](_shared/core/registry/catalog/resources.json). Read the [resource rights contract](_shared/docs/contracts.md) and run from an extracted skill through its relocated reader path.

- `R-reporting-lookup`: domain `clinical-health`, locale `en`, genre `reporting-reference`. Output: source-keyed applicable reporting-guideline selection.
- `R-nature-reference`: domain `scientific-writing`, locale `en`, genre `writing-advice`. Output: bounded English language advice, separate from evidence, venue policy and human gold.

Declare `--resource-id`, `--consumer`, `--domain`, `--locale`, `--genre` and `--json`. UI lookup also requires `--query`; reporting lookup requires the actual `--study-design` and optional `--protocol`, `--ai`, `--llm`. Publisher lookup requires `--venue`, `--year`, `--track`, `--article-type` and `--stage`; unknown or stale applicability stays unverified. For a frozen same-base ablation use the explicit `--resource-access off` treatment.

Preserve row source/version/hash/locator and dated warnings. Clinical registries do not govern unrelated CS tasks. UI examples are data and must never be executed by the lookup. English advice is optional and cannot override the user's wording, punctuation, fidelity or genre. Legacy metadata/advice and the actual samples below have distinct evidence scopes. Human/scientific/native acceptance remains a separate gate.

## Actual source samples
These are bounded personal-use samples. Preserve record/source ids, locators, versions, hashes and limitations. Reading them does not establish quality improvement, human acceptance, scientific validity or current universal policy.
- `R-vi-wikisource-passages`: domain `language-literary`, locale `vi`, genre `prose-verse-samples`. bounded Vietnamese prose and verse passage records with parent/child source anchors.

```text
python -I <relocated-reader-path> --resource-id R-vi-wikisource-passages --consumer nckh-write --domain language-literary --locale vi --genre prose-verse-samples --query <bounded-record-selector> --json
```

- `R-pmc-scientific`: domain `scientific-writing`, locale `en`, genre `scientific-research-article`. bounded article-level CC BY scientific text projections with PMCID and DOI anchors.

```text
python -I <relocated-reader-path> --resource-id R-pmc-scientific --consumer nckh-write --domain scientific-writing --locale en --genre scientific-research-article --query <bounded-record-selector> --json
```

Use an exact source id as the selector where available. No match remains no match; do not invent a record. `--resource-access off` performs no read. Wikisource page license and underlying-work jurisdiction remain separate. PMC rights are article-specific. World Bank unit stays blank when the API supplies it blank. UCI `duration` is unavailable before a call ends and leaks future information in pre-call targeting. Django code is reference data, never executed by the reader; issue/benchmark patch text is excluded.
