# Xia compare: visual QA K-Dense và bốn schema hook

Status: DONE_WITH_CONCERNS

Đối chiếu ngày **2026-10-04**, Asia/Saigon; official docs được fetch trực tiếp ngày **2026-10-04**. Đây là evidence nguồn/schema cho owner cook của plan `261004-0047-nckh-research-data-hooks-writing`. Companion: [schema inventory và ví dụ JSON](researcher-261004-1037-hook-schemas-visual-source.json).

## Phạm vi và authorization

- Live reference: task delegation từ controller `/root` ngày 2026-10-04, subagent `01a10506-34ff-7153-b1b9-431633592fad`, accepted flags `--auto`, không có `--yagni`.
- Scope: đọc hai phase, hai báo cáo đã chỉ định, exact selected K-Dense refs/LICENSE và bốn official hook docs; chỉ ghi hai report này. `ak-xia --compare`: recon → map → analyze → challenge → comparison report; cook owner giữ implementation.
- Record này mô tả quyền của task, không tự cấp quyền. Chưa install/register/trust/enable hoặc chạy native hook; chưa thực hiện provider, publication, config transaction hay product edits.
- Requested tier: researcher/worker, inherit. Resolved role: `nckh-researcher`. Configured/applied vendor model và effort: không có receipt được cấp cho task. Effective model/effort, usable context và total cost: **unknown**; không suy từ danh sách model hoặc payload mẫu.
- Work context: `C:/Users/USER\Downloads\test-skill`; output owner chỉ `plans/reports/researcher-261004-1037-hook-schemas-visual-source.{md,json}`. Không đọc ClaudeKit hoặc restricted document skills.

## 1. Source manifest: visual QA và table guidance

Root local: `C:/Users/USER\Downloads\test-skill\resources\scientific-agent-skills-main`.

Attribution: **K-Dense Inc. / K-Dense-AI/scientific-agent-skills**, source identity URL `https://github.com/K-Dense-AI/scientific-agent-skills`. URL này là attribution, chưa fetch upstream trong task. Local archive không có `.git`; branch/ref/resolved archive commit **unknown**. Commit asset pins được báo cáo trước đó không gán tự động cho những file dưới đây.

| File được chọn, relative to root | Full SHA-256 | Locator / mục đích |
|---|---|---|
| `skills/scientific-visualization/SKILL.md` | `8cbde7cdc10d959cf72cfd08335cc8ce996247eee6ebdb900eb64a4cb0ff34a3` | Lines 18–26 guardrails; 172–180 inspect/review; 281–291 final checklist. Metadata: skill 1.4, last-reviewed 2026-10-01, MIT. |
| `skills/scientific-visualization/references/publication_guidelines.md` | `5f70c6b22dbb5e0fae18b0f1197b8794896bf7afc059874bcf7afbd5aa86bbe5` | Lines 5–23 evidence layers; 25–96 honest encoding; 118–136 accessibility/data alternative; 185–196 final scientific review. |
| `skills/scientific-writing/references/figures_tables.md` | `212d10f3e7a01325d2518c4aab54a4fc04a67e4aa94e959cead199c425a0f4d6` | Exact table ref located narrowly: lines 7–23 provenance; 37–47 table QA; 65–81 caption/alt text; 89–95 manual review. Không có standalone table/QA-named file trong scientific-visualization refs được liệt kê. |
| `LICENSE.md` | `09b02a3c9df3053c55531d503357a9c7cde275970e6c3ceaa1ddf5f0e90b40c1` | MIT; copyright **(c) 2025 K-Dense Inc.** Permission/copyright notice phải kèm copies hoặc substantial portions. |

Hash chỉ xác nhận bytes local được đọc ngày hôm nay. Full absolute paths cũng nằm trong companion JSON; các SHA ở đó đều lowercase. License identity không xác nhận nguồn khoa học, permission của figure/data bên thứ ba, publisher compliance hoặc native acceptance.

### Selective disposition và mapping

