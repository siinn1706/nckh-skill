# Checkpoint r34 đang kiểm chứng

Source hiện là r34, 281 pins, canonical hash `8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34`. Plan vẫn in-progress, 44/45; native surface task chưa đủ evidence.

## Kết quả đã có

- r31 sửa AGY non-blocking permission output thành `ask`; r32 sửa closure-test expectation. Full r32 đạt 183 tests và một Windows symlink skip.
- r33 sửa codec đọc `TargetFile`, `AbsolutePath`, `DirectoryPath`, `SearchDirectory`, `SearchPath`. [Native file cases r33](../runs/nckh-native-261004-2112-r33-attempt-01/agy-native-file-summary.json) đạt allow-write, protected-write denial và protected-read denial trên AGY 1.2.16/Gemini 3.8 Flash medium/dangerous.
- [AGY workspace plugin r33](../runs/nckh-native-261004-2112-r33-attempt-01/agy-native-workspace-plugin-summary.json) có hai same-tool callbacks, một policy receipt và một actual tool execution. Plugin nằm trong project thử; không có global installation.
- [Full r33](../runs/nckh-native-261004-2112-r33-attempt-01/deterministic-r33-attempt-01.json) thất bại: 186 tests, một error và một skip. [Actual Windows diagnostic](../runs/nckh-native-261004-2112-r33-attempt-01/receipt-parent-resolution-diagnostic-01.json) ghi child/root resolve mismatch khi receipt parent xuất hiện đồng thời; không quy lỗi này thành path escape thật.
- r34 tạo contained receipt directory trước child resolution; project/no-links/atomic-write/kernel-lock guards giữ nguyên. [Review/focused run](../runs/nckh-native-261004-2112-r33-attempt-01/source-receipt-parent-review.json) đạt 15 tests, gồm 150 fresh directories × 6 concurrent calls và traversal rejection.

## Đang chạy và còn mở

[R34 run ownership](../runs/nckh-native-261005-0005-r34-attempt-01/ownership.json) bind source checkpoint và failed predecessor. Full deterministic và four-variant build đang chạy; archive/extract/smoke/previews/preservation chưa đạt ở r34. Không lấy r32 pass hoặc native r33 để gọi latest r34 delivery complete.

Cursor đã đăng nhập và native init xác nhận Grok 4.7 500K Extra High. R31 allow/deny/fault observations giữ nguyên; uncovered/duplicate có native hook timeout anomalies. AGY native file/plugin subset đạt ở r33; per-event/surface matrix vẫn chưa đủ. Claude model/tool oracle, Codex duplicate/other events và direct Codex Desktop/IDE, Cursor IDE, AGY IDE receipts còn thiếu.

R31 Cursor/AGY và r33 AGY matching configs/payload/plugin files đã cleanup; protected native global hashes unchanged. Native conversation/trust history và tất cả failed receipts giữ nguyên. Installed r25 chưa update. Hai owner mẫu VI/EN của r29 đã accepted; stable/scientific/release lanes riêng.
