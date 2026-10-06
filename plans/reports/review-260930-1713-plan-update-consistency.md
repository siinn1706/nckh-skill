# Rà soát nhất quán sau cập nhật kế hoạch

## Phạm vi và kết luận

Đã đọc toàn bộ tám file kế hoạch hiện hành trong
`plans/260930-0905-vietnamese-research-skill-kit/` và hai hồ sơ
`red-team-260930-0905-adjudication.md`, `synthesis-260930-0905-skill-kit-selection.md`.
Lượt đọc này bao gồm caveat host-specific mới trong
`design-routing-hooks-cost.md`. Không gọi runtime, provider, web hay subagent;
không coi test tương lai là bằng chứng đã chạy.

Kết luận: cả 11 finding đã duyệt đều có owner, yêu cầu/điểm triển khai và phép
kiểm tương lai tương ứng. Các yêu cầu bổ sung về hooks/subagents, rule cards có
phạm vi nguồn chính chủ, failure taxonomy, tối ưu cost, `plan → cook` với live
catalog và tag tùy chọn, English future instructions, cùng context cap dùng chung
đã được phủ. Không thấy thiếu scope hay mâu thuẫn làm thay đổi kiến trúc đã
được duyệt. Có hai điểm diễn đạt nên làm rõ trước khi triển khai; cả hai không
đòi hỏi runtime mới hay kiến trúc mới.

## Đối chiếu 11 finding đã duyệt

| Finding | Owner và yêu cầu cụ thể | Phép kiểm tương lai đã có |
|---|---|---|
| 1. Quyền cook/resume | P1 ghi authorization thật theo task/workspace/revision/hash/scope và không coi file `approved` là authority (`phase-01-start.md:65-69`). | Cook drift phải invalidate và xin lại quyền material; worker không được cấp quyền qua `approved: true` (`phase-01-start.md:196-200`). |
| 2. Timeout/rollback | P1 có `attempt_id`, `timeout-unknown`, reconcile trước retry và quarantine/invalidate (`phase-01-start.md:70-74`); P5 giữ rollback candidate và receipt stale (`phase-05-evaluation-and-packaging.md:155-160`). | Timeout cùng handle không dispatch bản sao; dependency/output stale phải hiện rõ (`phase-01-start.md:201-202`, `phase-05-evaluation-and-packaging.md:194`). |
| 3. Upstream/contract drift | P1 lưu contract revision, dependency closure, mapping và mid-run drift (`phase-01-start.md:75-78`, `161-162`); P5 qualification theo affected families (`phase-05-evaluation-and-packaging.md:148-157`). | Hash đổi thành candidate, descendant bị invalidate, không tự rollback/global update (`phase-01-start.md:194`, `phase-05-evaluation-and-packaging.md:187`, `194`). |
| 4. Claim/profile/status | P2 có verdict-to-wording và venue/profile conflict (`phase-02-evidence-and-research.md:65-82`); P3 fidelity; P5 aggregate gate không bị đổi tên trạng thái (`phase-03-vietnamese-and-english-writing.md:63-68`, `phase-05-evaluation-and-packaging.md:50-55`). | Claim unsupported, venue leakage và pending-gate rename đều bị chặn (`phase-02-evidence-and-research.md:182-184`, `phase-05-evaluation-and-packaging.md:185`, `191`). |
| 5. Factual delta sau polish | P3 so claim/attribution/số/đơn vị/phủ định/modality/population/time/causal language và đưa delta về P2 (`phase-03-vietnamese-and-english-writing.md:63-68`, `135-137`). | Translation/polish làm đổi certainty, quantity hoặc thêm fact phải fail/evidence-pending (`phase-03-vietnamese-and-english-writing.md:154-165`). |
| 6. Freshness của nguồn/policy | P2 định nghĩa `as_of`, `status_source`, trigger recheck và `freshness-pending` (`phase-02-evidence-and-research.md:72-78`, `145-146`); P5 map stale descendants (`phase-05-evaluation-and-packaging.md:148-157`). | Source policy/artifact/dependency stale làm mất cached pass (`phase-05-evaluation-and-packaging.md:194`). |
| 7. Private/package boundary | P1 tách task store, allowlist, containment, junction/symlink và redaction (`phase-01-start.md:79-82`); P5 allowlist distribution (`phase-05-evaluation-and-packaging.md:90-94`, `158-160`). | Private draft/holdout/URL token trong bundle bị block (`phase-05-evaluation-and-packaging.md:195`). |
| 8. Tool/source boundary | P1 tách host enforcement khỏi reminder (`phase-01-start.md:83-86`); P2 coi source instruction là data (`phase-02-evidence-and-research.md:179`, `186`, `199`). Design hiện đã nêu host-specific hook bypass và continuation caveat (`design-routing-hooks-cost.md:89-99`). | Hook fail/absent/reentrant, source injection và đường tool không thực sự bị guard phải unavailable/block (`phase-05-evaluation-and-packaging.md:102-104`, `phase-05-evaluation-and-packaging.md:195`). |
| 9. Visual QA đúng artifact | P4 gắn `qa_run_id`, source/data/render/manifest hash, viewer/font và stale khi sửa (`phase-04-slides-and-scientific-visuals.md:59-63`, `121-123`). | Source/render mismatch hoặc QA cũ không được handoff (`phase-05-evaluation-and-packaging.md:188`, `194`). |
| 10. Eval stop/holdout | P5 khóa reviewer/coverage/threshold/budget, giới hạn ba vòng, exposure và replacement lineage (`phase-05-evaluation-and-packaging.md:57-64`, `135-147`). | Holdout bị lộ phải thay/ghi no-blind; vòng thứ tư dừng nếu chưa có approval (`phase-05-evaluation-and-packaging.md:192-193`). |
| 11. Coverage và plan-only outputs | P1 nêu allowed plan/research/validation/journal/task records (`phase-01-start.md:28-30`, `195`); standards map capability → owner/mode/output/test (`standards-and-failure-catalog.md:92-118`). | Không tag vẫn tự route; plan-only không tạo implementation/paid/egress authority (`phase-05-evaluation-and-packaging.md:186`, `design-routing-hooks-cost.md:203-205`). |

