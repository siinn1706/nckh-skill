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

Native UI/menu, headless dispatch, implicit routing, actual model/effort,
tool/hook coverage and OS/symlink cells require their own authorized disposable
runs. A CLI binary, documentation, TOML parse or copied file is insufficient.

