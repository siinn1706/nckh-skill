# Red-team contract review — plan 261004-0047

## Scope and verdict

- Reviewed all six requested plan files and the requested current consumers: `core/build.py`, `core/evaluation.py`, `core/resources.py`, `skills.json`, `resources.json`, `personal-use.json`, `scripts/search-resource.py`, `tests/acceptance/test_profile.py`, `tests/release/test_qualification.py`, and `tests/resource/test_consumers.py`.
- Lens: hostile Assumption Destroyer; Standard-tier Fact Checker and Contract Verifier. This is a plan review, not a code review. No lint, build, test, install, native/provider, paid, model, or external run was performed.
- The plan correctly preserves pending approval, source/rights provenance, the personal-use versus stable/scientific boundary, and the existing `nckh-write` compatibility intent. It is not yet an executable contract: the findings below can make a nominal `37→39` implementation fail closed or pass while violating the stated preservation guarantees.

## Findings

### HIGH — New writer resource consumers are not assigned, so the promised writing samples cannot be read or packaged

**Plan evidence:** `phase-01-start.md:16-18,28-34,40-43` requires the two new writers and says to reuse bounded Wikisource/PMC samples, but its ownership list does not modify the resource consumer registry; `phase-04-integration-and-personal-acceptance.md:16,38-39` promises nine-resource closure and selected writer reads without naming the new consumer bindings.

**Code evidence:** The current registry assigns `R-nature-reference` to only `nckh-write,nckh-taste` (`core/registry/catalog/resources.json:124-163`), `R-vi-wikisource-passages` to only `nckh-write,nckh-taste` (`:165-259`), and `R-pmc-scientific` to `nckh-write,nckh-evidence,nckh-method` (`:261-328`). `search-resource.py:206-223` rejects a consumer absent from that list, while `build.py:220-229` selects/packages required resources only when the identity is listed as a consumer. `resources.py:52-58` validates explicit consumers; it does not inherit `nckh-write` resources for a new identity.

**Concrete failure:** Current writing-resource caller counts are R-nature **2**, R-Wikisource **2**, R-PMC **3**; `nckh-humanwrite` and `nckh-paperwrite` each have **0** bindings. A future lookup with either new consumer fails at the consumer check, and a normal build silently declares no required resource for that skill. The plan can therefore reach “9 resources” while its P1 sample-read and P4 selected-writer-read exits are impossible.

**Required plan correction:** Name the exact resource→consumer matrix (or explicitly remove the sample requirement). If reuse is intended, update `resources.json`, each new route’s reader/reference invocation, source-lock/closure ownership, and focused consumer tests in one transaction; do not rely on `nckh-write` compatibility to imply resource inheritance.

### HIGH — The 39-identity transition omits a hard count consumer and does not define an exact preserved identity set

**Plan evidence:** `phase-01-start.md:24-27` names `build.py`/`evaluation.py` as the hard-coded-37 owners and `personal-use.json`/`test_profile.py` as profile owners, but omits `core/acceptance.py` and the catalog schema; `phase-04-integration-and-personal-acceptance.md:14,24-25,37-38` repeats “exact 39” without an explicit old-set equality check. The stated preservation requirement is `phase-01-start.md:14-15` and `phase-04-integration-and-personal-acceptance.md:14`.

**Code evidence:** `core/acceptance.py:75-82` rejects any profile or catalog whose unique count is not **37**, and `load_profile` reaches that validator (`:172-177`). `core/contracts/catalog.schema.json:12-15` has only `minItems: 37`, not exact cardinality or membership. `core/build.py:166-190` and `core/evaluation.py:74-91` also validate only a count/dictionary-derived set. The acceptance test and qualification test retain literal 37/148 assertions (`tests/acceptance/test_profile.py:21-30`; `tests/release/test_qualification.py:12-19,34-49`).

