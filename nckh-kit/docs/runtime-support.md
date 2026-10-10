# Runtime projection and evidence

All native qualification cells remain **unverified**. The
[invocation matrix](../evals/cases/runtime/invocation-matrix.json) retains 224 cells
for eight surfaces, entrypoints, modes and invocation forms.
The separate [writer matrix](../evals/cases/runtime/writer-invocation-matrix.json)
adds 256 planned native cells and 20 supplemental scenarios. These do not change
the historical matrix or create an observed invocation receipt.

| Surface | Project skills | Global skills | Native agents |
|---|---|---|---|
| Claude Code | `.claude/skills` | `.claude/skills` | `.claude/agents/*.md` |
| Codex desktop / CLI / IDE | `.agents/skills` | `.agents/skills` | `.codex/agents/*.toml` |
| Cursor IDE / Agent CLI | `.cursor/skills` | `.cursor/skills` | `.cursor/agents/*.md` |
| Antigravity CLI | `.agents/skills` | `.gemini/antigravity-cli/skills` | `.agents/agents/*.md`; global `.gemini/config/agents` |
| Antigravity IDE | `.agents/skills` | `.gemini/config/skills` | `.agents/agents/*.md`; global `.gemini/config/agents` |

Global paths are relative to the selected home; project paths are relative to the
selected project. Cursor compatibility and nested roots can expose definitions
from other directories. Same bytes do not establish native deduplication or
precedence. The installer checks visibility and physical ownership before writes.

Native agent templates inline their required policies and preserve parent
permissions. Codex omits model/effort for inheritance; Claude has separate fields;
Cursor encodes effort in the model parameter string. Antigravity uses documented
aliases and does not assume per-agent effort support. These are encodings, not
receipts of host consumption. No automatic hook trust or permission bypass is used.

The per-host hook closure is packaged inactive for all four hosts. Project
activation/configuration is separate from skill installation; see
[portable hooks](installation.md#portable-hooks). Each codec follows its host's
documented event/response shape. Codex hosted tools and `write_stdin` have
coverage exceptions; AGY crash/timeout/exit behavior remains unverified. Native
surface/version/event qualification is still required before enabling a route.

Codex `apply_patch` hooks carry patch text in `tool_input.command`. The codec
reads bounded canonical patch headers for add, update, delete and move paths;
both the source and destination of a move pass through the same containment and
protected-path policy. It rejects missing, malformed or unsupported patch
envelopes and does not execute patch text or export its content in public
receipts. Shell commands still lack structured file targets; this patch reader
does not establish shell protected-path coverage.

Native test operators must verify project trust before and after a CLI run.
An invocation-only hook-trust bypass does not establish that workspace trust
will remain unchanged: a scoped dangerous Codex CLI run was observed to persist
its own project trust. Package configuration does not grant that authority;
native permission/trust behavior and project cleanup require separate evidence.

Optional plugin export uses the same generated skills. Claude and Cursor use
their manifest directories; Codex uses a portable root manifest; Antigravity uses
its root manifest. Native agents are projected into Claude/Cursor/Antigravity
plugins. Codex agent files remain separate because plugin agent consumption is
unverified. Export does not copy to host roots, register, enable, trust or test a
plugin. Its separate lifecycle fields remain false until observed operations.

Official encoding sources refreshed on 2026-10-01 (Asia/Saigon):

- [Claude custom agents](https://code.claude.com/docs/en/sub-agents), [plugin manifest](https://code.claude.com/docs/en/plugins-reference)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [portable plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Cursor custom agents](https://prod.cursor.com/docs/subagents), [plugins](https://prod.cursor.com/docs/reference/plugins)
- [Antigravity agents](https://www.antigravity.google/docs/subagents), [plugins](https://www.antigravity.google/docs/plugins)

## Implicit routing and observed versions

Implicit routing, where the host picks a skill from the request alone, is
unverified and weak when several large skill kits share one host. In one observed
Claude Code session with about 170 installed skills, the skill listing showed
`nckh-*` names without descriptions, so the host had only names to choose from.
Invoke the skill by name (for example `/nckh-plan` in Claude Code) and install only
the kits a project needs (`--kits`). Descriptions carry Vietnamese cues from the
[route boundaries](../core/registry/catalog/route-boundaries.json); this reduces the
risk but does not remove a host listing limit.

## Advisory nudge hooks

Two advisory nudges address failures seen when no skill is loaded: a routing hint
that names up to two installed `nckh-*` skills whose Vietnamese cues match the
prompt, and an EOL/BOM guard that compares a file before and after a write tool and
asks the agent to restore changed line endings or a lost BOM. They only add
context. They never block, never invoke a skill, never edit files and still run
when the controller context is missing. They exist only for project-scope installs
with hooks (`--hooks advisory`, the project default); global installs have no hooks.
Turn them off with `--hooks off` or by removing the owned hook configuration
([portable hooks](installation.md#portable-hooks)).

The hint is a mechanical cue match, not model routing. On the third blind-authored
held-out set it named the expected skill for 72.2% of natural prompts (65/90) and
gave no hint for any of the 10 prompts that belong to no skill. About three in ten
natural prompts get no hint, so explicit invocation (`/nckh-plan`, Codex
`$nckh-plan`) remains the reliable route. The current threshold is owned by
`tests/release/test_routing_prompts.py`; the prompt suite lives in
`evals/cases/routing/`. A prompt that already invokes `/nckh-…` or `$nckh-…` gets
no hint. Known limitation, deferred to r46: a prose-fixing request such as
"sửa lỗi chính tả" can draw an `nckh-fix` hint, because cues are matched without
reading intent (`core/route_hint.py`). The guard checks only the tools each codec lists in `WRITE_TOOLS`; new
files, linked paths and shell writes are not checked, and its size, per-session and
age limits live in `core/edit_guard.py`.

| Host | Routing hint | EOL/BOM guard |
|---|---|---|
| Claude | `UserPromptSubmit` → `additionalContext` | `PreToolUse` snapshot, `PostToolUse` → `additionalContext` |
| Codex | `UserPromptSubmit` → `additionalContext`, `$nckh-*` syntax | `apply_patch`: `PreToolUse` snapshot, `PostToolUse` → `additionalContext` |
| Cursor | `beforeSubmitPrompt` has no context channel: the hint is recorded with `delivered: false` | `preToolUse` snapshot, `postToolUse` → `additional_context` |
| Antigravity | No prompt event: no hint | `PostToolUse` has no context channel: receipt only, `delivered: false` |

This table is codec behavior. Whether each host surface consumes and shows the
context remains unverified until a native receipt for that surface and version.

Each adapter records its surfaces' observed versions with `revision` and `as_of`:
[Claude](../adapters/claude/adapter.json), [Codex](../adapters/codex/adapter.json),
[Cursor](../adapters/cursor/adapter.json) and [Antigravity](../adapters/agy/adapter.json).
A version ending in `-observed-unverified` was seen on a local binary but has no
native qualification cell; `unknown` means no version was observed.

Native UI/menu, headless dispatch, implicit routing, actual model/effort,
tool/hook coverage and OS/symlink cells require their own authorized disposable
runs. A CLI binary, documentation, TOML parse or copied file is insufficient.

