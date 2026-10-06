---
title: "Test đọc full kit skill nckh"
description: "Test đọc skill, hook và resource của full kit nckh. Gemini do người dùng chạy riêng. Lỗi thì xuất report từ log local, không sửa kit."
status: pending
priority: P1
effort: "3h"
branch: "none"
tags: [nckh, test, hooks, resources, gemini]
blockedBy: []
blocks: []
created: 2026-10-06
---

# Test đọc full kit skill nckh

## Overview

Viết và chạy một unittest đọc được toàn bộ skill kit `nckh`: link trong `SKILL.md` và reference, resource đã khai trong catalog, và hook runner. Lần chạy có log trong session này là CPython local. Người dùng tự mở Gemini và chạy cùng lệnh ở ngoài. Nếu có lỗi đọc, xuất một report Markdown từ stdout/stderr local. Không sửa kit để ép test xanh trong plan này.

<!-- Updated: Validation Session 1 - Gemini là phiên người dùng tự chạy, không spawn subagent -->

Bản nháp chưa chạy: `plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py`. Quan sát cũ tại `plans/reports/261006-2056-nckh-kit-read-test.md` chỉ là giả thuyết cần chạy lại, không phải kết quả của plan này.

## Goals

| # | Goal | Priority |
|---|------|----------|
| 1 | Một testcase phủ skill source, projection `.agents/skills`, catalog resource, và hook | P1 |
| 2 | Chạy unittest local và ghi lệnh để người dùng tự chạy trên Gemini | P1 |
| 3 | Report `.md` chỉ khi lệnh thất bại, và khớp output lần chạy | P1 |

## Phases

| # | Phase | Status |
|---|-------|--------|
| 1 | [Khóa testcase đọc kit](./phase-01-start.md) | Pending |
| 2 | [Chạy suite local, giao lệnh Gemini](./phase-02-run-read-suite.md) | Pending |
| 3 | [Xuất report nếu có lỗi](./phase-03-write-failure-report.md) | Pending |

## Cross-Plan Dependencies

Không có plan nào chặn plan này. Các plan đang mở chạm cùng kit nhưng plan này chỉ đọc cây hiện tại:

| Relationship | Plan | Status |
|---|---|---|
| none | [261002-0832-nckh-skill-resource-quality](../261002-0832-nckh-skill-resource-quality/plan.md) | in-progress |
| none | [260930-1910-nckh-portable-skill-kit](../260930-1910-nckh-portable-skill-kit/plan.md) | in-progress |
| none | [261004-0047-nckh-research-data-hooks-writing](../261004-0047-nckh-research-data-hooks-writing/plan.md) | in-progress |

## Success Criteria

- [ ] `python -m unittest discover -s plans/261006-1433-nckh-kit-gemini-read-test -p test_kit_read.py -v` chạy từ workspace root và exit code được lưu
- [ ] Có file lệnh để dán vào Gemini riêng; session này không spawn Gemini
- [ ] Mọi assertion đỏ của lần chạy local có mặt trong report; không có lỗi bị tóm tắt mất
- [ ] Suite xanh thì không tạo report lỗi
- [ ] Cook không sửa kit sau report

## Not in scope

- Sửa shadow `tests/hooks`, vá bytes resource, hoặc cài skill còn thiếu
- Cài hook native vào `.cursor`, `.agents`, `.codex`, `.claude`
- Chạy full `discover -s tests` ngoài file `test_runner.py` dùng để chứng minh import hook
- Đổi catalog, hash, hoặc qualification khoa học

## Unresolved Questions

- Bốn file hook native hiện không có. Test phải ghi nhận vắng mặt, không khóa điều kiện "bắt buộc vắng".
- Output Gemini riêng của người dùng chưa có. Report của cook không được ghi rằng Gemini đã chạy.

## Validation Log

### Verification Results
- **Tier:** Standard
- **Claims checked:** 24
- **Verified:** 22 | **Failed:** 0 | **Unverified:** 2

#### Checked
1. [Fact Checker] `plans/261006-1433-nckh-kit-gemini-read-test/test_kit_read.py` — file có. `assertEqual(absent, ...)` tại dòng 200.
2. [Fact Checker] `nckh-kit/scripts/search-resource.py:78` — `def _verify_source(resource, root, reader=None)`.
3. [Contract Verifier] `_verify_source` callers: `search-resource.py:261`, `tests/resource/test_real_sources.py:35`, nháp `test_kit_read.py:56`. Plan không đổi chữ ký.
4. [Fact Checker] `nckh-kit/hooks/runner.py:22` — `HOSTS = {claude, codex, cursor, agy}`.
5. [Fact Checker] `nckh-kit/scripts/hook-preflight.py` và `configure-hooks.py` có mặt.
6. [Fact Checker] `skills.json` có 43 `id`. Sáu id không có thư mục trong `.agents/skills` (37 `SKILL.md`): `nckh-humanwrite` dòng 662, `nckh-paperwrite` 676, `nckh-dataset` 690, `nckh-statistics` 704, `nckh-telemetry` 718, `nckh-aiops` 732.
7. [Fact Checker] `.cursor/`, `.claude/` không có. `.agents/hooks.json` và `.codex/hooks.json` không có.
8. [Fact Checker] `plans/reports/261006-2056-nckh-kit-read-test.md` có mặt. `tests/hooks/test_runner.py` và `tests/hooks/__init__.py` có mặt.