## Yêu cầu bổ sung của người dùng

- Hooks/subagents có owner và boundary rõ trong design §3–4; P1 yêu cầu quyền
  host thật, child grant không lớn hơn parent và shared reservation
  (`design-routing-hooks-cost.md:67-120`, `phase-01-start.md:108-115`). P5 có
  các ca hook crash/absent/reentrant, timeout, permission và budget race.
- Official-scoped rules và failure taxonomy nằm ở standards §1–3: rule card có
  source/section/revision/applicability/exception/check/owner/trigger và F01–F20
  có rule, owner/check và boundary (`standards-and-failure-catalog.md:1-86`). P2
  materialize rule cards theo task/venue/genre, không biến heuristic thành luật
  chung (`phase-02-evidence-and-research.md:106-108`, `151-155`).
- Cost optimization được ràng buộc bởi quality floor và accepted-task denominator,
  tính controller/agent/hook/tool/retry/review, giữ unknown và không claim savings
  khi thiếu telemetry (`design-routing-hooks-cost.md:175-199`; P5
  `phase-05-evaluation-and-packaging.md:66-71`, `102-107`).
- Luồng user-facing chỉ là `research-plan → research-cook`; live catalog được
  resolve trước, tag là tùy chọn, thiếu route là `NOT_CALLABLE`, không auto-install
  hay API bịa (`design-routing-hooks-cost.md:10-59`; `phase-01-start.md:105-107`,
  `156-160`).
- Future skill instructions được quy định bằng English, còn output theo
  `output_language` (`plan.md:17`; `phase-01-start.md:28`, `121-122`, `154-155`;
  P2/P3 requirement 1).
- Context soft/hard dùng công thức exact, tính catalog/instructions/reference/
  hook/delegate và shared pool, kể cả retained context/cached tokens
  (`plan.md:24-25`; `design-routing-hooks-cost.md:126-173`; P1
  `phase-01-start.md:111-115`; P5 `phase-05-evaluation-and-packaging.md:105-107`).
- Không automatic extension installation, global mutation, provider charge mặc
  định, mixed-venue universal policy hay imagined API: các ranh giới này được
  ghi ở `plan.md:27`, P1 `phase-01-start.md:88-90`, design `45-59`, và standards
  `1-15`, `80-82`.

## Điểm cần làm rõ

1. **Tag bị bỏ qua và tag không hợp lệ đang dùng cùng một diễn đạt.**
   `design-routing-hooks-cost.md:10-14` nói tag là tùy chọn nhưng câu “Tag sai
   định dạng/không có phải được báo” có thể đọc thành thiếu tag là lỗi; trong khi
   P5 yêu cầu no-tag request phải tự chọn capability (`design-routing-hooks-cost.md:203-205`).
   Sửa nhỏ nhất: ghi rõ “tag bị bỏ qua → automatic live-catalog route; tag sai
   định dạng hoặc không khả dụng → báo conflict và fallback/`NOT_CALLABLE`; không
   tự cài”. Đây là clarification, không phải yêu cầu thêm router.

2. **Lifecycle state và artifact/gate status chưa được tuyên bố là hai trục.**
   P1 có lifecycle `plan → approved → cook → review → handoff` và critic output
   `accepted|needs-revision|pending|rejected` (`phase-01-start.md:52-55`, `95-96`),
   P3/P4 dùng `draft|evidence-pending|human-review-required|accepted`, còn P5
   dùng aggregate `accepted-for-scope|blocked` (`phase-03-vietnamese-and-english-writing.md:55`,
   `phase-04-slides-and-scientific-visuals.md:51`,
   `phase-05-evaluation-and-packaging.md:50-55`, `81`). Đây có thể là các scope
   khác nhau, nhưng hiện chưa nói rõ nên dễ đọc `accepted` cục bộ thành accepted
   toàn scope. Sửa nhỏ nhất: thêm một câu ở P1 rằng lifecycle là trục tiến trình;
   artifact/gate statuses là trục độc lập, trong đó chỉ aggregate
   `accepted-for-scope` mới đóng gate scope và không status cục bộ nào ghi đè
   `pending/fail` bắt buộc.

Không phân loại notation `W` ở index/P1 so với `W_i` trong design là blocker: design
đã định nghĩa per-context caps và pool neo theo controller; có thể giữ `W` như ký
hiệu rút gọn ở index.

## Trạng thái

Status: DONE_WITH_CONCERNS
Summary: Mười một finding đã duyệt và toàn bộ yêu cầu bổ sung đều có owner, contract và test tương lai; không có thiếu scope nghiêm trọng. Cần làm rõ semantics của tag bỏ qua và trục status trước triển khai để tránh route hoặc acceptance bị hiểu sai.
Concerns/Blockers: Hai clarification nêu trên; không phải blocker cho bản kế hoạch và không yêu cầu triển khai trong lượt này.
