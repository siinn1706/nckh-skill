# Audit runtime/evaluation/packaging NCKH

## Kết luận

`--validate-only` chạy được và giữ đúng trạng thái pending; narrow release/build tests
đạt. Nhưng package evaluator hiện chưa đủ tin cậy để chứng minh frozen evaluation
integrity: có hai lỗi contract trực tiếp (negative oracle mâu thuẫn expected route;
required-family validation chỉ kiểm đếm) và một gap liên kết evidence. 148 lượt
native direct development là evidence có thật ở controller corpus riêng, không phải
package manifest đã được runner cập nhật. Stable qualification vẫn NO-GO đúng theo
plan.

## Phạm vi

Đã đọc `nckh-kit/core/evaluation.py`, `agent_runs.py`, `build.py`, `guards.py`,
`processes.py`, `evals/run-evals.py`; toàn bộ 37 skill case manifests,
`required-families.json`, `qualification.json`, baselines/rubrics; candidate receipts;
build/release tests; `nckh-kit/docs/qualification.md`; plan và phase 7.

Đã đối chiếu direct evidence tại `plans/reports/testing-261001-direct-skill-development.md`,
`plans/evaluation/direct-skill-tests/development-corpus.json`, `results.json`,
`controller-reviews.json` và `run-native-suite.py`.

## Findings

### High — Negative cases có oracle mâu thuẫn với route/expected outcome

Tất cả 37 case có `type: "negative"` đều khai báo `expected_route:
"reject-this-skill"` và expected outcome là reject/handoff, nhưng
`oracle.acceptance` lại lặp tiêu chí acceptance của chính skill. Ví dụ
`nckh-kit/evals/cases/research-writing-visuals/nckh-write.json:49-84` yêu cầu
reject việc search literature, nhưng oracle chỉ yêu cầu prose usable/fidelity/no
invented citation; không có điều kiện reject/handoff. Mẫu tương tự xuất hiện ở
37/37 negative manifests, không có negative oracle nào chứa điều kiện reject.

`nckh-kit/core/evaluation.py:27-28` chỉ kiểm tra các field truthy và `:35-38`
chỉ kiểm tra đủ bốn ID. Vì vậy `python evals/run-evals.py --validate-only` vẫn pass
dù evaluator nhận route reject nhưng không có oracle reject tương ứng. Đây là lỗi
đánh giá thực, không phải yêu cầu prompt phải dài hơn.

**Khuyến nghị:** sửa negative oracle để kiểm tra owner/handoff/không thực hiện task,
hoặc thêm schema/validator buộc oracle phủ expected route/outcome; thêm regression
test. Không dùng direct score để âm thầm ghi đè manifest cũ.

### High — `validate_cases` không xác thực nội dung 19 required families

`nckh-kit/core/evaluation.py:41-43` chỉ kiểm tra `len(families) == 19` và 19 ID
duy nhất. Không kiểm tra `scenario`, `skills`, `status`, `input_rights`,
`provenance`, `oracle`, `evaluator`, `receipt_reference`, cũng không kiểm tra skill
IDs trong family có trong catalog/case IDs. File malformed hoặc 19 family trỏ tới
skill không tồn tại vẫn vượt `--validate-only`.

`evaluation.py:44-45` cũng tải protocol/rubrics nhưng không validate schema/shape của
`qualification.json`; các phần bắt buộc như `development_max_rounds`, `split`,
`baselines`, `forbidden` có thể thiếu mà validator không báo (runner có thể chỉ
fail muộn bằng `KeyError`).

**Khuyến nghị:** schema riêng cho required families/protocol; validate field types,
allowed status/rights, catalog/case mapping và required protocol keys. Giữ các
status `not-run`; structure validation không được promote qualification.

### Medium — Direct 148 evidence chưa được liên kết vào package evaluator

`plans/reports/testing-261001-direct-skill-development.md:5-21` ghi đủ 37 × 4 =
148 prompt native, latest 147 pass/1 fail (`nckh-cro:positive`, thiếu `noindex`).
`:25-45, :55-71` ghi rõ đây là exposed development dùng synthetic owned fixtures,
shared session và controller review; không phải human gold, protected holdout,
matched baseline hay full native matrix. `development-corpus.json` có SHA-256
`bbb6d312df45c4bad75bef5b5e8b5a42202dfcf0122382ee59e51ce84c63de84`; native receipts
và controller reviews có hash riêng.

Trong package, các manifest vẫn `status: "not-run"`/`receipt_reference: null`,
`candidate-runner-cleanup.json:1-3,63-72` vẫn ghi `agent_cases_not_run: 148`, và
`nckh-kit/docs/qualification.md:6-18` vẫn coi 148 package cases là gate mở. Đây
là hai corpus/contract khác nhau, nhưng chưa có machine-readable mapping/hash-bound
receipt từ direct corpus về original IDs/families. Vì thế không được diễn giải
package `not-run` là “không có behavior evidence”, cũng không được diễn giải 147/1
là package qualification.

