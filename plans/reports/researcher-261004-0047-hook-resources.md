# Rà soát hook/resource ClaudeKit cho kế hoạch NCKH giới hạn

As-of: 2026-10-04 Asia/Saigon. Chỉ đọc các archive dưới `resources/` và bốn
điểm tích hợp NCKH được chỉ định; không chạy source script, cài đặt, gọi mạng
hay ghi config. Archive không có `.git`, nên commit upstream là **unknown**;
chỉ có package version `claudekit-engineer 2.20.0` và `claudekit-marketing 1.4.0`.

## Kết luận ngắn

Không được sao chép hook/source ClaudeKit vào NCKH. Hai `LICENSE` thực tế đều
ghi proprietary/confidential, cấm copy/modify/distribute/use nếu không có license
mua hoặc permission bằng văn bản (`resources/claudekit-engineer-main/LICENSE:1-11`,
`resources/claudekit-marketing-main/LICENSE:1-11`); vì vậy package metadata ghi
`"license": "MIT"` (`resources/claudekit-engineer-main/package.json:16-29`,
`resources/claudekit-marketing-main/package.json:12-29`) là xung đột rights cần chặn, không
phải căn cứ để tái phân phối. Chỉ rút ra **mẫu hành vi**, rồi re-implement độc lập.

## Source manifest quyết định

SHA256 tính trên bytes hiện có; tám file dưới là toàn bộ file upstream được hash.

| File | Locators | SHA256 |
|---|---|---|
| `resources/claudekit-engineer-main/LICENSE` | 1-18 | `4C12181CA8DC84ED629CDFF11F0EC8A659EBC61E1B844BBF51136C6C2ABA0BAE` |
| `resources/claudekit-marketing-main/LICENSE` | 1-18 | `4C12181CA8DC84ED629CDFF11F0EC8A659EBC61E1B844BBF51136C6C2ABA0BAE` |
| `resources/claudekit-engineer-main/claude/settings.json` | 17-137 | `6501E93366E3CC43CC4EE6E28F732CB0A6E2E21BA66C7B24B938F99D84C30EB4` |
| `resources/claudekit-marketing-main/claude/settings.json` | 8-133 | `0D3D5480C72764D2819C912C73360C8B38514488F462163812652B523D71913A` |
| `resources/claudekit-engineer-main/claude/hooks/managed-hooks.json` | 1-15 | `8943A25AD32A9CA9DE63C5856EB4B47B510261CBA360E36B4F9274BE266406DB` |
| `resources/claudekit-engineer-main/claude/hooks/session-init.cjs` | 149-205, 213-255, 363-378 | `D875A63885A0821993E5C4EC48BCBE7D0CA023B5C0C300F27D58B732ABE707E4` |
| `resources/claudekit-engineer-main/claude/hooks/privacy-block.cjs` | 91-160, 163-187 | `2201764E710297DAB6F71ED7DC1B99D4C4EB8CEC3A357FE5B87BBB79D8E29500` |
| `resources/claudekit-engineer-main/claude/hooks/lib/transcript-parser.cjs` | 80-127, 138-239, 267-299 | `10C731AE15CE090DEC0F0275702563C529F8D287731A8EA785B590D921B61F74` |

Hai `THIRD_PARTY_NOTICES.md` còn nêu BSD-2-Clause imageio/imageio-ffmpeg và
GPLv3 FFmpeg (`resources/claudekit-engineer-main/claude/skills/THIRD_PARTY_NOTICES.md:7-41`,
marketing bản tương ứng:7-41). Không mang code/asset đó vào bundle NCKH; nếu
rights sau này được làm rõ vẫn phải giữ notice và kiểm tra copyleft riêng.

## Anatomy: entry → data → side effect

