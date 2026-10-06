# Acquisition report — bounded real sources

**Acquisition date:** 2026-10-03, Asia/Saigon  
**Scope:** personal-use lane authorized by [brainstorm contract](brainstorm-261003-personal-use-contract.md).  
**Staging root:** [`plans/evaluation/personal-use/source-acquisition/`](../evaluation/personal-use/source-acquisition/)  
**Status:** `DONE_WITH_CONCERNS`

## Outcome

Eleven reader-ready records were acquired from authoritative routes and written to [`derived/reader-ready.jsonl`](../evaluation/personal-use/source-acquisition/derived/reader-ready.jsonl):

| Lane | Count | Result |
|---|---:|---|
| Vietnamese Wikisource | 6 | Three pinned root pages remain catalog/front-matter locators, and one pinned prose/verse child page was acquired for each parent work with rendered passage extraction and parent/child lineage. |
| PMC scientific full text | 2 | Full JATS/XML snapshots; both article XML files contain an exact CC BY 4.0 statement. |
| World Bank measurement | 1 | Viet Nam `SP.POP.TOTL`, 2000–2025, 26 observations with country/date/value/unit fields. |
| SWE-bench | 1 | Real Django task `django__django-10087`, with dataset row, linked Django ticket 29518, base commit, and BSD 3-Clause license at that commit. |
| UCI Bank Marketing | 1 | Official archive preserved; first 10 rows of nested `bank.csv`, semicolon-delimited, retained as actual values. |

No synthetic sample, label, translation, measurement or human score was created. Raw bytes remain under `raw/`; transformation is recorded in [`extract-sources.py`](../evaluation/personal-use/source-acquisition/scripts/extract-sources.py). [`manifest.json`](../evaluation/personal-use/source-acquisition/derived/manifest.json) contains the full raw/derived hash inventory and a `resource_index` with named consumers, licenses, raw lineage and development/public status.

Every derived record has a named `domain`, `consumer` list, exact source locator, license label/version, retrieval/version object, raw hash and rights rationale. The SWE-bench task additionally marks issue-authored text and benchmark patch as development-private until their separate rights are reviewed.

## Acquisition routes and rights evidence

### Vietnamese Wikisource

The three requested root revisions remain catalog/front-matter locators. Their child records provide the actual passage samples:

