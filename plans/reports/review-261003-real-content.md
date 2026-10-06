# Frozen real-resource content sanity

Status: DONE

## Scope

Bounded read-only content review of the five normalized resource files and their registry, rights records and named staging inputs. The request began against r23; root moved to r24 to synchronize the bundle provenance schema while these five resources and the registry stayed unchanged. The final check observed source-lock revision `24`; all five file hashes and the registry matched its pins.

No source edits, acquisitions, full test suite, build, freeze, install, UI or provider calls were performed by this reviewer. Only this report was written. Content checks establish the stated snapshot identity and bounded projection behavior, not human gold, scientific validity, model benefit or public-release rights.

## Findings

No concrete content defect was found in the reviewed five-file snapshot.

## Actual bounds and package hashes

| Resource file under `nckh-kit/core/profiles/resources/` | JSONL records | Actual bounded contents | SHA-256 |
|---|---:|---|---|
| `vi-wikisource.jsonl` | 3 | Three child passages; 104,786 / 9,349 / 10,420 characters | `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f` |
| `pmc-scientific.jsonl` | 2 | Two article projections, 9,000 characters each | `b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45` |
| `worldbank-series.jsonl` | 1 | One wrapper containing 26 observations, 2000–2025 | `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2` |
| `uci-bank-marketing.jsonl` | 1 | One wrapper containing first 10 `bank.csv` rows and all 17 columns | `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123` |
| `swe-bench-reference.jsonl` | 1 | One wrapper containing two Django code fixtures and task locators | `e81048922d196fd302555f192d289d51d82449b0ae724fc05cb2e2b4bfeb90cf` |

Total: eight JSONL wrapper/passage records across five files. Nested observations, table rows and fixtures are counted separately above.

Registry `nckh-kit/core/registry/catalog/resources.json`: `08280a57da31f62d88666b4dcca5f6b31589d73f0544c5751ba4632f1cd1ad9b`.

## Source identity and projection checks

### Wikisource

- Packaged rows equal the three `actual_passage=true` rows selected from the six-record staged `derived/vi-wikisource.jsonl`; the three catalog/front-matter roots are excluded.
- Child oldids are `179899`, `19383`, `71961`; corresponding parent oldids are `179667`, `106841`, `80653`.
- Each child title, page ID and revision ID matches its named raw API `parse` object. Child API and rendered-page HTML hashes match each record's raw provenance and registry lineage.
- Parent IDs provide context; no catalog root is counted as a passage. Text content equals the staged normalized child records without additional package edits.
- The rights record retains page-level CC BY-SA terms separately from the underlying-work rationale and jurisdiction caveat. This review does not clear external redistribution.

### PMC

- `PMC13623134` / DOI `10.1371/journal.pone.0358656` and `PMC13623154` / DOI `10.1371/journal.pone.0359403` match the article IDs in their staged JATS/XML.
- Both packaged titles match XML article titles. Both XML hashes match record provenance and registry lineage.
- Each named XML contains the CC BY 4.0 license URL and Creative Commons Attribution statement; the rights record scopes this evidence to these two articles.
- Packaged excerpts are bounded to 9,000 characters per article. The original XML is not a packaged dependency.

### World Bank

- All 26 projected observations equal the named raw API fields for country, ISO3, indicator identity/name, year, value, unit, observation status and decimal metadata.
- Years are exactly 2000–2025. The blank unit remains blank; no rounding or recalculation was observed.
- Raw hash and response `lastupdated=2026-07-13` match the record's provenance/version. This remains a dated snapshot.

### UCI Bank Marketing

- The nested `bank.zip` bytes exactly equal the member extracted from the staged official outer ZIP; its recorded SHA-256 matches.
- Parsed semicolon-delimited `bank.csv` headers and first ten data rows exactly equal the packaged values. All 17 columns are retained.
- Dataset DOI and original authors remain in the record. The bounded/nonrepresentative-sample and post-contact `duration` caveats remain explicit.

### Django fixtures and private-source boundary

The wrapper contains exactly these two upstream paths at base commit `02cd16a7a04529c726e5bb5a13d5979119f25c7d`:

| Upstream file | Encoded UTF-8 bytes | SHA-256 of packaged content and staged raw |
|---|---:|---|
| `django/core/management/commands/sqlmigrate.py` | 2,742 | `6ca06cab795d7b1f1247c1a1327ac0ec54bc9295c68e3cbc95ac7f10be817371` |
| `tests/migrations/test_commands.py` | 67,864 | `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a` |

