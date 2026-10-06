# NCKH r30 — checkpoint sau xác nhận owner và thử native

Trạng thái: **technical PASS; owner VI/EN accepted; native evidence còn pending, plan 44/45**.

Thực thi theo [plan](../261004-0047-nckh-research-data-hooks-writing/plan.md) và quyền trực tiếp của người dùng. Native grant chỉ áp dụng project thử riêng; gói đang dùng r25 chưa đổi. [Structured record](delivery-261004-1707-r30-native-checkpoint.json) giữ source, input/artifact, archive và receipt hashes.

## Xác nhận đã hoàn tất

[Owner feedback](../runs/nckh-native-261004-1707-attempt-01/owner-feedback.json) ghi đúng lời người dùng: `1. cho phép; Mẫu VI: chấp nhận; Mẫu EN: chấp nhận`. Hai mẫu bind r29/input/artifact hashes đã hiển thị trong [writer trial](reviewer-261004-1037-writer-forward-test.md). Writer instructions giữ nguyên bytes ở r30. Feedback này chỉ chấp nhận hai mẫu; scientific/stable, holdout, economics và native acceptance có hồ sơ riêng.

## Sửa từ bằng chứng native

Claude 2.1.272 trên Windows với Git Bash đã loại backslashes trong command string của r29, báo executable không tồn tại. r30 truyền executable và `args` trực tiếp. Chỉ ba pinned files đổi: `core/hook_config.py`, `tests/hooks/test_config.py`, `docs/installation.md`; focused hooks đạt 21/21. [Diff](../runs/nckh-native-261004-1707-attempt-01/source-review.diff) / [Inline review](../runs/nckh-native-261004-1707-attempt-01/source-review.json) / [Freeze delta](../runs/nckh-native-261004-1707-attempt-01/r30-source-checkpoint.json). Không có independent reviewer mới hoặc Git checkout.

r30 có **281 pins**, canonical source-lock hash `55a4b60779228f3be3ae42d7691a49dec1df1b4e6f26139a32435aa1914562e1`. Đúng 39 skills/156 base cases/19 families/9 resources; historical 148 IDs và 224 matrix cells giữ nguyên. r29 archives/receipts/history không bị ghi đè.

## Kiểm chứng r30

| Kiểm tra | Kết quả thực | Receipt |
|---|---|---|
| Full deterministic | 182 tests, `OK (skipped=1)`, 1222.501 giây theo unittest; symlink fixture bị giới hạn quyền Windows | [Complete unchanged suite](../runs/nckh-native-261004-1707-attempt-01/deterministic-r30-attempt-02.json) |
| Reproducibility/build | 4 variants × 4 hosts, 16 persistent bundles | [Build context](../runs/nckh-native-261004-1707-attempt-01/delivery-context.json) |
| Archive/extract | 16 ZIP thực, giải nén ngoài source rồi verify | [Archive chain](../runs/nckh-native-261004-1707-attempt-01/archive-summary.json) |
| Resource/writer reads | 216 reads; 48 resource-OFF disabled/no-read observations | [Extracted smoke](../runs/nckh-native-261004-1707-attempt-01/smoke-summary.json) |
| Hook portability | 24 primary/reference projections; runner/manual/config preview; disposable projects không đổi | [Smoke receipts](../runs/nckh-native-261004-1707-attempt-01/smoke-summary.json) |
| Installer preview | 8 surfaces, mỗi preview 39 skills + 6 agents; không viết project | [Preview](../runs/nckh-native-261004-1707-attempt-01/installer-previews.json) |
| Preservation | 509 protected hashes, installed r25 và 4 legacy schema-v1 bundles giữ nguyên | [Preservation](../runs/nckh-native-261004-1707-attempt-01/final-preservation.json) |

Public package contract giữ resource access ON; OFF chỉ là internal comparison. [Đủ 16 archives](../runs/nckh-native-261004-1707-attempt-01/archives/) chưa được publish hoặc cập nhật installation.

## Native theo đúng surface/version/event

