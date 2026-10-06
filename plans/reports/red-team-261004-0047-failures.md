# Red-team failure review — NCKH research/data/hooks plan

## Scope and verification

- Reviewed all six plan files under `plans/261004-0047-nckh-research-data-hooks-writing/`, plus `researcher-261004-0047-native-hook-capabilities.md` and `review-261004-0047-current-kit.md`.
- Read the requested build/evaluation/install/guard/source-freeze/visual/resource/installer/schema/adapter-test sources. This was review-only: no build, test, install, native, model, provider, or source mutation was performed.
- Baseline claim check: r26/243 pins/37 identities/9 resources and installed r25/43 items are supported by the current-kit report; hook `not-installed`/`unverified` is supported by the capability report and adapter test. These are read-only report/code claims, not freshly generated receipts.
- Finding rule: only concrete end-to-end failure paths or contract gaps are included. Historical 37/148/224 evidence is not treated as a defect where the plan explicitly preserves it.

## Findings

### F1 — HIGH — P1 validation is ordered before the only permitted source-lock update

**Evidence.** The plan makes r26 read-only and gives freeze/revision ownership exclusively to P4 (`phase-01-start.md:10`; `phase-04-integration-and-personal-acceptance.md:15,23`). P1 nevertheless lists `python evals/run-evals.py --validate-only` as an implementation gate (`phase-01-start.md:45-47`), while the source map says new P1/P2 artifacts must be tested before the broad validator (`source-adoption-map.md:32`).

**Failure path.** P1 must add the two writer skill/reference trees and case/profile JSON. `source_members()` scans new `.md`/`.json` files (`nckh-kit/core/build.py:41-57`), but `verify_source_lock()` requires the lock file set to match exactly and rejects a changed inventory (`nckh-kit/core/build.py:90-98`). `run-evals --validate-only` reaches `validate_cases()` and then verifies that lock (`nckh-kit/evals/run-evals.py:49-52`; `nckh-kit/core/evaluation.py:72-77,115-118`). With the lock intentionally unchanged until P4, the named P1 gate deterministically fails with “source lock inventory changed.”

**Narrow correction.** Mark the P1/P2 invocation as pre-change baseline-only, or move post-change `--validate-only` to the P4 freeze checkpoint. If the phase requires post-change validation, add an explicit approved staged-lock transition before that gate while retaining one freeze owner; do not silently bypass lock verification.

### F2 — HIGH — The 37→39 migration omits live profile/schema/test owners and mixes candidate counts with historical counts

**Evidence.** P1 names `build.py`/`evaluation.py` and profile JSON/test updates but not the acceptance reader/schema or the other fixed-count callers (`phase-01-start.md:25-35`). P4 says to update catalog/profile/build/eval atomically to 39 while retaining old case history (`phase-04-integration-and-personal-acceptance.md:38,41,59`).

**Failure path.** Adding 39 profile rows makes the existing acceptance loader reject the profile because it requires exactly 37 skills and a 37-row catalog (`nckh-kit/core/acceptance.py:75-82`). The catalog schema still only declares the old lower bound (`nckh-kit/core/contracts/catalog.schema.json:12-15`), and the existing acceptance/release tests assert 37/148 (`nckh-kit/tests/acceptance/test_profile.py:21-25`; `nckh-kit/tests/release/test_qualification.py:12-16,34-49`). Meanwhile `scripts/compare-matched.py` intentionally freezes the historical 148/37 diagnostic input (`nckh-kit/scripts/compare-matched.py:51-65`). A blanket count replacement breaks history; a partial replacement fails the candidate validator/tests.

**Narrow correction.** Add a count-inventory table to P1/P4 classifying every caller as candidate (`39/156`) or immutable historical (`37/148`, and runtime `224`), then list exact owners: `core/acceptance.py`, catalog schema, acceptance/release tests, and historical comparison checker. Update only candidate owners and assert that historical artifacts remain unchanged.

### F3 — HIGH — P3 hook files have no source-lock, artifact, or installer packaging route

**Evidence.** P3 requires `hooks/runner.py`, `hooks/hooks.json`, four codecs, and a manual fallback (`phase-03-portable-hooks.md:32-41,56`); P4 requires four-host on/off/plugin bundles and scoped receipts (`phase-04-integration-and-personal-acceptance.md:16,39,59`).

**Failure path.** The current artifact builder’s source areas do not include `hooks` (`nckh-kit/core/build.py:18-21`), and `_materialize_host()` starts closure from selected skill trees/resources only (`nckh-kit/core/build.py:218-231`). The generated manifest records skills/agents/plugin/resources, with no hook member (`nckh-kit/core/build.py:305-340`). Therefore implementing the listed P3 files leaves them unpinned and absent from every bundle; manually injecting them makes the manifest’s actual-file set fail its ownership check (`nckh-kit/core/build.py:358-371`).

