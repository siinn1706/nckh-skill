# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A portable skill kit ("NCKH"): 43 `nckh-*` skills (core 16, engineer 13, marketing 13, xia 1) plus six optional agents, packaged for four agent hosts (Claude Code, Codex, Cursor, Antigravity/`agy`). Skill instructions are English; user-facing docs (`README.md`, `docs/`) are Vietnamese. Python 3.11+, standard library only — no third-party deps, no pytest.

Current source lock and packages identify experimental **r46**. The owner authorized GitHub sharing and replacement/cleanup of superseded installed skills on 10 October 2026. Stable qualification remains NO-GO; `nckh-kit/docs/release-checklist.md` retains historical pending gates. Never mark them passed, delete matrix cells, or shrink approved scope to make a check green.

## Layout and data flow

```
nckh-kit/            source of truth
  skills/{core,engineer,marketing,tooling}/nckh-*/SKILL.md (+ references/)
  agents/            six optional agent roles
  core/              library: build, install, hooks, guards, resources, schema, paths…
    registry/catalog/{skills,resources}.json   skill identity/deps; resource provenance/consumers
    registry/source-lock/source-lock.json      sha256 + rights pin for every source file
    contracts/ profiles/ policies/ workflows/  schemas and shared profile/resource data
  adapters/<host>/adapter.json                 per-host projection (surfaces, global/project roots)
  hooks/             portable hook runner + codecs/templates
  installer/         nckh-installer.py (engine), install.ps1 / install.sh wrappers
  scripts/           build-artifacts, freeze-source-lock, search-resource, configure-hooks…
  evals/             cases, protocols, rubrics, run-evals.py
  tests/             unittest suites (run with nckh-kit as top-level)
packages/<host>/     built, hash-verified distribution bundles (manifest.json, source-lock.json, skills/, hooks/, plugin/)
scripts/             repo-level: verify-public-package.py, install-global-kits.py, audit-publication.py
resources/           upstream reference snapshots (not dependencies; keep their licenses)
plans/               plans, reports, journals, run evidence (stateful records, not product docs)
```

Pipeline: edit `nckh-kit/` source → freeze source lock → `build-artifacts.py` produces per-host bundles → `packages/` holds the published output → installer copies a verified package into a host's project/global skill roots and records ownership in `.nckh-state/`.

Key invariants enforced in `core/build.py`:
- `verify_source_lock` fails if any source file is added/removed/changed without re-freezing ("source lock inventory changed" / "source drift"). Any edit under `nckh-kit/` therefore requires `python nckh-kit/scripts/freeze-source-lock.py --write`, which needs owner review — don't freeze silently.
- `_shared/core/...` files inside each packaged skill's `references/` are copies of `nckh-kit/core/` produced by the build; don't hand-edit files under `packages/` — rebuild.
- Bundles carry `resource_access`; distributed packages must be `on`. `off` exists only for same-base comparison.

## Commands

All from the repo root unless noted.

```sh
# Full deterministic test suite (must run with nckh-kit/ as cwd; tests import `core` and `tests._lab`)
cd nckh-kit && python -B -m unittest discover -s tests -t . -p "test_*.py"

# Single module / single test
cd nckh-kit && python -B -m unittest tests.hooks.test_config
cd nckh-kit && python -B -m unittest tests.hooks.test_config.HookConfigTests.<test_name>

# Same suite via the eval harness, writing a receipt
python nckh-kit/evals/run-evals.py --run-deterministic [--output RECEIPT.json]
python nckh-kit/evals/run-evals.py --validate-only

# Build: reproducibility check, or real output (output dir must be absent or empty)
python nckh-kit/scripts/build-artifacts.py --all --plugin --resource-access on --check
python nckh-kit/scripts/build-artifacts.py --all --plugin --resource-access on --output dist

# Verify the four published packages against the source lock
python scripts/verify-public-package.py

# Installer (always --dry-run first, then --yes)
python nckh-kit/installer/nckh-installer.py list-skills
python nckh-kit/installer/nckh-installer.py install --package packages --runtime claude-code --scope project --project PATH --kits core engineer marketing --mode copy --models balanced --with-agents --hooks advisory --dry-run
python nckh-kit/installer/nckh-installer.py doctor --state-dir PATH/.nckh-state
```

Runtimes: `claude-code`, `codex-desktop|cli|ide`, `cursor-ide|cli`, `agy-ide|cli`. Global scope requires `--hooks off`.

Tests create scratch trees via `tests/_lab.py:lab_root()`, which refuses roots whose ancestors already contain visible `nckh-*` skills. If that error fires, set `NCKH_TEST_ROOT` to a writable directory outside those ancestors.

## Repo-specific rules

- Read `docs/repository-maintenance.md` before deleting/moving files. Don't remove `.nckh-state/` (install ownership/rollback), active run dirs under `plans/runs/`, or the `plans/261006-2210-r41-*` test plans that other agents are using. `github-publication/` is a gitignored compatibility path kept during testing.
- Never invoke models or providers in tests/evals; `run-evals.py --run-agent` requires an approved plan hash and explicit authority.
- Installer `--yes` never overrides ownership conflicts, modified files, or "duplicate visibility" — resolve the cause, don't wipe state.
- Look up skill IDs, resources, and pinned revisions in the registry/lock JSON rather than copying them into docs.
