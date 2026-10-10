# Offline build and owned installation

Run package commands from the `nckh-kit` directory. Entry wrappers forward to the
same Python engine: [PowerShell](../installer/install.ps1),
[POSIX shell](../installer/install.sh), [engine](../installer/nckh-installer.py).
They check Python 3.11+ and never download it.

Without arguments, either wrapper prints usage and examples and exits 2 before
any installation. Python selection probes both version and executable readability
(hook configuration hashes the selected interpreter). Windows Store execution
aliases that cannot be read are skipped; `NCKH_PYTHON` selects an explicit usable
interpreter. The selected executable is reported on stderr; engine JSON and exit
status remain intact.

`--package` is optional. The engine first looks for a manifest in `nckh-kit/dist`,
then in the repository's `packages` directory, including host subdirectories.
An explicit `--package` takes precedence; absent manifests produce an error listing
the searched paths. Build and verification still check the selected bundle hashes.

## Build

```text
python scripts/build-artifacts.py --all --check
python scripts/build-artifacts.py --all --plugin --check
python scripts/build-artifacts.py --all --plugin --output dist
python evals/run-evals.py --run-deterministic --output evals/results/local-checks.json
```

The output must be absent or empty. A build uses sibling staging, validates the
complete closure and promotes it after verification. Prior candidates are
preserved. [Source locks](../core/registry/source-lock/source-lock.json) include
instructions, contracts, adapters, code, recipes and tests. Re-freezing increments
the revision and archives the previous lock; it requires source review.

Resource candidates use source-lock/bundle format 2 and the shared verifier.
Format 1 local-only artifacts retain their original contract. Data dependencies
come from the [resource registry](../core/registry/catalog/resources.json), with
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
existing install plus [candidate evidence](../installer/schemas/candidate-evidence.schema.json)
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

Visibility includes the destination, compatibility/global roots on each ancestor,
and, for project installs, nested projects up to eight directory levels. Project
scans prune `.git`, `node_modules`, `.venv`, `venv`, `site-packages`, `__pycache__`,
`dist`, `build`, `.tox`, `AppData`, symlinks and Windows junctions/reparse points.
Definitions inside those excluded trees are outside the nested-project scan.
Global installs inspect destinations and ancestors only; a project below home
does not block a global install. A project install also probes the home-level
roots of the selected home (`--home`, default the real home), even when the
project is outside that home. Native deduplication remains unverified.

### Lối thoát khi trùng visibility

Lỗi `duplicate visibility` liệt kê từng bản trùng trong `sources`, mỗi đường dẫn
kèm nguồn: `destination` (thư mục cài đặt của transaction này), `nested` (gốc
skill khác bên trong project, kể cả gốc tương thích ngay tại project; với
`--scope global` là các gốc skill khác ngay dưới home, cạnh thư mục cài đặt),
`global` (gốc ngay dưới thư mục home khi cài theo project, kể cả khi project nằm
ngoài home) hoặc `ancestor` (gốc trên một thư mục cha của nơi cài đặt). Home là
giá trị `--home`, mặc định là home thật của người dùng. Cách xử lý mặc định là xóa
hoặc đổi tên bản không phải `destination` rồi chạy lại `--dry-run`.

Vì vậy, khi máy đã có bản cài global cùng tên skill, cài theo project ở bất kỳ đâu,
kể cả ngoài home (ví dụ ổ khác), sẽ dừng với `duplicate visibility` loại `global`.
Hãy xóa bản global hoặc chấp nhận bằng cờ ở đoạn dưới. Bản cài cũ có transaction
chưa ghi home vẫn chỉ quét theo cách trước đây; `doctor` chưa thấy bản trùng ở
home cho tới khi chạy `update`. Nếu đường dẫn home có thành phần là link (symlink,
junction), installer không ghi home, dùng cách quét cũ theo home thật và in cảnh
báo nêu thành phần đó; truyền `--home` bằng đường dẫn không chứa link để quét các
gốc global của home (xem `_scan_home` trong `core/install.py`).

