---
phase: 3
title: "Xuất report nếu có lỗi"
status: todo
priority: P1
effort: "1h"
dependencies: [2]
---

# Phase 3: Xuất report nếu có lỗi

## Overview

Nếu unittest local thoát khác 0, viết một report Markdown từ `local-unittest.txt`. Nếu thoát 0, không tạo report lỗi. Không sửa kit.

<!-- Updated: Validation Session 1 - report-only, một log local -->

## Requirements

- Functional: report nằm tại `plans/261006-1433-nckh-kit-gemini-read-test/reports/kit-read-report.md`. Có lệnh, cwd, Python, exit code, số passed/failed/skipped, thời lượng, và từng failure với error, vị trí, và nguyên nhân nhìn thấy được từ stack hoặc JSON probe. Dòng đầu ghi runner là CPython local, chưa có output Gemini.
- Non-functional: không chép `plans/reports/261006-2056-nckh-kit-read-test.md` vào làm kết quả. Không bịa screenshot. Không sửa skill, hook, resource, hay test để làm xanh. Suite xanh thì phase này chỉ ghi evidence "exit 0" trên plan, không viết file lỗi.

## Architecture

Nguồn sự thật là `reports/local-unittest.txt`. Report nhóm lỗi theo skill link, resource read, hook invoke, và import discover. Cùng một message lặp trên nhiều skill thì liệt kê đủ cặp skill/resource, không ghi "và các skill khác".

## Related Code Files

- Create: `plans/261006-1433-nckh-kit-gemini-read-test/reports/kit-read-report.md` khi exit khác 0
- Read: `plans/261006-1433-nckh-kit-gemini-read-test/reports/local-unittest.txt`

## Implementation Steps

1. Đọc `local-unittest.txt`. Nếu exit 0 và danh sách fail rỗng, đánh dấu phase xong mà không tạo report lỗi.
2. Nếu exit khác 0, viết report theo các mục Test Results Overview, Failed Tests, Critical Issues, Recommendations, Unresolved Questions.
3. Đối chiếu từng mục Failed Tests với một dòng thật trong log trước khi lưu file. Dừng. Không sửa kit.

## Success Criteria

- [ ] Exit khác 0 thì report tồn tại và mỗi failure trong log local có một mục
- [ ] Exit 0 thì không có `kit-read-report.md`
- [ ] Không có diff sửa kit hoặc test ở phase này
- [ ] Report không ghi Gemini đã chạy và không đề xuất cách làm yếu test để pass

## Risk Assessment

Probe JSON có thể rất dài khi nhiều resource thiếu bytes. Cắt stack tới đoạn gây lỗi, nhưng giữ đủ path và resource id. Không gom thành một câu "catalog lệch" rồi bỏ danh sách.
