# Cursor CLI r35: direct template5s controls

## Kết quả

[Structured bindings](./delivery-261005-0905-r35-cursor-template-controls.json) đối chiếu bốn genuine native turns trên Cursor CLI `2026.09.15-d2fe57e`: một lượt allow trước đó và ba controls mới. Cả bốn có native error **Hook script timed out after 5000ms** với `failClosed`; ba thao tác ghi không tạo marker, thao tác đọc giữ fixture nguyên vẹn. Direct template5s chưa qualified và nguyên nhân timeout chưa xác định. Source r35/281 pins giữ hash `4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255`.

| Control | Policy receipt được quan sát | Kết quả native | Oracle |
|---|---|---|---|
| Public Write allow, lượt trước | allow | Timeout5s | Marker absent |
| Public Write plan-only | allow ở preread stage | Timeout5s | Marker absent; policy prevention unverified |
| Private Write | block | Timeout5s | Marker absent; native policy prevention unverified |
| Public Read allow | allow | Timeout5s | Exact fixture unchanged; read control unqualified |

Các definitions gọi đúng packaged runner, timeout5s, không observer hoặc fault injection. Grant chọn `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`; native init trả `Grok 4.7 500K Extra High`. Backend/billing attestation không được quan sát. Không đổi timeout/source/config toàn cục để làm controls đạt.

## Collector repair và bảo toàn

Verifier đầu tiên thất bại ở assertion timeout vì Read result đặt lỗi trong `error.errorMessage`; collector chỉ đọc `reason`/`message`. [Failed verifier preimage](../runs/nckh-native-261005-0905-r35-cursor-template-controls-attempt-01/verify-template-controls.failed-preimage.py) được giữ trước khi thêm đúng trường đã quan sát. [Verifier đã sửa](../runs/nckh-native-261005-0905-r35-cursor-template-controls-attempt-01/verify-template-controls.py) chạy exit0 và xác nhận bốn timeout; raw controller summary, native streams và failed assertions lịch sử được giữ nguyên. Repair chỉ sửa extraction, không đổi kết quả native thành PASS.

Hai batches cleanup gỡ52 matching config/payload members, preserve historical project members và raw global config hashes; final audits zero matching. Read fixture và policy receipts tiếp tục được giữ làm bằng chứng. Plan vẫn **in-progress44/45**, native checkbox unchecked. Owner acceptance bind đúng hai r29 VI/EN samples; installed r25 và scientific/stable/release gates riêng.

## Còn mở

Cursor template5s và intermittent timing cause; prompt/stop callbacks; other tool routes; direct Cursor IDE receipts và full event/version/surface evidence.
