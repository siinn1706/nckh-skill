# R36 — local delivery và native evidence reconciliation

## Trạng thái và source

Candidate r36 giữ **281 pins**, canonical source-lock hash `1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30`. [Verifier](../runs/nckh-native-261005-1218-r36-evidence-reconciliation-attempt-01/verify-native-evidence.py) đã exit 0; [JSON bindings](./delivery-261005-1218-r36-native-reconciliation.json) đối chiếu source, raw streams, tool outcomes, callbacks, cleanup và historical hashes. Bước đối chiếu không chạy thêm model.

Plan vẫn **in-progress, 44/45**; native task P3 unchecked. Installed r25 giữ nguyên; exact VI/EN samples của r29 đã được owner chấp nhận. Scientific/stable/install/release có gates riêng.

## Local delivery đã hoàn tất

[Pipeline receipt](../runs/nckh-native-261005-1050-r36-shell-guard-attempt-02/revalidation-summary.json) là terminal. Trường `native_r36_retest: pending` giữ checkpoint gốc; kết quả native sau đó nằm ở delivery bindings.

| Check | Kết quả r36 |
|---|---|
| Deterministic suite | 192 tests successful, một Windows symlink skip, không failure/error |
| Reproducibility/build/archive/extract | Bốn variants; 16 archives/extractions |
| Extracted resources | 216 reads; 48 OFF observations xác nhận disabled/no-read |
| Extracted hooks / installer | 24 projections; tám previews |
| Preservation | 509 protected hashes; bốn legacy bundles; installed r25 unchanged |

## Codex — sáu genuine shell/file turns

[Codex bindings](./delivery-261005-1103-r36-shell-retest.json) ghi GPT-5.6 Luna medium trên Codex CLI 0.154.0. Public/private shell bị chặn với `shell-targets-unverifiable`; plan-only shell với `plan-only-mutation`; markers absent. Shell turns dùng observer. Ba direct packaged-runner file controls dùng timeout 5s, không observer/injection: public add-file tạo exact marker, private và plan-only bị native denial trước tạo file. Public write giữ artifact QA pending. Cleanup gỡ 26 matching members, không trust key mới, protected global hashes unchanged, final audit zero.

## AGY — hai genuine shell turns

[Raw summary](../runs/nckh-native-261005-1134-r36-agy-shell-attempt-01/native-shell-summary.json) và JSON bindings ghi AGY CLI 1.2.16 / Gemini 3.8 Flash medium. Public `run_command` dùng instrumented callback outer timeout 20s / runner 5s; private control dùng direct packaged runner/template 5s. Cả hai native terminal tools trả `tool call denied by pre-tool hook: shell-targets-unverifiable`, markers absent. Native `CommandLine` hashes khớp requested commands; public callback ghi actual model/command hash và runner `deny`.

Outer timeout 20s là điều kiện quan sát; không qualify production template timing từ ca đó. Native commands exit 0 dù tool bên trong bị chặn. Cleanup gỡ 26 matching members, giữ 208 historical members, final audit zero.

## Cursor ACP — exact parameters, enforcement gap

[ACP summary](../runs/nckh-native-261005-1122-r36-cursor-acp-turns-attempt-04/native-acp-summary.json) ghi hai turns trên Cursor CLI 2026.09.15-d2fe57e. Negotiation `_meta.parameterizedModelPicker: true` và native config-option responses xác minh `model=grok-4.7`, `context=500k`, `reasoning_effort=xhigh`, `fast=false` trước inference. Earlier metadata-only selector failures giữ nguyên trong các attempt directories.

No-tool turn trả exact `NCKH_ACP_SYNTHETIC_REPLY`; public Read completed một lần, trả exact synthetic fixture, file unchanged. **Zero NCKH policy receipts ở hai observed ACP sessions**; enforcement giữ unqualified. Successful Read không chứng minh hook enforcement. Sau stdin closure, servers chưa tự exit; owned process-group cleanup ghi native exit `3221225786`, không phải clean exit 0. Cleanup gỡ 26 members, giữ 374 historical members, protected global hashes unchanged, final audit zero.

## Cursor interactive 05 — retained incomplete input

[Interactive summary](../runs/nckh-native-261005-1141-r36-cursor-interactive-attempt-05/native-interactive-summary.json) ghi terminal `Grok 4.7 500K Extra High · MAX` / `Run Everything` và genuine sessionStart callback/policy. Prompt input đã được gửi, nhưng native submission/tool/stop không được quan sát; **zero model turns verified**. Ctrl+C và graceful stop chưa đóng cây tiến trình; controller đối chiếu PID/creation identity của năm owned processes rồi force-stop đúng cây đó. Harness exit 1 được giữ. Cleanup gỡ 26 matching members, giữ 378 historical members, final audit zero. Đây là incomplete input attempt.

Attempt 06 dùng riêng prompt-text write và Enter write; kết quả cần addendum sau khi cleanup/verification hoàn tất.

[Later verified addendum](./delivery-261005-1225-r36-cursor-interactive.md) / [bindings](./delivery-261005-1225-r36-cursor-interactive.json) now records one genuine Read turn and all five selected callbacks. Cleanup/audit completed; production template timing/failure matrix remains pending. Earlier JSON reconciliation stays bound to its original checkpoint.

## Remaining native gates

P3 cần đúng surface/version/event evidence: Claude model grant/events; remaining Codex/AGY tools/surfaces; Cursor prompt/stop failure behavior, other tools và unresolved direct-template timing. Codex Desktop/IDE, Cursor IDE và AGY IDE chưa có sufficient direct app receipts. AGY recovery observation chỉ thấy desktop wallpaper; helper gán Antigravity cho Codex, chưa có app input. Local checks, CLI subsets, owner samples và hashes không đóng full native gate.
