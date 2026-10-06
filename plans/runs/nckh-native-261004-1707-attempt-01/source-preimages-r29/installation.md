# Offline build and owned installation

Run package commands from the `nckh-kit` directory. Entry wrappers forward to the
same Python engine: PowerShell (historical evidence path: `../installer/install.ps1`; unavailable in the cleaned checkout),
POSIX shell (historical evidence path: `../installer/install.sh`; unavailable in the cleaned checkout), engine (historical evidence path: `../installer/nckh-installer.py`; unavailable in the cleaned checkout).
They check Python 3.11+ and never download it.

## Build

```text
python scripts/build-artifacts.py --all --check
python scripts/build-artifacts.py --all --plugin --check
python scripts/build-artifacts.py --all --plugin --output dist
python evals/run-evals.py --run-deterministic --output evals/results/local-checks.json
```

The output must be absent or empty. A build uses sibling staging, validates the
complete closure and promotes it after verification. Prior candidates are
preserved. Source locks (historical evidence path: `../core/registry/source-lock/source-lock.json`; unavailable in the cleaned checkout) include
instructions, contracts, adapters, code, recipes and tests. Re-freezing increments
the revision and archives the previous lock; it requires source review.

Resource candidates use source-lock/bundle format 2 and the shared verifier.
Format 1 local-only artifacts retain their original contract. Data dependencies
come from the resource registry (historical evidence path: `../core/registry/catalog/resources.json`; unavailable in the cleaned checkout), with
exact upstream provenance, license/attribution and an actual standalone reader.
Unlisted data, copied-rights gaps, missing dependencies and private paths fail.

Use `--resource-access off` on the build command for a frozen same-base comparison.
The source lock, code and instruction policy remain the same; the resource closure
and its manifest hash differ. An off bundle contains no copied resource bytes.
The standalone lookup must receive the corresponding `--resource-access off`
treatment; it returns a disabled observation without reading resources.

After extracting a candidate outside the repository, verify actual reads with:

```text
python -I scripts/resource-smoke.py --bundle EXTRACTED --cwd OUTSIDE_REPO --unset-pythonpath --output RECEIPT
```

The harness uses absolute extracted-reader paths, `python -I`, a separate working
directory and no `PYTHONPATH`. A success records observed data/reader/output hashes;
it establishes portable reads, not runtime/native/human qualification. The three
installer consumers reuse this shared bundle verifier and tree hashes.

## Preview

```text
python installer/nckh-installer.py install --package EXTRACTED --runtime codex-cli --scope project --project PATH --kits core --mode copy --models balanced --dry-run
```

Select the actual surface, kits, project/global scope, copy/symlink and model
policy explicitly. The interactive wizard displays these choices and the exact
transaction. Add `--with-agents` to include optional native agent files. Python
tools do not infer account rights, inspect credentials or call trial models.

Confirm the reviewed transaction with `--yes`. This confirms the selected action;
conflicts, edited files, source drift and missing qualification still stop it.
`--replace-skill NAME` is an explicit reviewed replacement of that edited item;
`--keep-edited` keeps edited items and their baseline ownership hash. Duplicate
definitions and differing shared projections require resolution before commit.

## Update

```text
python installer/nckh-installer.py update --package EXTRACTED --runtime codex-cli --scope project --project PATH --kits core --mode copy --models balanced --candidate-evidence RECEIPT --dry-run
```

`install` cannot promote changed owned content. Changed `update` requires an
existing install plus candidate evidence (historical evidence path: `../installer/schemas/candidate-evidence.schema.json`; unavailable in the cleaned checkout)
bound to the candidate's source-lock and closure hashes, affected identities and
actual hash-bound check receipts. The declared evidence class needs a matching
typed receipt; static evidence cannot be labeled native or agent behavior.
Pending or fixture-only qualification is rejected.
Accepted static checks cover their stated scope only; they cannot establish native
or human qualification. Hashes establish integrity, not origin or scientific merit.

## Models

```text
python installer/nckh-installer.py config-models --runtime codex-cli --scope project --project PATH --models custom --capabilities CAPABILITIES --dry-run
```

This operation previews native agent files under the selected host's agent root.
It uses the same staging, backup, ownership and rollback engine. It does not edit
the parent's global/session model. Capability input uses `native_models.HOST`
with `as_of`, `evidence_reference`, `per_agent_override`, `allowed_models`, observed
`models` and a fast/worker/deep `mapping` containing exact `model` and `effort`.
Model IDs and effort must be eligible for their tier and host encoding. Custom
without an observed mapping fails. Cost optimization also requires measured cost
and an accepted quality floor.

Without a native mapping, standard profiles encode inheritance and report
`inherit-only; tier model mapping unavailable`. Configured and encoded fields stay
separate from applied/effective settings; only a native receipt can establish the
latter. Antigravity agent aliases are inherit/flash/pro; per-agent effort remains
unverified and is rejected when requested.

## Doctor, recovery and uninstall

```text
python installer/nckh-installer.py doctor --state-dir STATE
python installer/nckh-installer.py uninstall --state-dir STATE --install-id ID --dry-run
python installer/nckh-installer.py list-skills
```

Doctor is read-only. It checks owned tree hashes and local reference closure,
parses native TOML/generated frontmatter, reports configured fields, verifies
retained candidate provenance/receipt integrity and inspects duplicate visibility.
Receipt classes, input provenance and stated scopes remain separate from artifact
integrity; a missing or changed receipt makes its qualification unverified. Edited
YAML outside the generated subset remains unverified. Missing source bundles do
not imply that a current copied skill has stopped working; candidate integrity
and installed content are reported separately. Live host freshness, discovery,
hook enforcement and effective models remain unverified.

