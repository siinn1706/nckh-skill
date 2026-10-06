# Tương thích runtime cho skill NCKH portable

**As-of:** 2026-09-30, Asia/Saigon. **Phạm vi:** Claude Code, Cursor và Google Antigravity/`agy`; Codex do parent xử lý. Chưa chạy consumer runtime, model/provider call, plugin thật, hook thật, GUI hay paid prompt.

## Kết luận và xếp hạng

Khuyến nghị **1 — một core `SKILL.md` theo Agent Skills + adapter mỏng theo host + coordinator cục bộ**. Core chỉ giữ `name`, `description`, hướng dẫn và `scripts/`, `references/`, `assets/` cần thiết. Adapter sở hữu path, invocation, model/effort, quyền, isolation, plugin và hook. Không bê nguyên frontmatter hoặc event name của một host sang host khác.

Khuyến nghị **2 — `NOT_CALLABLE` khi capability bắt buộc chưa được chứng minh**. Nếu model/effort, tool isolation, hook enforcement hoặc execution interface không có, chỉ fallback về `inherit/default` khi plan đã cho phép; không im lặng đổi model, bỏ guard hay coi việc đọc `SKILL.md` là đã chạy skill.

Khuyến nghị **3 — một worker mặc định; parallel chỉ cho track độc lập**. Mỗi child nhận delegation packet tối thiểu gồm scope, input/hash, output schema, quyền, path, egress, model/effort, budget, timeout và report path. Context mới không kế thừa hội thoại cha ở cả ba runtime; parent phải truyền context cần thiết.

### Nhãn bằng chứng

- `[local-help-observed]`: lệnh binary cục bộ đã chạy trong workspace, không có prompt/provider.
- `[official-docs]`: tài liệu vendor/maintainer chính thức, truy cập ngày trên.
- `[implementation-source]`: mã nguồn/manifest runtime đã đọc trực tiếp; **chưa thu được bằng chứng loại này trong lượt này**.
- `[unverified]`: chưa có consumer run hoặc docs không xác nhận semantics; không dùng làm release gate đạt.

## Phiên bản cục bộ

| Runtime | Quan sát an toàn |
|---|---|
| Claude Code | `C:/Users/USER\.local\bin\claude.exe`, `2.1.272 (Claude Code)`; `--help`, `claude agents --help`, `claude plugin --help` đã chạy. `[local-help-observed]` |
| Cursor IDE | `C:/Users/USER\AppData\Local\Programs\cursor\resources\app\bin\cursor.cmd`, `3.22.12`, build `3a92974361033b2051526321308c2740fe5912c0`, x64. Đây là IDE launcher, không phải bằng chứng Agent CLI. `[local-help-observed]` |
| Cursor Agent | `C:/Users/USER\AppData\Local\cursor-agent\agent.ps1`, `2026.09.15-d2fe57e`; `--version` và `--help` đã chạy. `[local-help-observed]` |
| Antigravity CLI | `C:/Users/USER\AppData\Local\agy\bin\agy.exe`, `1.2.13`; `--help` đã chạy. `[local-help-observed]` |

## Ma trận feature/runtime

| Feature | Claude Code | Cursor | Antigravity/`agy` |
|---|---|---|---|
| Skill format | `SKILL.md`, Agent Skills standard + extension | `SKILL.md`, bắt buộc `name`/`description` | `SKILL.md`, skills tự chọn theo mô tả |
| UI invocation | Chat slash `/skill-name`; auto invoke theo description | Agent chat `/skill-name`; cũng có Custom Modes | TUI auto-select; slash skill đăng ký; `/skills` để xem |
| CLI/headless | `claude -p/--print`; không có `run-skill` riêng trong help | `agent -p/--print`; `cursor.cmd` không thay cho `agent` | `agy -p/--print/--prompt` |
| Fresh subagent context | Có; `context: fork` cho skill | Có; editor/CLI/Cloud Agents | Có; `invoke_subagent` |
| Parallel/background | Foreground/background; docs nêu mặc định tối đa 20 | Foreground/background; nhiều child song song | Concurrent/background; nesting tối đa 10 theo docs |
| Per-agent model/effort | `model`, `effort`; CLI `--model`, `--effort low\|medium\|high\|xhigh\|max` | `model: inherit` hoặc ID; effort trong `model[effort=...]` | Agent `model: inherit\|flash\|pro`; CLI `--model`, `--effort` |
| Isolation/tools | `tools`, allow/deny tools, permission mode, `isolation: worktree` | `readonly`, sandbox, `--worktree`, permission hooks | `tools`, command policy, sandbox, `inherit/branch/share` workspace |
| Plugins | `plugin.json`; skill/agent/hook/MCP; `--plugin-dir` | portable `plugin.json` hoặc `.cursor-plugin/plugin.json`; `--plugin-dir` | skill/agent/rule/MCP/hook; `agy plugin ...` |
| Hooks | settings + plugin `hooks.json`; `PreToolUse`, `SubagentStart`, ... | stdio JSON; `preToolUse`, `subagentStart`, ...; `failClosed` | `.agents/hooks.json`; `PreToolUse`, `PostToolUse`, `PreInvocation`, ... |
| Confidence for portable adapter | Cao nhất, nhưng semantics vẫn host-specific | Cao nếu phát hiện đúng `agent` CLI | Tốt cho CLI; IDE/global paths khác CLI |

