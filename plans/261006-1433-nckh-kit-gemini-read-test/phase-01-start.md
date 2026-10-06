---
phase: 1
title: "Khóa testcase đọc kit"
status: todo
priority: P1
effort: "1h"
dependencies: []
---

# Phase 1: Khóa testcase đọc kit

## Overview

Chốt một unittest đọc được skill, hook và resource. Bản nháp `plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py` được giữ nếu nó kiểm đúng hợp đồng; sửa assertion khóa "hook native phải vắng".

## Requirements

- Functional: mỗi skill trong `nckh-kit/core/registry/catalog/skills.json` có `SKILL.md` ở source và ở `.agents/skills`. Link Markdown tương đối trong skill source và skill đã cài phải trỏ tới file tồn tại. Mỗi resource trong catalog source và trong catalog nhúng của skill đã cài phải đọc được qua `_verify_source` của reader cùng root. ID `R-*` trong `resource-lookup.md` phải có trong catalog gần nhất. `nckh-kit/hooks` và `scripts/hook-preflight.py`, `scripts/configure-hooks.py` parse được. Runner nhận context hợp lệ cho cursor, agy, claude, codex và exit 0. `python -m unittest discover -s tests -p test_runner.py` từ `nckh-kit` import được `hooks.runner`.
- Non-functional: test thất bại bằng danh sách lỗi thật. Không mock file thiếu thành pass. Không xóa assertion để né shadow package `tests/hooks`.

## Architecture

Reader mỗi root là subprocess riêng để `import core` không dính package của root trước. Root source là `nckh-kit`. Root đã cài là `.agents/skills/<skill>/references/_shared` khi có `resources.json`. Hook invoke gọi `nckh-kit/hooks/runner.py` bằng subprocess, không `import hooks` trong process của discover.

## Related Code Files

- Modify: `plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py`
- Read: `nckh-kit/scripts/search-resource.py`
- Read: `nckh-kit/hooks/runner.py`
- Read: `nckh-kit/core/registry/catalog/skills.json`
- Read: `nckh-kit/core/registry/catalog/resources.json`

## Implementation Steps

1. Đọc lại `test_kit_read.py` và đối chiếu từng assertion với Requirements.
2. Bỏ assertion bắt bốn path hook native phải vắng. File có mặt thì phải parse được JSON. File vắng ghi vào receipt, không làm test đỏ chỉ vì chưa cài.
3. Giữ fail khi link gãy, skill catalog thiếu file, resource thiếu bytes hoặc lệch hash, lookup ID không có trong catalog, runner trả exit khác 0, hoặc discover mặc định không import được `hooks.runner`.

## Success Criteria

- [ ] File test nằm ở `plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py`
- [ ] Assertion hook native không yêu cầu file phải vắng
- [ ] Chưa chạy suite ở phase này ngoài kiểm tra syntax `python -m py_compile plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py`

## Risk Assessment

Nháp hiện tại có `assertEqual(absent, <cả bốn path>)` tại dòng 200. Giữ nguyên sẽ đỏ khi người dùng cài hook, và xanh khi chưa cài, nên không phát hiện JSON hỏng. Sửa assertion trước khi chạy suite local.

<!-- Updated: Validation Session 1 - giữ fail khi thiếu skill đã cài và khi discover không import được hooks.runner -->
