# Project installer and native route scout

Date: 2026-10-03, Asia/Saigon. Workspace: `C:/Users/USER/Downloads/test-skill`.

Authorization reference: controller `/root` → `/root/technical_review`, current phase-4 read-only delegation. Owned output is this report only. Source/config/install changes, model/provider dispatch, external messages and global changes were outside this scout. The model was requested as inherited; configured/applied/effective model/effort and usage telemetry are unknown. No nested agent was created.

## Verified entrypoint and installed identity

There is no `scripts/install-kit.py` or repository README at the requested locations. The owning navigation is [docs/index.md](../../nckh-kit/docs/index.md) → [installation.md](../../nckh-kit/docs/installation.md). The exact Python entrypoint is [installer/nckh-installer.py](../../nckh-kit/installer/nckh-installer.py), wrapped by `installer/install.ps1` and `installer/install.sh`.

`installer/nckh-installer.py:39` exposes six operations: `install`, `update`, `doctor`, `config-models`, `list-skills`, `uninstall`. It has no public `rollback` operation.

Current `.nckh-state/ownership.json` contains one install:

| Field | Actual value |
|---|---|
| Install ID | `d5811d724fe29cb5016c7c3a` |
| Scope/surface | `project` / `codex-desktop` |
| Kits/mode | `core engineer marketing` / `copy` |
| Targets | `.agents/skills` and `.codex/agents` |
| Native agents | `with_agents: true` |
| Installed content | 37 skill folders + 6 native agent files |
| Source/closure | Historical r14 source lock `2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03`; closure `3715cf7f083aac9f8d458a3cabd8018ba33c4e3e039c388ed41c8ec9da187a5a` |

`core/install.py:80`–`82` derives the ID from the selected surface list, resolved skill roots and scope. A new package, model policy or kit selection does not supply an arbitrary ID. Keep `--runtime codex-desktop`, the exact project and project scope to preserve the existing identity. Adding `agy-ide` or changing to `codex-cli` changes the identity; `--install-id` is read for uninstall and does not force an update to use an existing ID.

`nckh-installer.py:97`–`99` inherits `with_agents` from the existing install during update when the flag is omitted. The current update therefore retains the six agents.

## Read-only checks actually run

Commands ran from `C:/Users/USER/Downloads/test-skill/nckh-kit` with `PYTHONDONTWRITEBYTECODE=1`.

### Existing Codex identity

```powershell
python installer/nckh-installer.py update --package dist --runtime codex-desktop --scope project --project 'C:/Users/USER/Downloads/test-skill' --kits core engineer marketing --mode copy --models balanced --dry-run
```

Actual preview, summarized without changing the transaction:

```json
{
  "status": "preview",
  "install_id": "d5811d724fe29cb5016c7c3a",
  "surfaces": ["codex-desktop"],
  "with_agents": true,
  "actions": {"unchanged": 43, "create": 0, "replace": 0, "conflict": 0, "keep-edited": 0},
  "native_models": ["inherit"]
}
```

The harness session `67685` completed, exit 0. This checks the preserved `dist` subject and identity; it is not an update to the new personal-use source.

### Cursor duplicate-definition guard

```powershell
python installer/nckh-installer.py install --package dist-resource-quality-r22/on --runtime cursor-ide --scope project --project 'C:/Users/USER/Downloads/test-skill' --kits core engineer marketing --mode copy --models balanced --dry-run
```

Actual result was blocked with `duplicate visibility`, including:

```text
surface: cursor-ide
skill: nckh-cook
physical_paths:
  C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-cook
  C:/Users/USER\Downloads\test-skill\.cursor\skills\nckh-cook
reason: duplicate visible definitions; no native dedup proof
```

The harness session `5170` completed with wrapper exit 1; the installer emitted a blocked JSON result. The engine's error branch returns 4 (`nckh-installer.py:120`–`122`); the tool wrapper result is retained separately here. No Cursor root was created. At the end of this scout `.cursor/skills` and `.agents/agents` did not exist, and the ownership SHA-256 remained unchanged.

## Exact Codex update route for the new candidate

The new built package root and typed candidate receipt do not exist in the inspected phase-4 inputs yet. The source currently retains `dist`, `dist-resource-quality-r22`, `dist-runner` and `dist-runner-cleanup`; none is invented as the new subject. Assign the controller's actual reviewed paths to the two variables below. All remaining arguments are concrete and preserve the current ownership route.

```powershell
$project = 'C:/Users/USER/Downloads/test-skill'
$candidatePackage = '<absolute newly built package root containing codex/manifest.json>'
$candidateEvidence = '<absolute current candidate-evidence JSON path>'

python installer/nckh-installer.py update --package $candidatePackage --runtime codex-desktop --scope project --project $project --state-dir 'C:/Users/USER/Downloads/test-skill/.nckh-state' --kits core engineer marketing --mode copy --models balanced --candidate-evidence $candidateEvidence --dry-run
```