| Record | Role and pinned route | Parent relation | Raw/derived evidence |
|---|---|---|---|
| `vi-wikisource-179667` | Catalog root [`oldid=179667`](https://vi.wikisource.org/w/index.php?title=T%C3%A0i_m%E1%BA%A1ng_t%C6%B0%C6%A1ng_%C4%91%E1%BB%91&oldid=179667) | Parent work: Tài mạng tương đố | [`JSON`](../evaluation/personal-use/source-acquisition/raw/vi-wikisource-179667.json), [`HTML`](../evaluation/personal-use/source-acquisition/raw/vi-wikisource-179667.html); `sample_role=catalog-locator` |
| `vi-wikisource-179899` | Actual prose child [`oldid=179899`](https://vi.wikisource.org/w/index.php?title=T%C3%A0i_m%E1%BA%A1ng_t%C6%B0%C6%A1ng_%C4%91%E1%BB%91%2FCu%E1%BB%91n_th%E1%BB%A9_nh%E1%BA%A5t&oldid=179899) | `parent_source_id=vi-wikisource-179667`, `parent_oldid=179667`; Tài mạng tương đố/Cuốn thứ nhứt | [`API JSON`](../evaluation/personal-use/source-acquisition/raw/vi-child-tai-179899.json), [`HTML`](../evaluation/personal-use/source-acquisition/raw/vi-child-tai-179899.html); 104,786 derived characters |
| `vi-wikisource-106841` | Catalog root [`oldid=106841`](https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m&oldid=106841) | Parent work: Thầy trò trong khám | [`JSON`](../evaluation/personal-use/source-acquisition/raw/vi-wikisource-106841.json), [`HTML`](../evaluation/personal-use/source-acquisition/raw/vi-wikisource-106841.html); `sample_role=catalog-locator` |
| `vi-wikisource-19383` | Actual prose child [`oldid=19383`](https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m%2FI&oldid=19383) | `parent_source_id=vi-wikisource-106841`, `parent_oldid=106841`; Thầy trò trong khám/I | [`API JSON`](../evaluation/personal-use/source-acquisition/raw/vi-child-thay-tro-19383.json), [`HTML`](../evaluation/personal-use/source-acquisition/raw/vi-child-thay-tro-19383.html); 9,349 derived characters |
| `vi-wikisource-80653` | Catalog root [`oldid=80653`](https://vi.wikisource.org/w/index.php?title=Truy%E1%BB%87n_Ki%E1%BB%81u_(b%E1%BA%A3n_Tr%C6%B0%C6%A1ng_V%C4%A9nh_K%C3%BD_1911)&oldid=80653) | Parent work: Truyện Kiều (bản Trương Vĩnh Ký 1911) | [`JSON`](../evaluation/personal-use/source-acquisition/raw/vi-wikisource-80653.json), [`HTML`](../evaluation/personal-use/source-acquisition/raw/vi-wikisource-80653.html); `sample_role=catalog-locator` |
| `vi-wikisource-71961` | Actual verse child [`oldid=71961`](https://vi.wikisource.org/w/index.php?title=Truy%E1%BB%87n_Ki%E1%BB%81u_%28b%E1%BA%A3n_Tr%C6%B0%C6%A1ng_V%C4%A9nh_K%C3%BD_1911%29%2FT%C3%BAy_Ki%E1%BB%81u_thi_t%E1%BA%ADp&oldid=71961) | `parent_source_id=vi-wikisource-80653`, `parent_oldid=80653`; Truyện Kiều (bản Trương Vĩnh Ký 1911)/Túy Kiều thi tập | [`API JSON`](../evaluation/personal-use/source-acquisition/raw/vi-child-kieu-71961.json), [`HTML`](../evaluation/personal-use/source-acquisition/raw/vi-child-kieu-71961.html); 10,420 derived characters |

Root `text` fields are catalog/front-matter wikitext with markup removal only. Child `text` fields are visible passages from the pinned rendered `parse.text`, extracted by the stdlib `HTMLParser`: `.prp-pages-output` is selected when present, otherwise `.mw-parser-output`; navigation, page numbers, references, tables, images, styles and parser metadata are skipped. Whitespace and paragraph/verse boundaries are normalized; no spelling, translation or literary content was added or corrected. The child API JSON and direct oldid HTML are both preserved, and `actual_passage=true` is recorded in each child record.

Page-level license reference: [Wikimedia CC BY-SA text](https://foundation.wikimedia.org/wiki/Legal%3AText_of_the_Creative_Commons_Attribution-ShareAlike_4.0_International_License/en). Public-domain markings are source-page claims and require a separate jurisdiction check before redistribution.

### PMC full text

Full text was retrieved through the official Europe PMC XML route after an official Europe PMC search identified `cc by`. License was checked in each article's own `<license>` node; PMC-wide “Open Access” was not treated as a universal license.

| Record | Article | Route | Article-level license |
|---|---|---|---|
| `pmc-PMC13623134` | “Distinct prior expectations shape tactile and proprioceptive localization”, DOI [`10.1371/journal.pone.0358656`](https://doi.org/10.1371/journal.pone.0358656) | [`PMC13623134 fullTextXML`](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13623134/fullTextXML) | CC BY 4.0; XML statement says the article is distributed under the Creative Commons Attribution License and permits reuse with attribution. |
| `pmc-PMC13623154` | “Gender disparities in leadership of methodological research in health science”, DOI [`10.1371/journal.pone.0359403`](https://doi.org/10.1371/journal.pone.0359403) | [`PMC13623154 fullTextXML`](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13623154/fullTextXML) | CC BY 4.0; the same exact article-level attribution statement is present in this XML. |

Raw XML is full text. The derived `text` is a deterministic title + abstract + body-paragraph excerpt capped at 9,000 characters; the cap does not alter the preserved source. This lane is suitable for English scientific writing/factual-slot inspection, with biomedical/health-science domain limits.

### World Bank chart measurement

- **Route:** [`SP.POP.TOTL` API snapshot](https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100).
- **Raw:** [`worldbank-vnm-population-2000-2025.json`](../evaluation/personal-use/source-acquisition/raw/worldbank-vnm-population-2000-2025.json).
- **Snapshot:** `lastupdated=2026-07-13`, one API page, 26 rows, dates 2000–2025, country `VNM`, indicator `SP.POP.TOTL`, values preserved as returned. The record retains `country`, `country_iso3`, `indicator`, `date`, `value`, `unit`, observation status and decimal fields.
- **Rights:** [World Bank summary terms](https://data.worldbank.org/summary-terms-of-use) and [public licenses](https://datacatalog.worldbank.org/public-licenses) state a CC BY 4.0 default with additional terms and possible third-party indicator restrictions. The source terms remain attached to the record.
- **Derived:** [`worldbank-series.jsonl`](../evaluation/personal-use/source-acquisition/derived/worldbank-series.jsonl). No values were recalculated or rounded.

This is a dated measurement snapshot. It does not establish that the values remain current or that a chart is scientifically/visually accepted.

### SWE-bench engineering task

- **Dataset slice:** [`swe-bench-rows-0-100.json`](../evaluation/personal-use/source-acquisition/raw/swe-bench-rows-0-100.json), fetched from the [official Hugging Face dataset server](https://datasets-server.huggingface.co/rows?dataset=SWE-bench%2FSWE-bench&config=default&split=test&offset=0&length=100). The raw slice was used only to select one row, `django__django-10087`.
- **Task:** repository `django/django`, version `2.2`, base commit `02cd16a7a04529c726e5bb5a13d5979119f25c7d`, problem statement, patch, test patch, fail-to-pass and pass-to-pass fields are preserved in [`swe-bench.jsonl`](../evaluation/personal-use/source-acquisition/derived/swe-bench.jsonl) for development use. Public/resource packaging should expose the issue/commit locator and verified code fixture only until issue-authored text and benchmark patch rights are separately reviewed.
- **Issue provenance:** the dataset row points to PR [`django/django#10087`](https://github.com/django/django/pull/10087), whose body links the actual Django ticket [`#29518`](https://code.djangoproject.com/ticket/29518). Both the GitHub API response and ticket HTML are preserved.
- **Commit provenance:** [base commit](https://github.com/django/django/commit/02cd16a7a04529c726e5bb5a13d5979119f25c7d) and API response are preserved.
- **Verified code fixtures:** [`sqlmigrate.py`](../evaluation/personal-use/source-acquisition/raw/swe-django-02cd16-sqlmigrate.py) and [`test_commands.py`](../evaluation/personal-use/source-acquisition/raw/swe-django-02cd16-test_commands.py) were fetched from the exact base commit. Their upstream locators, base commit, byte counts and SHA-256 values are in the `code_fixture` array in [`swe-bench.jsonl`](../evaluation/personal-use/source-acquisition/derived/swe-bench.jsonl). The implementation contains `class Command`; the test fixture contains `test_sqlmigrate` cases.
- **Rights:** [`LICENSE`](https://raw.githubusercontent.com/django/django/02cd16a7a04529c726e5bb5a13d5979119f25c7d/LICENSE) at the exact base commit is BSD 3-Clause for the verified Django code fixtures. This does not relabel the SWE-bench dataset row, issue body, problem statement, benchmark patch or test patch as BSD. Those task/issue fields are explicitly marked development-private.

The task is usable for engineering workflow inspection, not evidence of developer quality, benchmark superiority or task-license clearance for public redistribution.

### UCI Bank Marketing

- **Official source/license page:** [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank), DOI [`10.24432/C5K306`](https://doi.org/10.24432/C5K306). The saved page states CC BY 4.0 and exposes the official download route.
- **Archive route:** [`bank+marketing.zip`](https://archive.ics.uci.edu/static/public/222/bank%2Bmarketing.zip), saved as [`uci-bank-marketing.zip`](../evaluation/personal-use/source-acquisition/raw/uci-bank-marketing.zip). The nested official `bank.zip` is also preserved as [`uci-bank.zip`](../evaluation/personal-use/source-acquisition/raw/uci-bank.zip).
- **Bounded sample:** first 10 actual data rows from nested `bank.csv`, parsed with its official semicolon delimiter; header and values are preserved in [`uci-bank-marketing.jsonl`](../evaluation/personal-use/source-acquisition/derived/uci-bank-marketing.jsonl).
- **Use boundary:** direct phone marketing campaign/term-deposit response data. `duration` is post-contact and may leak the target in a prospective task; the sample is not campaign copy, a causal uplift result or a representative population.

## Hashes

The machine-readable manifest contains every raw and derived hash. Canonical raw bytes are summarized here:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `raw/vi-wikisource-179667.json` | 6,998 | `2e7d19ffff95d522b9e568429015603453678d7b1fb8a5b9b4f1047b7b445acd` |
| `raw/vi-child-tai-179899.json` | 196,461 | `0542592b40dbcc5d70f1f7ed3048f8b66729e4850c0dcca123a0cd5984d57352` |
| `raw/vi-child-tai-179899.html` | 246,434 | `4073c3e913d5433d8e553bca68bad2b53ff421add7a12196f582fc310cb0c15f` |
| `raw/vi-wikisource-106841.json` | 23,017 | `8b170f06825f99961f992b48ee757a75556f0fba6a3f3c4a9996540257eda037` |
| `raw/vi-child-thay-tro-19383.json` | 31,106 | `f52fbe45efebb62659384352ae8151bf3aa19d048b45418b17cdf39f9c977c1a` |
| `raw/vi-child-thay-tro-19383.html` | 71,196 | `5220e82099a8fa6a0beced7f660c14afdbeba9d79893c5fac6dbf627ccfa7661` |
| `raw/vi-wikisource-80653.json` | 18,609 | `789c1716f59efc02cd9c448b0a9ef6fcd89af9f9b7683a89503e12e5463c0096` |
| `raw/vi-child-kieu-71961.json` | 32,541 | `a2962b4d7906ca59637321dc6471951ccd33838a0fbd0cd58652a0f64e2db965` |
| `raw/vi-child-kieu-71961.html` | 84,956 | `28666363a4d0038911b50d0abff3dba65245e830e25ea1cd885e65a894d52483` |
| `raw/pmc-PMC13623134.xml` | 255,867 | `14988d37144b0315a4ef272f45b204568400a0fe33ee4e0905dc4c397f52ee06` |
| `raw/pmc-PMC13623154.xml` | 128,666 | `135e35ecbac31f8a2429ce25426d2564c3a87aa66f4f2ebaf3fd1bd15114c69c` |
| `raw/worldbank-vnm-population-2000-2025.json` | 5,217 | `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781` |
| `raw/swe-bench-rows-0-100.json` | 3,711,425 | `bd74ce0833a6af7cc6bdfde07cb2a1f4e92f2feaed4342e612ee8ee393a24d50` |
| `raw/swe-django-02cd16-license.txt` | 1,552 | `b846415d1b514e9c1dff14a22deb906d794bc546ca6129f950a18cd091e2a669` |
| `raw/swe-django-02cd16-sqlmigrate.py` | 2,742 | `6ca06cab795d7b1f1247c1a1327ac0ec54bc9295c68e3cbc95ac7f10be817371` |
| `raw/swe-django-02cd16-test_commands.py` | 67,864 | `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a` |
| `raw/uci-bank-marketing.zip` | 1,023,843 | `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4` |
| `raw/uci-bank.zip` | 579,043 | `99d7e8eb12401ed278b793984423915411ea8df099e1795f9fefe254f513fe5e` |

Derived reader hashes:

| Artifact | SHA-256 |
|---|---|
| [`derived/reader-ready.jsonl`](../evaluation/personal-use/source-acquisition/derived/reader-ready.jsonl) | `16175d1edc8116d07d9e952584f3ef47b3227cf8bd7d599cc30c695bff4f893e` |
| [`derived/vi-wikisource.jsonl`](../evaluation/personal-use/source-acquisition/derived/vi-wikisource.jsonl) | `04a21133aecb70fd3027891430869530f1e3df6eb7f2ee0771c4f409f64628f6` |
| [`derived/pmc-scientific.jsonl`](../evaluation/personal-use/source-acquisition/derived/pmc-scientific.jsonl) | `b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45` |
| [`derived/worldbank-series.jsonl`](../evaluation/personal-use/source-acquisition/derived/worldbank-series.jsonl) | `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2` |
| [`derived/swe-bench.jsonl`](../evaluation/personal-use/source-acquisition/derived/swe-bench.jsonl) | `1a8f89f611e12f59c92606adbaa1ccc8da3bd4dff818ff751d573395f7374535` |
| [`derived/uci-bank-marketing.jsonl`](../evaluation/personal-use/source-acquisition/derived/uci-bank-marketing.jsonl) | `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123` |

The renamed extraction script [`scripts/extract-sources.py`](../evaluation/personal-use/source-acquisition/scripts/extract-sources.py) has SHA-256 `1fc189fee9e5655f769f86dba091acbfd32d807233ce1633342f4948fe63fdc1`; the manifest records the same self-hash and the complete raw inventory.

## Deterministic extraction and checks

Command run from the workspace:

```powershell
python plans/evaluation/personal-use/source-acquisition/scripts/extract-sources.py
```

The script:

- preserves the three pinned Wikisource root records as catalog locators and derives one actual rendered passage from each pinned child oldid;
- uses a stdlib `HTMLParser` over rendered child `parse.text`, retaining visible prose/verse and paragraph boundaries while excluding page metadata, references and navigation;
- parses each PMC XML article, retains the exact license statement, and bounds the derived excerpt at 9,000 characters while keeping full XML;
- projects World Bank fields without value transformation;
- selects exactly one SWE-bench row, joins it to preserved issue/commit/license evidence, and verifies the two pinned Django code fixtures at the base commit;
- extracts exactly 10 rows from the official nested UCI `bank.csv` using an explicit semicolon delimiter;
- writes per-lane JSONL, combined `reader-ready.jsonl`, and the raw/derived manifest.

Validation completed: all six Wikisource API files parsed as JSON; all three child records have `actual_passage=true`, parent IDs, child oldids and non-empty rendered passage text; both PMC files parsed as well-formed XML and exposed CC BY 4.0 license nodes; the World Bank response parsed as one-page/26-observation JSON; the SWE task, issue, commit, BSD license and both code fixtures parsed, with expected implementation/test markers; the UCI outer/nested ZIPs opened and the 10-row sample parsed into 17 columns.

## Concerns and remaining gates

- Wikisource page-level CC BY-SA terms and the underlying-work public-domain rationale remain separate legal questions. The child passage records preserve the page license and do not convert the source-page rationale into a universal redistribution conclusion.
- The SWE-bench issue body, problem/task text, benchmark patch and dataset bytes retain their own provenance and remain development-private. Django's BSD 3-Clause evidence applies to the two verified upstream code fixtures at the pinned base commit, not automatically to those task artifacts.

Status: DONE_WITH_CONCERNS  
Summary: Acquired and hashed three pinned Wikisource catalog roots plus one actual rendered prose/verse child page for each parent work, two article-level CC BY 4.0 PMC full texts, one World Bank series, one provenance-complete SWE-bench Django task with pinned code fixtures, and one bounded UCI Bank Marketing sample; produced 11 reader-ready records and a deterministic renamed extraction script.  
Concerns/Blockers: Legal separation remains required between Wikisource page terms and underlying-work status, and between SWE-bench issue/task artifacts and the BSD-licensed Django code fixtures.