#### Unverified
1. Slug `gemini-3.8-flash-high` không nằm trong repo. Có trong danh sách model của session. Không còn là runner của plan.
2. Subagent `generalPurpose` không phải file trong repo. Plan không spawn subagent.

### Session 1 — 2026-10-06
**Trigger:** User chọn `/ak:plan validate` sau khi plan được tạo.
**Questions asked:** 4

#### Questions & Answers

1. **[Scope]** Catalog có 43 skill. `.agents/skills` chỉ có 37. Thiếu nckh-humanwrite, nckh-paperwrite, nckh-dataset, nckh-statistics, nckh-telemetry, nckh-aiops. Test nên xử lý thế nào?
   - Options: Fail nếu thiếu bất kỳ skill catalog nào trong `.agents/skills` | Chỉ assert skill đã cài; skill thiếu ghi vào report nhưng không làm test đỏ | Chỉ đọc source `nckh-kit`, bỏ qua `.agents/skills`
   - **Answer:** Fail nếu thiếu bất kỳ skill catalog nào trong `.agents/skills`
   - **Rationale:** Full kit trên projection Cursor phải đủ 43 skill. Thiếu file là lỗi đọc.

2. **[Scope]** `python -m unittest discover -s tests` không import được `hooks.runner` vì `tests/hooks` che package. Đây là lỗi layout test, không phải file hook đọc hỏng. Có giữ assertion này không?
   - Options: Giữ. Suite đỏ cho đến khi discover import được runner | Bỏ khỏi suite đọc. Chỉ gọi runner bằng subprocess
   - **Answer:** Giữ. Suite đỏ cho đến khi discover import được runner
   - **Rationale:** Lỗi import hook khi discover mặc định phải bị test bắt, không được giấu bằng cách chỉ gọi subprocess.

3. **[Assumptions]** Workspace không có `.gemini/`. Gemini trong plan này là gì?
   - Options: Model `gemini-3.8-flash-high` chạy cùng lệnh unittest | Đọc thêm projection `nckh-kit/dist/**/agy` nếu có | Phải cài skill vào `.gemini` rồi mới đọc
   - **Answer:** Other
   - **Custom input:** tôi sẽ mở gemini và chạy riêng
   - **Rationale:** Session này không spawn Gemini. Cook ghi lệnh để người dùng tự chạy. Report local không được gán cho Gemini.

4. **[Scope]** Nếu suite đỏ, cook dừng ở đâu?
   - Options: Chỉ xuất report .md, không sửa kit | Viết report rồi sửa các lỗi đọc trong cùng lần cook
   - **Answer:** Chỉ xuất report .md, không sửa kit
   - **Rationale:** Plan dừng ở bằng chứng lỗi. Sửa kit là việc sau, ngoài cook này.

#### Confirmed Decisions
- Missing installed skills: fail — 43 catalog ids phải có `SKILL.md` trong `.agents/skills`
- Discover shadow: keep — `discover -s tests -p test_runner.py` phải import được `hooks.runner`
- Gemini: user-run — không spawn subagent; người dùng mở Gemini riêng
- After report: report-only — không sửa kit

#### Action Items
- [x] Sửa phase 2: bỏ spawn Gemini, thêm file lệnh cho phiên riêng
- [x] Sửa phase 3: report chỉ từ log local, không nhận là Gemini đã chạy
- [x] Giữ fail-full và assertion discover trong phase 1

#### Impact on Phases
- Phase 1: không đổi hợp đồng fail-full và discover
- Phase 2: bỏ subagent; thêm prompt/lệnh cho Gemini ngoài session
- Phase 3: một log local; không sửa kit

### Whole-Plan Consistency Sweep
- Files reread: plan.md, phase-01-start.md, phase-02-run-read-suite.md, phase-03-write-failure-report.md
- Decision deltas checked: 4 (fail-full, giữ discover, Gemini do người dùng chạy, report-only)
- Reconciled stale references: 3 (goal 2, tiêu đề phase 2, kiến trúc spawn Gemini)
- Unresolved contradictions: 0
- Các chỗ còn chữ "spawn" hoặc `gemini-3.8-flash-high` nằm trong log quyết định và trong câu cấm, không còn là bước thực hiện.

<!-- slug: nckh-kit-gemini-read-test -->

## Repository cleanup

The workspace-only draft test was moved into this plan directory to preserve the frozen r41 source inventory. Its source-root locator was adjusted; assertions and pending test status were retained. Run the updated command from the workspace root.
