# Compatibility matrix — facts, scope và release probes

Ma trận thiết kế thuộc [kế hoạch đã duyệt ngày 01/10/2026](plan.md). Phê duyệt không thay ngày thu bằng chứng bên dưới và không xác nhận native compatibility.

As-of **30/09/2026, Asia/Saigon**. `D` = official documentation; `L` = local help/
version; `T` = native tool surface hiện có trong chat; `U` = chưa thực nghiệm NCKH.
Không có ô nào là NCKH host acceptance đã pass. Version dưới đây là **installed
observed**, không tuyên bố newest release của vendor.

Local: Codex CLI **0.154.0**; Claude Code **2.1.272**; Cursor IDE **3.22.12**;
Cursor Agent CLI **2026.09.15-d2fe57e**; Antigravity CLI **1.2.13**.
Codex App/IDE build và Antigravity IDE build chưa đo. CLI Codex help trả exit 0
kèm cảnh báo không tạo PATH aliases/temp vì access denied; không đổi CODEX_HOME
hoặc sandbox để che cảnh báo. Đây không phải consumer failure/pass của NCKH.

## 1. Skill paths và cách gọi theo surface

Các path là vendor convention trong tài liệu, dùng để thiết kế adapter; installer
phải resolve OS/home/workspace thực và kiểm overlap trước write. Không có root
global thống nhất cho bốn host.

| Runtime/surface | Project / user-global skill roots | Invocation đã có căn cứ | Điều chưa được suy ra |
|---|---|---|---|
| Claude Code | `.claude/skills/` / `~/.claude/skills/` (D) | `/skill-name` hoặc implicit description; plugin có namespace (D) | Slash text trong headless prompt chưa NCKH-probe (U). |
| Codex desktop | `.agents/skills/` / `~/.agents/skills/` theo local skill docs (D,T) | Enabled skills có trong menu `/`; `$` cũng được docs desktop nêu (D) | Chưa quan sát menu/version UI thực trong lượt này; không thay slash bằng dollar bắt buộc. |
| Codex CLI | `.agents/skills/` từ CWD lên repo root / `~/.agents/skills/` (D,L cho binary) | `/skills`, `$skill` và implicit theo docs (D) | Desktop slash menu không tự chứng minh `/skill` direct ở mọi CLI version (U). |
| Codex IDE extension | Local skill discovery được hỗ trợ (D) | `/skills` hoặc `$` theo skill docs (D) | Có editor context không có nghĩa same UI/commands với desktop (U). |
| Cursor IDE/Agent CLI | `.cursor/skills/` hoặc `.agents/skills/`; user counterparts (D) | Agent chat `/skill-name` + implicit (D); standalone `agent` CLI (L) | `cursor` IDE launcher không thay Agent CLI; headless dispatch cần probe (U). |
| Antigravity CLI/TUI | `.agents/skills/` / `~/.gemini/antigravity-cli/skills/` (D) | TUI slash skill + `/skills`, implicit; `agy -p` là prompt runner (D,L) | `-p` không phải arbitrary skill API; headless slash còn U. |
| Antigravity IDE | `.agents/skills/` / `~/.gemini/config/skills/`; legacy global path còn có hỗ trợ (D) | Skill discovery theo docs (D) | Không lấy TUI invocation/CLI global root áp nguyên lên IDE (U). |

