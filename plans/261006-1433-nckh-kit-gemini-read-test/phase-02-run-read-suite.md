---
phase: 2
title: "Chạy suite local, giao lệnh Gemini"
status: todo
priority: P1
effort: "1h"
dependencies: [1]
---

# Phase 2: Chạy suite local, giao lệnh Gemini

<!-- Updated: Validation Session 1 - không spawn Gemini; người dùng tự chạy -->

## Overview

Chạy unittest bằng CPython trong workspace. Ghi cùng lệnh vào một file để người dùng dán vào Gemini riêng. Session này không spawn Gemini và không đợi output đó.

## Requirements

- Functional: một lần chạy local từ workspace root với lệnh discover bên dưới. Lưu exit code, thời lượng, số test, và phần fail vào `plans/261006-1433-nckh-kit-gemini-read-test/reports/local-unittest.txt`. Viết `plans/261006-1433-nckh-kit-gemini-read-test/reports/gemini-run-prompt.md` chứa đúng lệnh và câu "không sửa test, không sửa kit".
- Non-functional: không gọi subagent Gemini. Không sửa test hoặc kit trong lúc chạy.

## Architecture

Một process `python -m unittest`. File prompt chỉ là hướng dẫn cho phiên Gemini bên ngoài. Log local là nguồn của phase 3.

## Related Code Files

- Read: `plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py`
- Create: `plans/261006-1433-nckh-kit-gemini-read-test/reports/local-unittest.txt`
- Create: `plans/261006-1433-nckh-kit-gemini-read-test/reports/gemini-run-prompt.md`

## Implementation Steps

1. Từ workspace root chạy và lưu nguyên stdout/stderr:

```text
python -m unittest discover -s plans/261006-1433-nckh-kit-gemini-read-test -p test_kit_read.py -v
```

2. Viết `gemini-run-prompt.md` với cwd, lệnh, và lệnh cấm sửa kit/test.
3. Chuyển phase 3 với log local. Không so với một lần chạy Gemini vì lần đó chưa xảy ra trong session này.

## Success Criteria

- [ ] `local-unittest.txt` có exit code
- [ ] `gemini-run-prompt.md` có cùng lệnh
- [ ] Không spawn subagent và không sửa kit trong phase này

## Risk Assessment

`_verify_source` hash toàn bộ resource nên lần chạy có thể lâu. Không hạ probe xuống `is_file()` để cho nhanh. Discover `test_runner.py` chỉ để chứng minh import; không thay bằng full suite. Output Gemini của người dùng đến sau không được ghi đè log local.
