# Cài NCKH candidate vào Codex project

Ngày 01/10/2026, Asia/Saigon. Candidate `0.1.0-experimental` đã được cài vào `C:/Users/USER/Downloads/test-skill` sau khi người dùng trả lời **“Cho phép cài vào project này”** cho preview gồm 37 skills và 6 vai trò tùy chọn.

## Phạm vi và kết quả

- Surface đã chọn: `codex-desktop`; project scope, copy, Core/Engineer/Marketing và Xia, chính sách `balanced` với model inheritance.
- Preview được kiểm tra lại (historical evidence path: `../../nckh-kit/evals/results/codex-preview-approved.json`; unavailable in the cleaned checkout) khớp hoàn toàn preview đã duyệt: 43 mục, không xung đột. Source vẫn có 181 pins và hash `2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03`.
- Receipt cài đặt (historical evidence path: `../../nckh-kit/evals/results/codex-install.json`; unavailable in the cleaned checkout): `installed`, 43 thay đổi; ID `d5811d724fe29cb5016c7c3a`.
- Đích thực: 37 thư mục trong `.agents/skills`, 6 file TOML trong `.codex/agents`. Ownership và transaction journal được giữ ở `.nckh-state`.
- Doctor (historical evidence path: `../../nckh-kit/evals/results/codex-doctor.json`; unavailable in the cleaned checkout): 43 mục `current`, 37 closures đầy đủ, 6 TOML hợp lệ, candidate integrity `current`, không duplicate visibility; transaction `committed`, không recovery conflict.
- Preview sau cài (historical evidence path: `../../nckh-kit/evals/results/codex-installed-preview.json`; unavailable in the cleaned checkout): cả 43 mục `unchanged`, không xung đột. Đây là kiểm tra chỉ đọc; chưa chạy lại giao dịch cài, update, rollback hoặc uninstall trên project thật.

Installer chạy với quyền nâng khỏi sandbox vì `.agents` và `.codex` là thư mục được bảo vệ; automatic approval review cho phép giao dịch đã được người dùng duyệt. Các tiến trình kiểm tra/cài đặt đã kết thúc.

## Giới hạn nghiệm thu

Receipt ban đầu chứng minh giao dịch file trên Windows project này. Trong goal continuation tiếp theo, [discovery/repeat audit](audit-261001-1813-native-progress-and-runner-gap.md) ghi catalog native của phiên có đủ 37 IDs và actual PowerShell repeat có zero changes, các hash/ownership/policy giữ nguyên. Invocation, hiệu lực của sáu vai trò, model/effort và hooks vẫn chưa được quan sát. Installation không cấp quyền cho paid/provider runs hoặc publication.

148 skill cases và 224 native cells đầy đủ vẫn chưa được chạy. Có quan sát scoped cho Windows project-copy `owned-install-noop`; toàn bộ 10 kịch bản installer/OS trên các scope được quảng bá vẫn chưa nghiệm thu đầy đủ. Corpus VI/EN, quyền sử dụng mẫu, người review, tiêu chí đã duyệt và protected holdout còn thiếu. Candidate vẫn experimental; stable/public distribution giữ NO-GO. Plan vẫn in-progress, 28/36 tasks, chưa có phase được nghiệm thu đầy đủ.

## Nhật ký

[Nhật ký hiện có](../journals/2026-10-01-nckh-portable-candidate-implementation.md) xác thực thành công bằng đường dẫn tuyệt đối và filename stem, `ok: true`, exit 0. Đầu vào relative path trả exit 1 không có chẩn đoán, kể cả khi dùng cùng chỉ mục project; đây là giới hạn lookup quan sát được của CLI, không phải lỗi nội dung nhật ký.

## Đầu vào còn thiếu

Nghiệm thu chất lượng cần corpus được phép dùng và người chấm phù hợp; nghiệm thu native/OS cần môi trường, phạm vi chạy và receipts tương ứng. Publication và paid/provider evaluation cần quyền riêng.