Mọi ô trên là `[official-docs]` trừ phiên bản/binary và cờ CLI đã đánh dấu `[local-help-observed]`. “Supported” không có nghĩa là đã chạy được trong workspace này.

## Path và invocation thực tế

### Claude Code

- Project: `.claude/skills/<skill-name>/SKILL.md`; global: `~/.claude/skills/<skill-name>/SKILL.md`; nested project directories được discover; `--add-dir` thêm directory skills. Plugin dùng `<plugin>/skills/...` và namespace plugin. `[official-docs]`
- UI: gõ `/skill-name [arguments]`; auto invocation phụ thuộc `description`; `disable-model-invocation` có thể tắt auto. `[official-docs]`
- CLI: `claude -p "<prompt>" --model <model> --effort <level> --output-format text|json|stream-json`. Help có `--agent`, nhưng không có subcommand `run-skill`; truyền slash command trong prompt headless cần probe riêng. `[local-help-observed]` + `[unverified]`
- Subagent: `.claude/agents/`, `~/.claude/agents/`, hoặc `--agents` JSON; skill frontmatter có `context: fork`, `agent`, `background`. Fresh context không có transcript cha. `[official-docs]`

### Cursor

- Project: `.agents/skills/`, `.cursor/skills/`; global: `~/.agents/skills/`, `~/.cursor/skills/`; compatibility path gồm `.claude/skills/`, `.codex/skills/` và global tương ứng. Nested directories được scope. `[official-docs]`
- UI: Agent chat `/skill-name`; skill cũng có thể thành Custom Mode. Đây là IDE/Agent chat, không suy ra CLI behavior. `[official-docs]`
- CLI thật: `agent -p "<prompt>" --model <model> --mode plan|ask --sandbox enabled|disabled --output-format text|json|stream-json --plugin-dir <dir> --worktree`. Binary wrapper cục bộ xác nhận các cờ này; không cung cấp API key hoặc prompt trong probe. `[local-help-observed]`
- `cursor.cmd agent --help` chỉ lặp help IDE launcher; adapter phải phát hiện `agent.ps1`/`agent` độc lập trước khi gọi. `[local-help-observed]`
- Subagent: `.cursor/agents/`, compatibility `.claude/agents/`, `.codex/agents/`; global tương ứng. `readonly: true`, `is_background: true`, shared checkout mặc định, worktree khi yêu cầu. `[official-docs]`

### Antigravity / `agy`

- CLI workspace: `<workspace-root>/.agents/skills/<skill-folder>/`; CLI global: `~/.gemini/antigravity-cli/skills/<skill-folder>/`; plugin CLI: `~/.gemini/antigravity-cli/plugins/<name>/skills/`. `[official-docs]`
- IDE workspace vẫn `.agents/skills/`; IDE global là `~/.gemini/config/skills/`; legacy `~/.gemini/antigravity/skills/` còn được hỗ trợ. Không gộp global CLI và IDE. `[official-docs]`
- TUI: skill liên quan tự được chọn; skill đã đăng ký có slash command như `/deploy-staging`; `/skills` duyệt danh sách. `[official-docs]`
- CLI: `agy -p "<prompt>" --model <model> --effort <level> --agent <agent> --output-format text|json|stream-json`; `--json-schema`, `--sandbox`, `--print-timeout`, `--continue` cũng có trong help. Không có `run-skill` riêng; slash trong headless prompt chưa consumer-probe. `[local-help-observed]` + `[unverified]`
- Agent: `.agents/agents/<name>.md` hoặc `<name>/agent.md`; global `~/.gemini/config/agents/`; `invoke_subagent` hỗ trợ concurrent session và workspace `inherit|branch|share`. `[official-docs]`

## Model, effort, context và parallelism