**Concrete failure:** Updating the listed catalog/profile/eval files to 39 while leaving `core/acceptance.py` unchanged makes `test_profile` setup and every `load_profile`/`lookup` call fail with “exactly 37”. Conversely, changing all counts to 39 still permits a 39-unique-ID catalog that drops a legacy identity and adds a typo/new ID: profile equality only compares profile to that catalog (`core/acceptance.py:105-116`), and no current schema or count check proves that all old 37 remain.

**Required plan correction:** Add every count consumer to the owner table, including `core/acceptance.py`, `catalog.schema.json`, and literal test expectations. Define one exact expected set (`old 37 ∪ {nckh-humanwrite,nckh-paperwrite}`) and reject both missing legacy IDs and duplicate/extra catalog entries; count-only checks are insufficient for the compatibility claim.

### MEDIUM — P1–P3 edits precede the only permitted source-lock freeze, but the listed validation/build commands require a frozen inventory

**Plan evidence:** `phase-01-start.md:10` makes r26 read-only and assigns freeze/revision only to P4; P1 then adds skills/cases and lists `evals/run-evals.py --validate-only` at `:32-47`. The phase dependency order places P4 after P1–P3 (`plan.md:24-31`), while P4 says to re-run/update/freeze and build at `phase-04-integration-and-personal-acceptance.md:37-42`.

**Code evidence:** `core/build.py:90-98` rejects any source-member set not equal to the lock inventory. `core/evaluation.py:72-77,115` invokes that check from `validate_cases`; `evals/run-evals.py:49-52` invokes `validate_cases` for `--validate-only`. `build.py:193-210` performs the same check before and during materialization.

**Concrete failure:** Adding a new `SKILL.md`, reference, eval case, or test under a locked source area before P4 makes the named P1/P2/P3 `--validate-only` or build path fail with “source lock inventory changed”. The plan currently has no staged-lock/temporary-worktree contract and no statement that all lock-dependent checks are deferred until P4, so phase completion and evidence timing are contradictory.

**Required plan correction:** Put an explicit freeze boundary before the first lock-dependent validation/build, or mark P1–P3 checks as non-locking design checks and defer the listed commands until P4. Keep the user’s “P4 is the only freeze owner” decision; only clarify sequencing and receipts.

### MEDIUM — New writer cases and the proposed writer matrix have no single executable validator

**Plan evidence:** `phase-01-start.md:32-34,43-47` makes the new policy/JSON cases and `test_writer_consumers.py` conditional (“only if”); `phase-04-integration-and-personal-acceptance.md:31-32,38-40,49` introduces `writer-invocation-matrix.json` and `test_writer_matrix.py` as optional/future checks while the exit still claims dynamic writer checks.

**Code evidence:** `core/evaluation.py:14-37,72-95` validates four cases per catalog identity and historical required families, but `:104-115` reads only the fixed historical `evals/cases/runtime/invocation-matrix.json` and checks 224 cells. `evals/run-evals.py:49-52` has no writer-matrix path. `tests/release/test_qualification.py:12-23` asserts only the old 37/148/19/224 aggregate. Likewise, the reader has only reviewed resource branches for registered IDs (`scripts/search-resource.py:206-223,266-274`).

**Concrete failure:** A malformed, incomplete, or semantically empty new writer matrix can coexist with a passing existing `--validate-only`, because the proposed file is not read. A Humanizer adaptation can likewise be added as Markdown/JSONL without a deterministic resource ID/reader/artifact receipt: the generic reader does not consume arbitrary Markdown, and JSONL lookup requires a registered consumer/locale/genre. The plan’s “reader→artifact→test” exit is therefore not mechanically observable for the NEW candidates.

**Required plan correction:** Choose an owning validator and make it mandatory for the accepted plan: either extend the existing evaluator with an explicit writer-matrix schema/reader, or require the new test/CLI and define its count, route, negative, receipt, and no-side-effect oracles. Separately decide whether Humanizer is an owned local policy (outside the resource registry, with its own hash/reader/test) or a registered resource (with catalog consumer/rights/closure rows); do not leave “Markdown/JSONL, generic reader if schema validates” as the contract.

