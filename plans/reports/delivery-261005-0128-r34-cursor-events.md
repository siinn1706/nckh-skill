# Cursor CLI native event addendum — r34

## Scope và source

Unchanged r34 source hash `8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34`; [main delivery](./delivery-261005-0005-r34-cursor-agy.md) giữ full local tests/build/archive evidence. [Bindings](./delivery-261005-0128-r34-cursor-events.json) ghi 20 completed native turns trên Cursor CLI `2026.09.15-d2fe57e`, gồm ba baselines, 15 injected faults và hai project + transient-plugin duplicates. Plan vẫn **in-progress, 44/45**.

Direct grant chọn `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]` với `--force --trust --sandbox disabled`. Native config và command selector bind đúng lựa chọn; callbacks chỉ có legacy model `grok-4.7-xhigh`/`grok-4.7`, không có `model_id`/`model_params`. Chưa có backend/billing attestation. Existing global hooks giữ enabled và bytes unchanged; observed CLI help không có flag isolation tương ứng. Đây là evidence trong configured native environment.

## Native event coverage

Project definitions có đủ năm selected events; actual callbacks chỉ gồm `sessionStart`, `preToolUse`, `postToolUse`. `beforeSubmitPrompt` và `stop` có zero callbacks trong các turns này. Không gọi hai events universally unsupported hoặc bỏ chúng khỏi advertised contract; CLI route giữ unobserved và các surface khác pending.

Allow tạo marker và một completed Shell item. Policy deny trả native `rejected` với `plan-only-mutation`, marker absent. Controller deliberately bỏ tool mapping trả `manual`, host vẫn thực thi Shell/tạo marker; đây là uncovered controller route, không phải native unknown-tool injection.

## Fault observations

Faults được chèn sau genuine native callbacks. Bảng ghi **marker được tạo**, không phải universal PASS:

| Selected event | Malformed input | Malformed output | Timeout | Crash | Unsupported selected codec |
|---|---:|---:|---:|---:|---:|
| sessionStart | Có | Có | Có | Có | Có |
| preToolUse | Không | Không | Không | Không | Không |
| postToolUse | Có | Có | Có | Có | Có |

Cả năm `preToolUse` faults có native rejected tool và marker absent với `failClosed=true`. Post-tool faults xảy ra sau marker creation. `sessionStart` faults không ngăn Shell trong các lượt này. Timeout handler2s/sleeper8s: observer có thể vẫn hoàn tất sau khi native host đã báo timeout; callback exit0 không thay host/tool result. Public template5s và production timing chưa qualified. Official [Cursor hook docs](https://cursor.com/docs/hooks) có timeout/failClosed contract; actual receipts quyết định kết luận cho version/surface này.

## Project + plugin duplicate

Hai new cases đều có hai same-tool pretool callbacks, một idempotent policy receipt, một Shell success và một marker. Case command giống nhau chạy thành công; case thêm owned `--callback-source plugin` cũng chạy thành công và cho explicit project/plugin provenance. Không có global plugin installation.

Historical [r34 duplicate timeout](./delivery-261005-0005-r34-cursor-agy.md) vẫn được giữ: runners exit0 nhưng native host từ chối vì 20s timeout. Hai successes mới xác nhận route có thể chạy; chưa xác định root cause hoặc chứng minh timeout đã biến mất ổn định. Không sửa source hay tăng timeout để che failure.

## Cleanup và gates

Ba owned projects gỡ **82 matching files**, config/payload/plugin không callable. Protected native config hashes unchanged; [process audit](../runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/final-process-audit.json) zero matching task processes. Kênh exec cũ không còn handle khi recovery; completed command receipts, cleanup artifacts và read-only process inventory được kiểm trước tiếp tục, không restart batch.

Native checkbox còn unchecked: missing CLI prompt/stop callbacks, protected paths/other tools, intermittent timeout diagnosis, direct Cursor IDE receipts và production timing. Full four-host/surface contract, installed r25 và scientific/stable/release gates giữ riêng.