- Claude cho phép alias/full model ID, `inherit`, override per invocation và `CLAUDE_CODE_SUBAGENT_MODEL`; effort có thể kế thừa/cấu hình. `xhigh`/`max` là bằng chứng local CLI hiện tại, không phải portable enum. `[official-docs]` + `[local-help-observed]`
- Cursor chọn `inherit` hoặc model ID; tham số dạng `claude-opus-... [effort=high,context=...]` theo docs. Parent/model plan/admin có thể override; model ID và account availability phải resolve lúc chạy. Không tự suy ra có cờ `--effort` độc lập. `[official-docs]` + `[local-help-observed]`
- `agy` custom agent chỉ được docs nêu `inherit|flash|pro`; CLI local nhận `low|medium|high|max`, trong khi bảng headless docs không đồng nhất về `max`. Ghi `max` là local-only cho đến khi release probe. Pinned model không tồn tại phải fail nonzero theo docs; không silent fallback. `[official-docs]` + `[local-help-observed]` + `[unverified]`
- Cả ba đều fresh-context child; không coi fresh context là quyền mới. Claude docs nêu tối đa concurrent mặc định 20; Antigravity docs nêu nesting tối đa 10; Cursor chỉ xác nhận nesting limit theo docs, con số cần lấy ở release hiện hành. `[official-docs]` + `[unverified]`
- Coordinator phải tính context thực tế của catalog, `SKILL.md`, references, tool schema, hook injection và delegation packet; không coi child là “miễn context/miễn phí”. Chỉ dùng parallel khi input/output độc lập, owner file rõ và budget đã reserve.

## Plugins và hooks

| Runtime | Plugin contract | Hook contract và giới hạn |
|---|---|---|
| Claude | `.claude-plugin/plugin.json`; plugin có skills, agents, hooks, MCP; `--plugin-dir` load theo session. `[official-docs]` | User `~/.claude/settings.json`, project `.claude/settings.json`, local `.claude/settings.local.json`, plugin `hooks/hooks.json`. `PreToolUse` có allow/deny/ask/defer/modify; `SubagentStart` inject context nhưng không chặn create. Async không block; thường exit 2 block, lỗi khác phần lớn fail-open. `[official-docs]` |
| Cursor | Portable Agent Plugin root `plugin.json`; Cursor Plugin `.cursor-plugin/plugin.json`; CLI có `--plugin-dir`. `[official-docs]` + `[local-help-observed]` | `~/.cursor/hooks.json`, `.cursor/hooks.json`, JSON stdio; permission hook allow/deny, exit 2 block; invalid JSON/schema block action; lỗi khác fail-open mặc định, `failClosed: true` đổi chính sách. Một số hook không có trong Cloud Agents. `[official-docs]` |
| `agy` | CLI `.agents/plugins/`, global `~/.gemini/antigravity-cli/plugins/`; IDE/global `~/.gemini/config/plugins/`; `agy plugin list/install/enable/disable/uninstall`. `[official-docs]` | Workspace `.agents/hooks.json`; global `~/.gemini/config/hooks.json` hoặc CLI settings; plugin `hooks.json`. `PreToolUse` stdout JSON bắt buộc `decision: allow\|deny\|ask\|force_ask\|deny_unless_prior_grant`; `deny` hard-block. `PostToolUse` trả `{}`, invocation/stop trả injection hoặc continue/terminate. Generic nonzero/timeout/invalid-output của handler chưa được docs xác định. `[official-docs]` + `[unverified]` |

Hook event name, process failure và permission semantics không portable. Dùng hook cho receipt/telemetry khi chưa kiểm chứng; coordinator preflight mới là gate bắt buộc cho write, egress, paid call, model pin và budget. Không dùng prompt text để giả lập authorization.

## Adapter/fallback contract đề xuất

1. **Discovery:** đọc live catalog và version; kiểm tra skill path đúng scope. Không lấy sự hiện diện của file, plugin hay CLI help làm consumer-run proof.
2. **Invocation:** adapter giữ một route cho UI và một route cho headless; lưu command, output format, model/effort, cwd, timeout và exit status. Nếu slash dispatch trong `-p` chưa probe, trạng thái là `UNVERIFIED`, không báo “đã invoke skill”.
3. **Model:** nếu host pin được model/effort đã duyệt, dùng nó; nếu không, `inherit/default` chỉ khi plan cho phép, còn lại `NOT_CALLABLE`. Không hạ `max` thành `high` âm thầm.
4. **Isolation:** ưu tiên Claude `tools`/worktree, Cursor `readonly`/sandbox/worktree, Antigravity tool policy/sandbox/branch. Nếu thiếu isolation, narrow allowlist/no-write hoặc `NOT_CALLABLE` cho route an toàn-critical.
5. **Hooks:** map semantic events riêng từng host; kiểm tra decision thật. Không ánh xạ máy móc `PreToolUse`, `SubagentStart`, `PostToolUse`; hook thiếu/crash phải được coordinator xử lý trước operation bắt buộc.
6. **Receipt:** ghi runtime/version, path/namespace, skill hash, model/effort, child/workspace mode, tool/egress, output hash, usage, retries, status và uncertainty. Không chuyển `DONE` thành human-reviewed/scientifically valid nếu chưa có gate tương ứng.

