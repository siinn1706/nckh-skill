# Nguồn chính thức cho hướng DevOps/AIOps

Ngày truy cập: 05/10/2026, Asia/Saigon. Đây là kiểm tra nguồn cho plan; không tải dataset, chạy benchmark, triển khai cluster hoặc gọi model.

## Quyết định có căn cứ

| Nguồn | Quan sát từ nguồn chính | Áp dụng vào kit | Giới hạn |
|---|---|---|---|
| [RCAEval](https://github.com/phamquiluan/RCAEval) | README mô tả benchmark RCA cho microservice, có metrics/logs/traces tùy suite và hệ thống; root-cause service/indicator là annotation của benchmark. | Benchmark card phải giữ suite, hệ thống, modalities, task, label semantics, phiên bản và split. Thiếu logs/traces không được sinh giả. | Trạng thái trang hiện tại không phải pinned dataset receipt. Khi cook phải pin revision, archive/hash, data license và từng baseline. |
| [RCAEval licensing](https://github.com/phamquiluan/RCAEval#licensing) | Repository chứa nhiều license; README nêu CausalRCA và RUN không có license, code/dataset do tác giả sở hữu được phát hành theo MIT. | Không suy rộng root MIT cho toàn bộ baseline; metadata-reference cho candidate chưa rõ quyền, chỉ adapt component có quyền rõ. | Không tải hoặc tái phân phối code/data ở lượt này; rights ledger từng artifact vẫn là gate. |
| [AIOpsLab](https://github.com/microsoft/AIOpsLab) | Framework cung cấp môi trường microservice, workload/fault injection, telemetry và giao diện đánh giá agent; có lựa chọn local/remote Kubernetes. | Dùng anatomy question → environment → workload/fault → telemetry → agent → oracle → cleanup để lập protocol nghiên cứu. | Cluster context, workload, fault injection và remote/cloud side effects phải được cấp quyền theo project; không mặc định thực thi qua kit. |
| [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/) | Semantic conventions thống nhất tên/thuộc tính cho telemetry; tồn tại theo traces, metrics, logs, profiles và resources. | Telemetry contract giữ schema/semantic-convention version, units, timestamp, resource/service identity và correlation key. | Conventions không chứng minh root cause. Chỉ chọn phần phù hợp logs/metrics/traces; version/status phải pin ở lần cook. |

## Source-manifest cho handoff

Các URL trên là nguồn reference đọc qua web, chưa có bytes/commit/hash pin cục bộ. Không ghi một SHA giả cho trang remote. Phase 1 của plan mới phải resolve commit/ref, license và nội dung liên quan; Phase 5 tạo metadata cards có provenance sau review. Benchmark dataset thực nằm ở project nghiên cứu, ngoài package source/dist.

## Quyết định Xia

- `EXISTS`: authorization, source/evidence/claim, resource registry/reader, process ownership và scientific visual preflight.
- `NEW`: scientific dataset manifest, telemetry mapping, benchmark/split/metric protocol và experiment artifact chain.
- `CONFLICT`: import toàn bộ RCAEval baseline theo root MIT; chạy AIOpsLab bằng ambient kube context; dùng topology/correlation như chứng minh nhân quả.
- Mode chọn: `--port` ở mức thiết kế và plan; không sao chép package hay triển khai code.
- Critical assumptions: quyền dữ liệu/từng component; đúng đơn vị độc lập/split; isolation và ownership của môi trường fault injection. Risk score: Medium, ba assumptions cần resolve trước tác động tương ứng.

## Phạm vi bằng chứng

Nguồn chính được dùng để xác minh anatomy và giới hạn áp dụng. Không có đo lường chất lượng skill, training, corpus release, native qualification hoặc kết quả RCA trong báo cáo này.
