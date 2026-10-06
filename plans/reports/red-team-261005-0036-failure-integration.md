# Red-team plan: Failure Mode Analyst + Flow Tracer

- Ngày: 05/10/2026, Asia/Saigon; work context `C:/Users/USER/Downloads/test-skill`.
- Scope: review-only toàn bộ `plan.md` và P1–P7 đã có body, current-kit review/source reports và các source consumers hẹp. Không chạy source, test, lint, build, provider hoặc installer; không sửa product source.
- Adoption map và acceptance matrix còn đang author ở lượt này; không lập finding từ việc chúng chưa hoàn tất. Writer/visual/hooks là baseline hậu cook theo user, không tạo task lặp. Không có `--yagni`.
- Ba findings Medium; không có Critical/High finding mới. Các drafting corrections về actual split membership, task decision time, caps trước allocation, outside CWD và dynamic schema lookup đã có owner, không tính lại thành findings.

## F1 — Medium: resource registration P5 phụ thuộc catalog integration bị hoãn tới P7

**Evidence:** `plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-02-research-and-statistics.md:20` và `:48` giao controller integrate catalog/profile/four base cases ở P7. `phase-05-curated-research-resources.md:44`–`:47` yêu cầu packs có consumers statistics/telemetry/aiops/dataset; `:54` và `:56` yêu cầu end-to-end provenance rồi đăng ký/đọc typed packs, `:70` đề xuất CLI với consumer `nckh-telemetry`. P7 `phase-07-integration-and-qualification.md:42`–`:44` mới integrate exact identity/profile/mapping và complete readers. Current `nckh-kit/core/resources.py:52`–`:58` kiểm mọi resource consumer phải nằm trong catalog và từ chối unknown identity trước khi trả registry.

**Concrete failure:** P5 đăng ký `R-telemetry-dictionary` với consumer `nckh-telemetry` trong khi catalog vẫn là P1 baseline. `registry()` trả `resource consumer missing, duplicate or unknown`; lỗi xảy ra cho toàn registry, nên cả existing-resource compatibility checks dùng registry cũng fail. Nếu hoãn registration tới P7 thì CLI/test của new packs ở P5 chưa verify được, trong khi P6 đã phụ thuộc P5 artifacts hoàn tất. Đây là thiếu thứ tự prerequisite, không phải yêu cầu nới validator.

**Fix / owner:** Controller khóa một bước integration tuần tự trước gate P5: integrate exact catalog/profile/base-case skeleton và các exact-set prerequisites, rồi đăng ký/source-kind/readers của packs; hoặc tách P7 thành integration trước pilot và final freeze/qualification sau P6. Nêu rõ P5 dùng registry thật nào và cổng nào phải pass trước P6; giữ final freeze và full qualification ở một owner. Domain owners tiếp tục chỉ ghi specialty files.

## F2 — Medium: pinned-source regression được đặt trước freeze cần thiết cho chính nó

**Evidence:** `phase-07-integration-and-qualification.md:45` yêu cầu narrow new tests + existing affected regression suites trước `:46` sole freeze. Command block cũng đặt existing `tests.release.test_qualification` ở `:67` trước `freeze-source-lock.py --write` ở `:68`. `nckh-kit/tests/release/test_qualification.py:13` gọi `validate_cases()`, và `nckh-kit/core/evaluation.py:173` gọi `verify_source_lock()`. `nckh-kit/core/build.py:201`–`:206` từ chối inventory hoặc byte drift; `:305` build cũng verify lock trước materialization. Các existing closure regressions trong phạm vi P7 gọi build tại `nckh-kit/tests/build/test_closure.py:78`–`:79`, và trực tiếp lock verifier tại `nckh-kit/tests/resource/test_closure.py:34`.

**Concrete failure:** P2–P6 tạo schemas/helpers/skills/packs và P7 sửa catalog/readers/tests. Lock P1 vẫn pin baseline; existing release/closure regression bắt buộc fail do đúng invariant source drift trước khi controller được đến sole freeze. Một cook tuần tự có thể bị chặn ở gate :45 hoặc bị cám dỗ bỏ assertions, dù implementation không có lỗi domain.

