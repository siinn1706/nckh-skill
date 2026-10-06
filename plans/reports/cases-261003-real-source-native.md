# Candidate native cases — bounded real sources

**Prepared:** 2026-10-03, Asia/Saigon  
**Scope:** five bounded personal-use candidate cases using the acquired real-source lane  
**Case file:** [`real-source-cases.json`](../evaluation/personal-use/native/cases/real-source-cases.json)  
**Acceptance profile:** [`personal-use.json`](../../nckh-kit/core/profiles/acceptance/personal-use.json)  
**Status:** `prepared-not-run`

## Outcome

Prepared exactly five candidate native tasks. Each task names one real reader record, its exact locator, the input artifacts and hashes, actual content anchors, a prompt that must use those bytes, an output locale/format/path, observable checks and limitations.

| Case | Skill contract | Real source used | Output contract |
|---|---|---|---|
| `real-source-vi-prose-taste-01` | `nckh-taste`, `nckh-write` | Wikisource `Thầy trò trong khám/I`, child oldid `19383`, parent oldid `106841` | Vietnamese Markdown taste/fidelity memo |
| `real-source-en-scientific-fidelity-01` | `nckh-write` | PMC `PMC13623154`, DOI `10.1371/journal.pone.0359403`, article-level CC BY 4.0 | English Markdown claim-fidelity brief |
| `real-source-worldbank-visual-01` | `nckh-visuals` | World Bank Viet Nam `SP.POP.TOTL`, 26 observations from 2000–2025 | Vietnamese editable SVG plus Markdown QA receipt |
| `real-source-django-code-review-01` | `nckh-code-review` | Django code fixtures at base commit `02cd16a7a04529c726e5bb5a13d5979119f25c7d` | English review-only Markdown report |
| `real-source-uci-analytics-01` | `nckh-analytics` | UCI Bank Marketing first 10 `bank.csv` rows, 17 columns | Vietnamese Markdown descriptive analytics memo |

The JSON is a preparation artifact. No model was dispatched, no native output was claimed, and no output artifact listed in a case exists yet. A future native run must create the specified artifact and preserve its own route/model receipt, input hashes, output hash and failure/timeout state.

## Frozen source packet

The cases point to the acquired snapshot rather than a live re-fetch. The shared reader file is [`reader-ready.jsonl`](../evaluation/personal-use/source-acquisition/derived/reader-ready.jsonl), SHA-256 `16175d1edc8116d07d9e952584f3ef47b3227cf8bd7d599cc30c695bff4f893e`. The manifest is [`manifest.json`](../evaluation/personal-use/source-acquisition/derived/manifest.json), SHA-256 `48d6b7ca16d777a7248197c5271f697fdcd05cc99e0f15aec6600d273ade5998`.