After the controller has checked that preview against its existing grant, the corresponding authorized commit is the same command with `--yes` replacing `--dry-run`:

```powershell
python installer/nckh-installer.py update --package $candidatePackage --runtime codex-desktop --scope project --project $project --state-dir 'C:/Users/USER/Downloads/test-skill/.nckh-state' --kits core engineer marketing --mode copy --models balanced --candidate-evidence $candidateEvidence --yes
```

Use `update`, because `install` rejects replacement of changed owned content. No `--replace-skill` or `--keep-edited` is justified by the unchanged baseline check. If the actual new preview reports an edit, preserve it and resolve the concrete item under the existing scope; `--yes` is not an overwrite bypass.

Candidate evidence is enforced by `core/install.py:300`–`332`:

- `qualification` must be `accepted-for-scope`; fixture-only or pending qualification is rejected.
- Candidate source-lock/closure hashes must match each host manifest.
- Affected identities must cover all `create`/`replace` items, including native agents if changed.
- Receipt paths must be absolute, with matching byte hashes and typed pass receipts.
- Receipt source/closure maps and affected identities must match; evidence class cannot be escalated from static checks to native evidence.

Accepted static/deterministic receipts can authorize the stated package check scope. They do not create owner, native or scientific acceptance.

## Neutral root and Cursor route requirements

| Surface | Declared project destination | Existing route consequence |
|---|---|---|
| Codex desktop | `.agents/skills`; agents `.codex/agents` | Existing owned route; update it first while preserving the ID. |
| Antigravity IDE | `.agents/skills`; optional agents `.agents/agents` | Same physical skill root as Codex. A second ownership record needs actual neutral consumer evidence and identical projections. |
| Cursor IDE | `.cursor/skills`; optional agents `.cursor/agents` | Compatibility roots also include `.agents/skills`, `.claude/skills` and `.codex/skills`. The separate copy is currently blocked by the observed duplicate visibility. |

For co-ownership of `.agents/skills`, `core/install.py:164`–`171` requires:

```json
{"qualified_neutral_consumers": ["codex-desktop", "agy-ide"]}
```

This is the mechanical capability field, not a grant or a runtime receipt. Supply it only after the controller observes those actual consumers reading the same approved neutral subject. Same bytes or adapter documentation do not prove native consumption/deduplication. Different hashes with other owners are rejected at `:165`–`167`, and replacement with other owners is rejected at `:191`–`192`; do not create Antigravity co-ownership before the Codex content update settles.

The declaration above does **not** bypass Cursor's two-physical-root conflict. `visibility_conflicts()` (`core/install.py:85`–`121`) compares canonical paths across parent/nested/compatibility roots and returns a conflict whenever more than one physical definition is visible; `plan_install()` rejects that result. There is no qualified-neutral flag branch in this duplicate-path check.

For the requested Cursor run in the current project, the controller can first inspect whether the actual selected Cursor UI consumes the existing single `.agents/skills` definitions. This route is suggested by Cursor's declared compatibility roots, but it is not runtime-proven in this scout. If consumed, record the actual path/discovery/run evidence and keep the single physical definitions; do not claim a `.cursor/skills` install occurred. If the host does not consume them, preserve the blocked route and resolve the setup before claiming the required run. The earlier scout's generic Cursor install preview is now narrowed by this live guard result.

Cursor must remain **Grok 4.7 Extra High only**, with no fallback. Antigravity must remain **Gemini 3.8 Flash High**. Reobserve project/model before each dispatch. `--models balanced` configures kit agent policy; it does not select either IDE's current main-agent model. Existing standard native agent policy encodes inheritance without observed tier mappings. `core/native.py:33` rejects arbitrary Antigravity IDs or per-agent effort; its allowed aliases are `inherit`, `flash`, `pro`. Those aliases cannot establish the main-agent UI model or effective High effort.

## Current application model inventory

The inspected [native-model matrix](../evaluation/personal-use/native-model-matrix.json) declares nine choices:

```text
gpt-6.1-sol
gpt-6-astra
gpt-6-sol
gpt-6-luna
gpt-5.6-sol
gpt-5.6-terra
gpt-5.6-luna
gpt-5.5
gpt-reserve
```

All nine remain `not-run` with `observed_effective: null` in this snapshot. The matrix explicitly labels the inventory `native-tool-documented-selection-enum`; it is not an observed available-model response.

[Catalogue attempt 1](../evaluation/personal-use/native-model-catalogue-attempt-01.json) and [attempt 2](../evaluation/personal-use/native-model-catalogue-attempt-02.json) both record `status: unavailable`, `models: []`, `error: proxy exited before response`. Their owned proxy PIDs were closed and the existing daemon preserved. No standalone native model-enumeration tool was present in the current enabled tool-name metadata check.

