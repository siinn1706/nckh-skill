# Phản biện plan NCKH resource quality

Ngày: 02/10/2026, Asia/Saigon. Subject: sáu Markdown trong [plan](../261002-0832-nckh-skill-resource-quality/plan.md), source revision 18. **Người dùng đã duyệt; bảy Accept đã được áp dụng vào tài liệu plan.** Không có quyền thực thi/import/install/provider phát sinh. Các `file:line` trong findings là evidence của bản **trước chỉnh sửa**, giữ để truy vết, không giả định là line hiện tại của plan.

## Phương pháp và kết quả

- Hai reviewer độc lập: Security Adversary và Assumption Destroyer. Runtime từ chối tạo reviewer mới thứ ba (`agent thread limit reached`); tái sử dụng tác giả plan cho Failure Mode self-audit, sau đó controller đối chiếu source. Không gọi đó là ba review độc lập.
- Tại lượt review trước duyệt, đã đọc toàn bộ sáu file plan; reviewer dùng Fact Checker/Contract Verifier ở mức Standard. Có 14 raw findings và một phát hiện sequencing của controller; sau gộp còn **10 nhóm: 7 Accept, 3 Reject**. Severity sau thẩm định: 3 High, 7 Medium; không có Critical được xác minh. Bảy Accept sau đó được người dùng duyệt ở mức sửa plan, không phải phê duyệt triển khai.
- Mọi finding được giữ có plan/source `file:line`. Các nhận xét mô tả tính năng đang được lên kế hoạch không tự trở thành bug của code hiện tại.
- Sampling của Security: 46 claims, 30 verified / 2 current-contract conflicts / 14 unverified-or-proposed. Assumptions: 25 claims, 13 verified / 4 conflicts / 8 unverified-or-proposed. Hai mẫu có giao nhau, **không cộng thành số claim độc lập**. Failure self-audit không cung cấp claim-count matrix. Đây không phải kiểm chứng đầy đủ mọi claim hay chất lượng skill.

## Findings đã thẩm định

### R1 — Quyền dữ liệu và bundle schema chưa khép kín — High — Accept (thu hẹp)

**Evidence:** `phase-03-resource-packaging.md:21-25` muốn resource mapping vào manifest nhưng ownership `:30-35` thiếu `nckh-kit/installer/schemas/bundle.schema.json`. Schema này `:3-4` đóng unknown fields, `:54` cố định rights; `core/build.py:59,66,86,94-98,227,330` gắn/đòi owned-local-package và copied=false. `core/install.py:68-76,283-294` dùng shared verifier.

**Failure:** data có phép nhưng ghi đúng copied-upstream sẽ bị reject; giữ nhãn owned thì sai provenance. Thêm trường mapping ngoài schema cũng fail.

**Sửa đề xuất:** P3 sở hữu cả source-lock/build/bundle schema versioning và regression của installer consumers. Pin copied-upstream data, license/NOTICE, source bytes và disposition rõ; giữ hỗ trợ đọc lịch sử local-only, không đổi nhãn hay viết lại lock cũ. Để `verify_bundle` là owner kiểm tra dùng chung; chứng minh `resolve_targets`, `refresh_targets`, `plan_install` vẫn tiêu thụ đúng bundle/tree qua tests. **Không bắt buộc dựng thêm resource receipt engine riêng cho từng caller** nếu invariant đã được verifier/tree hash bảo vệ.

### R2 — So sánh revision 14 với candidate không tách được tác dụng resource — High — Accept

**Evidence:** `phase-04-behavioral-qualification.md:10,14-17,41-45` muốn đo resource contribution nhưng cho current-NCKH revision 14 và candidate mới. `evals/baselines/baselines.json:10-16` có same-agent/selective-delegation, chưa map sang current/candidate; `core/agent_runs.py:147-160` không chứa matched-condition mapping.

**Failure:** cải thiện có thể do code/instruction/evaluator/wrapper đổi, không phải data.

**Sửa đề xuất:** pin condition→subject/input/wrapper/model/split/resource closure. Thêm cặp resource-on/off trên cùng base code và instruction policy, giữ một thay đổi được đo; ghi riêng hash của mỗi closure/config, không giả định hai artifact khác nhau phải có cùng hash. So sánh 14→candidate chỉ là migration comparison. Giữ hoặc map rõ same-agent/selective-delegation của protocol cũ; không bỏ lặng lẽ. Một upstream baseline phải là subject thật được phép, không chỉ “mượn pattern” rồi gán nhãn upstream.

### R3 — Hash freeze không phải phê duyệt nội dung — Medium — Reject dạng mở rộng validator tự cấp quyền

**Evidence:** `core/agent_runs.py:115-125` pin reference hashes; `:127-146` kiểm riêng budget. Nhưng `docs/qualification.md:101-110` đã nói hash chỉ chứng minh integrity, caller phải kiểm quyền/reviewer/threshold; `core/policies/authorization-policy.md:3-6` không cho JSON tạo authority. P4 `:28,41-45,53` cũng đòi grant và independent review.