**Khuyến nghị:** giữ hai lớp evidence, nhưng thêm aggregate/receipt riêng ghi
corpus hash, source/install revision, execution condition, case mapping và review
class; hoặc ghi rõ direct corpus là controller evidence ngoài package runner. Không
đổi package case thành `pass`, không nâng `qualification` khỏi pending.

### Medium — Closure builder không hỗ trợ resource extension dù closure nhận chúng

`nckh-kit/core/build.py:16-19,39-50` chỉ đưa `.md`, `.json`, `.yaml`, `.toml`,
`.py`, `.ps1`, `.sh` vào source-lock. Nhưng `:195-206` lấy mọi file selected skill
directory qua `rglob`/`closure`. Reproduction read-only trên temporary tree cho
thấy `skills/demo/data.csv` xuất hiện trong `closure(...)` nhưng không trong
`source_members(...)`; materialization sẽ dừng ở `:205-206` với
`unlicensed/unpinned closure member`.

Source tree hiện hành không có `.csv/.jsonl/.svg` ngoài allowlist nên đây là
safe-fail packaging gap, chưa phải mất dữ liệu. Tuy nhiên một skill có data/diagram
resource hợp lệ không build được, trong khi contract không nói rõ extension bị cấm.

**Khuyến nghị:** hoặc document/guard allowlist là contract, hoặc mở rộng có chủ đích
cho resource formats thực sự cần (kèm secret/license/hash tests). Không đưa raw
private corpus vào dist.

### Low — `development_round` có thể gắn nhãn protected holdout thiếu freeze

`nckh-kit/core/evaluation.py:76-80` trả `split: "protected-holdout"` khi
`exposed_holdout=False`, không kiểm tra freeze/rights/reviewer/threshold/partition.
Test `tests/release/test_qualification.py:22-25` chỉ phủ exposed branch và round 4;
không có production caller được tìm thấy. Đây là helper contract gap, chưa quan sát
tác động runtime.

**Khuyến nghị:** yêu cầu frozen holdout receipt trước khi trả protected-holdout,
hoặc trả pending/unknown; thêm test default branch.

## Evidence đã xác minh

- `python evals/run-evals.py --validate-only`: pass; source-lock
  `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d`; 37
  identities, 148 skill cases, 19 families, 224 native cells; qualification
  pending, cost unknown.
- `python -m unittest tests.release.test_qualification tests.release.test_agent_runs
  tests.release.test_runner tests.build.test_closure`: 19 tests pass. Không chạy
  provider/native mới, không build/install mutation.
- `core/agent_runs.py:163-170` không đưa oracle/expected outcome vào JSON input;
  `:147-160,182-190` giữ completed-unreviewed, accepted count 0, unknown
  cost/model; `:173-240` recheck source/input/driver/freeze hashes và giữ private
  traces. Đây là phần contract đang làm đúng.
- `build.py`/`verify_bundle` giữ source-lock, closure hash, no-links, ownership và
  plugin/native qualification unverified; candidate receipts không thay native/human.

## Reconciliation với plan

Architecture 37-skill độc lập và plan đã duyệt vẫn phù hợp. Phase 7 đã ghi direct
run 148 prompt nhưng vẫn mở human/holdout/full-native acceptance; cách tách này đúng.
CRO failure phải giữ nguyên như coverage failure, không sửa oracle sau kết quả. Cần
sửa validator/oracle contract trước khi gọi package evaluator complete, nhưng không
xoá direct receipts hoặc hạ giá trị các controller observations.

## Unresolved questions

- `plans/evaluation/direct-skill-tests` có được coi là evidence namespace chính thức
  ngoài package runner không? Nếu có, cần owner/schema/mapping; nếu không, docs nên
  gọi nhất quán là controller development evidence.
- Resource formats nào thực sự được phép trong portable closure? Hiện chưa có
  resource source thật cần mở rộng allowlist.

Status: DONE_WITH_CONCERNS
Summary: Audit read-only runtime/evaluation/build đã hoàn tất; xác nhận 2 lỗi validator/oracle, 1 gap direct-evidence linkage, 1 safe-fail resource gap và 1 helper gap. Narrow checks pass; không sửa source/build/install/provider.
Concerns/Blockers: Negative oracle contradiction và family count-only validation làm `--validate-only` chưa đủ tin cậy để chứng minh frozen eval integrity; direct 148 evidence tồn tại nhưng hiện không phải package receipt.