**Fix / owner:** Controller chia verification rõ: (1) schema/domain tests không phụ thuộc frozen lock + independent source review; (2) sole candidate freeze sau khi các owner ngừng sửa; (3) tất cả pinned release/build/resource closure regressions, validate/deterministic và packaging. Nếu bước (3) phát hiện lỗi thì preserve failed receipt, sửa đúng owner, corrective freeze rồi rerun affected descendants, theo invariant đã ghi ở P7:46. Sửa command order tương ứng; không đổi validators hay ghi check pass trên dirty source.

## F3 — Medium: installer preview command thiếu model profile bắt buộc

**Evidence:** `phase-07-integration-and-qualification.md:75` truyền runtime/scope/project/kits/mode/dry-run nhưng không có `--models`. Current `nckh-kit/installer/nckh-installer.py:62` chỉ mở prompt cho install/update khi không dry-run; `:100`–`:101` yêu cầu `args.kits`, `args.mode`, `args.models` đều có trước `:110`–`:112` preview. `:120`–`:122` trả blocked exit 4 khi thiếu.

**Concrete failure:** Dù extracted package hợp lệ và target disposable, command đã ghi luôn dừng với `non-interactive requires --runtime --scope --kits --mode --models explicitly`, không tạo transaction preview. Loop tám surfaces theo command này không thể tạo evidence P7:48/:58 yêu cầu.

**Fix / owner:** Integration controller thêm `--models balanced` hoặc đúng profile đã freeze từ live accepted model policy cho mọi command preview; ghi profile/runtime/package/target hashes trong receipt. `--models` chỉ cấu hình preview, không cấp provider/native execution authority. Giữ `--dry-run`, không thay installer để thêm silent default.

## Verified controls và concerns bị bác bỏ

| Concern đã truy vết | Quyết định theo evidence |
|---|---|
| Hardcode snapshot r34 hoặc target 43/172 | Không lập finding: P1:32 và :38–43 require final handoff/exact baseline, report delta trước source edits; plan.md:20–22 giữ snapshot là historical và target contingent. |
| Thêm catalog identity đơn lẻ hoặc làm arbitrary counts | Không lập finding: P7:32/:36 require consumer inventory/exact set; source `core/build.py:125–129`, `core/acceptance.py:75–114`, `core/evaluation.py:130–150` đều fail closed; plan sở hữu migration cùng profile/cases/tests. |
| Owned-reference bị nhét vào legacy copied record | Không lập finding mới: P5:34–38/:54/:76 require additive dispatcher và same-closure rollback, giữ legacy variants; current `core/resources.py:162–201`, `core/build.py:502–511/:595–604` chứng minh dispatch thật cần cập nhật. Inventory phải bao gồm bundle-v2 schema, exported manifest và helper/hook dependency closure vì `core/build.py:38–46/:473–474` dùng những schemas này. |
| Historical format1/2 hoặc writer matrix bị đổi để đạt count | Không lập finding: P7:36/:43/:48 giữ historical lane và legacy verification; `core/evaluation.py:21–65/:117–127` tách writer/static/protected qualification khỏi scientific dataset split. |
| Preview/build bị gọi là native/scientific pass | Không lập finding: P7:78/:82 giữ evidence lanes riêng; installer :110–112 chỉ trả preview, bundle verifier `core/build.py:541–542` cấm builder claim runtime plugin state. |
| Rollback có thể xóa concurrent baseline/private inputs | Không lập finding: P1:61, P3:64, P5:76, P6:65, P7:84 require matching owned preimages/hashes, preserve failures/history/raw/private data và không kill ngoài ownership. |

## Independent gate matrix

