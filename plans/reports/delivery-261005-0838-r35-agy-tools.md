# AGY CLI tools và direct template — r35

## Phạm vi và kết quả

[Structured bindings](./delivery-261005-0838-r35-agy-tools.json) đối chiếu **9 native turns** thuộc bốn batches trên AGY CLI `1.2.16`, với exact model selector `gemini-3.8-flash-medium`, effort `medium` và dangerous flags đã được người dùng cấp quyền. Current source giữ **r35/281 pins**, source-lock hash `4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255`; source không sửa trong các lượt này. Backend/billing attestation chưa observed.

| Ca | Native observation | Thao tác và policy |
|---|---|---|
| `replace_file_content` public | `DONE`; actual `TargetFile` khớp fixture | Đúng nội dung revised; một PreToolUse callback và preflight allow |
| `replace_file_content` private | Native `ERROR`: `private-holdout-credential-path` | Một PreToolUse block; actual before/after hashes giữ nguyên |
| `multi_replace_file_content` public | Native unknown-tool error | Zero PreToolUse; fixture giữ nguyên; preventive route chưa verified |
| `list_dir` public | Native unknown-tool error | Zero PreToolUse; fixture giữ nguyên; preventive route chưa verified |
| `list_dir` private | Model hoàn tất nhưng không gọi tool | Zero PreToolUse; không dùng unchanged fixture làm prevention evidence |
| `find_by_name` public | Native unknown-tool error | Zero PreToolUse; fixture giữ nguyên; chưa suy support ở IDE |
| `grep_search` public | Model hoàn tất nhưng không gọi tool | Zero PreToolUse; availability và prevention còn unverified |
| Direct template `write_to_file` allow | `DONE`; actual `TargetFile` khớp | Tạo đúng marker; preflight allow |
| Direct template `write_to_file` plan-only | Native `ERROR`: `plan-only-mutation` | Preflight block; marker absent |

Native tool errors không làm toàn model turn có exit khác 0. Kết luận dựa vào actual terminal tool state, policy và requested side effect; CLI exit0 không phải universal PASS. Callback path fields và native tool parameters của observed file routes được đối chiếu với exact fixture paths.

## Template5s

[Direct-template run](../runs/nckh-native-261005-0852-r35-agy-template-attempt-01/native-tool-summary.json) dùng packaged r35 runner trực tiếp, timeout **5 giây**, không observer hoặc fault injection trong active definitions. Hai controls write allow/plan-only-deny đạt đúng expected native outcome. Direct policy receipts bind actual preflight, advisory/stop và pre-delivery khi có; synthetic allow case còn `artifact-final-bytes-missing-or-stale` ở pre-delivery. Đây là timing/control evidence cho đúng AGY CLI/version/definitions đã chạy; chưa đóng artifact QA hoặc scientific acceptance.

## Historical attempts và cleanup

Ba tool batches dừng tại assertion vì unknown tool hoặc model không gọi tool. Raw summaries giữ `running`; các terminal reconciliation 0838 (historical evidence path: `../runs/nckh-native-261005-0838-r35-agy-tools-attempt-01/terminal-reconciliation.json`; unavailable in the cleaned checkout), 0844 (historical evidence path: `../runs/nckh-native-261005-0844-r35-agy-tools-attempt-02/terminal-reconciliation.json`; unavailable in the cleaned checkout) và 0848 (historical evidence path: `../runs/nckh-native-261005-0848-r35-agy-tools-attempt-03/terminal-reconciliation.json`; unavailable in the cleaned checkout) ghi partial terminal state riêng. Không sửa/regrade native receipts, không lặp lại unknown-tool cases để tạo PASS.

Cả bốn batches cleanup **104 matching config/payload members** theo owned hashes và giữ historical project members. Final process audits có zero matching task processes. Hai protected global config paths giữ exact before/after hashes; controller không direct-write global. Việc tạo reconciliation 0848 ban đầu bị auto-review từ chối do thiếu bảo vệ một output trước ghi; câu lệnh không chạy. Sau khi xác nhận cả hai outputs chưa tồn tại, bước tạo mới dùng `CreateNew`, không thể ghi đè retained evidence, và completed.

[Evidence verifier](../runs/nckh-native-261005-0852-r35-agy-template-attempt-01/verify-agy-tool-evidence.py) kiểm native command/stream/log/definition/callback/policy bindings, model/effort flags, actual fixture hashes, removed members, protected hashes và process audits cho toàn bộ 9 turns. Review thực hiện inline. Current [r35 local delivery](./delivery-261005-0710-r35-patch-retest.md) không cần chạy lại vì kit source và inputs giữ nguyên.

## Acceptance còn mở

`multi_replace_file_content`, `list_dir`, `find_by_name` chưa callable trên observed CLI route; không suy AGY IDE cũng unavailable. `grep_search` chưa có actual invocation. Other tools, other surfaces và full per-event failure/duplicate matrix giữ gaps riêng. Plan tiếp tục **in-progress, 44/45**, native checkbox unchecked. Owner acceptance giữ đúng hai r29 VI/EN samples; installed r25, publication, scientific/stable/release gates không đổi.
