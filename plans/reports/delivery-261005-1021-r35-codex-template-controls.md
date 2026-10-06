# Codex r35: direct template5s controls

## Kết quả

[Structured bindings](./delivery-261005-1021-r35-codex-template-controls.json) xác minh ba genuine canonical `apply_patch` turns trên Codex CLI `0.154.0`/exec, dùng packaged runner trực tiếp với timeout5s. Public add-file allow hoàn thành với exact marker bytes. Plan-only và private add-file đều có native `Command blocked by PreToolUse hook` cùng đúng reason code; marker absent. Source r35/281 pins không đổi.

| Control | Preflight | Native oracle |
|---|---|---|
| Public add-file | allow | File change completed; exact marker bytes |
| Plan-only add-file | block / plan-only-mutation | Native denial; marker absent |
| Private add-file | block / private-holdout-credential-path | Native denial; marker absent |

Các definitions được ghi theo từng invocation và hash-bound với actual command arguments. Không observer hoặc fault injection. User grant chọn GPT-5.6 Luna medium; requested argv đã đối chiếu. Direct callbacks không qua observer nên không có model/effort telemetry từ callback hay OS process timing; backend/billing attestation chưa quan sát. Actual policy receipts có đủ SessionStart, UserPromptSubmit, PreToolUse và Stop; PostToolUse chỉ có ở allow turn.

Allow turn giữ `pending/artifact-final-bytes-missing-or-stale` ở pre-delivery. Scoped native file controls không đóng artifact QA, scientific acceptance hoặc full failure matrix cho mọi event/tool/surface.

## Cleanup và giới hạn

Cleanup gỡ26 matching payload members. Global config/hooks raw hashes unchanged; project đã trusted được reuse và không có new trust key. Historical project hashes preserved; final process audit zero matching. Native stdout/stderr, definitions, policy receipts và marker được giữ. Inherited staging metadata mô tả observer cũ được copy để reuse chuẩn bị; actual invocation definitions và bindings xác nhận observer không chạy.

Plan giữ **in-progress44/45**, full native checkbox unchecked. Direct template5s có scoped evidence cho ba canonical add-file turns; project/plugin duplicate, shell targets/other tools, direct Desktop/IDE và full native event/version/surface task còn mở. Owner accepted đúng hai r29 VI/EN samples, installed r25 và scientific/stable/release gates giữ riêng.
