# Report thiết kế testcase r41 — 2026-10-06 Asia/Saigon

## Kết quả

Đã tạo bộ testcase dùng chung cho hai plan AGY/Cursor, bao phủ 43 skill r41. Kiểm tra frozen source và hai package pass ở lớp static. Chưa chạy native host, model/provider, hooks activation, installer transaction hoặc human/scientific review trong delivery này.

| Kiểm tra thực sự chạy | Kết quả | Bằng chứng |
|---|---|---|
| Local source validator `nckh-kit/evals/run-evals.py --validate-only` | FAIL vì inventory thêm file chưa pin. | [Receipt lỗi](../261006-2210-r41-shared-testcases/source-validation.json) |
| Frozen published source validator | PASS: 43 identities, 172 base cases, 19 families, 224 historical native cells, 256 writer native cells, 20 writer scenarios, 12 domain scenarios. | [Receipt frozen source](../261006-2210-r41-shared-testcases/published-source-validation.json) |
| Authored suite và cả hai `verify_bundle` | PASS: source pins, package hashes, 215 skill cases, 35 bindings/host; native vẫn not-run. | [Suite receipt](../261006-2210-r41-shared-testcases/suite-validation.json) |
| Hai plan, `ak plan validate` và `ak plan parse` | PASS ở lớp cấu trúc; execution status pending. | [AGY validate](../261006-2210-r41-agy-full-skill-test/ak-validate.json), [AGY parse](../261006-2210-r41-agy-full-skill-test/ak-parse.json), [Cursor validate](../261006-2210-r41-cursor-full-skill-test/ak-validate.json), [Cursor parse](../261006-2210-r41-cursor-full-skill-test/ak-parse.json) |
| Rà soát delivery cuối | PASS: hai index 53 dòng, bốn phase mỗi plan, 17 Markdown được kiểm tra, không broken link hoặc scaffold stub. | [Delivery receipt](../261006-2210-r41-shared-testcases/delivery-validation.json) |
| Chuẩn bị case disposable với suite cuối | PASS: tạo workspace/prompt/result NOT_RUN cho regression và writer flags; không dispatch. | [AGY case preparation](../runs/r41-agy-preparation-check-02/agy-ide/nckh-test-fixture-contract/result.json), [Cursor case preparation](../runs/r41-cursor-preparation-check-02/cursor-ide/writer-nckh-humanwrite-conflicting-flags/result.json) |
| Regression fixture gốc | Đúng baseline thiết kế: 3 test, 2 intentional failures, 1 pass; exit 1. Đây không phải lỗi skill. | [Stdout](../261006-2210-r41-shared-testcases/fixture-regression.stdout.txt), [stderr đầy đủ](../261006-2210-r41-shared-testcases/fixture-regression.stderr.txt) |

## Findings đã xác minh

### Source local không phải inventory r41 nguyên trạng

Error nguyên văn: `source lock inventory changed; review and freeze the new revision`.

Đối chiếu `source_members()` với lock cho thấy file thêm duy nhất là `tests/release/test_kit_read.py`; không thiếu member và không có pinned file đổi hash. Lock và evaluation case bytes trùng frozen published source r41. Đây là lỗi preflight của cây source local, chưa phải native skill failure.

Không sửa, xoá file hay freeze revision mới. Hai plan dùng `github-publication/nckh-kit` làm evaluation owner đóng băng; package subject vẫn là `publication-r41/{agy,cursor}`. Nếu chạy deterministic suite trên cây local chưa xử lý chênh lệch, không được chứng nhận source r41 bằng receipt đó.

### 40 skill có positive/outcome prompt giống nhau

[Baseline review](../261006-2210-r41-shared-testcases/baseline-review.json) ghi đầy đủ 40 identities. Giữ nguyên 172 case IDs và oracle gốc; thêm một distinct fixture-contract case cho **mỗi** 43 skill. Hai prompt trùng không tự chứng minh hai feature hay hai nguồn evidence độc lập.

### Case nguồn có thể thiếu input concrete

Nhiều prompt gốc trỏ “this supplied source”, “accepted plan” hoặc “actual dataset” mà không mang file input. Suite bổ sung fixture local có hashes, authored rights và oracle cụ thể. Operator phải bind đúng input/failure condition trước dispatch; chưa có input đúng tình huống thì BLOCKED/fixture. Không tự đặt metrics hoặc coi fixture synthetic là corpus thực.

### Session hook diagnostic chưa có root cause

Trong phiên controller Codex, runtime nhiều lần phát notice `hook-input-or-context-invalid` quanh tool calls. Các thao tác được tool trả output và receipt riêng. Chưa có payload/handler/host trace để quy lỗi notice này cho r41 hoặc cho AGY/Cursor; ghi là environment diagnostic unresolved, không chấm FAIL native host từ notice của controller.

## Coverage được thiết kế

- Mỗi surface IDE/CLI: 172 case gốc + 43 fixture-contract + 12 domain + 20 writer = 247 behavioral scenarios. Hai surface mỗi host: 494 planned attempts trước retry; chưa dispatch native.
- Mỗi host: 56 invocation cells, 64 writer native cells, 35 resource bindings, sáu agent, plugin lifecycle, hooks theo từng event, 10 installer acceptance scenarios và cleanup.
- Các integration checks có happy/error paths, malformed/timeout/crash/unsupported/duplicate hooks, relocation, edited ownership và rollback. Những lớp này giữ verdict riêng, không cộng vào behavioral pass hay code coverage.
- Human taste, scientific fidelity/validity, protected holdout, provider cost/model qualification và các OS chưa chạy đều pending. Source/package/test design integrity không thay native observation hoặc quality acceptance.

## Phạm vi còn pending

Execution của hai plan trên host thật; exact host versions/interfaces/models và budget quan sát lúc chạy; independent grading theo trace/artifact; cleanup receipts. Hai plan giữ status pending. Mọi lỗi lúc chạy phải xuất report per host/attempt theo [report template](../261006-2210-r41-shared-testcases/report-template.md); không ghi đè failed attempt, không tự sửa skill trong scope test.