**Thẩm định:** không có bằng chứng hash được thiết kế làm human approval. Test fixture không phải quyền chạy thật. Giữ yêu cầu caller/operator review ở gate; không tự thêm sáu schema/approval engine hay coi parser có thể chứng nhận human consent. Nếu sau này automation bỏ gate manual thì đó là thay đổi contract phải review riêng.

### R4 — Route hiện tại có giới hạn 900 giây mỗi ca — Medium — Accept (làm rõ)

**Evidence:** P4 `:10,61` nói không cắt mặc định 15 phút nhưng `:50-54` vẫn liệt kê adapter; `core/agent_runs.py:102-106` chặn timeout trên 900 giây. `docs/qualification.md:97` xác nhận đây là **per-case**, không phải tổng deadline của tác vụ. Direct report `testing-261001-direct-skill-development.md:63,79` đã có ca 1,201.094 giây.

**Sửa đề xuất:** phân biệt tổng deadline đã được người dùng bỏ với timeout từng process/case. Ghi route hiện tại chỉ dùng được khi case budget phù hợp; trường hợp dài hơn phải có route/adapter được duyệt và ownership/test cụ thể trước chạy. Không tự tái áp deadline 15 phút toàn tác vụ, cũng không bỏ mọi giới hạn/cleanup. Proposed compare script không được coi là đã tồn tại.

### R5 — Protected holdout không được đi qua development runner — Medium — Accept (thu hẹp)

**Evidence:** P1 `:29` đã lên kế hoạch sửa helper `core/evaluation.py:76-80`; helper chỉ có test caller tại `tests/release/test_qualification.py:22-25`. Runner thực tế `core/agent_runs.py:154,163-168` chỉ phát development, và `docs/qualification.md:116` nói protected execution unavailable. `evals/protocols/qualification.json:4,28-38` giữ tối đa 3 development rounds, một holdout run và exposure→development.

**Sửa đề xuất:** nhắc rõ các invariant hiện hữu trong P1/P4; helper thiếu freeze trả pending/error. Giữ current adapter development-only; protected holdout còn NOT_CALLABLE/pending cho đến khi có private route, inputs và human grant thật. Không tự mở rộng lượt này thành xây hệ protected-holdout mới; không biến việc sửa unit test thành runtime support.

### R6 — Shortlist chưa nối tới những resource cụ thể trong matrix — Medium — Accept (thu hẹp)

**Evidence:** P2 `:22-32` có S1/S2/S3; `resource-map.md:12-50` vẫn chủ yếu là tên R-* tổng quát; matrix-wide contract `:52-54` yêu cầu reader trước implementation. [Shortlist](researcher-261002-0832-source-shortlist.md) đã có actual path/commit/hash/reader/domain và gap VI/EN.

**Sửa đề xuất:** link shortlist vào P2; thêm decision rows cho đúng resource đang đề xuất (reporting-guideline registry, publisher profiles, UI lookup, Nature references), với consumer, domain, rights/status, output và test. Giữ nguồn clinical khỏi generic CS; UI data chỉ cho UI. Corpus VI/EN chưa có thì để missing/blocked-input, **không bịa mẫu và không coi JSON registry là corpus văn phong**. Không yêu cầu 37 manifests hoặc reader mới cho mọi skill.

### R7 — Cấm triển khai ở lượt hiện tại bị viết thành cấm cả phase tương lai — Medium — Accept

**Evidence:** P1 `:26-29,38-41` có task sửa evaluator/contracts/tests, nhưng `:68` lại nói “Không có implementation ... trong phase này”. `core/build.py:53-77` freeze thật có ghi lock/history.

**Sửa đề xuất:** ghi rõ lượt hiện tại chỉ author/review plan; future P1 được sửa đúng owner khi có authorization thực thi. Baseline revision 18/hash là snapshot phải giữ trong lịch sử, không phải lệnh cấm mọi revision mới. Không restore lock cũ đơn độc lên source mới hay xóa lịch sử khi rollback.

### R8 — Thiếu hệ phân loại private-path mới — Medium — Reject là một lỗi hiện hành đã chứng minh

**Evidence:** reviewer chỉ ra closure theo link và secret regex không nhận diện holdout (`core/build.py:20,102-138`). Tuy nhiên `core/policies/authorization-policy.md:17-20` đã yêu cầu private store ngoài source/dist; `core/agent_runs.py:96-98` kiểm private store không nằm trong root/project/workspace. P3 `:22-25,39` đã yêu cầu allowlist/fail-closed, không đóng gói holdout/receipts.