**Narrow correction.** Choose one explicit ownership model before P3 exit: either extend source-lock/build/bundle manifests and installer projection with a bounded hook closure, or declare hooks external/manual and remove them from the portable-bundle acceptance claim. Keep host registration/trust as a separate post-package gate.

### F4 — HIGH — Config-merge and rollback acceptance has no executable owner or CLI path

**Evidence.** P3 requires preserving shared Codex/AGY `.agents`, leaving invalid JSON untouched, and writing only owned hook blocks (`phase-03-portable-hooks.md:41`). P4 then requires install/update/config lifecycle, rollback-conflict receipts, and preserved config ownership (`phase-04-integration-and-personal-acceptance.md:42,49,55,59`), but lists only a future test/receipt and no concrete config-mutator entrypoint (`phase-04-integration-and-personal-acceptance.md:32,49`).

**Failure path.** Existing installer operations expose install/update/doctor/config-models/uninstall only (`nckh-kit/installer/nckh-installer.py:37-56,86-118`). The transaction stages only skill directories or native-agent text (`nckh-kit/core/install.py:570-594`), and rollback validates every journal target as a skill-named file under owned skill roots (`nckh-kit/core/install.py:499-515`). No path parses/merges a host JSON config or journals an owned hook block. The proposed invalid-JSON/shared-`.agents` cases therefore cannot be invoked through the stated installer preview/rollback flow; adding a JSON target to the current journal would be rejected or be outside the ownership model.

**Narrow correction.** Name a concrete config-merge owner and invocation (new hook-config transaction or an explicitly scoped `core/install.py` extension), with hash-bound owned blocks, parse-failure no-write behavior, and journal/rollback conflict semantics. Add the command and target fixtures to P4 before claiming installer lifecycle coverage.

### F5 — MEDIUM — The P4 build → smoke → installer command chain does not produce the package it later consumes

**Evidence.** P4 asks for persistent four-host on/off/plugin bundles, extraction/smoke, and installer preview (`phase-04-integration-and-personal-acceptance.md:39,41,47`). The listed build commands use `--check`, while the smoke command expects `EXTRACTED` and the installer command omits `--package` (`phase-04-integration-and-personal-acceptance.md:47`).

**Failure path.** `build-artifacts.py --check` builds both candidates in temporary trees and discards them after the context exits; only the non-check path writes `args.output/host` (`nckh-kit/scripts/build-artifacts.py:24-38`). `resource-smoke.py` requires an already extracted bundle with a manifest (`nckh-kit/scripts/resource-smoke.py:21-27,85-94`), while the installer defaults to `ROOT / "dist"` (`nckh-kit/installer/nckh-installer.py:37-40`) and then resolves/verifies that package (`nckh-kit/core/install.py:65-75`). Running the listed commands in order leaves no defined bundle at the installer’s default path.

**Narrow correction.** Add an explicit persistent build command for each on/off/plugin matrix, an owned extraction path/receipt, and pass `--package <bundle-root>` to installer preview (or define and verify `dist` as the output). Resolve `PATH`, `EXTRACTED`, and `STATE` to concrete per-run paths before the gate.

## Claim/caller verification summary

| Claim | Result | Evidence |
|---|---|---|
| Source r26, 243 pins, 37 identities, 9 resources | Supported as current read-only baseline | `plans/reports/review-261004-0047-current-kit.md`; current `build.py`/registry contracts |
| Installed r25, 43 current items, no conflict | Supported by the supplied doctor/current-kit report; not rerun | `plans/reports/review-261004-0047-current-kit.md` |
| Four adapters have no installed/verified hook coverage | Supported | `plans/reports/researcher-261004-0047-native-hook-capabilities.md`; `nckh-kit/tests/runtime/test_adapters.py:31-40` |
| P1/P2/P3 proposed CLIs/files exist today | Contradicted where marked future; plan itself marks them future | `phase-01-start.md:47`, `phase-02-scientific-visuals.md:45`, `phase-03-portable-hooks.md:46` |

## Unresolved questions

1. Are hooks intended to be shipped inside the four host bundles, or intentionally kept as a separate manual package? The current plan asserts both portable hooks and no packaging owner.
2. Which 37/148 checks are immutable historical evidence versus candidate checks that must become 39/156? The plan needs this classification before implementation.

Status: DONE_WITH_CONCERNS
Summary: Identified five concrete plan/source contract failures: lock-validation ordering, incomplete 37→39 propagation, un-packaged hooks, non-executable config rollback coverage, and a build/smoke/installer handoff gap. No product or plan files were modified.
Concerns/Blockers: The plan is reviewable, but the listed corrections are required before its implementation gates can execute end to end.