## Probes còn lại trước release

- Với fixture disposable, chạy discovery và cùng một skill trên UI lẫn headless của từng host; xác nhận precedence project/global/plugin, nested path, namespace và slash dispatch trong `-p`/`--print`. `[unverified]`
- Gọi một custom subagent read-only; xác nhận fresh context, packet truyền đủ, foreground/background, parallel join, cleanup và shared-vs-worktree/branch behavior. Không dùng provider/paid prompt ngoài grant. `[unverified]`
- Pin một model hợp lệ, một model không hợp lệ và từng effort được plan cho phép; ghi exit/JSON output; đặc biệt kiểm tra `agy --effort max` và Cursor parameterized effort. `[unverified]`
- Hook fixture không side effect: allow/deny/ask, invalid JSON, stdout sai schema, nonzero, timeout và crash; đo semantics thực tế của cả ba, nhất là `agy` generic failure. `[unverified]`
- Load/disable plugin tạm thời; xác nhận skill/agent/hook/MCP namespace và cleanup. Không install marketplace hoặc publish artifact trong probe. `[unverified]`
- Đo context/window và usage receipt trên phiên bản target; kiểm tra limit/concurrency thực tế, stale catalog/hash, timeout-unknown và retry budget. `[unverified]`
- Re-run version/help và official docs ngay trước release; các cờ `max`, model ID, nesting/concurrency và IDE-vs-CLI path là drift points.

## Nguồn chính thức và phạm vi

**Claude Code:** [Skills](https://code.claude.com/docs/en/skills) (format/path/invocation), [Sub-agents](https://code.claude.com/docs/en/sub-agents) (context/isolation/model/parallelism), [Hooks](https://code.claude.com/docs/en/hooks) (events/permissions/failure), [Plugins](https://code.claude.com/docs/en/plugins) (manifest/load), [CLI reference](https://code.claude.com/docs/en/cli-reference) (flags).

**Cursor:** [Skills](https://prod.cursor.com/docs/skills) (path/format/UI), [Subagents](https://prod.cursor.com/docs/subagents) (context/parallel/isolation/model), [Hooks](https://prod.cursor.com/docs/hooks) (stdio/events/fail-closed), [Plugins](https://prod.cursor.com/docs/plugins) (plugin formats), [CLI parameters](https://prod.cursor.com/docs/cli/reference/parameters) và [headless](https://prod.cursor.com/docs/cli/headless) (Agent CLI), [CLI using](https://prod.cursor.com/docs/cli/using) (interactive/headless distinction).

**Antigravity:** [CLI headless](https://www.antigravity.google/docs/cli/headless) (print/model/effort/output), [CLI features](https://www.antigravity.google/docs/cli/features) (TUI/CLI commands), [Skills](https://www.antigravity.google/docs/skills?tab=ide) (workspace/global distinction), [Subagents](https://www.antigravity.google/docs/subagents?tab=cli) (agents/context/workspace/parallelism), [Hooks](https://www.agy.dev/docs/hooks/) (locations, events, JSON decisions), [Plugins](https://www.antigravity.google/docs/plugins?tab=cli) (bundles/paths), [changelog](https://www.agy.dev/docs/changelog?tab=cli) (release drift).

Các nguồn trên là tài liệu vendor được đối chiếu theo từng runtime; không có mã nguồn host để gắn nhãn `[implementation-source]`. URL và behavior có thể drift; release phải chụp lại version/help/docs.

## Status

**Status:** DONE_WITH_CONCERNS

**Summary:** Đã hoàn tất nghiên cứu đối chiếu Claude Code 2.1.272, Cursor IDE 3.22.12 + Cursor Agent 2026.09.15-d2fe57e và `agy` 1.2.13; đã ghi path, invocation, agent/context, model/effort, plugin, hook và adapter/fallback contract. Core portable nên giữ host-neutral; mọi host-specific action đi qua adapter.

**Concerns/Blockers:** Chưa có consumer run, hook execution, plugin fixture, subagent run hoặc provider/model call; slash dispatch headless, generic hook failure của `agy`, Cursor nesting limit, model availability và `max` cross-version còn `[unverified]`. Không release route cần các capability này cho đến khi các probe ở trên có receipt thật.