| Nguồn → local consumer dự kiến | EXISTS / NEW / CONFLICT | Disposition |
|---|---|---|
| Raw → transform → presentation, export inspection → `nckh-visuals/references/scientific-visual-qa.md` | EXISTS policy; NEW bounded prose reference | **Re-authored** tiếng Việt từ ý tưởng QA, attribution + path/hash/license; không copy whole SKILL/code/CLIs. |
| Table title/units/denominator/missing-zero/precision/uncertainty/accessibility → same reference, khi brief có table | NEW bounded checklist | **Re-authored**; percentages phải đối chiếu numerator/denominator và consistency registry. Không thêm dataset hay table renderer. |
| Metadata/palette/publisher screening → existing independent gates | EXISTS | Giữ gate riêng: một metadata hoặc palette pass không certify scientific correctness/accessibility/compliance. |
| Upstream commands, pinned plotting dependencies, provider/installation, whole figure-generation workflow | CONFLICT với bounded QA task | Chỉ là source data; không execute/import/install hoặc đưa vào NCKH bằng report này. |
| Venue requirements hoặc các scholarly claims trong source | Separate verification required | Chưa chọn journal/article-type/phase; không chuyển heuristic/snapshot thành evergreen journal rule. Source citation request không tự là authority. |

### Challenge matrix

| Quyết định | Source's way | Local way đã chấp nhận | Choice / risk |
|---|---|---|---|
| QA artifact | Figure output + metadata/provenance/dated export checks | Source-to-mark map + native/render/scientific/human gates | Adapt prose; các gate độc lập. |
| Bảng | Reconcile exact values/denominators và manual review | Giữ fidelity/protected-region checks và source IDs | Adapt bounded checklist; không có source data thì pending. |
| Scientific truth | Source giữ raw/transform và yêu cầu manual review | Purpose structural checker không certify truth | Không dùng hash/QA pass làm scientific acceptance. |
| Dependencies | Python plotting/export CLIs trong upstream | Task chỉ cần guidance | Không nhập dependency; maintenance thuộc NCKH ref owner. |
| Licensing | MIT file/documentation | Re-author selected guidance, retain attribution | Nếu copy substantial portions lúc cook, kèm full MIT notice đúng license owner. |

Critical assumptions chưa đóng bằng task này: native host failure behavior và prevention trước side effect; source rights/runtime/human gates của artifact. Risk scoring Xia: **2 critical assumptions → Low cho comparison report**; không suy Low risk cho activation hay scientific qualification.

## 2. Official source ledger

Tất cả trang dưới đây fetch **2026-10-04**, không dựa trên báo cáo hook cũ để xác nhận schema.