**Thẩm định:** chưa quan sát private data lọt bundle; giả thiết đưa holdout vào source trái policy không chứng minh hiện có leak. Giữ private-exclusion negative tests trong P3 và kiểm mapping allowlist; không bắt buộc phát minh taxonomy/governance framework mới. Nếu implementation thực sự đưa private file vào source thì phải dừng và review lại.

### R9 — Upstream được xem như instruction đáng tin — Medium — Reject kết luận đó

**Evidence:** `core/policies/authorization-policy.md:3-6` đã coi retrieved instructions là untrusted task data. P2 `:20,24,59-62` chỉ cho selective cleared material, re-authored instructions và không gọi provider/native trái phép; plan không cấp quyền chạy code upstream.

**Thẩm định:** hash không chứng minh an toàn là đúng, nhưng plan không tuyên bố điều ngược lại. Giữ content/script review trước adoption và boundary data/instruction; không tự ban toàn bộ script hoặc thêm lớp installer “approval” chỉ bằng JSON. Dữ liệu upstream không được thực thi như lệnh là invariant hiện hữu phải giữ.

### R10 — P2 build checks đứng trước support data/rights của P3 — High — Accept (sequencing)

**Evidence:** index `plan.md:25-26` cho P3 phụ thuộc P2; P2 `:67-69` chạy build sau content changes; P3 `:21-26` mới mở registry/data/rights. `core/build.py:45,86,205-206` loại extension hoặc từ chối unpinned/right states.

**Failure:** chọn CSV thật ở P2 rồi đòi candidate build pass trước khi vào P3 tạo vòng phụ thuộc; freeze sai nhãn để qua gate sẽ vi phạm yêu cầu nguồn.

**Sửa đề xuất:** P2 chốt selection/rights/staged bytes và source-level consumer checks, chưa promote unsupported resource vào source-lock/dist. P3 làm schema/closure support và mới chạy full candidate/extracted smoke. Các check baseline hiện hữu phải ghi baseline subject cụ thể, không được gọi là candidate resource pass. Khi P2 cần chỉnh vì P3 fail, giữ staged candidate và failed receipt.

## Phê duyệt và application record

Người dùng trả lời **“duyệt”** cho đề nghị sửa bảy điểm đã thu hẹp trong tài liệu. Lượt follow-up chỉ áp dụng plan amendments, không sửa source/installed state, không nhập data, chạy provider hoặc triển khai. R3/R8/R9 giữ nguyên Reject; không thêm approval engine, private-data taxonomy hay blanket script ban.

| Accepted delta | Applied plan surfaces | Bound retained |
|---|---|---|
| R1 | P1 write/freeze handoff; P3 format/rights/bundle schema, shared verifier and installer-consumer regression; index | P3 format ownership khác P1 lock writes; historical local-only records/history được giữ. |
| R2 | P4 same-base off/on condition mapping; index acceptance; resource-map evidence contract | Separate artifact hashes; preserve same-agent/selective-delegation; real pinned permitted upstream; revision 14 migration is not resource causality. |
| R4 | P4 overview/route owner/run contracts/risks; index open gates | 1–900 seconds per case on current adapter; no total 15-minute deadline; longer case needs approved route/tests, not unbounded execution. |
| R5 | P1 helper guards/round/exposure contract; P4 development/holdout invariants; index | 3 development rounds, 1 protected run, exposure → development; current route development-only; no new holdout engine. |
| R6 | P2 shortlist link/full upstream paths; resource-map four supplemental candidate decisions | Existing upstream readers versus proposed NCKH adapters, domain/rights/output/smoke; VI/EN missing/blocked-input; no invented rows or 37 manifests. |
| R7 | Index current/future scope; P1 future implementation boundary; P1/P3/P4 rollback | Plan approval is not execution; source + schema + lock rollback must be coherent; revision 18/history immutable, later revision permitted only with authority. |
| R10 | Index dependencies; P2 staged-only selection/validation/ownership; P3 support → promotion → P1 freeze → build; resource map | P2 checks on unchanged baseline are not candidate proof; failed receipts/staged candidate retained for rework. |

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all four `phase-*.md`, `resource-map.md`; current red-team/validation/journal states reconciled separately.
- Decision deltas checked: 7; reconciled stale-detail groups: 7; unresolved contradictions within these approved amendments: 0. Source-lock format ownership versus write/freeze ownership and initial P1 baseline versus later P3 handoff are explicit.
- Structural validation/parse pass: 4 phases, 29 phase tasks, 0 complete; original identity table remains an exact 37-ID catalog match. Supplemental candidate table has 4 decisions, not 4 new skills. Local-link/integrity results are in the [validation record](validation-261002-0832-nckh-resource-plan.md).
- These checks do not close corpus VI/EN, reviewer, per-file rights, CRO/SEO, callable route, native/runtime or protected-holdout acceptance. No rejected proposal was reintroduced; implementation remains pending and needs a separate user request.