Nếu bản trùng thuộc người dùng và chỉ nằm ở `ancestor`/`global`, có thể chấp nhận
bằng `--acknowledge-ancestor-visibility`. Cờ này không bao giờ bỏ qua trùng
`nested` hay hai `destination` cùng hiển thị; `--yes` cũng không vượt qua bất kỳ
conflict nào. Transaction ghi các mục đã chấp nhận vào `acknowledged_visibility`,
bản ghi ownership giữ lại trường này và `doctor` hiển thị nó cùng
`visibility_conflicts` hiện tại. `update` chỉ mang chấp nhận cũ sang khi bản ghi
ownership có đúng cùng skill, surface và đường dẫn nguồn; bản trùng mới hoặc đã đổi
cần truyền lại cờ. Host vẫn thấy cả hai bản; thứ tự ưu tiên giữa
chúng chưa được kiểm chứng.

Lỗi hợp đồng đối số được báo trước khi quét filesystem: `--scope global` cùng
`--hooks advisory` (mặc định) dừng ngay với `automatic hooks require project scope`,
nên hãy thêm `--hooks off` cho cài đặt global.

After an owned uninstall, empty skill/agent roots are removed. A released root
lock is removed only when it is the parent's sole remaining entry; user files
and locks beside retained content are preserved. Cleanup holds the shared
installer coordination lock after closing root locks.
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

Project `install` and `update` default to `--hooks advisory`. Their dry-run shows
the per-host hook config targets and events; confirming installation also registers
the owned advisory callbacks. Add `--hooks off` to skip hook configuration.
Global skill installation requires `--hooks off` because hook context and ownership
are project-specific. Existing enforcement definitions are never automatically
downgraded, and changed owned payloads require explicit removal of their old version.

Advisory callbacks preserve actual policy/failure diagnostics while emitting no
deny or prompt block. Cursor uses `failClosed=false` in this mode. Missing context
is reported as unavailable, never as a passed check. Host trust and native
qualification stay separate. Skill uninstall does not remove independently owned
hook configuration; use the hook removal transaction documented below.