| Case | Source ID and locator | Exact input lineage |
|---|---|---|
| VI prose/taste | [`vi-wikisource-19383`](https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m%2FI&oldid=19383) | Child API JSON `raw/vi-child-thay-tro-19383.json`, 31,106 bytes, SHA-256 `f52fbe45efebb62659384352ae8151bf3aa19d048b45418b17cdf39f9c977c1a`; child HTML `raw/vi-child-thay-tro-19383.html`, 71,196 bytes, SHA-256 `5220e82099a8fa6a0beced7f660c14afdbeba9d79893c5fac6dbf627ccfa7661`; derived lane `derived/vi-wikisource.jsonl`, SHA-256 `04a21133aecb70fd3027891430869530f1e3df6eb7f2ee0771c4f409f64628f6` |
| EN scientific fidelity | [`pmc-PMC13623154`](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13623154/) | Full XML `raw/pmc-PMC13623154.xml`, 128,666 bytes, SHA-256 `135e35ecbac31f8a2429ce25426d2564c3a87aa66f4f2ebaf3fd1bd15114c69c`; derived lane `derived/pmc-scientific.jsonl`, SHA-256 `b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45` |
| World Bank visual | [`worldbank-vnm-SP.POP.TOTL-2000-2025`](https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100) | API JSON `raw/worldbank-vnm-population-2000-2025.json`, 5,217 bytes, SHA-256 `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781`; derived lane `derived/worldbank-series.jsonl`, SHA-256 `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2` |
| Django code review | [`django__django-10087`](https://huggingface.co/datasets/SWE-bench/SWE-bench), using only its `code_fixture` entries | `sqlmigrate.py`, 2,742 bytes, SHA-256 `6ca06cab795d7b1f1247c1a1327ac0ec54bc9295c68e3cbc95ac7f10be817371`; `test_commands.py`, 67,864 bytes, SHA-256 `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a`; exact BSD license SHA-256 `b846415d1b514e9c1dff14a22deb906d794bc546ca6129f950a18cd091e2a669`; derived lane `derived/swe-bench.jsonl`, SHA-256 `1a8f89f611e12f59c92606adbaa1ccc8da3bd4dff818ff751d573395f7374535` |
| UCI analytics | [`uci-bank-marketing-bank-csv-first-10`](https://archive.ics.uci.edu/dataset/222/bank) | Outer ZIP `raw/uci-bank-marketing.zip`, 1,023,843 bytes, SHA-256 `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4`; nested ZIP `raw/uci-bank.zip`, 579,043 bytes, SHA-256 `99d7e8eb12401ed278b793984423915411ea8df099e1795f9fefe254f513fe5e`; derived lane `derived/uci-bank-marketing.jsonl`, SHA-256 `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123` |

## Case checks and boundaries

### VI prose and taste

The task reads the actual `Thầy trò trong khám/I` passage and anchors the memo to the opening narrative and dialogue phrases. It requires Vietnamese register, rhythm, archaic vocabulary, audience and genre observations, with subjective suggestions kept separate from preserved source text. Expected checks include exact source identity/oldids, three unchanged content anchors, position-specific observations and no claim of complete literary or native-reader authority.

The source is one pinned child page. The parent record warns that issue XIV is missing. Page-level CC BY-SA terms and the underlying-work public-domain rationale remain separate legal questions.

### EN scientific writing fidelity

The task uses the actual PMC title, abstract and preserved XML to create a five-row claim ledger and a short conclusion. The specified anchors include the 1,375-study count, first/last-author counts, 486/848 last-author counts, percentages and association wording. The acceptance checks require exact numbers and certainty, association language rather than causality, PMCID/DOI/license provenance and an explicit distinction between the 9,000-character projection and full XML.

The projection is bounded and the selected article is health-science/biomedical in scope. Fluent prose is not scientific validity, peer-review acceptance or a general writing benchmark.

### World Bank data and visual

The task must use all 26 non-null observations, with 2000=`77,154,011` and 2025=`101,598,527`. The raw `unit` field is `""`; the task explicitly preserves the blank and forbids inventing `persons` or another supplied unit. The output requires an editable SVG, source-to-mark mapping, axes, caption, Vietnamese alt text, response metadata, hashes and a QA receipt. A generated visual cannot be called render-passed or editable until inspected.

The API snapshot is dated and values may be revised. The blank unit is a source limitation. Sorting dates for display is allowed; value transformation, interpolation and causal explanation are not.

### BSD Django code review

The task reads only the two verified upstream code fixtures. It directs the reviewer to inspect `class Command`/`handle` and the three actual `sqlmigrate` test methods at the pinned line locations. The output must report actionable findings with file/line, impact, why or reproduction and required edit, or an explicit no-finding result with inspected scope. It is review-only and cannot edit code, merge, publish or claim security guarantees.

The issue body, problem statement, benchmark patch, test patch and dataset task text are excluded from the case input and remain development-private. BSD-3-Clause evidence applies only to the two verified Django code fixtures. Without ticket text or test execution, the case cannot judge ticket intent or runtime behavior.

### UCI analytics

The task uses the actual first ten `bank.csv` rows and all 17 preserved columns. It requires the observed target count `y=no=10`, `y=yes=0`, month counts `may=5`, `apr=2`, `feb=1`, `jun=1`, `oct=1`, and the negative `balance=-88`. It requires a Vietnamese descriptive memo with delimiter, DOI, archive lineage, hashes, data-quality notes and explicit separation from causal lift, forecast or population response rate.

The sample is bounded and not representative. `duration` is post-contact and may leak the target in prospective prediction. No fabricated positive outcomes, segments or uplift may be added.

## Native route contract

Every case inherits the route constraints in the JSON:

- Cursor may use only **Grok 4.7 Extra High** and must preserve an unavailable/error result without fallback.
- Antigravity may use **Gemini 3.8 Flash High** and must preserve an unavailable/error result without fallback.
- The current application may use all callable models, but the effective model must come from a native receipt rather than catalogue metadata.

No model dispatch, installation, global configuration change, package change, external write, publication or benchmark packaging was performed while preparing these cases.

Status: DONE_WITH_CONCERNS  
Summary: Prepared five bounded real-source candidate native tasks with exact source IDs, locators, raw/derived hashes, content anchors, output contracts and observable acceptance checks for VI prose/taste, EN scientific fidelity, World Bank visuals, BSD Django code review and UCI analytics.  
Concerns/Blockers: Native execution and owner review remain pending by design; source-specific limitations and the Wikisource/SWE rights boundaries remain attached to the cases.
