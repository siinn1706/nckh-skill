# Red-team plan: Security Adversary + Fact Checker

- Ngày: 2026-10-05, Asia/Saigon. Work context: `C:/Users/USER/Downloads/test-skill`.
- Review độc lập tài liệu plan; không chạy source/scripts/tests/build, không sửa product source.
- Lần đọc đầu: `plan.md`, P1–P3 đã hoàn chỉnh. P4–P7/adoption/matrix đang được author: chưa review stubs, không lập finding vì sections chưa viết.
- Writer/visual/hooks là baseline hậu cook theo chỉ dẫn user; không đề xuất task lặp.
- Kiểm tra source hẹp: authorization/evidence/preservation policies, resource rights validators, contained/no-links helpers và current bounded-reader path. Báo cáo nguồn/manifest đã được đọc.
- Lần đầu có **1 Medium finding**, không có Critical/High finding trong các phần đã hoàn chỉnh. Kết quả full sweep và resolution hiện tại được nối phía dưới; lịch sử không bị xóa.

## Finding S1 — Medium: giới hạn input chưa thành gate trước allocation

**Plan locator:** `plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-03-scientific-datasets-and-telemetry.md:42`; verification tại `:58` và `:60`.

**Evidence:** P3 yêu cầu “bounded counts/bytes từ task”, canonical/contained paths và không load unlimited corpus, nhưng chưa khóa cách enforce trước read/parse/hash, aggregate budget/output budget hoặc failure oracle cho oversized input. Pattern sở hữu hiện có dùng `Path(path).read_bytes()` cho toàn file tại `nckh-kit/core/paths.py:20–21` và `scripts/search-resource.py:65–68`. Reader gọi đường này sau rights/hash selection; đó không phải streaming cap. Path containment/rights không giới hạn dung lượng.

**Concrete failure:** Cook tạo dataset/telemetry validator bằng helpers hiện tại. Input là file telemetry 20GB hợp lệ trong private root đã được grant, task ghi budget 1MB. Validator read/hash file trước rồi mới so count/bytes, làm agent hoặc máy cạn bộ nhớ trước khi trả oversized-input verdict. Đây là gap acceptance của plan mới, không yêu cầu audit/fix generic reader ngoài scope.

**Suggested fix:** P3 phải quy định trusted positive limits per-file + aggregate + record/line + bounded returned output; validate limits trước opening/parsing, đọc/hash theo bounded stream, reject size/record-limit vượt cap trước tạo derivative artifact. Nếu archive intake được chọn, giới hạn extracted total/member count/paths và compression expansion trước extraction. Thêm oversize/cap-missing/cap-invalid/one-huge-record tests; failure giữ receipt nhỏ, không partial artifact hay raw telemetry ở output.

## Các quyết định đã được xác minh, không tạo finding

- P1 `:38–43`, `:55–61` yêu cầu final cooked handoff, resolve pending attempts, exact pins/hashes, no edit trước baseline completion và stop khi drift; không hardcode r34 làm runtime revision.
- P1 `:41` và plan `:29–30` chặn literal ClaudeKit/proprietary document copy, giữ reference-only khi rights chưa rõ; report sources xác nhận root/nested conflicts. Không đảo quyết định này vì MIT metadata.
- P1 `:42`, P3 `:41`, plan `:75` giữ data acquisition/runtime/provider/cloud/fault/native/publication quyền riêng; credentials hoặc source text không cấp quyền, đúng `authorization-policy.md:3–16`.
- P3 `:33–37`, `:43–45`, `:64` giữ raw/normalized/redacted hashes, raw/labels private, no fake modality, label-feature separation và split invalidation.
- `authorization-policy.md:5–7` đã phân loại retrieved instructions là untrusted data; P3 `:42` cấm arbitrary source commands. Không tự gọi đây là enforced prompt-injection sandbox.
- Public resources ON và no private measurements/logs/labels/raw runs thuộc plan `:29`; việc closure/multi-source public provenance cần review P5/P7 khi được viết.

## Trạng thái lần đầu — historical

Status: DONE_WITH_CONCERNS
Summary: Đã hoàn tất sweep ban đầu các phần plan hoàn chỉnh P1–P3 với một gap Medium về cap trước allocation; rights/grants/baseline defenses hiện có được giữ.
Concerns/Blockers: Full-plan verdict chưa có vì P4–P7/adoption/matrix đang author. Chờ controller báo hoàn tất để review phần còn lại; không suy ra missing requirement từ stub.

## Full sweep sau khi hoàn tất draft — 2026-10-05

Đã đọc toàn bộ 10 files: `plan.md`, `phase-01-start.md`, `phase-02-research-and-statistics.md`, `phase-03-scientific-datasets-and-telemetry.md`, `phase-04-devops-and-aiops-methods.md`, `phase-05-curated-research-resources.md`, `phase-06-reproducible-experiment-workflows.md`, `phase-07-integration-and-qualification.md`, `source-adoption-map.md`, `acceptance-matrix.md`. Chỉ review plan; không chạy các command triển khai/kiểm chứng được đề xuất.