- Encoding each nested `content` string as UTF-8 produces exactly the corresponding staged raw bytes, length and hash. The second file has 67,824 Unicode characters but 67,864 bytes; the stored byte count is correct.
- No dictionary fields named `problem_statement`, `patch`, `test_patch`, `issue_body`, `dataset_row`, `body` or `issue_text_reference` occur anywhere in this wrapper. The `private_fields` list contains field names as boundary metadata, not their contents.
- Actual staged problem statement (230 characters), benchmark patch (960) and test patch (1,021) do not occur in the serialized package as literal or JSON-escaped text. No benchmark dataset row object is packaged.
- The staged GitHub issue's entire 43-character `body` is the ticket URL `https://code.djangoproject.com/ticket/29518`. That string is present only as the permitted `task_locator.issue_locator`; it is a source locator, not an issue-prose payload. A naive byte-substring check initially flagged this, and checking the actual source/field placement resolved it as a false positive.
- Packaged BSD license bytes exactly equal the staged Django license. The notice scopes rights to the two code fixtures and keeps task/issue/benchmark rights separate.

## Rights and raw lineage bindings

Every package file hash equals its registry artifact hash and r24 source-lock pin. All license/notice hashes equal the actual packaged rights files. All 14 declared raw upstream hashes (six Wikisource, two PMC, one World Bank, two UCI, three Django including the license) match actual named staged files and are retained in registry lineage. These registry lineage items have no packaged raw `path`.

| Rights/notice file under the resource directory | SHA-256 |
|---|---|
| `wikisource-rights.md` | `41f9ceeda447546ec7a73b2e74b9bb4fc777c191f2a9a100239f1d65610e4fa4` |
| `pmc-rights.md` | `bc5b60966d872fe96dfbc49a38e1009170a2117796e9147021373f5b5a57d979` |
| `worldbank-rights.md` | `ea51d41b42f8fca82fa0c350622f156f8f921abf2204db4dc7b83980c072e7cd` |
| `uci-rights.md` | `1da0584a1daf4fc1cc01e9d2028067d1a0c930f451cce7fef3b5753ef40bd096` |
| `swe-bench-rights.md` | `b846415d1b514e9c1dff14a22deb906d794bc546ca6129f950a18cd091e2a669` |
| `swe-bench-notice.md` | `635acff745ff0f7a181088745159f737cec450d1faaacf9dbc5fa0f16746d9eb` |

## Staging evidence read

Paths below are relative to `plans/evaluation/personal-use/source-acquisition/`.

| Staged file | SHA-256 |
|---|---|
| `derived/manifest.json` | `48d6b7ca16d777a7248197c5271f697fdcd05cc99e0f15aec6600d273ade5998` |
| `derived/vi-wikisource.jsonl` | `04a21133aecb70fd3027891430869530f1e3df6eb7f2ee0771c4f409f64628f6` |
| `raw/vi-child-tai-179899.json` | `0542592b40dbcc5d70f1f7ed3048f8b66729e4850c0dcca123a0cd5984d57352` |
| `raw/vi-child-tai-179899.html` | `4073c3e913d5433d8e553bca68bad2b53ff421add7a12196f582fc310cb0c15f` |
| `raw/vi-child-thay-tro-19383.json` | `f52fbe45efebb62659384352ae8151bf3aa19d048b45418b17cdf39f9c977c1a` |
| `raw/vi-child-thay-tro-19383.html` | `5220e82099a8fa6a0beced7f660c14afdbeba9d79893c5fac6dbf627ccfa7661` |
| `raw/vi-child-kieu-71961.json` | `a2962b4d7906ca59637321dc6471951ccd33838a0fbd0cd58652a0f64e2db965` |
| `raw/vi-child-kieu-71961.html` | `28666363a4d0038911b50d0abff3dba65245e830e25ea1cd885e65a894d52483` |
| `raw/pmc-PMC13623134.xml` | `14988d37144b0315a4ef272f45b204568400a0fe33ee4e0905dc4c397f52ee06` |
| `raw/pmc-PMC13623154.xml` | `135e35ecbac31f8a2429ce25426d2564c3a87aa66f4f2ebaf3fd1bd15114c69c` |
| `raw/worldbank-vnm-population-2000-2025.json` | `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781` |
| `raw/uci-bank-marketing.zip` | `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4` |
| `raw/uci-bank.zip` | `99d7e8eb12401ed278b793984423915411ea8df099e1795f9fefe254f513fe5e` |
| `raw/swe-django-02cd16-sqlmigrate.py` | `6ca06cab795d7b1f1247c1a1327ac0ec54bc9295c68e3cbc95ac7f10be817371` |
| `raw/swe-django-02cd16-test_commands.py` | `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a` |
| `raw/swe-django-10087-issue.json` | `f3480574807aa7b61dc5de927c7a5375f0c8a18cb3360e9fdbd954c3b471075e` |
| `raw/swe-bench-rows-0-100.json` | `bd74ce0833a6af7cc6bdfde07cb2a1f4e92f2feaed4342e612ee8ee393a24d50` |
| `raw/swe-django-02cd16-license.txt` | `b846415d1b514e9c1dff14a22deb906d794bc546ca6129f950a18cd091e2a669` |

Concerns/Blockers: None for the bounded content sanity scope. Root owns full verification; no full-suite or generated-bundle acceptance is claimed here.
