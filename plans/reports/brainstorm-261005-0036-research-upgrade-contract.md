# Contract nâng cấp kit nghiên cứu DevOps/AIOps

## Outcome

Tạo review có bằng chứng cho kit hiện tại và cả bảy thư mục `resources/`, source-adoption map theo Xia, rồi plan nâng cấp sâu về phương pháp, dữ liệu, thống kê và thực nghiệm DevOps/AIOps. Lượt này kết thúc ở báo cáo và plan; các phase implementation đều pending.

## Constraints

- Theo steering của user, baseline thiết kế là kết quả hoàn tất `plans/261004-0047-nckh-research-data-hooks-writing/plan.md`. Agent khác đang cook; không giao lại writer, research visual guard hoặc hooks đã thuộc plan đó.
- Snapshot đọc được r34/39 identities/9 resource groups chỉ là quan sát hiện tại. Future baseline theo user là giả định lập kế hoạch; không suy thành native/stable/scientific qualification.
- Chỉ nâng cấp năng lực phục vụ nghiên cứu khoa học. Giữ hợp đồng tương thích hiện có của marketing/engineer; không phát triển thêm campaign, sale, operational autopilot, cluster production hoặc generic media.
- Giữ hai writer `humanwrite`/`paperwrite`, locale VI/EN, resource access ON, source rights và tách static/deterministic/agent/native/human/scientific evidence.
- Không chạy code nguồn tải về, provider, benchmark, dataset ingest, build/install/hook changes hoặc paid evaluation ở lượt review/plan. File output của lượt này ở `plans/`; runtime plan index chỉ là projection project-local có backup.
- Không có `--yagni`. Chọn lọc vì domain fit và ownership, không tự cắt chức năng user yêu cầu.

## Non-goals

Triển khai nâng cấp, thay code/config/global skills, publish, chứng nhận khoa học, bổ sung domain biology/clinical khi không phù hợp DevOps/AIOps, sao chép nguyên kit hoặc tạo một mega-SKILL.

## Acceptance của lượt planning

1. Có inventory metadata đủ bảy source roots; source anatomy chuyên sâu cho candidate hữu ích, license/provenance và disposition rõ. Không gọi inventory review là audit mọi dòng code.
2. Findings gắn source file/line và khác biệt so với post-cook baseline; phần đã thuộc plan trước không thành phase mới.
3. Plan index ngắn; phase files có đúng owner/path, steps, acceptance, validation commands, risk/rollback và thực nghiệm không fake.
4. Bounded resources luôn có producer → reader → consumer → artifact → verification; phân biệt metadata/reference với telemetry/dataset thật.
5. Independent review, links/frontmatter/parse/validate và whole-plan sweep; không mô tả những check đó như bằng chứng chất lượng khoa học hoặc skill đã cải thiện.

## Trade-offs

| Hướng | Assumption chính | Fails first | Chi phí |
|---|---|---|---|
| Chỉ tăng references cho 39 owner hiện có | Owner hiện tại đủ phân vai scientific data/statistics/telemetry/AIOps | `nckh-data` là DB/migration, `analytics`/`experiment` là marketing; scientific chain bị chia sai domain | Ít catalog changes nhưng route nhập nhằng và thiếu artifact contract |
| Bốn owner khoa học nhỏ + làm sâu owner hiện có (đề xuất) | Nghiên cứu DevOps/AIOps cần bốn artifact families riêng | Description/routing không phân biệt dataset chung và telemetry chuyên biệt; xử lý bằng explicit handoff và near-miss cases | Catalog/cases phải migrate chính xác; reference files đọc theo nhu cầu |
| Import rộng scientific kit + DevOps frameworks | Volume/import tương đương completeness | Rights/nested license, dependency/service side effects và biology/marketing scope overwhelm | Bảo trì/runtime footprint cao, khó đánh giá ảnh hưởng từng phần |

Better approaches: bốn owner nhỏ phù hợp hơn việc bồi references vào owner khác domain hoặc import nguyên kit. Evidence là mô tả sở hữu hiện tại của `nckh-data`, `nckh-analytics`, `nckh-experiment`, cùng license conflicts ở ClaudeKit/document packages. Cost of switching là +4 identity/case migration, không phải framework mới.

## Kiến trúc được đề xuất

| Owner mới | Owned artifact | Boundary/handoff |
|---|---|---|
| `nckh-dataset` | Dataset card, immutable manifest, quality/lineage report, split và release decision | DB migration vẫn `nckh-data`; telemetry-specific mapping giao `nckh-telemetry`; chưa có quyền thì metadata-only |
| `nckh-statistics` | Analysis plan/readout với estimand, unit, assumptions, effect size, uncertainty và reproducible computation | Không chứng minh causal bằng correlation; không viết thành result khi thiếu actual data/run |
| `nckh-telemetry` | Logs/metrics/traces schema mapping, time alignment/correlation và missingness audit | Không sinh modality thiếu; không tự collect production; normalized payload không chứa ground truth bị lộ |
| `nckh-aiops` | RCA/anomaly/forecasting/retrieval/agent benchmark protocol, baselines/ablations và evidence-grounded readout | Không remediation/fault injection/cloud side effect mặc định; method/statistics/dataset giữ ownership |

Target đề xuất là 43 identities và 172 base cases nếu baseline cuối thực sự giữ 39/156. Cook P1 phải reconcile exact membership với bàn giao cuối của agent trước; không hardcode r34 hoặc pin count hiện tại. Không di chuyển/đổi tên `nckh-experiment` khỏi marketing. Scientific experiment workflow được sở hữu bởi method/cook/devops references và project artifact manifests, không thêm một orchestration engine.

## Resources dự kiến

Bốn reference packs có reader, không đặt quota rows tùy tiện: statistical recipes, telemetry dictionary, benchmark cards và AIOps evaluation recipes. Chúng là curated references có source locators, không phải measurements hoặc human gold. Telemetry thật của ít nhất một pilot khi cook nằm project-local với quyền/size/hash rõ; không đưa corpus lớn vào portable package. Cookbook, search protocol, replication checklist và runbook là linked Markdown khi không cần machine reader.

## Xác nhận scope

User đã xác định research-only và DevOps/AIOps, và trực tiếp cho phép lấy post-cook plan trước làm baseline. Đã gửi một câu hỏi tùy chọn về ưu tiên: cả ba hướng / RCA-anomaly / LLM-RAG-agent. Chưa nhận lựa chọn tại lúc ghi contract; giả định bao phủ cả ba, ưu tiên nền tảng chung. Đây là assumption có thể đổi trong plan, không phải approval hoặc quyết định do user đã trả lời.
