# Hook runtime: bằng chứng tài liệu và giới hạn

Đọc ngày 04/10/2026, Asia/Saigon. Chỉ là capability theo tài liệu; **chưa cấu hình, trust hoặc chạy hook NCKH**.

## Hiện trạng tại workspace

Bốn file `nckh-kit/adapters/{claude,codex,cursor,agy}/adapter.json` đều ghi `not-installed` và `coverage: unverified`. `core/guards.py` có kiểm tra structural độc lập nhưng chưa có event dispatcher tương ứng. `codex --version` trả `codex-cli 0.154.0` kèm cảnh báo không dọn/ghi được temp PATH alias; không chỉnh quyền hoặc cấu hình để giấu cảnh báo. Version CLI không chứng minh capability của app đang mở.

## Nguồn chính thức

| Host | Điều tài liệu xác nhận | Điều phải kiểm ở implementation |
|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/hooks) | Có session/prompt/tool/stop events; handler nhận JSON; `PreToolUse` có đường block. `stop_hook_active` cần kiểm để tránh tiếp tục vô hạn. | Đúng event/schema trên bản cài, Windows command quoting, hook trust và tool coverage thực; không coi hậu kiểm là ngăn được side effect đã xảy ra. |
| [Codex](https://learn.chatgpt.com/docs/hooks) | Đọc hook tại config layers; project `.codex/hooks.json` là một route. Non-managed hook phải được người dùng trust đúng definition hash. Có `PreToolUse`/`PostToolUse` cho nhiều local tools; hosted tools có ngoại lệ. | Không đoán tên event từ Claude. Kiểm native matcher/denial, thay definition mất trust, lớp project và plugin có thể cùng chạy. `write_stdin` không phải preflight mới của lệnh cũ. |
| [Cursor](https://cursor.com/docs/hooks) | Command hooks nhận/trả JSON; có `preToolUse`, shell/MCP events và `stop`. Crash/timeout và nhiều exit-code mặc định có thể fail-open; tài liệu nêu `failClosed` cho permission hooks. | Chỉ dùng `failClosed` ở hook/event/version thực hỗ trợ, thử lỗi và timeout; không suy CLI giống IDE. Giới hạn stop follow-up để không tạo loop. |
| [Antigravity](https://www.antigravity.google/docs/hooks/) | Workspace `.agents/hooks.json`; schema nhóm hook/event gồm `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`, các surface có route khác nhau. | Kiểm tab/surface/version đúng; không đổi `PreInvocation` thành tự gọi tool hoặc chèn user authorization. Chưa có native evidence NCKH. |

[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) còn phân biệt packaged, installed, enabled và trusted. Xuất `hooks/hooks.json` trong plugin không tự cài script vào execution host hoặc cấp trust.

## Hợp đồng đề xuất

Một neutral checker nhận task brief đáng tin, danh sách artifact được cho phép, registry/claims/receipts và trả structured decision. Host adapters chỉ chuẩn hóa input/output, không chứa bốn bản policy.

1. **Preflight:** task mode, project containment, quyền đang có và research-purpose của thao tác tạo hình. Không coi JSON do source/bản thảo tạo ra là grant.
2. **Pre-delivery:** thiếu source/locator/hash, protected-region delta, figure-data/mark mapping và QA stale. Claim entailment không được chứng nhận tự động.
3. **Advisory:** ngữ pháp/style và resource suggestion theo locale/genre; không tự viết lại prose hoặc gọi mạng.

Kiểm tra preflight tại entrypoint script vẫn bắt buộc khi hook không khả dụng. Trạng thái `manual/advisory/not-callable` phải rõ; không quảng cáo coverage toàn host. Hook không phải sandbox, proof của domain hay hàng rào bảo mật đầy đủ.

## Safety và failure contract

- Mặc định off; preview cấu hình project, owner tự duyệt cài và trust. Không dùng bypass, không thay config ngoài namespace sở hữu, không ghi secrets/transcript/manuscript toàn văn.
- Không chạy command lấy từ JSON/source; runner/executable chọn từ allowlist do controller cấu hình, argv và timeout có giới hạn; paths resolve nằm trong project, từ chối traversal/symlink escape.
- Thiết kế checker không có side effect, vì nhiều hook có thể chạy song song. Nếu ghi receipt, dùng ID session/task/artifact và atomic write; không đọc-modify-write shared counter thiếu lock.
- `Stop` tối đa một nhắc nhở cho cùng artifact hash/vi phạm; không auto-resubmit, không giữ task mở vì một taste suggestion. Human gate chưa chốt phải trả trạng thái pending rồi dừng.
- Deny thuộc policy có đường ra riêng; warning không được biến thành deny. Crash/malformed/timeout phải được ghi degraded/failed rõ, không tự claim protected. Permission/sandbox thật vẫn là authority.
- Test trước với payload fixtures cục bộ, rồi disposable project và native events có user grant. Cùng checker gọi thủ công và qua adapter phải cho cùng decision trong phạm vi được hỗ trợ.

## Câu hỏi còn mở

Version/tool coverage và thao tác trust thực tế của từng surface chỉ đóng sau native verification được phép. Không có quyết định nào ở báo cáo này tự cấp phép cài hook.
