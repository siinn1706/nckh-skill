# Codex CLI r37: PostToolUse trên canonical apply_patch

[Bindings đã kiểm tra](../runs/nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47/verified-posttool-observations.json) ghi bảy lượt Codex CLI **0.154.0 / exec**, yêu cầu GPT-5.6 Luna/medium. Mỗi lượt có đúng một native add-file patch, một cặp PreToolUse/PostToolUse cùng tool-use ID, turn/session và command hash; một file_change completed, marker đúng bytes và final reply. Callback báo model gpt-5.6-luna; backend effort/billing attestation chưa được quan sát.

[Brief chốt trước model](../runs/nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47/frozen-brief.json) giữ outer/inner5s, sleeper khai báo8s, tối đa bảy lượt/bảy yêu cầu patch, không retry hoặc whole-turn deadline. Các ca cũ r34 dùng shell/timeout2s giữ nguyên; ca này bổ sung đường patch và binding của r37.

## Kết quả thật

| Ca PostToolUse | Quan sát observer/policy | Native file outcome |
|---|---|---|
| Allow | advisory/delivery-bindings-current-review-separate; additionalContext | Completed, exact marker |
| Policy deny | block/bounded-input-exceeded; additionalContext | Completed, exact marker |
| Malformed input | degraded block/hook-input-or-context-invalid; additionalContext | Completed, exact marker |
| Malformed output | Chuỗi JSON lỗi do observer phát; không selected receipt | Completed, exact marker |
| Timeout | Snapshot intentional sleep8s; không selected receipt | Completed, exact marker |
| Crash | Observer exit17 có chủ ý; không selected receipt | Completed, exact marker |
| Unsupported selected codec | Runner exit3/empty JSON, degraded block receipt | Completed, exact marker |

Ở cả bảy ca, marker còn absent khi callback PreToolUse bắt đầu, rồi **đã có exact expected SHA256 khi callback PostToolUse bắt đầu**. Native item và bytes chứng minh thao tác ghi đã hoàn tất. Không có rollback hoặc preventive-denial claim từ các lỗi sau thao tác.

Normal context khai báo trước bytes dự kiến của một marker tổng hợp; runner kiểm đúng file/hash sau native patch. Đây là binding của test artifact, không phải scientific QA. Policy-deny context chứa33 empty reference records do controller sở hữu để kích hoạt bounded-input-exceeded; chúng không đại diện nguồn nghiên cứu thật hoặc kiểm quyền sử dụng nguồn.

Malformed input/output, sleeper, crash và unknown selected codec là fault injection sau callback native thật. Unknown codec selector không phải sự kiện host không biết được host phát. Native exec JSON không cung cấp hook notification states trong dữ liệu đã lưu; báo cáo chỉ xác nhận completed file_change/turn, actual callbacks, receipt/wire và bytes quan sát được. Timeout giữ snapshot sleep/no receipt cùng configured5s, không suy thêm trạng thái native chưa được ghi.

## Integrity, kết thúc và giới hạn

Tổng35 genuine callbacks/32 policy receipts; bốn selected PostToolUse receipts, bảy receipts cho mỗi sự kiện còn lại. Snapshot lúc native exit và snapshot sau descendant reconciliation được giữ riêng. Normal expected context hash được đối chiếu bằng phép dựng lại từ last-case JSON và thay đổi artifact.path đã chốt trong controller; đây là derived verification, không phải raw snapshot của context cũ. Deny context hash đối chiếu trực tiếp tệp giữ lại.

[Cleanup](../runs/nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47/cleanup.json) gỡ26 staged payload members còn khớp hash, giữ538 tệp lịch sử và toàn bộ marker/observation/receipt. Native/controller đều exit0. [Audit cuối](../runs/nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47/process-final-audit.json) kiểm union2164 PID/creation identities: zero matching/tracked-live, không dừng process. Global config/hooks hashes giữ nguyên; không thêm project trust key, cài plugin hoặc controller direct-write global.

Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên. Inline invocation definitions tái dùng project đã trusted và grant model/native hiện có. Review inline; không có independent reviewer. Full native task vẫn **unchecked / 44 of45 / P3 active**. Stop current-patch cells, project/plugin cache authority, các host/tool/surface còn thiếu và Claude selection vẫn mở.
