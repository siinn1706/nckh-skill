# Documentation report — real personal-use resources

**Date:** 2026-10-03, Asia/Saigon  
**Scope:** documentation-only update for the five bounded personal-use resource
packs. Resource/core implementation, source lock, build, installer and runtime
files were outside this ownership.

## Observed paths

- `nckh-kit/docs/contracts.md`
- `nckh-kit/docs/qualification.md`
- `nckh-kit/docs/personal-use.md`
- `nckh-kit/core/registry/catalog/resources.json`
- `nckh-kit/core/profiles/acceptance/personal-use.json`
- `nckh-kit/core/profiles/resources/vi-wikisource.jsonl`
- `nckh-kit/core/profiles/resources/pmc-scientific.jsonl`
- `nckh-kit/core/profiles/resources/worldbank-series.jsonl`
- `nckh-kit/core/profiles/resources/swe-bench-reference.jsonl`
- `nckh-kit/core/profiles/resources/uci-bank-marketing.jsonl`
- `nckh-kit/core/profiles/resources/wikisource-rights.md`
- `nckh-kit/core/profiles/resources/pmc-rights.md`
- `nckh-kit/core/profiles/resources/worldbank-rights.md`
- `nckh-kit/core/profiles/resources/swe-bench-rights.md`
- `nckh-kit/core/profiles/resources/swe-bench-notice.md`
- `nckh-kit/core/profiles/resources/uci-rights.md`

The registry contained these five resource IDs at inspection:
`R-vi-wikisource-passages`, `R-pmc-scientific`,
`R-worldbank-vietnam-population`, `R-django-sqlmigrate-fixtures` and
`R-uci-bank-marketing`.

## Hashes

SHA-256 values observed after the documentation edit:

```text
nckh-kit/docs/contracts.md                                      67854498a02689fe5b07543497a4c8d3a7d317b3820405625afae385e54efa9c
nckh-kit/docs/qualification.md                                 d303632881f94a871aba7e1644d5787c14d15966d966b4c8260ba6ec906f5e9c
nckh-kit/docs/personal-use.md                                   f294b62012772c4ee0ede22886177350fb23fe8fff94be17c412b587ce179455
nckh-kit/core/registry/catalog/resources.json                   08280a57da31f62d88666b4dcca5f6b31589d73f0544c5751ba4632f1cd1ad9b
nckh-kit/core/profiles/acceptance/personal-use.json             627ebaf58c97212e790ed794739767cff710a552a40e3231c24d86bf0d979341
nckh-kit/core/profiles/resources/vi-wikisource.jsonl            36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f
nckh-kit/core/profiles/resources/pmc-scientific.jsonl            b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45
nckh-kit/core/profiles/resources/worldbank-series.jsonl          a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2
nckh-kit/core/profiles/resources/swe-bench-reference.jsonl      e81048922d196fd302555f192d289d51d82449b0ae724fc05cb2e2b4bfeb90cf
nckh-kit/core/profiles/resources/uci-bank-marketing.jsonl       647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123
```

## Tests

- Relative Markdown links in the three edited docs: 24 checked, 0 missing.
- Expected five new registry IDs: 5 present, 0 missing.
- The edited docs contain the five actual registry IDs and the current registry
  consumer routes; the former four-resource-only wording was removed.

## Failures and incomplete evidence

- No resource, build, installer, provider, native-host, owner-feedback or
  scientific/human acceptance test was run by this documentation-only change.
- The report does not treat registry validation, hashes, parsing, local tests or
  documentation links as proof of native acceptance, owner taste, human gold,
  scientific validity, causal uplift or public redistribution clearance.
- The frozen source lock was not edited.

## Limitations

- The five packs remain bounded personal-use inputs: three historical Wikisource
  child passage records with parent/root metadata, two article projections, one
  dated World Bank series, two pinned Django code fixtures with a task locator,
  and ten UCI rows.
- Rights are scope-specific. Wikisource attribution and underlying-work status,
  article-level PMC licenses, World Bank terms and third-party indicators,
  Django BSD coverage for the two fixtures, and UCI attribution remain separate
  records.
- Owner feedback remains pending until the user records feedback against the
  actual artifact revision, artifact hash and input hashes.
