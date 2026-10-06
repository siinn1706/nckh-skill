# Planning validation — NCKH DevOps/AIOps upgrade

Ngày 2026-10-05, Asia/Saigon. Plan authority: [index](../261005-0036-nckh-devops-aiops-research-upgrade/plan.md), bảy phase files, adoption map và acceptance matrix. Baseline thiết kế là plan `261004-0047` sau cook theo user; execution P1 phải reconcile actual final handoff.

## Validation state — complete for planning

Whole-plan semantic/ownership sweep và bốn review lenses đã hoàn tất. Không còn consequential finding mở ở cấp plan. Không có implementation, source tests, build/install, provider hoặc scientific benchmark run trong lượt planning.

| Actual check | Kết quả | Receipt |
|---|---|---|
| `ak plan validate` | Exit 0, `valid=true`, không errors | [Validate JSON](plan-261005-0036-validate.json) |
| `ak plan parse` | Exit 0; 7 phases, 39 tasks, 0 done, 0% progress; index pending, parser projects phase status thành todo | [Parse JSON](plan-261005-0036-parse.json) |
| Whole-plan structure/links | 10 Markdown files; index 81 lines; exact phases 1–7; tất cả phase frontmatter pending; 39 unchecked/0 checked; 43 local links/0 broken | [Whole-plan receipt](plan-261005-0036-whole-plan-check.json) |
| Input integrity | Hai raw manifest hashes và hai scientific metadata fingerprints bind adoption map; 69 selected source-file hashes khớp, 0 drift/missing | [Whole-plan receipt](plan-261005-0036-whole-plan-check.json) |
| Command/path labels | Existing referenced test modules tồn tại; proposed modules/classes/CLI được ghi là tương lai; local versus pinned checks, OUTSIDE CWD và explicit models đã đối chiếu source | [Controller review](red-team-261005-0036-controller-scope.md), [flow review](red-team-261005-0036-failure-integration.md) |
| Project-local index | Reindex applied; plan mới recognized với 7 phases; non-plan directories reported unrecognized/reserved, không deleted hoặc pinned làm active cook | [Reindex JSON](plan-261005-0036-reindex.json), pre-reindex SQLite backup (historical evidence path: `backup-261005-0036-final-plan-store.sqlite`; unavailable in the cleaned checkout) |

File hashes trong whole-plan receipt là final ten-file plan identity sau controller thêm validation links. Index re-projection không sửa plan files hoặc nguồn implementation của agent khác.

## Decisions và assumptions

- User xác định research-only, DevOps/AIOps và post-cook baseline; writer/visual/hooks không thành task lặp.
- Một câu hỏi ưu tiên tùy chọn đã gửi, chưa có đáp án. Plan dùng assumption bao phủ nền tảng chung, RCA/anomaly/forecasting và LLM/RAG/agent; không ghi đó là user approval.
- Chọn bốn owner với artifact boundaries riêng và bốn bounded reference packs. Source rights/runtime/pilot chọn khi cook; không cần quyết định bổ sung để giao plan.
- Draft corrections thực hiện scope đã được yêu cầu, không đảo user decision. Implementation checkboxes vẫn pending.

## Review inputs

[Scientific assumptions](red-team-261005-0036-scientific-assumptions.md), [failure/integration](red-team-261005-0036-failure-integration.md), [security/rights](red-team-261005-0036-security-rights.md), [controller scope/contracts](red-team-261005-0036-controller-scope.md), [aggregate source review](review-261005-0036-research-upgrade-summary.md).

### Adjudication

| Lens / initial finding | Final disposition |
|---|---|
| Scientific F1 High — actual split membership oracle | Resolved: canonical actual memberships/intervals, hash/count reconciliation và intersection/window falsifiers; hashes khác nhau không đủ chứng minh disjoint. |
| Scientific F2 Medium — blanket post-incident/threshold restriction | Resolved: task decision-time policy, permitted frozen RCA diagnostic window, train-fitted preprocessing, validation-only thresholds/selection, sealed test. |
| Security S1 Medium — cap sau allocation | Resolved: trusted positive per-file/aggregate/record/output caps trước read/parse/allocation; streaming/hash bounds; oversize refuses, không clipped complete. |
| Controller R1 Medium — CWD dưới repository | Resolved: permitted owned OUTSIDE root ngoài WORK và mọi extracted bundle, actual mapping/receipts/cleanup trong RUN. |
| Flow F1 Medium — new resource consumers trước catalog | Resolved: serial exact catalog/profile/base-case/source-kind prerequisites và actual local pack gate P5 trước P6. |
| Flow F2 Medium — pinned checks trước freeze | Resolved: independent checks/review → source-owner quiescence → sole freeze → pinned regressions; corrective revisions giữ failures và rerun descendants. |
| Flow F3 Medium — preview thiếu models | Resolved: explicit verified frozen model profile, sample `--models balanced`; dry-run vẫn chỉ preview. |
| Factual schema lookup/hash transcription | Corrected: dynamic schema path lookup, no registration table; lock hash typo sửa có note trong historical review. |

Bốn final lenses đã đọc đủ ten-file scope. Tổng một High/sáu Medium được resolved **trong plan**, không ghi source/runtime remediation đã hoàn thành. Không thêm findings để đạt quota; independent reports giữ initial evidence và final resolution, không xóa lịch sử.

## Handoff

Planning complete; implementation pending. Execution bắt đầu P1 bằng final cooked handoff của plan trước, rồi quyền/ref/rights/pilot selection và exact membership. Candidate chỉ experimental; actual deterministic/agent/native/owner/scientific gates được ghi ở acceptance matrix, chưa có verdict cho implementation mới. Ước lượng 15–22 ngày công là planning estimate, phụ thuộc handoff và runtime/pilot thực tế.

Local journal `plans/journals/2026-10-05-nckh-devops-aiops-research-upgrade-plan.md` đã được CLI tạo/đọc lại/validate: exit 0, `ok=true`; receipts ở `journal-261005-0036-{create,validate}.json`. AgentWiki publish skipped. Final integrity receipt `plan-261005-0036-handoff-integrity.json` xác nhận ten-file plan hashes không drift sau index/journal, 14 links của handoff reports không lỗi, 0 implementation tasks completed và 0 long-lived processes started.

Plan files là authority. Project-local AgentKit DB là projection có backup; không pin plan mới thay task cook đang hoạt động của agent khác. Parse/hash/link/index chỉ chứng minh cấu trúc và integrity của tài liệu, không chứng minh kit đã nâng cấp hoặc scientific/native acceptance.