**Kết quả: 0 genuinely new consequential findings. S1 đã resolved ở cấp plan.** Không có Critical/High/Medium mới trong lens security/rights/fact-check của lần đọc này.

### Resolution của S1

| Locator hiện tại | Nội dung sửa đã xác minh |
|---|---|
| `phase-03-scientific-datasets-and-telemetry.md:42` | Controller-trusted per-file/aggregate bytes/records/output caps kiểm trước read/parse/allocation; bounded stream/hash; payload không nâng caps; oversize từ chối, không clipped complete |
| `phase-03-scientific-datasets-and-telemetry.md:60` | Oversize và aggregate excess là failure oracle trước unbounded allocation |
| `phase-05-curated-research-resources.md:50` | Resource typed JSONL có trusted byte/record/token/output budget, kiểm trước allocation và stream/hash giới hạn |
| `phase-06-reproducible-experiment-workflows.md:41` | Checker của graph/manifest/prediction cũng dùng trusted caps và stream; oversized graph/artifact không thành clipped success |
| `source-adoption-map.md:89` | Caps thống nhất toàn chain; artifacts không tự nâng cap, bounded failure reason |
| `acceptance-matrix.md:47` | Falsifier gồm oversized file và nhiều file dưới individual cap nhưng vượt aggregate; bounded stream/hash và refusal |

Resolution này xác nhận requirement và acceptance của tài liệu. Code/actual oversize behavior vẫn chưa được triển khai hoặc quan sát trong lượt planning; không ghi S1 như runtime đã pass.

### Defenses đã đối chiếu trên full plan

- **Rights/provenance:** P1 `:41`, P4 `:16,:45,:68`, P5 `:35–39,:54–56,:78`, adoption `:45–56` giữ no-copy ClaudeKit/proprietary document quartet, per-component RCAEval rights, unknown ZIP commits, authored-versus-copied distinctions. Additive owned provenance phải agree registry/pins/build/export/relocated/public verifier; legacy strict copy rules không được nới.
- **Untrusted data/authority:** P4 `:41,:49–50,:64`, P5 `:50,:78`, P6 `:42` và matrix `:75` giữ logs/docs/snippets/manifest argv là inert data. Validator không subprocess/provider/network/install; real agent/native prevention cần actual granted side-effect traces, không được certify từ unit fixture.
- **Private/gold/model data:** P3 `:33–37,:43–44,:64`, P4 `:35,:41,:47`, P5 `:58`, P7 `:44`, matrix `:41,:75` tách private raw/labels và gold khỏi features/model input/package; preserve transform/split/exposure chronology. Output/receipts phải theo shared private-data policy, không biến quyền đọc thành quyền chia sẻ.
- **Acquisition/runtime grants:** P1 `:38,:42`, P6 `:16,:43–46,:65`, plan `:75` giữ local pilot/provider/cloud/cluster/fault/native/install/publication target/budget authority riêng; ambient token/context hoặc JSON grant không cấp quyền.
- **Path/size/lifecycle:** P3 `:42`, P6 `:41–42`, P7 `:16,:32,:47–48,:84` có contained named roots, stream budget, owned process/temp cleanup, no-write preview và hash-bound preservation. Source containment/no-links helpers được dùng làm evidence pattern; đây không là OS sandbox/universal enforcement claim.
- **Baseline/concurrency/truthfulness:** P1 `:38–43,:55–65`, P7 `:32,:42,:46`, matrix `:9–16,:98–103` yêu cầu final cooked handoff, exact protected inputs, stop/invalidations khi drift, single freeze owner và separate technical/native/owner/scientific lanes. Không hardcode r34/39/156 thành completed baseline.
- **Public ON:** Plan `:29`, P5 `:74,:78`, P7 `:47,:82`, matrix `:86–87` giữ ON cho public packages; OFF chỉ internal same-base comparison và actual disabled/no-read. No actual pilot/private labels/provider traces đi vào package.

### Phạm vi handoff

Đã refresh các edited lines cuối: P5 `:27,:55,:72` đặt serial identity/profile/base-case/source-kind prerequisite trước consumer registration/read và để pinned compatibility sau freeze; P7 `:75,:78` truyền explicit `--models balanced` trong noninteractive dry-run và giữ model choice cần record/verify. Đây là fixes có owner đã được controller theo dõi, không lập finding mới hoặc đếm lại. Reviewer này không sửa plan/source hoặc grant implementation.

Status: DONE
Summary: Full sweep đủ 10 draft files hoàn tất với 0 finding mới; S1 historical được giữ và xác nhận resolved trong requirements/acceptance xuyên P3/P5/P6/adoption/matrix.
Concerns/Blockers: Không có blocker security/rights mới ở cấp plan. Actual permissions/rights closure/native behavior/scientific acceptance còn là execution gates tương lai; review tài liệu không thay thế các gate đó.

