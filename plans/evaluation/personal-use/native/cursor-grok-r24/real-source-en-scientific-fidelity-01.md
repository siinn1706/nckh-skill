# Claim-fidelity brief: PMC13623154

Case `real-source-en-scientific-fidelity-01`. This is not a new study.

## Source receipt and license

- `source_id`: `pmc-PMC13623154`
- PMCID: `PMC13623154`
- DOI: `10.1371/journal.pone.0359403`
- Locator: `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13623154/`
- Reader query: `pmc-PMC13623154`
- Reader: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-write\references\_shared\scripts\search-resource.py`
- Pack: `R-pmc-scientific`, domain `scientific-writing`, locale `en`, genre `scientific-research-article`, consumer `nckh-write`
- Receipt: `plans/evaluation/personal-use/native/cursor-grok-r24/reader-receipts/nckh-write__R-pmc-scientific__pmc-PMC13623154.json`
- Status: `matched`, one record
- Pack `resource_sha256`: `b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45`
- `record_sha256`: `546888bb164ac36cd719f432ccacb7ed3dba076704b8191c47c88f5efe2f0223`
- `reader_sha256`: `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`
- Raw XML: `raw/pmc-PMC13623154.xml`, SHA-256 `135e35ecbac31f8a2429ce25426d2564c3a87aa66f4f2ebaf3fd1bd15114c69c`, 128666 bytes
- Projection rule in the record: title, abstract and body paragraphs; maximum 9000 characters
- Excerpt actually read: 9000 characters, ending mid-sentence at `Scopus profiles, and`
- License field in the reader record: `CC BY 4.0`, URL `https://creativecommons.org/licenses/by/4.0/`, `verified_in` `raw/pmc-PMC13623154.xml`
- License sentence read from that XML: “This is an open access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.”
- `rights_rationale`: the article-level XML contains the CC BY 4.0 statement; PMC-wide Open Access status was not used as a universal license claim

The ledger below uses only the fully read 9000-character projection. Later XML sections were not used as claims.

## Five-row claim ledger

| # | Source anchor | Faithful paraphrase | Numbers and units | Certainty or association wording | Forbidden overclaim |
|---|---|---|---|---|---|
| 1 | Title: “Gender disparities in leadership of methodological research in health science” | The article frames its topic as gender representation in first and last authorship of methodological research in health science. | None in the title. | The title names the topic. It does not state a cause. | The title does not prove a universal gender effect or a mechanism. |
| 2 | “Of the 1,375 included studies, the genders of 1,332 first authors and 1,334 last authors were determined.” | Gender was determined for a subset of first authors and a subset of last authors among the included studies. | 1,375 included studies; 1,332 first authors; 1,334 last authors. | “Were determined” reports classification coverage, not a population rate for all studies. | Do not treat 1,375 as every methodological study, or 1,332/1,334 as complete gender data for every author. |
| 3 | “Among first authors, 675 (50.7%) were women, and 657 (49.3%) were men, indicating no gender difference.” | In the determined first-author set, the abstract reports those two counts and describes that contrast as no gender difference. | 675 (50.7%) women; 657 (49.3%) men. Denominator is the 1,332 determined first authors named in the previous sentence. | The phrase “indicating no gender difference” is the abstract’s wording for this first-author contrast. | Do not extend that phrase to last authors, to unread subgroups, or to a causal claim of equality. |
| 4 | “Among last authors, 486 (36.4%) were women, and 848 (63.6%) were men, with a statistically significant difference (χ² = 98.23, p < 0.001).” | Among determined last authors, the abstract reports a women/men split and a chi-square test. | 486 (36.4%) women; 848 (63.6%) men; χ² = 98.23; p < 0.001. | “Statistically significant difference” is the abstract’s test wording. | Do not read the chi-square or p-value as proof of cause, bias mechanism, or a difference outside this last-author contrast. |
| 5 | “In adjusted models, women’s last authorship was negatively associated with number of authors (adjusted odds ratio [aOR]=0.93, 95% CI 0.90–0.97).” | The adjusted model reports a negative association between women’s last authorship and the number of authors. | aOR=0.93; 95% CI 0.90–0.97. | The source says “negatively associated” and reports an adjusted odds ratio with a confidence interval. | Do not change association into “team size causes fewer women last authors,” and do not drop the interval. |

## Faithful conclusion

This brief restates claims from the bounded excerpt of PMC13623154 (DOI 10.1371/journal.pone.0359403). The abstract reports 1,375 included studies, with gender determined for 1,332 first authors and 1,334 last authors. Among first authors, 675 (50.7%) were women and 657 (49.3%) were men; the abstract describes this contrast as indicating no gender difference. Among last authors, 486 (36.4%) were women and 848 (63.6%) were men, with χ² = 98.23 and p < 0.001. In adjusted models, women’s last authorship was negatively associated with number of authors (aOR=0.93, 95% CI 0.90–0.97). Publication year was associated with women first authorship (aOR=1.03, 95% CI 1.01–1.05) and last authorship (aOR=1.05, 95% CI 1.02–1.07). These statements are observational associations from one health-science article. They do not establish causes, mechanisms, or effects outside the included studies. The derived text stops at 9,000 characters, so this conclusion does not use unread XML results.

## Limits and uncertainty

The same abstract, still inside the 9000-character excerpt, also says studies with women last authors had fewer listed co-authors than those with men (t = −3.63, p < 0.001; risk difference = −27.14%, 95% CI −32.50% to −21.77%). That sentence stays an association-style results statement. It is not a sixth rewritten study and not a cause.

The projection stops at 9000 characters while the methods sentence is unfinished. The raw XML remains the full-text snapshot at the hash above. Results that appear only after that cut are outside this ledger. Genderize.io, the ≥ 60% probability rule, and the search description are in the excerpt as methods text; this brief does not add an unseen validation of that classifier.

CC BY 4.0 here is the article statement read above. It is not a claim about other PMC articles, peer-review acceptance, or scientific validity. Owner review of this personal-use brief is `pending-personal-review`. No human-gold or scientific certification is asserted.
