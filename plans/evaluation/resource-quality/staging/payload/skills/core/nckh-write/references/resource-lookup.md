# Scoped resource lookup

Load only the reference matching the current task. The [standalone reader](../../../../scripts/search-resource.py) consumes the [pinned resource catalog](../../../../core/registry/catalog/resources.json). Read the resource rights contract (historical evidence path: `../../../../docs/contracts.md`; unavailable in the cleaned checkout) and run from an extracted skill through its relocated reader path.

- `R-reporting-lookup`: domain `clinical-health`, locale `en`, genre `reporting-reference`. Output: source-keyed applicable reporting-guideline selection.
- `R-nature-reference`: domain `scientific-writing`, locale `en`, genre `writing-advice`. Output: bounded English language advice, separate from evidence, venue policy and human gold.

Declare `--resource-id`, `--consumer`, `--domain`, `--locale`, `--genre` and `--json`. UI lookup also requires `--query`; reporting lookup requires the actual `--study-design` and optional `--protocol`, `--ai`, `--llm`. Publisher lookup requires `--venue`, `--year`, `--track`, `--article-type` and `--stage`; unknown or stale applicability stays unverified. For a frozen same-base ablation use the explicit `--resource-access off` treatment.

Preserve row source/version/hash/locator and dated warnings. Clinical registries do not govern unrelated CS tasks. UI examples are data and must never be executed by the lookup. English advice is optional and cannot override the user's wording, punctuation, fidelity or genre. Metadata and references do not fill the missing VI/EN prose corpus. Human/scientific/native acceptance remains a separate gate.