Kernel locks serialize physical targets and release when an
owned process exits, including a crash. Lock record files remain as diagnostics;
their presence is not an active lock. Legacy live/unknown owners are preserved.
Recovery rolls back an interrupted transaction; it does not resume staged writes.
Re-run the operation to reconcile its journal, then create and review a fresh preview.
Missing/changed backups and later edits remain in place with `rollback-conflict`
details. Restore the saved baseline or resolve the reported edit before retrying.

State/staging and all target roots must share a device. Select `--state-dir` on
that device when needed; the engine stops before mutation across devices.
Uninstall removes only unchanged owned files/directories and releases shared
owners. Edited residue, credentials, host roots and user plans are preserved.

Symlink mode requires a qualified host/OS and an immutable artifact that remains
available. Current qualification is unverified; use explicit copy for local
fixture checks. Windows fixture tests are not macOS/Linux or native host evidence.

## Portable hooks

Every new bundle carries a pinned per-host hook closure under `hooks/`, with its
local imports/contracts under `hooks/_shared/`. The manifest's typed `hooks`
record lists the exact runner, manual/config entrypoints, codec, template and
members. Hooks start `packaged-inactive`, with enabled/registered/trusted false.
Plugin export puts the same closure under `plugin/references/nckh-hooks/`; this
namespace is inactive and is not advertised as an auto-discovered hook component.
Legacy format 1/2 bundles without hook source pins remain readable.

The manual checker (historical evidence path: `../scripts/hook-preflight.py`; unavailable in the cleaned checkout) shares the synchronous neutral
policy (historical evidence path: `../core/hook_policy.py`; unavailable in the cleaned checkout). Its controller-selected context is a bounded
project-relative JSON file with task/operation mappings, existing grants,
brief/source references, and final artifact/QA bindings for delivery. Event
payloads cannot select context or supply authorization. It does not ingest
transcripts or raw prose; bounded artifact bytes are read only for integrity
hashes. It executes no payload command and uses no network/provider/model.
Declared factual slots are checked separately from semantic fidelity. Its exit
status is nonzero for block/pending/manual; it does not generate an artifact.

```text
python -I EXTRACTED/hooks/hook-preflight.py --project PROJECT --context CONTEXT < EVENT.json
python -I EXTRACTED/hooks/configure-hooks.py preview --project PROJECT --host codex --package EXTRACTED --events PreToolUse --context CONTEXT --output PREVIEW.json
```

`EVENT.json` uses the neutral event contract (historical evidence path: `../core/contracts/hook-event.schema.json`; unavailable in the cleaned checkout).
Preview is read-only for config/runtime; an explicit output stores a private
transaction with target/preimage/parent/interpreter/context/payload hashes and
owned definition IDs/locators. Exact project targets are Claude
`.claude/settings.local.json`, Codex `.codex/hooks.json`, Cursor
`.cursor/hooks.json`, and AGY `.agents/hooks.json`. Each host keeps its own native
JSON shape; unowned definitions and shared skills/agents are preserved.
CLI stdout shows a summary and preview hash; full prior config values stay in
the explicitly saved private preview. To prepare activation, preview additionally
selects `--surface` and `--host-version`; unknown values cannot activate a route.

Activation requires a separately approved preview hash, human grant and actual
native failure-path evidence bound to the selected event/version/surface/payload:

```text
python -I EXTRACTED/hooks/configure-hooks.py apply --project PROJECT --host codex --package EXTRACTED --preview-file PREVIEW.json --approved-hash HASH --grant-reference GRANT --native-evidence EVIDENCE.json
python -I EXTRACTED/hooks/configure-hooks.py preview --action remove --project PROJECT --host codex --package EXTRACTED --context CONTEXT --output REMOVE.json
python -I EXTRACTED/hooks/configure-hooks.py remove --project PROJECT --host codex --package EXTRACTED --preview-file REMOVE.json --approved-hash HASH
```

Evidence must retain eight observed paths per selected event: allow, policy deny,
malformed input/output, timeout, crash, unsupported route and duplicate invocation.
Hashes check integrity and cannot authenticate a fabricated observation or grant.
Native trust remains controlled by the host/user. Payloads stage into
`.nckh-state/hooks/<host>/<closure-hash>/`, before config writes; skill installation
and hook activation are separate transactions. Missing evidence, invalid or
duplicate JSON, changed-after-preview bytes and edited owned definitions stop.

Private transaction journals and raw config/ownership preimages are retained
under `.nckh-state/hooks/transactions/`. Interrupted transactions block new previews.
After reviewing the interrupted journal and its current canonical record hash:

```text
python -I EXTRACTED/hooks/configure-hooks.py recover --project PROJECT --host codex --transaction .nckh-state/hooks/transactions/JOURNAL.json --approved-hash JOURNAL_HASH
```

Recovery restores only matching before/after bytes. Later edits and changed
backups remain conflicts; no whole-file restoration overwrites unknown edits.
Remove deletes only matching owned definitions/files, and retains payloads still
referenced by any known host config. Event receipts suppress repeated successful
checks and one stop reminder per session/task/artifact/violation; failed attempts
remain separate. Stop codecs never request another model turn. Unknown tools and
unqualified native surfaces retain manual/unverified coverage; no native
preventive-enforcement claim follows from these local checks.