| Gate | Trạng thái review | Phạm vi |
|---|---|---|
| Outcome/scope/owners/compatibility intentions | Pass trong phần đã hoàn tất | Bốn specialty owners, existing engineering/marketing/cook giữ semantics; không duplicate writer/visual/hooks. |
| Integration prerequisite order | Pending correction | F1/F2 cần thứ tự cụ thể trước thực thi; không phát hiện lỗi source thực thi vì lượt này chỉ review plan. |
| Current verification command syntax | Pending correction | F3; outside-CWD drafting correction thuộc controller report, không count lại. |
| Full adoption/matrix sweep | Pending | Chờ full-doc handoff; không suy requirement thiếu từ drafts. |
| Implementation/deterministic/package/pilot/native/scientific acceptance | Not observed | Không chạy hoặc xác nhận các gates này ở lượt review. |

Status: DONE_WITH_CONCERNS
Summary: Đã truy vết toàn bộ phase bodies và current shared consumers; phát hiện ba lỗi Medium về thứ tự resource/catalog integration, source-lock-dependent regression trước freeze và installer preview thiếu --models.
Concerns/Blockers: Full adoption-map/acceptance-matrix sweep chờ controller báo hoàn tất; các findings cần adjudication trong controller session, không authorizes product repairs.

## Final reconciliation — toàn bộ 10 files đã hoàn tất

Controller đã handoff `plan.md`, P1–P7, `source-adoption-map.md` và `acceptance-matrix.md`; đọc lại toàn bộ body sau khi planner ngừng chỉnh sửa. F1/F2/F3 và locators phía trên được giữ nguyên như lịch sử draft trước correction. Bảng dưới dùng final line references và là kết luận review hiện hành. Không chạy source/test/build/installer/pilot; chỉ đọc source consumers cần thiết và băm hai planning source-manifests.

### Disposition của findings ban đầu

| Finding | Final evidence | Disposition |
|---|---|---|
| F1 — catalog prerequisite bị hoãn | P2 `phase-02-research-and-statistics.md:20/:48` handoff integration P5; P5 `phase-05-curated-research-resources.md:27/:55` controller serially integrate exact identities/profile/four-case/count consumers trước registration/read. P5 `:59/:72` require actual current-registry + standalone ON/OFF behavior before P6, dùng lock-independent subset; P7 `phase-07-integration-and-qualification.md:25/:32/:43` reconcile prerequisites đã tích hợp. `source-adoption-map.md:84–87` và `acceptance-matrix.md:26/:86/:98` cùng thứ tự. | **Resolved in plan.** New consumer được admit trước resource registry reads; P6 không nhận pack chưa có actual local behavior evidence. Không nới unknown-consumer guard. |
| F2 — pinned regressions trước freeze | P7 `:45–46` require independent domain/schema review → owner quiescence → sole candidate freeze → pinned release/resource/build/closure/full checks. Command block `:66–70` cùng thứ tự; source lock được freeze ở `:67`, pinned tests ở `:68`. P2 `:60`, P3 `:58`, P4 `:62`, P5 `:59/:72` phân biệt local/independent gates với pinned regressions. Adoption map `:87`, matrix `:93/:98` cùng rule. | **Resolved in plan.** Dirty-source lock failures không bị dùng như prerequisite để tới freeze. Corrective revisions và rerun descendants giữ failed receipts, không transplant verdict. |
| F3 — preview thiếu models | P7 `:75` cung cấp `--models balanced --dry-run`; `:78` yêu cầu profile explicit/frozen và giải thích dry-run không prompt. Matrix `:92` cũng yêu cầu supplied models. Current `nckh-kit/core/models.py:8` có profile `balanced`; installer `:47/:62/:100–112` dùng supplied profile trước preview. | **Resolved in plan.** Command đạt yêu cầu syntax về models; preview/runtime execution chưa được chạy hoặc ghi pass. |

### Full flow và source facts đã reconcile

