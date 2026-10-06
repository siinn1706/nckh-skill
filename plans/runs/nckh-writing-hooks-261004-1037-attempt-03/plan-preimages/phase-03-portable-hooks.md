---
title: "Phase 3: neutral deterministic portable hooks"
status: pending
---

# Phase 3: neutral deterministic portable hooks

## Outcome và data flow

Host event JSON → codec kiểm schema/size/event/tool/path → pure `hook_policy` đọc brief/artifact receipts bounded → `allow | advisory | block | pending | manual` → codec format exit/JSON/receipt theo host. Runner/codecs/templates/dependencies nằm trong portable package; module config riêng quản lý preview/apply/remove project-local. Manual entrypoint gọi cùng policy khi hook unavailable; hook không phải sandbox, scientific proof hay thay thế native permission.

## Điều kiện và contract

- [ ] Package ghi `enabled=false`, `mode=advisory`, không đăng ký host config. Chỉ hard-block policy rõ ràng (private/holdout/credential, thiếu rights hoặc prohibited/non-research generation); warning/style không tự thành deny. Research-only workflow luôn giữ nguyên dù host chưa enforce.
- [ ] Preflight kiểm task mode, project containment, quyền hiện có và research-purpose; pre-delivery kiểm source/locator/hash, protected-region delta, figure-data/mark map và stale QA; advisory chỉ góp ý writing/resource, không tự rewrite.
- [ ] Không chạy shell/argv lấy từ payload, không đọc full transcript/raw draft, không gọi network/provider/nested LLM. Event/public receipt không ghi secret/raw path/command; private config transaction giữ exact owned target paths/hashes để rollback, không ghi nội dung bản thảo. Allowlist executable do controller sở hữu, input/output/timeout bounded, path traversal/symlink escape từ chối.
- [ ] Idempotent theo session/task/artifact hash; atomic receipt khi cần, an toàn concurrent events; `Stop` tối đa một nhắc cho cùng artifact/violation, không auto-resubmit/giữ task vì taste suggestion.
- [ ] Codec unknown/malformed/timeout/crash ghi degraded/failed; controlled entrypoint phải dừng trước side effect, uncovered host route giữ manual/not-callable. Native deny/failure tests phải chạy đúng event/version trước activation; không suy fail-closed của host từ policy return. Trust/install/native execution cần grant riêng, không dùng blanket bypass.

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

- [ ] Define neutral event/decision schemas with bounded byte count, fields, timeout and reason codes; reject JSON payload as authorization/grant.
- [ ] Implement policy composition by reusing P1 fidelity and P2 purpose/artifact guards; preserve `manual/advisory/not-callable` status and entrypoint checks when no hook is installed.
- [ ] Implement four codecs from official schemas: Claude session/prompt/tool/stop with stop-loop guard; Codex project hook/trust-definition hash and local-tool scope; Cursor JSON/failClosed only where supported; AGY workspace hook/surface-specific routes. Do not copy ClaudeKit/Anthropic restricted document skills.
- [ ] Implement bounded package closure/schema/build verification theo contract trên; source-lock vẫn bất biến đến P4, package tests cần lock được xếp sau freeze.
- [ ] Implement `hook_config.py`/`configure-hooks.py` preview/apply/remove và isolated tests: changed config after preview, malformed/duplicate JSON, conflicting IDs, payload/config partial failure, concurrent attempts, user edits sau install, shared Codex/AGY paths, remove/rollback conflict. Apply/trust là grant riêng; test dùng disposable owned project, không cấu hình máy thật.
- [ ] Record host evidence per surface/version/event; unsupported surface remains pending/unverified rather than narrowing the advertised kit target or claiming four-host parity.

## Validation gates

Focused existing lock-independent command: `python -B -m unittest tests.runtime.test_adapters tests.evidence.test_guards -v` (cwd `C:/Users/USER\Downloads\test-skill\nckh-kit`). New mandatory unit tests: `python -B -m unittest tests.hooks.test_policy tests.hooks.test_runner tests.hooks.test_config tests.runtime.test_hook_adapters -v`; pure policy/config tests không gọi source build/lock. `tests.hooks.test_closure` và packaged config integration chạy ở P4 sau freeze, không bypass guard ở P3. Tên file/CLI mới là contract dự kiến, chưa tồn tại.

Native matrix bắt buộc cho mỗi enabled event/version/surface: allow, policy-deny, malformed input/output, timeout, crash, unsupported event/tool và duplicate project/plugin invocation. Record actual host response, side-effect absence khi deny, cleanup và definition/trust hashes; nếu host fail-open hoặc tool không covered thì ghi limitation/manual/not-callable, không kích hoạt route đó như enforcement. Payload fixtures hay post-delivery receipts không thay native preventive evidence.

## Risk và rollback

Risk: hook becomes implicit authority or fail-open safety boundary (L4×I5=20); mitigate off-by-default, explicit decision classes, manual fallback and host sandbox authority. Risk: config merge destroys shared/user edits (L3×I5=15); hash-bound owned blocks, invalid-json untouched, preview and transaction rollback. Risk: proprietary/unknown archive copied (L2×I5=10); reimplement behavior from public schemas only and retain rights conflict as no-copy evidence. Concurrency/stop loops (L3×I4=12); idempotence, atomic receipts and one-stop rule.

Rollback removes only owned hook blocks/files whose current hashes match the receipt; keeps later user edits, shared `.agents` definitions, old adapter unverified state and failed receipts. If a codec is unqualified, disable that host route and retain manual entrypoint; never mark it installed to close the gate.

## Measurable exit

Pure policy/manual runner/config transaction có bounded deterministic tests; bốn codecs dùng đúng schema riêng; ownership/hash conflict tests preserve user state. Package closure implementation đã khai báo đủ và chờ P4 freeze/build/extracted verification; chưa coi là packaged PASS ở P3. Draft giữ inactive, không raw transcript/network/shell payload behavior; live enforcement chỉ đổi trạng thái sau grant và native failure-path evidence tương ứng.

<!-- Updated: Validation Session 2 - approved A1 A3 A4 A9; plan-only -->
