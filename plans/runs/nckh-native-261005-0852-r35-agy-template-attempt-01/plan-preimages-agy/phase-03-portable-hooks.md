---
title: "Phase 3: neutral deterministic portable hooks"
status: in-progress
---

# Phase 3: neutral deterministic portable hooks

## Outcome và data flow

Host event JSON → codec kiểm schema/size/event/tool/path → pure `hook_policy` đọc brief/artifact receipts bounded → `allow | advisory | block | pending | manual` → codec format exit/JSON/receipt theo host. Runner/codecs/templates/dependencies nằm trong portable package; module config riêng quản lý preview/apply/remove project-local. Manual entrypoint gọi cùng policy khi hook unavailable; hook không phải sandbox, scientific proof hay thay thế native permission.

## Điều kiện và contract

- [x] Package ghi `enabled=false`, `mode=advisory`, không đăng ký host config. Chỉ hard-block policy rõ ràng (private/holdout/credential, thiếu rights hoặc prohibited/non-research generation); warning/style không tự thành deny. Research-only workflow luôn giữ nguyên dù host chưa enforce.
- [x] Preflight kiểm task mode, project containment, quyền hiện có và research-purpose; pre-delivery kiểm source/locator/hash, protected-region delta, figure-data/mark map và stale QA; advisory chỉ góp ý writing/resource, không tự rewrite.
- [x] Không chạy shell/argv lấy từ payload, không đọc full transcript/raw draft, không gọi network/provider/nested LLM. Event/public receipt không ghi secret/raw path/command; private config transaction giữ exact owned target paths/hashes để rollback, không ghi nội dung bản thảo. Allowlist executable do controller sở hữu, input/output/timeout bounded, path traversal/symlink escape từ chối.
- [x] Idempotent theo session/task/artifact hash; atomic receipt khi cần, an toàn concurrent events; `Stop` tối đa một nhắc cho cùng artifact/violation, không auto-resubmit/giữ task vì taste suggestion.
- [x] Codec unknown/malformed/timeout/crash ghi degraded/failed; controlled entrypoint phải dừng trước side effect, uncovered host route giữ manual/not-callable. Native deny/failure tests phải chạy đúng event/version trước activation; không suy fail-closed của host từ policy return. Trust/install/native execution cần grant riêng, không dùng blanket bypass.

## File ownership (absolute paths)

Existing/reuse:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\guards.py:1-20,61-69` — factual/visual structural helpers; không nhồi host event policy vào đây.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\claude\adapter.json:42-55`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\codex\adapter.json:54-65`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\cursor\adapter.json:51-64`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\agy\adapter.json:48-61` — hook state/coverage hiện not-installed/unverified; chỉ cập nhật sau live receipt.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\install.py:124-254,554-642,714-791`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\paths.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\native.py:19-61` [REUSE/READ] — existing skill installer không merge hook JSON; tái dùng containment/locking/atomic primitives khi phù hợp, không tự mở rộng install thành cấp trust.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\build.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\installer\schemas\bundle-v2.schema.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\build\test_closure.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\resource\test_closure.py` [MODIFY] — thêm hooks source inventory, bounded manifest/closure/relocation/verification. P3 sở hữu phần hook trong build; P1 sửa identity trước, P4 mới freeze và chạy integrated build.
- Official capability evidence: `plans/reports/researcher-261004-0047-native-hook-capabilities.md:9-37`; ClaudeKit archive evidence/rights và side effects: `plans/reports/researcher-261004-0047-hook-resources.md:8-16,38-66`.

New:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\hook_policy.py` [NEW] — pure NCKH policy, no host imports; `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\hook-event.schema.json` và `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\hook-decision.schema.json` [NEW] — bounded neutral records.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\hooks\runner.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\hook-preflight.py` [NEW] — runner và bounded manual checker. Templates riêng [NEW]: `C:/Users/USER\Downloads\test-skill\nckh-kit\hooks\templates\claude.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\hooks\templates\codex.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\hooks\templates\cursor.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\hooks\templates\agy.json`; không có common host-config schema giả.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\hooks\codecs\claude.py`, `codex.py`, `cursor.py`, `agy.py` [NEW] — four thin codecs using each official host schema; no parity claim across surfaces.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\test_policy.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\test_runner.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\runtime\test_hook_adapters.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\fixtures\` [NEW]; adapter state changes and native receipts [MODIFY only after grant].
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\hook_config.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\configure-hooks.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\test_config.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\test_closure.py` [NEW, mandatory] — config transaction owner, entrypoint và conflict/relocation tests. Không sửa global config hoặc trust store.

## Package closure đã chọn

Thêm `hooks` vào `core/build.py::SOURCE_AREAS`; `_materialize_host` có per-host roots/dependency map rõ ràng cho runner, đúng codec/template, manual preflight, policy, guards, schema, paths và mọi local import/reference cần thiết. Mỗi member phải có source-lock pin và manifest `files` hash/source_path/source_sha256; thiếu import/schema/template, source drift, path escape hoặc extra file phải fail.

Bundle đặt runtime dưới `hooks/`, local dependencies dưới `hooks/_shared/`, giữ relative imports/refs chạy được khi relocate; manifest v2 thêm optional typed `hooks` record (host, entrypoint, codec, template, member paths, packaged-inactive và enabled/registered/trusted=false). Bundle v1 và v2 lịch sử không hooks vẫn đọc được; candidate mới bắt buộc có đúng bounded hook closure theo host, kể cả resource-off. Không nâng version hay sửa lock history chỉ để né compatibility.

Plugin projection mang cùng pinned closure dưới namespace inactive `plugin/references/nckh-hooks/`; không tạo auto-discovered active `hooks/hooks.json` hoặc đăng ký manifest khi chưa có grant. Khi activation được cấp quyền, template mới được materialize theo schema từng host; kiểm tránh project+plugin cùng chạy trùng definition. `verify_bundle` và schema kiểm cả standalone/projection, không suy packaged=registered=enabled=trusted. P4 smoke gọi packaged checker/runner bằng Python isolated từ ngoài repo, không đọc import từ checkout/PYTHONPATH.

## Hook-config transaction contract

CLI **dự kiến** `scripts/configure-hooks.py` có `preview`, `apply`, `remove`; preview nhận explicit project/host/package và action, chỉ xuất transaction. Apply/remove nhận đúng preview hash đã duyệt, không coi file preview là authorization. Module không dùng skill install operation để ngầm sửa hooks.

| Host | Exact project-relative config target | Owned JSON surface |
|---|---|---|
| Claude | `.claude/settings.local.json` | Chỉ definition trong `hooks.<Event>[]` và nested handlers do NCKH tạo; không chiếm toàn bộ `hooks` |
| Codex | `.codex/hooks.json` | Definition/event/matcher được codec tạo theo schema Codex; trust-definition hash do host/user quản lý |
| Cursor | `.cursor/hooks.json` | NCKH definitions trong `hooks.<event>[]`; giữ `version` và mọi entry không sở hữu |
| AGY | `.agents/hooks.json` | NCKH event/group definitions theo schema AGY; không đụng shared `.agents/skills` hoặc agents |