Nguồn paths và invocation:
[Claude Skills](https://code.claude.com/docs/en/skills),
[Codex Build skills](https://learn.chatgpt.com/docs/build-skills),
[desktop slash reference](https://learn.chatgpt.com/docs/reference/slash-commands),
[Cursor Skills](https://prod.cursor.com/docs/skills),
[Antigravity Skills](https://www.antigravity.google/docs/skills?tab=ide),
[Antigravity CLI features](https://www.antigravity.google/docs/cli/features).

Codex same-name skills không được merge; catalog có thể rút ngắn/omit metadata
khi quá lớn. Cursor còn compatibility roots `.claude/skills/`, `.codex/skills/`
và user-global counterparts bên cạnh `.cursor/skills/`, `.agents/skills/`. Vì vậy
installer chọn **một representation có hiệu lực trên mỗi surface** và phải kiểm
toàn visibility graph, không copy cùng skill vào mọi path “để chắc”. Symlink được Codex docs
hỗ trợ; host/OS khác vẫn cần qualification trước dùng mode đó.

### Projection của ba logical entrypoints

Áp dụng riêng cho `nckh-plan`, `nckh-cook`, `nckh-xia` (gọi chung là `NAME`). Mỗi
cell phải có receipt riêng trước quảng bá đã dùng được. Bảng sau là **syntax dự
kiến theo docs**, không có NCKH đã cài; native consumer status của tất cả cell còn U.

| Host/surface | UI/menu/explicit projection | Headless projection | Implicit routing |
|---|---|---|---|
| Claude interactive | `/NAME` theo skills docs (D) | Prompt runner có thật; direct slash dispatch U | Description (D), NCKH outcome U |
| Codex desktop | Enabled skill trong `/` menu; `$` cũng documented (D) | Không suy headless API từ desktop UI; dùng CLI cell riêng | Metadata/discovery (D), NCKH outcome U |
| Codex CLI | `/skills` hoặc `$NAME` (D) | Prompt runner không chứng minh slash hoặc `$` dispatch; U | D, NCKH outcome U |
| Codex IDE | `/skills` hoặc `$NAME` (D) | Không áp CLI headless contract lên IDE; N/A nếu không có interface riêng | D, NCKH outcome U |
| Cursor IDE Agent | `/NAME` trong Agent chat (D) | Dùng standalone Agent CLI cell, không `cursor.cmd` thay runner | D, NCKH outcome U |
| Cursor Agent CLI | Interactive skill selection theo native catalog; exact surface U | `agent -p` có thật (L), skill dispatch U | Native discovery D; NCKH routing U |
| Agy CLI/TUI | Slash registered skill và `/skills` (D) | `agy -p` có thật (L), skill dispatch U | D, NCKH outcome U |
| Agy IDE | Skill discovery D; exact slash/menu cần probe | Không dùng CLI behavior làm IDE proof | D, NCKH outcome U |

Required matrix key: logical entrypoint + mode + host/surface/version + invocation
(`ui-slash`, `native-menu`, `headless-prompt`, `implicit`). Cell state tách
`docs-only`, `observed`, `unverified`, `unsupported`, `not-applicable`; U không là
unsupported. Required route chưa có proof thì không dispatch tự động, report
UNVERIFIED/NOT_CALLABLE kèm lý do. Không tạo shell alias giả native support.

## 2. Agent, model và hooks

| Capability | Claude Code | Codex local App/CLI/IDE | Cursor | Antigravity |
|---|---|---|---|---|
| Separate child context | Subagents và skill `context: fork` (D) | Native agents, custom agents (D,T); context packet tùy spawn contract | Subagents (D) | `invoke_subagent` (D) |
| Parallel work | Foreground/background (D) | Parallel tools exposed trong chat (T); docs cả ba local surfaces (D) | Parallel/background (D) | Concurrent/background (D) |
| Custom agent paths | `.claude/agents/`, user counterpart (D) | `.codex/agents/*.toml`, user counterpart (D) | `.cursor/agents/`, compatibility roots (D) | `.agents/agents/`, global `.gemini/config/agents/` theo docs (D) |
| Per-agent model | `model`/inherit, alias hoặc model ID (D) | Custom agent `model`; spawn/default precedence host-specific (D,T) | `model` hoặc inherit (D) | Agent aliases inherit/flash/pro; không suy arbitrary per-agent IDs (D) |
| Reasoning | Agent effort/CLI effort, model-specific (D,L) | `model_reasoning_effort`; native schema effort theo model (D,T) | Parameterized model effort, không mặc định CLI `--effort` (D,L) | CLI `--effort`; custom-agent effort semantics còn phải probe (D,L,U) |
| Plugin | Native manifest, agent/skill/hook/MCP (D,L) | Portable manifest/Codex overlay, local skill/plugin surfaces khác nhau (D,T) | Portable hoặc Cursor manifest (D,L) | Plugin bundles, CLI/IDE roots khác (D,L) |
| Hook | Native settings/plugin events (D) | Hook config/plugin events + trust; tool coverage có ngoại lệ (D) | Native event names/casing, `failClosed` semantics (D) | Native JSON decision; generic error/timeout semantics chưa đủ (D,U) |
| Workspace isolation | Tool policy, sandbox/worktree theo config (D) | Parent permissions, optional agent config; không mặc định filesystem riêng (D,T) | Shared checkout hoặc worktree theo route (D) | Inherit/branch/share theo docs (D) |

Nguồn agent/model:
[Claude subagents](https://code.claude.com/docs/en/sub-agents),
[Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Cursor subagents](https://prod.cursor.com/docs/subagents),
[Antigravity subagents](https://www.antigravity.google/docs/subagents?tab=cli),
[Antigravity headless](https://www.antigravity.google/docs/cli/headless).

Không lấy một con số max threads/nesting của vendor làm fan-out policy NCKH.
Codex docs nói custom-agent file model/effort có precedence; plugin/role khác có
thể khóa model. Mapping phải kiểm effective settings, không chỉ request.
Current chat có tool spawn và hai research subtasks đã nhận việc; điều đó chỉ
xác nhận công cụ phiên này, không test custom NCKH agent config trên ba surfaces.

## 3. Các khác biệt phải đưa vào adapter

1. **Syntax là projection.** `/nckh-plan` là logical UX; adapter chọn skill handle
   thực trên surface. Không tạo shell alias hoặc mega dispatcher để giả UI support.
2. **`agy` đã xác minh là Antigravity CLI** qua version/help ở research report;
   không gộp user-global IDE/CLI roots. Effort `max` có trong help cục bộ nhưng
   docs chưa nhất quán; không đưa universal enum `max` vào core contract.
3. **Model selection không đồng nghĩa permission.** Unknown model/account/effort
   phải hiển thị; default native inheritance khác policy chọn tier của NCKH.
4. **Fresh context không là sandbox.** Child có thể dùng cùng filesystem và
   inherited rules/tools; ownership/read-only cần host enforcement thật.
5. **Plugins không thay skill semantics.** Portable source vẫn build host artifacts;
   hooks/config/agents không portable chỉ vì tất cả dùng Markdown hoặc JSON.
6. **Hooks không guard toàn bộ tool surface.** Codex hosted WebSearch không qua
   local tool hooks, `write_stdin` không rerun PreToolUse. Cursor/Claude/agy có
   failure contracts khác nhau; không map cùng tên event rồi nhận security pass.

Nguồn:
[Codex hooks/tool coverage](https://learn.chatgpt.com/docs/hooks),
[Claude hooks](https://code.claude.com/docs/en/hooks),
[Cursor hooks](https://prod.cursor.com/docs/hooks),
[Antigravity hooks](https://www.agy.dev/docs/hooks/),
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Cursor plugins](https://prod.cursor.com/docs/plugins),
[Antigravity plugins](https://www.antigravity.google/docs/plugins?tab=cli).

## 4. Host qualification, không suy từ documentation

P5/P6/P7 phải tạo receipt cho từng cell được quảng bá hỗ trợ:

- Fresh isolated test project + selected global fixture scope; no duplicate skills.
- Explicit invocation và natural VI/EN implicit routing với full dependency closure.
- Same-agent route; optional subagent fresh context, model/effort effective,
  permission, parallel join, timeout reconciliation và cleanup đúng owner.
- Hook allow/deny, absent/crash/invalid output/timeout và actual tool coverage.
- Project/global config precedence; native plugin namespace; update/uninstall
  không mất user edits; copy/symlink trên OS được quảng bá.
- Interactive stop/feedback/resume; auto complete authorized phases; không mở
  irreversible/paid/publish authority. Ghi cost/usage unknown đúng nghĩa.

Thiếu native feature: cùng-agent hoặc inherit chỉ khi vẫn thỏa required outcome
và quyền; còn lại `NOT_CALLABLE`/pending cho capability đó. Không im lặng coi
unsupported và unverified là cùng trạng thái. Một host pending không cấm authoring
core, nhưng cấm nhãn “đã tương thích cả bốn runtime”.

### Permission projection: auto không là vendor bypass mode

| Host | Mapping của NCKH auto | Điều phải quan sát |
|---|---|---|
| Claude Code | Giữ sandbox/permission mode và allowed tools hiện hữu đã được duyệt; không suy auto thành skip-permissions | Actual permission mode, tools allow/deny, approval/deny result và background child inheritance |
| Codex App/CLI/IDE | Giữ native sandbox/approval policy của surface; auto chỉ đổi routine workflow pause | Actual tool schema/permissions, approval outcome, child cannot broaden parent và hook bypass coverage |
| Cursor IDE/Agent CLI | Giữ native sandbox/read-only/tool policy; không map auto thành blanket force | IDE vs CLI policy, shared/worktree permission, MCP/web/file/shell coverage |
| Agy IDE/CLI | Giữ sandbox/command policy/prior grants của host; không map auto thành blanket allow | Inherited command/tool policy, allow/deny/ask semantics và effective child policy |

Adapter `auto_policy` record gồm host/surface/version, authorized local operations,
sandbox/approval mode, tool/egress allowlist, external/irreversible ask-or-deny,
mandatory human boundaries và stop behavior. Host approval prompt vẫn có thể xuất
hiện trong auto; đó không phải routine checkpoint của NCKH. Shell, file, MCP, web,
paid/external và irreversible routes đều cần negative tests; không invoke hành động
nguy hiểm thật để test denial. Không biết native enforcement thì block route bị
ảnh hưởng, không dùng instruction text như sandbox. Mọi blanket bypass/force flag
bị cấm phát sinh từ `--auto`; quyền explicit khác phải được xét độc lập.

### OS qualification target

| OS | Entry script | Bằng chứng hiện có | Fixture / native acceptance | Owner tương lai |
|---|---|---|---|---|
| Windows | install.ps1 | Local vendor version/help, chưa installer | Cả hai pending | P6 installer + P5 native adapter owner |
| macOS | install.sh | Design-only, chưa local lab | Cả hai pending | P6 installer + authorized macOS lab reviewer |
| Linux | install.sh | Design-only, chưa local lab | Cả hai pending | P6 installer + authorized Linux lab reviewer |

Trước P6 phải khóa host/surface/OS cells hợp lệ, lab owner thật và permission cho
mỗi run. Vendor không hỗ trợ một cell thì ghi unsupported với nguồn, không bịa lab.
POSIX script không tự chứng minh hỗ trợ macOS/Linux. Thiếu lab giữ pending; không
âm thầm bỏ OS/host khỏi promised release để đóng gate. Phase estimates không gồm
thời gian chờ lab/reviewer; user quyết định mọi giảm phạm vi advertised support.

## 5. Evidence ledger và giới hạn

Parent đọc package metadata/wrapper/README và `codex --version/--help`; package
chỉ có launcher JS/native binary nên không dùng nó như source proof cho agent
internals. Official pages được mở ngày as-of; URL Codex cũ redirect sang
`learn.chatgpt.com`. Không lấy Agents API docs làm Codex CLI behavior.

[Báo cáo ba runtime](../reports/researcher-260930-1910-runtime-compatibility.md)
ghi exact binary paths, flags, official sources và U probes. Không có live NCKH
consumer run, plugin/hook install, model availability test hay paid evaluation.
Tài liệu current có thể drift; release phải chụp lại version/docs/capability receipt.