- P5 lock-independent route có căn cứ current source: `nckh-kit/core/resources.py:45–99` đọc/validate current registry, resource/dependency/hash/rights và catalog consumers, không gọi global source lock. Standalone `nckh-kit/scripts/search-resource.py:3–11` chỉ import stdlib; `:206–232` gate OFF trước registry/files và ON kiểm declared consumer/locale/genre/domain/source hashes. P5 sẽ bổ sung new typed/source-kind dispatch theo scope; việc reader hiện chưa support new variant là công việc được plan chỉ rõ, không phải một check đã pass.
- P7 temp/CWD correction nhất quán ở `:16/:47/:63/:74/:78` và matrix `:89`: `OUTSIDE` được chọn/resolved/owned trong permitted temp ngoài `WORK`; CWD ở sibling ngoài extracted bundle; receipts giữ ở RUN trước cleanup. Không còn path `RUN/outside-cwd` được sử dụng làm command.
- P1 `:34` và P7 `:23/:38` giữ actual dynamic schema lookup, không dựng registration table hoặc bắt buộc thay engine. P2–P6 specialty contracts có owner/helpers/tests; P7 `:32/:38/:44` vẫn require narrowed consumer inventory và dependency/schema closure trước freeze. Chưa có finding mới về ordering hoặc ownership.
- Adoption map `:11–12` ghi hai raw source-manifest hashes khớp `Get-FileHash` đọc hiện tại: scientific `e10bfc3d2d682990bb40067aef9a1b9b15b2268d84923452acaf06b4d39ce959`; other `a5f5687c44f8c19114a0f61f345b406ee2f0b2d7bde7089f9acbf6453032a3ed`. Đây là input integrity; không clear redistribution/runtime/scientific gates.
- Adoption map `:17/:39/:45–56/:67/:94` giữ ZIP Git identity unknown, per-component/no-copy decisions và raw/private project data ngoài package. Matrix `:9–16/:90–101` giữ evidence lanes, actual real pilot, exact contingent count, owner versus scientific acceptance và mọi implementation gate pending. Không dùng successful lookup/hash/plan validation làm scientific acceptance.
- Domain owners hand off specialty files rồi stop shared edits: P1 `:20/:43/:65`, P7 `:32/:46`, adoption map `:84–90`. Same-closure rollback có current-hash/preimage guards và preserve failed/history/private/concurrent baseline. Không phát hiện concrete destructive rollback route còn thiếu trong plan.

### Final independent gate matrix

| Gate review | Final review status | Giới hạn |
|---|---|---|
| All10 files / dependency / ownership / shared-contract flow | Reviewed, no unresolved consequential finding | Tài liệu kế hoạch đã hoàn tất; không phải xác nhận implementation readiness từ parser/count. |
| F1/F2 prerequisite/freeze ordering | Resolved in plan | Actual local reader/pinned gates chỉ pass khi future cook thực hiện đúng order và ghi evidence. |
| F3 current CLI models requirement và outside CWD route | Resolved in plan | CLI/source compatibility được đọc tĩnh; không có installer hoặc smoke execution receipt. |
| Baseline/catalog/source kind/legacy/rollback intentions | Coherent within reviewed scope | P1 exact final cooked baseline và source-rights/runtime gates vẫn phải resolve trước actions. |
| Implementation/deterministic/package/real pilot/agent/native/owner/scientific | Pending / not observed by this review | Không gate nào được đóng bởi review tài liệu. |

**Remaining consequential findings: 0.** Không có unresolved question hoặc blocker cho completion của review plan trong lens này. Những execution gates tương lai vẫn giữ pending đúng scope; source hiện tại chưa được upgrade bởi lượt review.

Status: DONE
Summary: Đã đọc full10 files và reconcile F1/F2/F3; cả ba resolved in plan với cùng order/ownership/commands trong phases, adoption map và acceptance matrix. Không phát hiện consequential finding mới.
Concerns/Blockers: Không còn blocker cho plan review; implementation/runtime/rights/pilot/native/owner/scientific evidence chưa thực hiện và không được review này xác nhận pass.