| Thành phần | Dữ liệu/đường vào | Hành vi và failure |
|---|---|---|
| Registry/wiring | `managed-hooks.json` được sinh từ `claude/settings.json` (`managed-hooks.json:1-15`); settings gọi `node .claude/hooks/*.cjs` trên SessionStart, UserPromptSubmit, Pre/PostToolUse, Subagent* và Stop (`engineer/claude/settings.json:17-137`) | Claude-specific, chạy ở subprocess boundary (suy ra đồng bộ theo `exit`); không phải registry trung lập. |
| `session-init` | JSON stdin, `CLAUDE_ENV_FILE`, cwd/session/transcript | Đọc config/git/team; ghi env và session state; warm statusline; startup còn dọn `.shadowed/` bằng rename/rm (`session-init.cjs:149-205`, `:213-255`, `:55-108`). Catch cuối log rồi exit 0/fail-open (`:363-378`). Không tái dùng phần cleanup. |
| `privacy-block` | JSON stdin `tool_name/tool_input`; đọc stdin tới EOF | Pure checker quyết định allow/warn/block; block exit 2 và in path/approval marker, malformed/crash fail-open exit 0 (`privacy-block.cjs:91-160`, `:163-187`). `AskUserQuestion`, prefix `APPROVED:` và format là Claude coupling. |
| `scout-block` | JSON stdin, `.claude/.ckignore`, cwd | Sync read; empty input exit 2, parse/shape lỗi fail-open; `checkScoutBlock` có block exit 2 (`scout-block.cjs:52-101`, `:103-162`). Pattern/baseline là policy riêng, không bê nguyên. |
| Artifact gate | Pointer/env/`plans/**/harness` và năm JSON artifact | `validator.cjs` đọc bounded files, kiểm schema, secret-like fields và policy (`validator.cjs:60-173`); wrapper emit advisory `additionalContext` cho soft stage, block cho hard stage, manual CLI strict, opt-in và emergency env disable (`workflow-artifact-gate.cjs:75-117`). Đây là mẫu tốt cho policy/helper tách khỏi adapter. |
| Transcript reader | JSONL transcript | Stream từng dòng, đếm malformed, trả partial; chỉ giữ 20 tool/10 agent nhưng `target` chứa path hoặc 30 ký tự đầu Bash (`transcript-parser.cjs:80-127`, `:138-239`, `:267-293`). Dùng làm ý tưởng bounded reader, không ghi raw transcript. |
| Logging/notification | Hook metadata; `.env` provider vars | `hook-logger` ghi target/error vào `.claude/hooks/.logs`, lock retry/busy-wait và rotate 1000→500 dòng (`resources/claudekit-engineer-main/claude/hooks/lib/hook-logger.cjs:14-20`, `:31-118`); notification tuần tự `fetch` tới provider và luôn exit 0 (`resources/claudekit-engineer-main/claude/hooks/notifications/notify.cjs:89-153`, sender:81-125). Đây là privacy/network side effect, loại khỏi NCKH. |

Marketing fork không phải baseline ổn định: settings đăng ký
`brand-guidelines-reminder.cjs`, `campaign-tracking.cjs`, `approval-workflow.cjs`,
`write-compact-marker.cjs`, `session-end.cjs` (`marketing/claude/settings.json:20-60`,
`:112-133`) nhưng các file này không tồn tại trong archive; không copy registry
này. Hai fork vẫn có toggle `isHookEnabled` với mặc định enabled
(`marketing/claude/hooks/lib/ck-config-utils.cjs:64-72`, `:777-815`), song đây
chỉ là config precedent, không phải bằng chứng enforcement.

## EXISTS / NEW / CONFLICT (tích hợp hẹp)