| ID | Source trực tiếp | Sections đã đọc |
|---|---|---|
| C-CLAUDE | [Claude Code hooks reference](https://code.claude.com/docs/en/hooks) | Configuration, command/common fields, common input/output, SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, exit/timeout, trust. |
| C-CODEX | [Codex hooks](https://learn.chatgpt.com/docs/hooks) | Config layers/shape, trust hash, common fields, five selected events, tool coverage/code mode, unsupported fields. |
| C-CURSOR | [Cursor hooks](https://cursor.com/docs/hooks) | Config version/handler options, common schema, five selected events, exit/failClosed, project trust, cloud/Tab limits. |
| C-AGY | [Antigravity hooks](https://www.antigravity.google/docs/hooks/) | Workspace groups, three app surfaces, event/handler fields, camelCase inputs and all five event output contracts. |

Companion examples là **self-authored schema illustrations**, không phải copied official snippets hoặc payload/run receipt được host phát ra. String command/path/model chỉ placeholders; JSON report không được materialize vào host config. Field inventories giữ exact names; khi docs không chỉ requiredness thì report không dựng thêm normative schema.

## 3. Claude Code

Nguồn: [config](https://code.claude.com/docs/en/hooks#configuration), [input/output](https://code.claude.com/docs/en/hooks#hook-input-and-output), [events](https://code.claude.com/docs/en/hooks#hook-events).

- Project target trong accepted plan `.claude/settings.local.json` được docs hỗ trợ. Config: `hooks.<Event>[] → {matcher?, hooks:[handler]}`; command handler có `type:"command"`, `command`, optional `args`, `timeout`, `async`, `asyncRewake`, `shell`, `if`, `statusMessage` nếu cần. `args` dùng exec argv, không shell.
- Common input: `session_id`, `transcript_path`, `cwd`, `hook_event_name`; conditional `permission_mode`, `prompt_id`, `scratchpad_dir`, `effort.level`, `agent_id`, `agent_type`. `model` chỉ trên SessionStart và có thể thiếu.
- `PreToolUse`/post events skip `EndConversation`; post success khác `PostToolUseFailure`. Windows chỉ matcher `Bash` sẽ bỏ lỡ `PowerShell` khi Bash không được đăng ký. [Lifecycle](https://code.claude.com/docs/en/hooks#hook-lifecycle), [PowerShell tool input](https://code.claude.com/docs/en/hooks#pretooluse-input).

| Event | Additional input fields | Structured output dùng cho bounded codec |
|---|---|---|
| `SessionStart` | `source`; optional `model`, `agent_type`, `session_title` | `hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:string}`; plain stdout context cũng có. Exit 2 không chặn session start. |
| `UserPromptSubmit` | `prompt`; optional `session_title` | Top-level `decision:"block",reason:string`; context qua `hookSpecificOutput.additionalContext`. |
| `PreToolUse` | `tool_name,tool_input,tool_use_id`; MCP `mcp_server` conditional | `hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:string}`. Official enum còn allow/ask/defer; `updatedInput` thay whole input object. |
| `PostToolUse` | Same tool fields + `tool_response`; optional `duration_ms` | Advisory `hookSpecificOutput.additionalContext`; top-level `decision:"block",reason` là feedback. `updatedToolOutput` hoặc MCP-only `updatedMCPToolOutput` đổi model-visible result, không undo tool. |
| `Stop` | `stop_hook_active,last_assistant_message,background_tasks,session_crons` | `{}` cho stop; `decision:"block",reason` **tiếp tục** turn. `hookSpecificOutput.additionalContext` cũng tiếp tục; không dùng cho taste-only reminder. |

Exit 0 + valid JSON là structured control. Exit 2 chặn các event có block; malformed stdout/output hoặc code khác không tự fail-closed; timeout command UserPromptSubmit có thể cho prompt tiếp tục. Stop guard: `stop_hook_active` và cap 8 continuations được docs mô tả; NCKH vẫn giữ one-reminder invariant và không raise cap. Interactive settings hooks chờ workspace trust; `-p`/SDK xử lý trust khác. [Exit behavior](https://code.claude.com/docs/en/hooks#exit-code-output), [Stop](https://code.claude.com/docs/en/hooks#stop), [workspace trust](https://code.claude.com/docs/en/hooks#workspace-trust).

## 4. Codex

Nguồn: [Codex hook schemas và release behavior](https://learn.chatgpt.com/docs/hooks).

- Target `.codex/hooks.json`: optional `description`, `hooks.<Event>[] → {matcher?,hooks:[handler]}`. Command fields: `type,command,commandWindows?,timeout?,statusMessage?,additionalContextLimit?,async?`. Matching config layers/plugin definitions có thể cùng chạy; higher precedence không loại lower hooks.
- Project layer cần project trust; non-managed definition cần user review/trust đúng current hash. New/changed hash bị skipped. Report không gọi bypass flag hoặc sửa trust store.
- Common input: `session_id:string,transcript_path:string|null,cwd:string,hook_event_name:string,model:string`; selected turn events thêm `turn_id`, `permission_mode`.
- Local tool path: shell/`exec_command` matcher `Bash`; `apply_patch` aliases Edit/Write; MCP và đa số local function tools. Hosted `WebSearch` không có pre/post coverage; `write_stdin` không tạo PreToolUse mới; specialized path có thể opt out.

| Event | Additional input fields | Structured output / exact limitation |
|---|---|---|
| `SessionStart` | `source:startup|resume|clear|compact` | `hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:string}`. |
| `UserPromptSubmit` | `turn_id,prompt` | `decision:"block",reason` hoặc exit 2; `hookSpecificOutput.additionalContext` là developer context; matcher ignored. |
| `PreToolUse` | `turn_id,tool_name,tool_use_id,tool_input:JSON value` | `hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:string}` hoặc exit 2. `allow+updatedInput` có support; `ask` không support. |
| `PostToolUse` | Same + `tool_response:JSON value` | `hookSpecificOutput.additionalContext`; `decision:"block",reason` thay feedback/result, không undo tool. Code-mode nested promise rejects sau side effect; `continue:false` thay feedback nhưng không reject promise. |
| `Stop` | `turn_id,stop_hook_active:boolean,last_assistant_message:string|null` | Exit 0 cần JSON. `{}` cho stop; `decision:"block",reason` hoặc exit 2 tạo continuation prompt. `continue:false` takes precedence; matcher ignored. |

**Không emit** `continue`, `stopReason`, `suppressOutput` ở PreToolUse: docs nói run failed rồi tool **vẫn tiếp tục**. `updatedMCPToolOutput` không support ở PostToolUse; `suppressOutput` parsed nhưng chưa implement. Prompt/agent handlers parsed rồi skipped. Async hook không block/rewrite/steer triggering operation. SessionEnd advisory; Stop guard dùng `stop_hook_active`; numeric continuation cap không được trang này xác nhận. Linked `main` schema có thể ahead-of-release; page này là release behavior reference. Native app/CLI/tool/version evidence vẫn pending. [Direct official source](https://learn.chatgpt.com/docs/hooks).

## 5. Cursor

Nguồn: [Cursor hook reference](https://cursor.com/docs/hooks).

- Project target `.cursor/hooks.json`: `version:1,hooks.<lowerCamelEvent>:[handler]`; không nested matcher group kiểu Claude. Handler `command`, optional `type:"command"`, `timeout`, `matcher`, `failClosed`, stop-only `loop_limit`.
- Common input: `conversation_id,generation_id,model,hook_event_name,cursor_version,workspace_roots,user_email:string|null,transcript_path:string|null`; optional `model_id,model_params:[{id,value}]`.
- Exit 0 dùng JSON; permission hooks block malformed/schema-invalid output. Exit 2 deny. Crash/timeout/nonzero khác default fail-open; `failClosed:true` là documented override. `permission:"ask"` parsed nhưng chưa enforce tại preToolUse.

| Event | Additional input fields | Output |
|---|---|---|
| `sessionStart` | `session_id,is_background_agent,composer_mode?` | `env?,additional_context?`; fire-and-forget. `continue:false` không chặn session. |
| `beforeSubmitPrompt` | `prompt,attachments:[{type,file_path}]` | `continue:boolean,user_message?`. |
| `preToolUse` | `tool_name,tool_input,tool_use_id,cwd,agent_message?` | `permission:"allow"|"deny",user_message?,agent_message?,updated_input?`. |
| `postToolUse` | Same tool fields + `tool_output:string,duration:number` | `additional_context?`; MCP-only `updated_mcp_tool_output?`. `tool_output` là JSON-stringified result, không tự là object/raw terminal text. |
| `stop` | `status:completed|aborted|error,loop_count:number` | `{}` cho stop; `followup_message` nonempty auto-submits user message. NCKH không dùng field này. |

Stop per-script cap mặc định 5, `loop_limit:null` bỏ cap; giữ local one-reminder guard. Project hooks cần trusted workspace. Agent/Cmd+K khác Tab hooks. Cloud có pre/post/prompt/stop nhưng không sessionStart/sessionEnd, separate MCP hooks, Tab hooks hoặc workspaceOpen; early read-only turns không chạy hooks. Self-hosted workers có session boundary riêng. Vì vậy không suy IDE↔CLI↔cloud parity. [Cloud support và config](https://cursor.com/docs/hooks#cloud-agent-support).

## 6. Antigravity / AGY

Nguồn: [Antigravity hooks](https://www.antigravity.google/docs/hooks/).

- Target `.agents/hooks.json` đúng trên docs Antigravity 2.0, CLI và IDE. **Root là named groups**: `{ "<owned-group>": {enabled?:boolean,PreToolUse:...,PostToolUse:...,PreInvocation:...,PostInvocation:...,Stop:...} }`; không root `hooks`.
- Tool events dùng `[{matcher?,hooks:[handler]}]`. Invocation/Stop dùng **direct handler array**. Handler `command:string` required; `type:"command"` optional; `timeout:integer` optional/default 30s. Group `enabled` default true; inactive illustration đặt false.
- Common camelCase: `conversationId,workspacePaths:string[],transcriptPath,artifactDirectoryPath,modelName`. Không có documented `hook_event_name`, `cwd`, `session_id`; codec lấy event từ route/config do controller chọn.
- Chưa có documented SessionStart/SessionEnd/UserPromptSubmit tại trang này. PreInvocation là trước **mỗi model call**, không tương đương submitted user prompt.

| Event | Additional input fields | Output |
|---|---|---|
| `PreToolUse` | `toolCall:{name,args},stepIdx:integer` | `decision:allow|deny|ask|force_ask|deny_unless_prior_grant`, `reason?`, `permissionOverrides?:string[]`. NCKH deny không emit permissionOverrides. |
| `PostToolUse` | `toolCall,stepIdx,error?:string` | `{}`; không documented context/deny/rewritten-output fields. |
| `PreInvocation` | `invocationNum:integer,initialNumSteps:integer` | `injectSteps?:[{toolCall}|{userMessage}|{ephemeralMessage}]`; NCKH không inject toolCall hoặc userMessage. |
| `PostInvocation` | Same as PreInvocation | `injectSteps?`, `terminationBehavior:"force_continue"|"terminate"|""`. |
| `Stop` | `executionNum:integer,terminationReason:string,error?:string,fullyIdle:boolean` required | `decision:string` required: `"continue"` resumes; mọi giá trị khác cho stop. `reason?` nếu continue được inject như system message. |

PreToolUse hard deny là `decision:"deny"`. **Exit-code, crash, malformed-response, timeout outcome và numeric loop cap chưa được docs này quy định**: UNVERIFIED, không vay exit 2/stop_hook_active/failClosed từ host khác. Loop identifiers không là native cap; giữ owned idempotence/one-reminder, tránh continue/force_continue. Supported tools có `run_command,write_to_file,generate_image`; native surface/version/tool coverage vẫn pending. Common transcript location khác theo 2.0/CLI/IDE; không đọc transcript để đóng task này. [Input/output và schema](https://www.antigravity.google/docs/hooks/#input-and-output-contract).

## 7. Integration decisions và acceptance limits

| Integration point | Verified source fact | Cook consequence |
|---|---|---|
| Config merge | Ba host root `hooks`; AGY named groups; Cursor flat arrays; Claude/Codex nested groups | Bốn templates/codecs độc lập. Owned locator tương ứng từng shape; giữ unowned root/event members. |
| Preflight deny | Claude/Codex hookSpecificOutput; Cursor permission; AGY decision | Pure policy result không emit chung raw JSON; codec chọn exact native field. |
| Advisory pre-tool | Explicit allow có thể skip native approval ở Claude/AGY | Với allowed neutral policy, preserve normal native flow theo event; không dùng hook như authorization grant. |
| Post-tool | Side effect đã xảy ra; AGY only empty output | Không gọi post feedback là preventive enforcement. AGY advisory delivery qua post chưa có capability; giữ receipt/manual status. |
| Prompt/session | AGY invocation khác user prompt; Cursor session không block; cloud omissions | Unsupported event/surface là manual/not-callable/pending, không tự rename để giả parity. |
| Malformed/timeout | Khác nhau theo host/event/version; AGY unknown | Failure-path native matrix trước activation; controlled entrypoint vẫn synchronously stop trước side effect. |
| Stop loops | Claude/Codex block là continue; Cursor followup tự submit; AGY continue/force_continue | Default không emit continuation fields; bounded one reminder ghi receipt độc lập. |
| Packaging/trust | Draft bytes không registered/enabled/trusted | Giữ source package inactive; install/trust/native chạy là các gate riêng của controller. |

Không đóng native gate từ payload fixture: phải quan sát đúng host/version/surface/event với allow, deny, malformed input/output, timeout, crash, unsupported tool và duplicate project/plugin invocation. Deny preventive cần evidence side-effect absence; post receipts không thay thế.

Verification của report: companion JSON parse PASS; bốn selected local SHA-256 khớp bytes đọc; companion link và bốn source URL hiện diện. Không chạy native JSON/schema acceptance hay host commands từ ví dụ.

## Câu hỏi chưa đóng / concrete blockers

1. Native version/surface và tool coverage của bốn host: **UNVERIFIED**; task này chỉ docs/source comparison.
2. AGY failure/exit-code semantics và loop cap: **UNKNOWN** theo current official page; không được quảng cáo fail-closed.
3. Local K-Dense archive commit: **UNKNOWN**; selected path/hash/license đã verified, cần provenance owner bổ sung nếu release contract yêu cầu commit.
4. Real source/data rights, native editability/render/accessibility/scientific review và human acceptance: giữ gate của accepted plan; report không đánh giá artifact hay chạy hook.

Summary: Đã ghi exact selected visual/table path/hash/license/disposition và schema riêng của bốn host, cùng source URL/date, unsupported fields/surfaces và failure/loop limits.
Concerns/Blockers: Không có native hook receipt; AGY error semantics và upstream archive commit chưa xác minh. Không có blocker cho bounded comparison handoff.