Consequently:

- The recorded daemon enumeration **route** is not callable from those attempts.
- No specific one of the nine model IDs is established as dispatchable or established as rejected by this scout.
- Keep the nine as documented candidates until each permitted actual dispatch/output proves availability or produces an actual rejection. Do not label all nine callable, invent an unavailable subset, or claim coverage of hidden/chatgpt.com models.
- A successful creation request, a selected UI label or a model self-report still does not establish effective model telemetry.

No model/provider dispatch was performed by this scout. The earlier runtime report's CLI authentication and UI label observations remain historical observations; this scout did not log in, inspect tokens or replace the required IDE route with another CLI/model.

## Rollback and owned process route

Commit preflight (`core/install.py:554`–`569`) re-verifies bundles, target roots, ownership hash and the complete preview under kernel locks before writes. State/staging and exact target roots must share a device (`:364`–`371`). Backups and `index_before` are stored under `.nckh-state/transactions/<transaction-id>` and `.nckh-state/journal.json`.

- A commit error triggers `rollback()` automatically (`:638`–`640`).
- An interrupted journal is recovered by the next authorized commit entry: `recover_outstanding()` rolls it back, then raises to require a fresh preview (`:474`–`480`). A read-only dry-run does not perform recovery writes.
- A completed transaction has no public CLI rollback operation. For an explicitly authorized reversal, the controller can use `core.install.rollback(state_dir, journal, allowed_roots=...)` under `target_lock`, with the exact Codex roots `.agents/skills` and `.codex/agents`, after confirming the journal is the intended transaction.
- `rollback()` restores only current targets that still match the transaction's `after_hash` and backups matching `before_hash`. Later edits or changed/missing backups are retained as `rollback-conflict`; it never resets those edits to make rollback appear successful.
- `uninstall` is a separate operation, not an update rollback. It removes only unchanged singly owned items, preserves edited residue and releases shared owners.

For native commands, the actual process owner is `core/processes.py:111`–`129`/`:163`–`178`: Windows starts a suspended child, assigns it to a kill-on-close Job Object before resume, and closes only its owned group. It records PID, exit, duration and cleanup. POSIX uses an owned process group. Timeout preserves `timeout-unknown`; exit 0 is `completed-unreviewed`, not a task verdict. Do not use this route to terminate existing IDE/daemon processes owned by the user. Both reviewer dry-run harness sessions completed; no reviewer background process remains.

## Snapshot hashes

These hashes bind the source/state used by this scout; they are not behavior or quality certificates.

| Path relative to workspace | SHA-256 |
|---|---|
| `nckh-kit/core/install.py` | `7aeae862234362235f4b21f89679f9ff82a3bfbe23dec9984005b68e3db8e7b2` |
| `nckh-kit/core/processes.py` | `b545ac0e5ca01ecda7cead4656b0edf0ddef04cfbcd9a93ad7b9eb10a7f1cebd` |
| `nckh-kit/installer/nckh-installer.py` | `ee3684d7712bc64ec37c1017c2a91f1cb93b09aa4e97844a102de351a15debf4` |
| `nckh-kit/adapters/codex/adapter.json` | `1f3981be7bd2d917ce0321e0dd45325da15398a53e7fc2c9c00404fc70d2082c` |
| `nckh-kit/adapters/cursor/adapter.json` | `9a0a9859a7120f3a67895381c5cb60fc90aa11d6291651e11cc5cf6aca536d78` |
| `nckh-kit/adapters/agy/adapter.json` | `1b55b91c222445e914b158c11e93762ae4e1c732c1bf3f1f8034abbe76f558db` |
| `.nckh-state/ownership.json` | `da9dedca9668f657eb7fb053e2ad44ecf34a12f086eaeb52077d14ddaf543acf` |
| `plans/evaluation/personal-use/native-model-matrix.json` | `6d7cbe6b270246bd613179309f16831338af61523da798976e361ff48dfdf616` |

Unresolved inputs: controller's actual new bundle/evidence paths; observed neutral-root consumption for the selected hosts; actual dispatch outcomes for current-app model candidates. These are phase-4 work, not new external reviewer/holdout requirements.

Status: DONE_WITH_CONCERNS
Summary: Exact installer/update identity, candidate/ownership/rollback/process guards and model inventory limits are located. Read-only checks preserve the Codex ID and confirm that a separate Cursor copy is presently blocked by duplicate visibility.
Concerns/Blockers: standard Cursor physical install route is blocked in the current project; neutral-root consumption is not observed here; nine documented model choices are not yet dispatch-confirmed in the inspected matrix.