| Mục | Trạng thái | Quyết định plan |
|---|---|---|
| Pure access/artifact checks | EXISTS: `privacy-checker`, `scout-checker`, artifact validator | NEW: `nckh-kit/core/hook_policy.py` với kết quả `allow/advisory/block/pending`; độc lập, không nhập source ClaudeKit. Giữ `guards.py` cho structural/evidence contract (`nckh-kit/core/guards.py:1-43`). |
| Event registry | EXISTS: Claude settings + generated managed list | NEW: mapping tùy chọn trong adapter metadata; không auto-register. Bốn adapter hiện đều `hooks.state=not-installed`, enforcement “host permissions; no hook guarantee”, coverage unverified (`nckh-kit/adapters/claude/adapter.json:42-45`, `codex:54-57`, `cursor:51-54`, `agy:48-51`). |
| Host bridge | CONFLICT: upstream phụ thuộc `.claude`, Node, Claude event/payload/output | NEW chỉ khi có live host evidence: adapter mỏng đọc stdin, gọi pure policy, format host result. Codex/Cursor/AGY giữ `not-installed`; không suy ra parity. |
| Installer/native | EXISTS nhưng không có hook target: `install.py` chỉ plan/copy/symlink skill và native-agent, transaction/rollback theo ownership (`nckh-kit/core/install.py:124-254`, `:554-642`) | NEW slice không sửa `native.py` (chỉ encode agent host frontmatter/TOML: `nckh-kit/core/native.py:25-61`) và không cho installer copy hook. |
| Logging/telemetry | CONFLICT với private transcript/path/credential boundary | NEW mặc định không log raw input/path/command, không network; chỉ reason code + opaque hash nếu cần. |

## Đề xuất bounded, opt-in

1. Tạo pure `nckh-kit/core/hook_policy.py`: (a) phân loại đường dẫn/data class
   theo `public-tracked | external-archive | private/internal | holdout/credential`,
   (b) kiểm tra artifact có provenance/hash/access/rights và trả `pending` khi
   thiếu, không tự suy ra khoa học/Q1/human acceptance. Mặc định `enabled=false`,
   `mode=advisory`; chỉ hard-block explicit private/holdout policy.
2. Thêm test fixtures cho JSON stdin tối thiểu và adapter mapping, nhưng chưa
   đăng ký host. Adapter chỉ chuyển payload → policy → exit/JSON; không đọc
   transcript toàn phần, không ghi state/log, không gọi provider.
3. Sau approval riêng về rights và host contract, qualify Claude disposable
   project trước; chỉ khi có receipt thực tế mới đổi `hooks.state`/coverage.
   Không thay đổi guards/native/install trong slice đầu.

## Rủi ro, kiểm thử, rollback

- Rights/provenance: package MIT-vs-LICENSE proprietary và commit archive unknown
  là **NO-GO** cho copy/redistribution; giữ source chỉ làm evidence.
- Fail-open và host drift: unit-test malformed/empty payload, block/advisory/allow,
  idempotence, timeout/bounded input; test adapter không làm thay đổi file ngoài
  fixture. Static hashes không chứng minh enforcement.
- Privacy: assert không xuất raw path, command, transcript, env hay passphrase;
  không bật notification/network. Human/data-rights gate vẫn `pending`.
- Rollback: config off/no registry là mặc định; nếu đã wire trong disposable root,
  gỡ đúng file do adapter sở hữu, giữ user edits, khôi phục source-lock/ownership
  journal theo installer; không ghi global settings.

## Unresolved checks

1. Ai có written permission/licensing clarification để xử lý source ClaudeKit?
2. Host event/output contract và version nào được live-qualify cho từng adapter?
3. NCKH owner muốn hard-block lớp private/holdout nào, hay advisory-only?
4. Manifest/source-lock revision hiện hành và receipt coverage cần freeze trước khi
   đổi bất kỳ adapter state nào.

Status: DONE_WITH_CONCERNS
Summary: Đã lập inventory rights, event/data/side-effect anatomy và đề xuất policy helper trung lập, opt-in; upstream hook/source không đủ quyền để tái sử dụng và mọi enforcement host vẫn chưa được qualify.
Concerns/Blockers: LICENSE thực tế xung đột package metadata MIT; archive không có commit; marketing registry có lệnh trỏ tới file thiếu; cần written rights và live host receipts trước wiring.