The installed hooks also carry two advisory nudges: a routing hint on prompt
events and an EOL/BOM guard around write tools. They only add context, never block
or invoke a skill, and run even without controller context; snapshots live under
`.nckh-state/hooks/snapshots/` and are deleted after the post-tool comparison.
Host coverage, measured hint coverage and limits are in
[runtime support](runtime-support.md#advisory-nudge-hooks). Global installs have
no hooks and therefore no nudges.

In enforce mode, missing or invalid context fails closed only on events the host
can gate: `PreToolUse`/`preToolUse` and `UserPromptSubmit`/`beforeSubmitPrompt`.
`SessionStart`, `PostToolUse`, `Stop`, `PreInvocation` and `PostInvocation` return
advisory context with exit 0.

Every new bundle carries a pinned per-host hook closure under `hooks/`, with its
local imports/contracts under `hooks/_shared/`. The manifest's typed `hooks`
record lists the exact runner, manual/config entrypoints, codec, template and
members. Bundles start `packaged-inactive`, with enabled/registered/trusted false;
their `install_default: advisory` declares the project installer's activation policy.
Plugin export puts the same closure under `plugin/references/nckh-hooks/`; this
namespace is inactive and is not advertised as an auto-discovered hook component.
Legacy format 1/2 bundles without hook source pins remain readable.

The [manual checker](../scripts/hook-preflight.py) shares the synchronous neutral
[policy](../core/hook_policy.py). Its controller-selected context is a bounded
project-relative JSON file with task/operation mappings, existing grants,
brief/source references, and final artifact/QA bindings for delivery. Event
payloads cannot select context or supply authorization. It does not ingest
transcripts or raw prose; bounded artifact bytes are read only for integrity
hashes. It executes no payload command and uses no network/provider/model.
Declared factual slots are checked separately from semantic fidelity. Its exit
status is nonzero for block/pending/manual; it does not generate an artifact.

Mapped shell execution tools (`Bash`, `PowerShell`, `Shell`, `exec_command`,
`shell_command`, `run_command`) return `pending/shell-targets-unverifiable` before
execution. A command's full target/side-effect coverage cannot be established by
the ordinary `path` or `file_path` aliases. The policy does not parse or execute
arbitrary shell code, and an existing operation grant cannot turn unknown command
targets into verified paths. Native pre-tool codecs deny pending; unmapped routes
retain manual/unverified status. Plan-only mutation checks remain effective.
Use qualified direct file/patch routes for path-aware actions; shell permissions
and any manual execution remain separate from NCKH preventive qualification.

```text
python -I EXTRACTED/hooks/hook-preflight.py --project PROJECT --context CONTEXT < EVENT.json
python -I EXTRACTED/hooks/configure-hooks.py preview --project PROJECT --host codex --package EXTRACTED --events PreToolUse --context CONTEXT --output PREVIEW.json
```

`EVENT.json` uses the [neutral event contract](../core/contracts/hook-event.schema.json).
Preview is read-only for config/runtime; an explicit output stores a private
transaction with target/preimage/parent/interpreter/context/payload hashes and
owned definition IDs/locators. Exact project targets are Claude
`.claude/settings.local.json`, Codex `.codex/hooks.json`, Cursor
`.cursor/hooks.json`, and AGY `.agents/hooks.json`. Each host keeps its own native
JSON shape; unowned definitions and shared skills/agents are preserved.
Claude command hooks use the executable plus an argument array. Controller paths
are passed directly without shell interpolation, including on Windows with Git
Bash installed. Native qualification still binds the selected host version.
Cursor `preToolUse` uses a bounded 20-second timeout with `failClosed=true`.
Other selected handlers use a five-second timeout. A timing bound does not
qualify an event; activation still requires its native failure-path evidence.
CLI stdout shows a summary and preview hash; full prior config values stay in
the explicitly saved private preview. To prepare activation, preview additionally
selects `--surface` and `--host-version`; unknown values cannot activate a route.

Manual advisory activation uses `preview --mode advisory` and a confirmed apply
with a human grant. It does not require or establish native preventive evidence.
Enforcement remains the manual configurator's default; its activation requires a
separately approved preview hash, human grant and actual native failure-path
evidence bound to the selected event/version/surface/payload:

```text
python -I EXTRACTED/hooks/configure-hooks.py apply --project PROJECT --host codex --package EXTRACTED --preview-file PREVIEW.json --approved-hash HASH --grant-reference GRANT --native-evidence EVIDENCE.json
python -I EXTRACTED/hooks/configure-hooks.py preview --action remove --project PROJECT --host codex --package EXTRACTED --context CONTEXT --output REMOVE.json
python -I EXTRACTED/hooks/configure-hooks.py remove --project PROJECT --host codex --package EXTRACTED --preview-file REMOVE.json --approved-hash HASH
```

AGY `PreToolUse` always requires a `decision`. Non-blocking policy returns `ask`
to retain native permission checks and respect the host's Always Allow setting;
`block` and `pending` return `deny`. The codec does not grant permission with
`allow` or emit `permissionOverrides`.

AGY file and search tools use their documented native path fields: `TargetFile`
for writes/edits, `AbsolutePath` for file reads, `DirectoryPath` for directory
listing, `SearchDirectory` for name searches, and `SearchPath` for text searches.
The codec sends these paths through the same project containment and protected
path checks as legacy `file_path`/`path` fields. Required native targets must be
present and every supplied recognized path must be a nonempty string; supplying
a second alias cannot hide a protected target. These are local codec contracts;
native prevention still requires evidence for the selected tool/version/surface.
See [AGY tool arguments](https://antigravity.google/docs/hooks/#supported-tools).

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
remain separate. Missing-context receipts (`degraded-no-context`, in advisory and
enforce mode alike) are kept once per session and nudge, under names
`no-context-<64hex>.json`. Only files of that shape count toward a fixed cap; the
first hit writes a `cap-reached-no-context.json` marker and later missing-context
receipts are dropped. Checked (`checked-unreviewed`) and failed (`degraded-failed`)
receipts are never capped. A nudge the host wire did not carry (Cursor
`beforeSubmitPrompt`, an enforce block on `UserPromptSubmit`, an AGY EOL/BOM
finding) is recorded with `delivered: false`. The owner is `record_once` and
`_nudge_record` in `hooks/runner.py`. Stop codecs never request another model turn. Unknown tools and
unqualified native surfaces retain manual/unverified coverage; no native
preventive-enforcement claim follows from these local checks.

