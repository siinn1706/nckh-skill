---
title: "Phase 2: Mẫu và công việc thật"
status: in-progress
---

# 2. Mẫu và công việc thật

## Requirements

| Nguồn | Phạm vi nhỏ ban đầu | Consumers |
|---|---|---|
| Wikisource VI | Root 179667/106841/80653 và actual passages 179899/19383/71961, ghi thể loại/bối cảnh lịch sử | write, taste |
| PMC Open Access | Hai bài khoa học CC BY, license xác minh từng bài | write, taste, evidence |
| World Bank API | Một series có country/date/value/unit và raw snapshot | visuals, data |
| SWE-bench/upstream issue | Một task thật, pin/rights upstream kiểm được | fix, test, code-review |
| UCI Bank Marketing | Mẫu thật giới hạn, DOI/CC BY, duration leakage warning | analytics, experiment |

Samples là development/personal use, không human gold hoặc corpus đại diện. Nguồn không lấy được phải giữ failure; thay bằng nguồn primary tương đương và ghi rõ thay đổi.

## Todo

- [x] Download vào staging; giữ originals, URL/revision/time/hash và rights evidence.
- [x] Trích có lineage; không tạo synthetic corpus hoặc relabel third-party bytes thành owned.
- [x] Mở rộng schema/provenance tối thiểu cho VI/snapshot versions/verified rights/normalized extraction; giữ kiểm legacy.
- [x] Đăng ký resource riêng theo domain với consumer/reader/artifact.
- [x] Reader trả actual matching records/provenance; mismatch/off/no-match đúng; consumer instructions dùng thật.
- [x] Chạy reader/rights/closure tests và extracted smoke, ghi receipts.

Checkpoint acquisition: [report](../reports/acquisition-261003-real-sources.md), 11 records gồm ba actual child passages; hai Django code fixtures BSD đã ghim commit. World Bank có 26 giá trị non-null, raw unit trống. Issue/benchmark patch vẫn development-private. Packaging/reader khi đó còn mở; checkpoint mới bên dưới ghi phần đã hoàn tất.

Checkpoint mới: [resource integration](../reports/implementation-261003-real-resources.md) có năm compact packs mới, 12 consumer references và registry chín entries. [Content review](../reports/review-261003-real-content.md) đối chiếu actual bytes và rights. r24 đã qua full suite và extracted reader checks theo [runtime checkpoint](../reports/runtime-261003-candidate-r24-checkpoint.md); đây là source/package evidence, không human hoặc model verdict.

## Files and implementation

Resource worker đọc/sửa nckh-kit/core/resources.py, core/contracts/resource-*.schema.json, core/registry/catalog/resources.json, scripts/search-resource.py, scripts/resource-smoke.py, tests/resource/, consumer references/resource-lookup.md và core/profiles/resources/. Đọc core/build.py để giữ closure/provenance; chỉ sửa build khi extension thực sự cần. Không sửa acceptance/install/source lock. Researcher chỉ ghi plans/evaluation/personal-use/source-acquisition/ và report acquisition.

## Validation, risk and rollback

Chạy python -m unittest discover -s tests/resource; verify package/extracted reader sau freeze. Fixtures chỉ chứng minh guard. Rights phù hợp từng nguồn; raw sensitive data ngoài package. Rollback source/schema/registry/consumer cùng nhau từ snapshot trước sửa; giữ attempts/lock history.