Target Claude/Cursor đối chiếu [Claude hook locations](https://code.claude.com/docs/en/hooks#hook-locations) và [Cursor project config](https://cursor.com/docs/hooks); Codex/AGY theo capability record (historical evidence path: `../reports/researcher-261004-0047-native-hook-capabilities.md`; unavailable in the cleaned checkout). Không tìm/ghi global fallback. Host/surface/version không xác nhận target/schema thì chỉ preview/manual.

Transaction phải có canonical project/config path, resolved parent identity/hash, raw config preimage hash (hoặc explicit absent), owned definition IDs nội bộ `nckh:<host>:<event>:<policy>`, JSON pointer/member locator, old/new definition hashes, package closure hash và exact operations. IDs nằm trong receipt nội bộ, không chèn field host không hỗ trợ. Runtime files được stage hash-verified vào `<project>/.nckh-state/hooks/<host>/<closure-hash>/`; config chỉ trỏ stable owned payload, không trỏ output/temp build dễ mất.

Preview không ghi config/runtime. Apply lấy project/config transaction lock, re-resolve parent/no-links, đọc và compare preimage/definition/package hashes ngay trước atomic write; changed-after-preview, malformed/duplicate JSON, unknown ownership, target collision hoặc unsupported locking đều trả no-write/conflict và yêu cầu preview mới. Preserve unknown/unowned members; không giữ lock chỉ bằng suy đoán, không xây merge service. Chỉ bật selected events khi grant nêu rõ activation; không tự trust, publish hay bật provider.

Stage payload trước config, journal trạng thái cho partial failure; config write thất bại chỉ cleanup staged owned matching files. Remove/rollback dựa fresh preview/current hash: chỉ gỡ matching owned definitions, giữ sửa đổi/unowned entries mới và shared `.agents`; owned block bị sửa trả rollback-conflict, không restore toàn file backup đè người dùng. Xóa file config chỉ khi chính transaction tạo file và còn đúng toàn bộ hash; runtime file còn được definition tham chiếu không được xóa.

## Tasks

- [x] Define neutral event/decision schemas with bounded byte count, fields, timeout and reason codes; reject JSON payload as authorization/grant.
- [x] Implement policy composition by reusing P1 fidelity and P2 purpose/artifact guards; preserve `manual/advisory/not-callable` status and entrypoint checks when no hook is installed.
- [x] Implement four codecs from official schemas: Claude session/prompt/tool/stop with stop-loop guard; Codex project hook/trust-definition hash and local-tool scope; Cursor JSON/failClosed only where supported; AGY workspace hook/surface-specific routes. Do not copy ClaudeKit/Anthropic restricted document skills.
- [x] Implement bounded package closure/schema/build verification theo contract trên; source-lock vẫn bất biến đến P4, package tests cần lock được xếp sau freeze.
- [x] Implement `hook_config.py`/`configure-hooks.py` preview/apply/remove và isolated tests: changed config after preview, malformed/duplicate JSON, conflicting IDs, payload/config partial failure, concurrent attempts, user edits sau install, shared Codex/AGY paths, remove/rollback conflict. Apply/trust là grant riêng; test dùng disposable owned project, không cấu hình máy thật.
- [ ] Record host evidence per surface/version/event; unsupported surface remains pending/unverified rather than narrowing the advertised kit target or claiming four-host parity.

## Validation gates

Focused existing lock-independent command: `python -B -m unittest tests.runtime.test_adapters tests.evidence.test_guards -v` (cwd `C:/Users/USER\Downloads\test-skill\nckh-kit`). New mandatory unit tests: `python -B -m unittest tests.hooks.test_policy tests.hooks.test_runner tests.hooks.test_config tests.runtime.test_hook_adapters -v`; pure policy/config tests không gọi source build/lock. `tests.hooks.test_closure` và packaged config integration chạy ở P4 sau freeze, không bypass guard ở P3. CLI/schema/codecs đã có; full deterministic và extracted checks được ghi ở checkpoint bên dưới.

Native matrix bắt buộc cho mỗi enabled event/version/surface: allow, policy-deny, malformed input/output, timeout, crash, unsupported event/tool và duplicate project/plugin invocation. Record actual host response, side-effect absence khi deny, cleanup và definition/trust hashes; nếu host fail-open hoặc tool không covered thì ghi limitation/manual/not-callable, không kích hoạt route đó như enforcement. Payload fixtures hay post-delivery receipts không thay native preventive evidence.

## Risk và rollback

Risk: hook becomes implicit authority or fail-open safety boundary (L4×I5=20); mitigate off-by-default, explicit decision classes, manual fallback and host sandbox authority. Risk: config merge destroys shared/user edits (L3×I5=15); hash-bound owned blocks, invalid-json untouched, preview and transaction rollback. Risk: proprietary/unknown archive copied (L2×I5=10); reimplement behavior from public schemas only and retain rights conflict as no-copy evidence. Concurrency/stop loops (L3×I4=12); idempotence, atomic receipts and one-stop rule.

Rollback removes only owned hook blocks/files whose current hashes match the receipt; keeps later user edits, shared `.agents` definitions, old adapter unverified state and failed receipts. If a codec is unqualified, disable that host route and retain manual entrypoint; never mark it installed to close the gate.

## Measurable exit

Pure policy/manual runner/config transaction có bounded deterministic tests; bốn codecs dùng đúng schema riêng; ownership/hash conflict tests preserve user state. Package closure r29 đã build/extract và gọi entrypoints từ outside CWD; evidence class là local portability observation. Draft giữ inactive, không raw transcript/network/shell payload behavior; live enforcement chỉ đổi trạng thái sau grant và native failure-path evidence tương ứng.

<!-- Updated: Validation Session 2 - approved A1 A3 A4 A9; plan-only -->

## Execution checkpoint — r29

Full deterministic (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic.json`; unavailable in the cleaned checkout) đạt 181 tests, một Windows symlink skip. Extracted smoke (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/smoke-summary.json`; unavailable in the cleaned checkout) kiểm 24 primary/reference projections cho runner/manual/config preview, với disposable project bytes giữ nguyên. Delivery (historical evidence path: `../reports/delivery-261004-1037-r29-local-candidate.md`; unavailable in the cleaned checkout) ghi exact closure, config transaction tests/recovery và limits. Native event/version/surface failure-path evidence còn unchecked: official schema và codec fixture không thay actual host response; registration/activation/trust vẫn cần grant riêng.

## Current checkpoint — r30 native observations

Human grant (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/native-grant.json`; unavailable in the cleaned checkout) đã đến; registration/trust đúng definitions thử và cleanup đã được cấp quyền. Current delivery (historical evidence path: `../reports/delivery-261004-1707-r30-native-checkpoint.md`; unavailable in the cleaned checkout) giữ exact version/surface/event ledger; source-lock r30/281 pins chỉ sửa ba files do lỗi Claude Windows command-string mất backslashes. Claude dùng executable + `args`; focused hooks 21/21 và full unchanged deterministic suite 182 tests (`OK`, một symlink skip) sau freeze.

Claude r30 (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/native-r30-claude-summary.json`; unavailable in the cleaned checkout) thực sự gọi runner từ archive/extracted payload qua `SessionStart`: direct, normal/advisory, policy-block-as-context, malformed input/output, injected sleeper, crash exit17, unsupported codec event và duplicate project/plugin. Host `--init-only` exit0; duplicate có hai callbacks và một idempotent policy receipt. Chưa có tool prevention oracle hoặc model turn; không gọi startup observations là full native matrix.

Codex CLI 0.154.0 nhận project hooks và hai definition trust hashes; specialized local shell không tạo callback. Cursor CLI 2026.09.15-d2fe57e dừng ở authentication. AGY CLI 1.2.16 dừng ở eligibility khi proxy loopback từ chối network. Codex Desktop/IDE, Cursor IDE, AGY IDE vẫn chưa có live event receipts; không đổi advertised targets hoặc ghi unsupported từ account error. Một task native evidence vẫn unchecked.

Cleanup (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/native-cleanup.json`; unavailable in the cleaned checkout) gỡ matching configs và 362 staged payload members trong 14 project thử. Codex native metadata (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/codex-native-cleanup-observation.json`; unavailable in the cleaned checkout) xác minh hai test hooks disabled; trusted hashes/project trust có thể còn lưu. Không còn project config/payload để gọi; không sửa trực tiếp global trust store. Production `configure-hooks.py apply` chưa gọi, activation inactive. Tiếp tục preventive events cần native model turns/budget và host/account/surface prerequisites tương ứng.

## Continuation — Codex prompt admission

Addendum (historical evidence path: `../reports/delivery-261004-1707-r30-prompt-admission.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261004-1707-r30-prompt-admission.json`; unavailable in the cleaned checkout) giữ hai native observations mới trên Codex CLI 0.154.0/r30/UserPromptSubmit. Packaged runner tạo `block/bounded-input-exceeded`, host báo hook `blocked`, turn kết thúc với `items=[]`; nhánh advisory hoàn tất hook rồi gặp loopback connection failure, chưa có final turn notification trong cửa sổ 8 giây. Không có tool-side-effect oracle/model success hoặc full failure matrix.

Normal UI trust riêng đúng project definition mới; 27 global hooks và ba configured MCP servers tắt theo invocation, builtin `cua_repl` vẫn báo ready nhưng không được gọi. Sau thử, normal UI disable đúng hash; gỡ một matching config và 26 staged payload members; host list không còn project hook callable. Unrelated native hook-state hash giữ nguyên. Ba test hashes trusted/disabled còn lưu, project trust có thể còn lưu; process audit không thấy matching run process. Source r30 và checkbox native chưa đổi.

## Continuation — Codex prompt failure paths

Bảy native callbacks (historical evidence path: `../reports/delivery-261004-1707-r30-prompt-failures.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261004-1707-r30-prompt-failures.json`; unavailable in the cleaned checkout) dùng declared fault injection sau genuine UserPromptSubmit callback trên Codex CLI 0.154.0/r30. Policy deny và injected malformed runner input có native `blocked` và empty-items completed turn. Malformed output, 2-second timeout, intentional observer crash và unsupported selected codec đều native `failed`, rồi host vẫn thử provider refused-loopback. Unsupported codec có deterministic degraded block receipt nhưng không được host enforce; không đổi receipt thành native PASS.

Giữ route inactive/manual; còn duplicate project/plugin, unsupported native tool, PreToolUse prevention và event/surface gates khác. Trust/enable riêng observer qua normal UI, disable rồi gỡ matching config/26 payload members. Native store còn ba project-test keys disabled; hash UserPromptSubmit cũ được thay bằng observer hash, không có bốn current trusted hashes. Unrelated user-state hash không đổi; final audit có 0 matching run processes. Source/tests/build không đổi, checkbox native còn unchecked.

## Continuation — native model/tool turns

Model grant (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/model-medium-grant.json`; unavailable in the cleaned checkout) cho phép `gpt-5.6-luna` hoặc `gpt-6.1-sol`, mức `medium`; cả hai có trong native model/list. Model/tool checkpoint (historical evidence path: `../reports/delivery-261004-1707-r30-model-tools.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261004-1707-r30-model-tools.json`; unavailable in the cleaned checkout) ghi tám completed `gpt-5.6-luna/medium` turns, tám genuine PreToolUse callbacks trên Codex CLI 0.154.0 Windows app-server/stdio model unifiedExecStartup. Native matcher/tool là Bash. Trust/enable riêng đúng definition `sha256:f26dcc9290135bcf225d52cdff4a72130753dc33758b46a5ebf2a5b314e71206` qua normal TUI.

Allow thực sự tạo tệp oracle; policy deny `plan-only-mutation` và injected malformed runner input có native blocked, không completed command item và không có tệp. Malformed output, 2-second timeout, observer crash và unsupported selected codec đều native failed rồi shell vẫn exit0/tạo tệp: bốn fail-open cases. Bash thiếu controller mapping trả manual và host tiếp tục. Injections xảy ra sau callback; không gọi chúng là native host phát malformed/unknown event hoặc unsupported tool.

Mỗi lượt effective metadata xác nhận medium, 27 user hooks/ba configured MCP servers/13 plugins disabled theo invocation. Thread không fallback model khác; gateway backend model attestation và provider billing chưa observed. Bash chỉ có tool_input.command, không structured file_path/path; chưa chứng minh protected-path blocking từ thí nghiệm này. Duplicate project/plugin, các event còn lại và direct TUI/Desktop/IDE tracks chưa được qualified; checkbox native vẫn unchecked.

Cleanup mới (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/projects/codex-model/tool-probe-cleanup.json`; unavailable in the cleaned checkout) sau normal UI disable đã gỡ matching config/26 staged members. Native list không còn project hook callable; key mới trusted/disabled cộng ba keys lịch sử là bốn disabled keys trong hai projects. Unrelated state giữ nguyên, final process audit (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/process-audit-model-tools-final.json`; unavailable in the cleaned checkout) không có matching run processes. Host preflight (historical evidence path: `../runs/nckh-native-261004-1707-attempt-01/host-model-grant-prerequisites.json`; unavailable in the cleaned checkout) xác nhận Cursor CLI chưa đăng nhập; AGY models qua kết nối thật exit0 nhưng không liệt kê hai GPT models được phép, prompt eligibility/native coverage chưa thử. Source-lock r30, tests, archives và installed r25 giữ nguyên.

## Current continuation — r31–r34

Current source/revalidation checkpoint (historical evidence path: `../reports/checkpoint-261005-0005-r34-running.md`; unavailable in the cleaned checkout) ghi native Cursor/Grok 4.7 500K Extra High và AGY/Gemini 3.8 Flash medium grants đã sử dụng. AGY permission shape và native file fields đã sửa; r33 protected file read/write và project + workspace-plugin duplicate đạt. R34 receipt-parent repair đang revalidate. Historical native bindings giữ đúng packaged revision; per-event/surface task vẫn unchecked, không thu hẹp targets hoặc activation route.

## Current delivery — r34 native observations

Delivery r34 (historical evidence path: `../reports/delivery-261005-0005-r34-cursor-agy.md`; unavailable in the cleaned checkout) và bindings (historical evidence path: `../reports/delivery-261005-0005-r34-cursor-agy.json`; unavailable in the cleaned checkout) supersede running checkpoint bằng completed local checks. Full r34 đạt 187 tests, một Windows symlink skip. AGY r34 đạt ba native file cases và project/workspace-plugin duplicate; event fault run có 25 attempts, status `recorded-genuine-callbacks`. Cursor current allow tạo marker; duplicate có hai same-tool callbacks/một policy receipt nhưng native host vẫn báo timeout, không gọi qualified.

Current matching test files đã cleanup; final process audit zero matching task processes. Grants đã có, không hỏi lại; installed r25 giữ nguyên. Task host evidence per surface/version/event vẫn unchecked: latest report ghi source/version/event bindings và các Claude/Codex/Cursor/direct app gaps. Fault injection là controller-owned sau native callback thật; post-event side-effect timing giữ riêng. Historical r30–r33 receipts không regrade thành r34.

## Current continuation — r34 Codex CLI events

Codex addendum (historical evidence path: `../reports/delivery-261005-0052-r34-codex-events.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261005-0052-r34-codex-events.json`; unavailable in the cleaned checkout) ghi unchanged r34/281 pins trên Codex CLI 0.154.0 **exec** route với GPT-5.6 Luna medium. Inline `sessionFlags` definitions bypass hook-definition trust cho invocation; native CLI tự persist exact own workspace/project trust key, controller không direct-write global. App-server attempt tạo oracle nhưng không gọi hook; discovery/source-enum/collector failures được giữ riêng.

CLI allow tạo đúng oracle; policy deny ở PreToolUse không có shell execution hoặc oracle. Matching project file + inline definitions có hai callbacks/event; bỏ matching file còn một. Duplicate hai inline groups có hai same-tool PreToolUse callbacks, một idempotent receipt và một tool execution; project/plugin route chưa qualified.

25 injected faults sau genuine callbacks cover SessionStart, UserPromptSubmit, PreToolUse, PostToolUse và Stop. Malformed input ở prompt/pretool chặn marker; malformed output, timeout, crash và unsupported selected codec ở pretool vẫn cho shell tạo marker. PostToolUse/Stop observations diễn ra sau side effect. Không dùng marker hoặc CLI exit0 làm universal PASS, không gọi unknown codec injection là native unsupported-tool evidence; template/production timing vẫn cần observation riêng.

Cleanup gỡ 26 matching payload members; config đã park vào evidence, unrelated parsed global state unchanged sau khi bỏ own native trust key chỉ trong memory; post-cleanup audit zero matching task processes. Initial cleanup từ chối Windows receipt path trước mutation, helper normalization được sửa với preimages/failure record và containment/hash checks giữ nguyên. Native checkbox vẫn unchecked. Claude model/effort chưa có reply. Normal UI trust action bị automatic approval review từ chối và không chạy; native CLI route sau đó tự persist own workspace trust. Trust correction (historical evidence path: `../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json`; unavailable in the cleaned checkout) giữ report/helper preimages và unchanged native cleanup receipt; existing trusted scratch project được reuse theo native grant, thêm trust keys mới chưa authorized.

## Current continuation — r34 Cursor CLI events

Cursor addendum (historical evidence path: `../reports/delivery-261005-0128-r34-cursor-events.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261005-0128-r34-cursor-events.json`; unavailable in the cleaned checkout) ghi 20 completed native turns với exact Grok 4.7 500K Extra High selector trên CLI `2026.09.15-d2fe57e`, dangerous flags đúng existing grant; packaged source r34 không đổi. Native callbacks có legacy model strings nhưng thiếu `model_id`/`model_params`; không backend/billing attestation.

Allow tạo marker; policy deny rejected với `plan-only-mutation`, marker absent; deliberately uncovered controller mapping trả manual và host thực thi Shell. Actual callbacks cover sessionStart/preToolUse/postToolUse; beforeSubmitPrompt/stop có zero callbacks trong các configured turns, vẫn unobserved/pending trên route này. 15 declared faults cover ba observed events; năm pretool faults đều native rejected và không marker. Post-tool faults sau side effect; sessionStart faults vẫn cho tool thực thi. Selected timeout2s/sleeper8s có thể để observer hoàn tất sau native timeout; callback success không thay tool result.

Hai new project + transient-plugin duplicates đều có hai same-tool callbacks, một policy receipt, một Shell success/oracle; distinct source argument cho explicit project/plugin provenance. Historical 20s timeout giữ nguyên; chưa xác định root cause hoặc chứng minh hết intermittent failure. Existing global hooks không tắt do observed CLI help không có isolation flag; native environment và matching protected hashes được bind.

Cleanup ba owned projects gỡ 82 matching files; no global plugin installation, configs/payload/plugin không callable và final process audit zero matching task processes. Old exec handle missing ở recovery được reconcile qua terminal native receipts/cleanup/process inventory, không restart. Native checkbox vẫn unchecked; full surface/version/event scope giữ nguyên.

## Current source — r35 native patch-path repair

Native file failure (historical evidence path: `../reports/delivery-261005-0658-r34-codex-file-failure.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261005-0658-r34-codex-file-failure.json`; unavailable in the cleaned checkout) giữ bốn genuine `apply_patch` turns. Allow tạo file, plan-only policy deny chặn file, mapping absent trả manual/host thực thi. Protected private marker đã được tạo: r34 common codec chỉ đọc file_path/path nhưng actual tool_input.command chứa exact patch text. Native command hash khớp controller patch; đây là actual bypass, không fault injection.

R35 source checkpoint (historical evidence path: `../runs/nckh-native-261005-0710-r35-attempt-01/source-checkpoint.json`; unavailable in the cleaned checkout) sửa codex codec đọc bounded canonical add/update/delete/move headers, checks source/destination/aliases và giữ containment/protected-path rules. Không execute hoặc export patch body; shell targets vẫn unqualified. Three regressions trước sửa có 22 failures; 12 focused tests sau sửa PASS. Current r35 full/package revalidation đang chạy ở pipeline receipt (historical evidence path: `../runs/nckh-native-261005-0710-r35-attempt-01/revalidation-summary.json`; unavailable in the cleaned checkout); r35 native retest pending, historical r34 observations không regrade.

Native Codex dangerous file run persist đúng own project trust key. Parsed state sau khi bỏ key đó chỉ trong memory khớp baseline; controller không ghi trực tiếp global file. Original cleanup hash assertion fail được giữ. Repaired helper đã gỡ 26 payload files nhưng stalled trước receipt, root cause chưa xác định; exact owned PID53752/time được kiểm, clean stop rejected và force stop succeeded. Filesystem reconciliation xác minh all26 absent/config không callable; process audit zero matching. Native own trust và failures giữ nguyên. Không suy hook-trust invocation bypass đồng nghĩa không persist project trust.


## Current delivery — r35 native canonical patch retest

Delivery (historical evidence path: `../reports/delivery-261005-0710-r35-patch-retest.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261005-0710-r35-patch-retest.json`; unavailable in the cleaned checkout) bind four genuine Codex CLI 0.154.0 exec turns using GPT-5.6 Luna medium and verified extracted r35 payload. The existing native-trusted r34 file project was reused with a new evidence namespace. Callback command hashes matched each requested patch exactly. Allow/manual created markers; plan-only and private-path policy blocks had no completed file change and no marker. This verifies the repaired canonical add-file route; Eight further genuine attempts verified public update/delete/move; private update/delete, moves with private source or destination, and mixed public/private add were blocked before requested changes. Native command hashes matched each requested patch, and actual before/after hashes matched the outcomes. Shell targets, plugin duplicates and other surfaces retain their pending/manual status.

Cleanup removed 26 matching payload members, preserved historical project hashes and raw global config/hook hashes, added zero trust keys, and final process audit found zero matching task processes. Static cleanup helper review (historical evidence path: `../runs/nckh-native-261005-0658-r34-codex-file-attempt-01/cleanup-helper-review.json`; unavailable in the cleaned checkout) repairs receipt variable shadowing; no global overwrite was observed and the prior stall cause is not proven by its retained trace. Earlier native receipts remain unchanged. Full native checkbox remains unchecked.

## Current continuation — r35 Cursor file stages và template timing

Cursor file addendum (historical evidence path: `../reports/delivery-261005-0746-r35-cursor-files.md`; unavailable in the cleaned checkout) / bindings (historical evidence path: `../reports/delivery-261005-0746-r35-cursor-files.json`; unavailable in the cleaned checkout) bind 19 native turns trên CLI `2026.09.15-d2fe57e`, exact Grok4.7/500k/xhigh selector và verified extracted r35 payload. File allow/plan-only-deny/private/manual và native Read outcomes đã đối chiếu. Một outer edit có thể tạo Read rồi Write callbacks cùng tool ID; duplicate project/plugin có hai callbacks mỗi stage nhưng hai idempotent receipts tổng cộng. Năm original faults dừng ở Read; năm supplemental faults chọn đúng Write, native error và marker absent.

Supplemental timeout đầu dừng ở normal Read, không đưa lỗi tới Write; failure giữ riêng. Direct packaged runner với template5s, không observer/injection, bị native timeout và không marker dù policy allow; timing route chưa qualified và nguyên nhân timeout còn mở. Bốn batches cleanup 106 matching members, giữ historical project hashes và có zero matching process ở từng final audit. Protected hook/MCP/plugin config hashes không đổi; global CLI config before/after hashes khác và không bị gọi unchanged. Source r35, owner samples và native checkbox giữ nguyên.
