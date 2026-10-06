# Cursor CLI: điều tra tuyến workspace/plugin

**Trạng thái:** chỉ đọc source đang cài, không chạy code vendor hoặc gửi model prompt. Source kit vẫn r37; native task giữ 44/45, P3 active.

[Tài liệu hooks hiện tại của Cursor](https://cursor.com/docs/hooks#workspaceopen) mô tả `workspaceOpen` chạy trên desktop và CLI, có thể trả `pluginPaths` để nạp plugin cho workspace. Đây là một tuyến khác với `--plugin-dir` đã thử; tài liệu chưa chứng minh tuyến này hoạt động trong bản CLI đang cài.

[Kiểm chứng source](../runs/nckh-native-261006-0200-r37-cursor-workspace-route-inspection-attempt-42/verified-workspace-route-inspection.json) gắn với CLI `2026.09.15-d2fe57e`, vendor hash `9f51ecf275d932372bf367914708b0dd21bf9c9e807b5e20e789ec9e247d9f86`, khớp bản đã đọc ở native20. Có năm literal `workspaceOpen` và bảy literal `pluginPaths`, đều trong vùng shared normalization, response validation và aggregation. Chưa tìm thấy chỗ gọi runtime qua phép tìm literal này; tên động hoặc dispatch gián tiếp chưa được loại trừ.

[Native alias21](./delivery-261005-1930-r37-cursor-plugin-alias-controls.md) vẫn giữ project callback và thiếu plugin callback cho prompt/stop; native19 cũng giữ kết quả riêng. Điều tra này không sửa kết quả cũ hoặc kết luận platform unsupported.

Nếu tiếp tục giả thuyết, cần một phép quan sát startup mới chứng minh callback `workspaceOpen` và plugin path thực sự được nạp, trước khi gửi model prompt. Hiện có **zero CLI process mới, zero hook callback, zero model prompt** cho native42. Native41 đang có yêu cầu quyền riêng cho cache/metadata Codex; phần này độc lập với tuyến Cursor.