| Surface/version | Quan sát thực | Giới hạn |
|---|---|---|
| Claude Code 2.1.272, r30 | `SessionStart` gọi direct packaged runner; tám lượt instrumented entrypoints, tổng 10 callbacks gồm duplicate project/plugin hai callback | Chưa thử UserPromptSubmit, PreToolUse, PostToolUse, Stop; không có tool side-effect prevention oracle |
| Codex CLI 0.154.0, r29 | Host list nhận project definitions; hai hash được trust riêng; specialized local shell trả kết quả | Không có callback ở route đã thử, không suy model tool coverage |
| Cursor CLI 2026.09.15-d2fe57e, r29 | `Authentication required`, exit 1 trước callback | Cần phiên đăng nhập hợp lệ để chạy tiếp |
| AGY CLI 1.2.16, r29 | Eligibility check fail khi dùng loopback proxy, exit 1 trước callback | Không kết luận chưa đăng nhập hoặc không hỗ trợ hooks từ lỗi này; cần network/account eligibility được cấp quyền |
| Codex Desktop/IDE; Cursor IDE; AGY IDE | Chưa thử trong đúng app surface | Version/event native receipts vẫn pending, không đổi advertised targets |

[Claude startup observations](../runs/nckh-native-261004-1707-attempt-01/native-r30-claude-summary.json) ghi direct, normal/advisory, bounded policy-block, malformed input, malformed output, injected sleeper, crash exit17, unsupported codec event và duplicate project/plugin. Các lượt `--init-only` đều host exit0. SessionStart là advisory; policy block được mã hóa thành context. Sleeper đã vào callback nhưng chưa hoàn tất khi host/job đóng; receipt không tự xác nhận host timeout prevention. Unsupported codec test đổi selected codec event, không giả host phát event lạ. Duplicate tạo hai callback, một policy receipt do idempotence. Các quan sát này không hoàn thành full native preventive failure matrix.

## Cleanup và trust còn lưu

[Cleanup](../runs/nckh-native-261004-1707-attempt-01/native-cleanup.json) đạt: 14 project thử, bốn config còn lại và 362 staged payload members đã gỡ theo matching hashes, không conflict. Các config của lượt Claude r30 đã gỡ ngay sau mỗi run. Archives, extracted packages, context và evidence giữ lại. Owned process jobs đã đóng; không dừng tiến trình người dùng.

[Codex cleanup observation](../runs/nckh-native-261004-1707-attempt-01/codex-native-cleanup-observation.json) xác minh PreToolUse và SessionStart thử đã tắt bằng normal UI. Host vẫn lưu hai trusted hashes, và project trust có thể còn lưu; không có config/payload project để gọi. Không sửa trực tiếp trust store/global user definitions để xóa những record này.

Automatic approval review đã từ chối `Codex /hooks trust all` vì có thể bao gồm hooks sẵn có của người dùng. Action đó không chạy. Đã review/trust riêng đúng hai project definitions; [Rejection record](../runs/nckh-native-261004-1707-attempt-01/native-approval-review.json) giữ lý do và thay thế đã thực hiện.

## Failure history và công việc còn lại

- [Attempt 01](../runs/nckh-native-261004-1707-attempt-01/deterministic-r30.json) timeout ở hạn 900 giây của existing eval wrapper, phát `E` ở concurrent receipt test trước khi có traceback. Nguyên nhân lỗi chưa xác định. Cùng source r30, isolated test và full 182-test run sau đó đều pass; không sửa/giảm/skip test để qua. Lượt đầy đủ mất hơn 900 giây, dùng direct unchanged unittest discovery với owned process tracking và không đặt hạn toàn suite. Per-test timeouts giữ nguyên.
- [Native helper failure](../runs/nckh-native-261004-1707-attempt-01/native-r30-claude-attempt-01-helper-failure.json) là lỗi cleanup dùng Windows relative separators; direct packaged callback đã chạy. Giữ failure, gỡ matching config và tạo attempt mới; source không đổi.
- Native grant và owner VI/EN feedback đã hoàn tất. **Một checkbox P3 còn mở**: event/version/surface evidence đủ để quyết định từng route. Production hook activation vẫn inactive; không gọi production apply với evidence giả.
- Để thử PreToolUse/deny-side-effect matrix cần native model turns theo provider scope/budget riêng. Cursor cần login; AGY cần eligibility thành công qua kết nối thật. App/IDE tracks phải được thử trong đúng surface. Không lấy CLI evidence để đóng Desktop/IDE gate.

Gói r30 là candidate cục bộ đã kiểm chứng technical. Installed r25 update, public release và scientific/stable qualification chưa thực hiện.
