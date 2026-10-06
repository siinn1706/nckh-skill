# Review và định hướng nâng cấp nghiên cứu DevOps/AIOps

## Kết quả

Kit có nền tảng rõ về quyền, provenance, bảo toàn, reader và tách lớp acceptance. Phần chuyên môn scientific dataset/statistics/telemetry/AIOps còn mỏng: các owner hiện có chủ yếu dừng ở protocol chung hoặc nhiệm vụ engineer/marketing. Nâng cấp được đề xuất là bốn owner khoa học có artifact contracts riêng, làm sâu research/method và thêm reference packs được đọc có kiểm chứng.

Review này phục vụ plan mới tại [plan.md](../261005-0036-nckh-devops-aiops-research-upgrade/plan.md). Theo user, plan writing/visual/hooks đang do agent khác cook được xem là baseline tương lai đã hoàn tất; không bổ sung lại phần đó.

## Phạm vi đã đọc

| Root trong resources | File metadata được kiểm kê | Kết luận lựa chọn |
|---|---:|---|
| scientific-agent-skills-main | 177 | Chọn phương pháp, thống kê, dataset audit, model/time-series evaluation và reproducibility. Biology/clinical/lab automation không áp dụng vào DevOps/AIOps. |
| nature-skills-main | 20 | Chọn evidence cards, scientific reporting, experiment log và forensic review; bỏ venue/platform-specific mandates. |
| claudekit-engineer-main | 92 | Generic engineering owners phần lớn đã có; root rights conflict chặn copy. Thiết kế research environment/process checks từ nguồn công khai riêng. |
| claudekit-marketing-main | 118 | Không nâng cấp marketing. Unit/randomization/measurement ideas đã có owner hoặc được viết lại cho scientific design khi phù hợp. |
| humanizer-main | 1 | Writer đã thuộc plan trước; không nhập lại hoặc thêm detector/evasion. |
| languagetool-master | 0 | Đây là codebase grammar engine; English diagnostic optional. Không làm dependency scientific core hoặc công cụ tiếng Việt. |
| skills-main | 20 | Chọn nguyên tắc extraction/test artifact khi có quyền; document quartet có nested license conflict, không copy. |

Tổng là 428 file metadata, không phải 428 unique production identities: có templates/support/nonproduction và một tên file khác case. Inventory toàn bộ metadata + đọc sâu các candidate đã chọn, không phải audit mọi dòng code của bảy repository. [Coverage JSON](coverage-261005-0036-resources.json) và hai [source manifest](source-manifest-261005-0036-scientific.json), [other manifest](source-manifest-261005-0036-other.json) giữ từng entry/classification/hash. Local downloaded snapshots không có Git identity đã xác minh; ref/commit unknown không được điền bằng tên folder hoặc pin cũ.

## Findings và nâng cấp

| Khoảng trống có bằng chứng | Thay đổi đề xuất | Artifact chứng minh khi cook |
|---|---|---|
| `nckh-data` sở hữu DB schema/migration, chưa sở hữu research dataset lifecycle | Thêm `nckh-dataset` cho intake, curation, labels, lineage, splits/quarantine | Dataset card và immutable split manifest; actual data quality/overlap audit |
| `nckh-analytics`/`nckh-experiment` là KPI/A-B marketing | Thêm `nckh-statistics`; giữ marketing semantics | Analysis plan/readout có estimand, unit, dependence, effect size/uncertainty và actual calculation bindings |
| Generic devops/debug không chuẩn hóa observation→incident→verdict | Thêm `nckh-telemetry` | Logs/metrics/traces mapping có clock, unit, identity, coverage/joins và raw lineage |
| Không có domain owner cho offline/agent AIOps benchmark | Thêm `nckh-aiops` | Frozen task/labels/split/metric/baselines/ablation protocol và prediction/run-bound evaluation |
| Resource corpus hiện không đại diện CS/AIOps | Bốn reference packs + một pilot actual-source project-local khi cook | Reviewed reader observations riêng với dataset intake và real-run receipts |
| Generic 156 base IDs không kiểm các lỗi scientific domain mới | +16 base IDs cho bốn owner và supplemental risk cases | Leakage, dependence, missing signals, label exposure, ranking ties, failed-run denominator và grounded evidence oracles |

Exact file/line và tác động ở [current-kit review](code-reviewer-261005-0036-current-research-kit.md). Snapshot đọc hiện tại là r34/281 pins/39 identities/9 resources, zero pin drift ở thời điểm đó; đây không phải final revision của agent đang cook. Target 43 identities/172 base IDs chỉ đúng sau P1 reconcile exact membership của bàn giao cuối.

## Xia adoption và data

Đề xuất `--port` theo behavior/contract, không nhập nguyên kit. Dùng selected experimental design/statistics/power/EDA/Aeon/sklearn/SHAP/SimPy/DataLad/Nature evidence/reporting references; source anatomy, dependencies, rights và challenge decisions ở [scientific report](researcher-261005-0036-scientific-sources.md) và [other-kits report](researcher-261005-0036-other-resource-kits.md).

Bốn packs: statistical recipes, telemetry dictionary, benchmark cards, evaluation recipes. Mỗi pack có producer, truthful multi-source adaptation/rights lineage, named consumer/domain/locale/genre, bounded typed reader, expected artifact và tests. Re-authored text cần schema/reader variant thật; không giả là copied-upstream. Giữ resource access ON cho public package; OFF chỉ dùng internal comparison.

RCAEval, AIOpsLab và OpenTelemetry là primary references bổ sung, đã đọc qua web cho anatomy và scientific limits, chưa pin acquisition bytes. [Primary-source review](researcher-261005-0036-primary-aiops-sources.md) giữ URL và quyết định. Có nested baseline/license, cluster/fault side effects và telemetry-version gates riêng; root MIT không bao trùm mọi component.

## Kiểm chứng và giới hạn

Lượt này chỉ có source/metadata/hash review và plan artifacts. Không có upgrade implementation, benchmark/training, provider run, scientific evaluation, install/hook activation hoặc publication. Structural plan checks sau drafting chỉ kiểm links/frontmatter/phase/task consistency. Future deterministic fixtures, real computation, actual agent behavior, native/human/scientific acceptance giữ lanes riêng; kết quả của plan trước không grade identity mới.

Không có câu hỏi bắt buộc chặn planning. Một câu hỏi ưu tiên được gửi nhưng chưa có trả lời tại lúc ghi; default là bao phủ nền tảng chung + RCA/anomaly + LLM/RAG/agent. Dataset, budget và runtime của pilot được resolve từ project/rights khi cook; không coi assumption là user approval.