### MEDIUM — The research-only visual policy silently assumes all quantitative plots are measurement-backed

**Plan evidence:** `phase-02-scientific-visuals.md:14-16,37-41` allows measurement charts, sourced mechanisms, or illustrative artifacts and rejects model-created observations/measurements; `source-adoption-map.md:24-28` also bans a new chart dataset from synthetic data. No explicit non-goal says computational/theoretical simulation or derived plots are excluded.

**Code evidence:** The current visual contract says no synthetic measurements may masquerade as observed results (`skills/core/nckh-visuals/SKILL.md:24-32`) and requires real chart input, but it does not define a `derived/simulation` artifact class. The documentation similarly states “Charts require real data” and separates sourced/inferred mechanisms and illustrative artwork (`docs/research-and-writing.md:41-48`). Existing visual evals cover sourced/inferred provenance and invented measurements-as-real (`evals/cases/research-writing-visuals/nckh-visuals.json:7-18,38-43,149-172`), not a correctly labeled simulation output.

**Concrete failure:** A valid research task that plots a cited model’s simulated/analytical output with versioned parameters and uncertainty is neither an observed measurement nor merely an explanatory illustration; under the plan’s bounded enum (`:37`) it has no positive route and may be rejected as “model-created measurement”. This is a scope assumption, not a request to add a simulation pipeline.

**Required plan correction:** Resolve the user decision explicitly: state that computational/derived plots are out of scope, or add only a bounded labeled `derived/simulation` case whose contract preserves model/code/version, parameters, transformations, uncertainty, source hashes, and “not observed measurement” wording. Keep fabricated observations prohibited.

## Sample claim status

| Claim | Status | Evidence |
|---|---|---|
| Source baseline is r26, 243 pinned files, 37 identities, 9 resources, with no mismatching pins | VERIFIED | `plans/reports/checks-261004-0047-source-baseline.json:5-12`; current catalog files also contain 37 skill rows and 9 resource rows. |
| Installed candidate is r25/43 current items and differs from source only in the recorded four pins | VERIFIED | `plans/reports/review-261004-0047-current-kit.md:7-16`; the report explicitly treats this as a source delta, not an automatic defect. |
| Existing resource lookup is consumer/locale/genre/domain scoped and fail-closed | VERIFIED | `scripts/search-resource.py:206-229`; consumer counts above are explicit registry bindings, not inferred inheritance. |
| The finalized 37→39 transition can pass the current acceptance/profile path as written | FAILED | `core/acceptance.py:75-82` still requires 37; no phase owner names this consumer. |
| Humanizer upstream revision/currentness and broad-package provenance are established | UNVERIFIED | `plans/reports/researcher-261004-0047-writing-resources.md:15-18,55-65` records local hashes but unknown upstream revision and limits claims to selected bytes. |
| Structural counts imply writer quality, native behavior, scientific meaning, or human acceptance | FAILED / correctly rejected by the plan | `plan.md:33-39`; current evaluator returns static/pending evidence (`core/evaluation.py:116-124`). |

## Unresolved questions

1. Are correctly labeled computational/simulation/derived research plots inside the user’s “scientific-only” visual scope?
2. Which exact resources, if any, should be callable by each of `nckh-humanwrite` and `nckh-paperwrite`?
3. Is the Humanizer adaptation an owned local policy or a registry resource with a formal reader/artifact/test contract?
4. Should the new writer cases remain personal-use-only and outside the historical 19 required families, as implied by the separate writer matrix?

Status: DONE_WITH_CONCERNS
Summary: The review found five contract-level concerns; the strongest are missing new-writer resource bindings and incomplete 37→39 count/membership closure. No product files, plan files, source lock, configuration, or runtime state were changed.
Concerns/Blockers: Controller/user decision is required for writer resource mapping and the simulation/derived-visual scope; the other findings are plan sequencing/ownership corrections.
