---
title: NCKH kit read test
date: 2026-10-06
scope: nckh-kit source, .agents/skills projection, hooks, resources
model: grok-4.7-xhigh
---

# Test Report — 2026-10-06 — full nckh skill kit

## Summary

Source kit `nckh-kit` đọc được đủ 13 resource đã đăng ký. Hook runner chạy được trên claude, codex, cursor, agy khi import root là `nckh-kit`.

Hai lỗi thật:

1. `python -m unittest discover -s tests` đặt top-level là `tests/`. Package `tests/hooks` che `nckh-kit/hooks`, nên 5 module hook/installer/runtime không import được `hooks.runner`.
2. Bản skill Cursor tại `.agents/skills` copy catalog 9 resource vào từng skill nhưng chỉ kèm file của resource skill đó tiêu thụ. Đọc resource khác trong cùng catalog báo `resource or declared dependency is unavailable`. Bốn owned-reference resource và sáu skill core không có trong `.agents/skills`.

Markdown link của skill/docs, JSON, và Python parse không lỗi. Workspace này không có file cấu hình hook native.

## Test Results Overview

- **Discover sai top-level**: 276 kết quả trong 592.920s. Passed 270. Failed import 5 module. Skipped 1.
- **Hook/installer/runtime với `-t .`**: 43 tests. Passed 43. Failed 0.
- **Source resource read**: 13/13 `resource_read: true`, exit 0.
- **Installed consumer read khi file có trong bundle**: 21/21 pass.
- **Python**: 3.12 (`C:/Users/USER\AppData\Local\Programs\Python\Python312\python.exe`)
- **Model**: chỉ Grok 4.7 Extra High. Không spawn subagent model khác.

## Coverage Metrics

Không có coverage gate cho kit này. Lần chạy không đo line/branch coverage.

| Check | Result |
|---|---|
| Source markdown links | 416/416 đọc được |
| Installed markdown links | 431/431 đọc được |
| Doc links `nckh-kit/docs` | 76/76 đọc được |
| JSON parse (`nckh-kit` core/hooks/scripts/skills/docs/tests/adapters/installer/evals + `.agents/skills`) | 302/302 |
| Python parse cùng phạm vi | 116/116 |
| Source resource lookup | 13/13 |
| Hook invoke 4 host | 4/4 exit 0 |

## Failed Tests

### `python -m unittest discover -s tests -p test_*.py`

CWD: `C:/Users/USER\Downloads\test-skill\nckh-kit`  
`PYTHONPATH=C:/Users/USER\Downloads\test-skill\nckh-kit`  
Ran 276 tests in 592.920s. FAILED (errors=5, skipped=1). Exit 1.

Discover lấy `tests/` làm top-level. `tests/hooks/__init__.py` khiến `import hooks` ra package test, không ra `nckh-kit/hooks/runner.py`.

### `tests/hooks/test_closure.py`

- **Error**: `ModuleNotFoundError: No module named 'hooks.runner'`
- **Stack**:
  - `unittest/loader.py` `_find_test_path` → `_get_module_from_name` → `__import__('hooks.test_closure')`
  - `nckh-kit/tests/hooks/test_closure.py:10` `from core.hook_config import payload_from_bundle, preview_config`
  - `nckh-kit/core/hook_config.py:15` `from hooks.runner import strict_json`
- **Cause**: tên package `hooks` bị shadow.
- **Rerun**: `python -m unittest discover -s tests/hooks -t . -p test_*.py` → Ran 29 tests in 149.206s. OK.

### `tests/hooks/test_config.py`

- **Error**: cùng `ModuleNotFoundError: No module named 'hooks.runner'`
- **Stack**: `test_config.py:9` import `core.hook_config` → `hook_config.py:15` import `hooks.runner`
- **Rerun**: nằm trong 29 tests OK ở trên.

### `tests/hooks/test_runner.py`

- **Error**: cùng `ModuleNotFoundError`
- **Stack**: `test_runner.py:10` `from hooks.runner import invoke, record_once`
- **Rerun**: nằm trong 29 tests OK ở trên.

### `tests/installer/test_entrypoints.py`

- **Error**: cùng `ModuleNotFoundError`
- **Stack**: `test_entrypoints.py:19` `exec_module` trên `installer/nckh-installer.py` → dòng 20 import `core.hook_config` → `hook_config.py:15`
- **Rerun**: `python -m unittest discover -s tests/installer -t . -p test_entrypoints.py` → Ran 3 tests in 48.592s. OK.

### `tests/runtime/test_hook_adapters.py`

- **Error**: cùng `ModuleNotFoundError`
- **Stack**: `test_hook_adapters.py:7` `from tests.hooks.test_runner import payload` → `test_runner.py:10` import `hooks.runner`
- **Rerun**: `python -m unittest discover -s tests/runtime -t . -p test_hook_adapters.py` → Ran 11 tests in 0.491s. OK.

### Skip

`tests/evidence/test_visual_engine_binding.py`, `test_symlink_observation_is_rejected`.

`target.symlink_to(...)` ném `OSError`. Test gọi `skipTest("host does not permit a real symlink fixture: ...")`. Log discover không verbose nên message OSError cụ thể không được in. Đây là skip của fixture symlink, không phải assertion fail.

## Hook read

Invoke trực tiếp `hooks.runner.invoke` với `context.json` hợp lệ:

| Host | Event | Exit | Status | Decision | Mode |
|---|---|---|---|---|---|
| cursor | preToolUse | 0 | checked-unreviewed | allow | enforce |
| agy | PreToolUse | 0 | checked-unreviewed | allow | enforce |
| claude | PreToolUse | 0 | checked-unreviewed | allow | enforce |
| codex | PreToolUse | 0 | checked-unreviewed | allow | enforce |

File cấu hình native không có trong workspace, nên không có hook JSON để đọc:

- `.cursor/hooks.json`
- `.agents/hooks.json`
- `.codex/hooks.json`
- `.claude/settings.local.json`

`nckh-kit/scripts/hook-preflight.py` và `configure-hooks.py` parse được. Test hook/config/installer ở lần chạy `-t .` pass.

## Source resource reads

Reader: `nckh-kit/scripts/search-resource.py`  
Catalog: `nckh-kit/core/registry/catalog/resources.json`  
Cả 13 resource: exit 0, `status: matched`, `resource_read: true`.

| Resource | Consumer dùng để đọc |
|---|---|
| R-reporting-lookup | nckh-method |
| R-publisher-profile | nckh-visuals |
| R-ui-lookup | nckh-frontend |
| R-nature-reference | nckh-write |
| R-vi-wikisource-passages | nckh-write |
| R-pmc-scientific | nckh-write |
| R-worldbank-vietnam-population | nckh-visuals |
| R-uci-bank-marketing | nckh-market-research |
| R-django-sqlmigrate-fixtures | nckh-code-review |
| R-statistical-recipes | nckh-statistics |
| R-telemetry-dictionary | nckh-telemetry |
| R-aiops-benchmark-cards | nckh-aiops |
| R-aiops-evaluation-recipes | nckh-aiops |

`review_reference` của năm snapshot trỏ `plans/reports/acquisition-261003-real-sources.md`. Reader không mở field này. File có tại `C:/Users/USER\Downloads\test-skill\plans\reports\acquisition-261003-real-sources.md`, không nằm trong `nckh-kit/`.

## Installed skill resource reads

13 skill trong `.agents/skills` có catalog và reader. Catalog của mỗi skill liệt kê cùng 9 resource (không có 4 owned-reference). Mỗi bundle chỉ có file của resource skill đó tiêu thụ.

Đọc resource có file: 21/21 pass.

Đọc resource có trong catalog nhưng không có file, kể cả khi consumer đúng, trả:

```text
exit 3
{"status": "fail", "error": "resource or declared dependency is unavailable", "resource_read": false}
```

Chứng cứ: reader của `nckh-analytics`, `--resource-id R-reporting-lookup --consumer nckh-method`. Cùng reader đọc `R-uci-bank-marketing` với `--consumer nckh-analytics` thì `matched` và `resource_read: true`.

### Skill đọc được resource nào

| Skill | Đọc được | Catalog có nhưng thiếu bytes |
|---|---|---|
| nckh-analytics | R-worldbank-vietnam-population, R-uci-bank-marketing | R-reporting-lookup, R-publisher-profile, R-ui-lookup, R-nature-reference, R-vi-wikisource-passages, R-pmc-scientific, R-django-sqlmigrate-fixtures |
| nckh-campaign | R-uci-bank-marketing | 8 resource còn lại trong catalog 9 |
| nckh-code-review | R-django-sqlmigrate-fixtures | 8 resource còn lại |
| nckh-evidence | R-pmc-scientific | 8 resource còn lại |
| nckh-fix | R-django-sqlmigrate-fixtures | 8 resource còn lại |
| nckh-frontend | R-ui-lookup | 8 resource còn lại |
| nckh-market-research | R-uci-bank-marketing | 8 resource còn lại |
| nckh-marketing-plan | R-uci-bank-marketing | 8 resource còn lại |
| nckh-method | R-reporting-lookup, R-pmc-scientific, R-worldbank-vietnam-population | R-publisher-profile, R-ui-lookup, R-nature-reference, R-vi-wikisource-passages, R-uci-bank-marketing, R-django-sqlmigrate-fixtures |
| nckh-taste | R-nature-reference, R-vi-wikisource-passages | 7 resource còn lại |
| nckh-test | R-django-sqlmigrate-fixtures | 8 resource còn lại |
| nckh-visuals | R-publisher-profile, R-worldbank-vietnam-population | 7 resource còn lại |
| nckh-write | R-reporting-lookup, R-nature-reference, R-vi-wikisource-passages, R-pmc-scientific | R-publisher-profile, R-ui-lookup, R-worldbank-vietnam-population, R-uci-bank-marketing, R-django-sqlmigrate-fixtures |

96 cặp skill-catalog/resource này cùng một lỗi `resource or declared dependency is unavailable`.

File thiếu lặp lại theo resource: `reporting-guidelines.json`, `k-dense-license.md`, `k-dense-attribution.md`, `publisher-profiles.json`, `ux-guidelines.csv`, `ui-ux-pro-max-license.md`, `ui-ux-pro-max-attribution.md`, `english-writing-advice.md`, `nature-skills-license.md`, `nature-skills-attribution.md`, `vi-wikisource.jsonl`, `wikisource-rights.md`, `pmc-scientific.jsonl`, `pmc-rights.md`, `swe-bench-reference.jsonl`, `swe-bench-rights.md`, `swe-bench-notice.md`, `worldbank-series.jsonl`, `worldbank-rights.md`, `uci-bank-marketing.jsonl`, `uci-rights.md`.

### Bốn resource không có trong mọi catalog đã cài

Reader `nckh-method` đã cài, `--resource-id R-statistical-recipes --consumer nckh-method`:

```text
exit 3
{"status": "fail", "error": "resource ID missing or duplicated", "resource_read": false}
```

Cùng lệnh trên source reader, consumer `nckh-statistics`: exit 0, `matched`, `resource_read: true`, record `paired-case-difference`.

| Resource | Có trong source | Có trong `.agents/skills` |
|---|---|---|
| R-statistical-recipes | đọc được | không có ID trong catalog đã cài |
| R-telemetry-dictionary | đọc được | không có ID trong catalog đã cài |
| R-aiops-benchmark-cards | đọc được | không có ID trong catalog đã cài |
| R-aiops-evaluation-recipes | đọc được | không có ID trong catalog đã cài |

Sáu skill source không có thư mục trong `.agents/skills`: `nckh-aiops`, `nckh-dataset`, `nckh-humanwrite`, `nckh-paperwrite`, `nckh-statistics`, `nckh-telemetry`. Chúng là consumer của bốn resource trên. Source `nckh-method/references/resource-lookup.md` yêu cầu chọn `R-statistical-recipes` và `R-aiops-evaluation-recipes`. Bản `.agents/skills/nckh-method/references/resource-lookup.md` không có hai ID đó.

24 skill còn lại không có `references/_shared/scripts/search-resource.py` và không có catalog: `nckh-backend`, `nckh-brand`, `nckh-content`, `nckh-context`, `nckh-cook`, `nckh-copy`, `nckh-cro`, `nckh-data`, `nckh-debug`, `nckh-devops`, `nckh-docs`, `nckh-email`, `nckh-experiment`, `nckh-git`, `nckh-handoff`, `nckh-launch`, `nckh-plan`, `nckh-research`, `nckh-review`, `nckh-scout`, `nckh-security`, `nckh-seo`, `nckh-social`, `nckh-xia`. Chúng không khai báo resource pack. Link markdown của chúng đọc được.

## Build Status

Không chạy build host đầy đủ ngoài những gì test hook/installer đã gọi khi `-t .`. Các test đó pass. Không có lỗi compile Python trong phạm vi đã parse.

## Critical Issues

1. Discover mặc định từ `tests/` không load được hook tests vì `tests/hooks` shadow `nckh-kit/hooks`. Logic hook vẫn pass khi top-level là kit root.
2. Catalog nhúng trong từng skill Cursor liệt kê resource không có bytes. Đọc chúng fail đóng với `resource or declared dependency is unavailable`.
3. Bốn owned-reference resource và sáu skill core chỉ có ở `nckh-kit`, không có trong `.agents/skills`.

## Recommendations

1. Chạy unittest với top-level là `nckh-kit`: `python -m unittest discover -s tests -t .`
2. Đổi tên package test `tests/hooks` hoặc bỏ `__init__.py` để `import hooks` không đụng `nckh-kit/hooks` khi top-level là `tests/`.
3. Catalog trong từng skill bundle chỉ nên liệt kê resource có bytes, hoặc bundle đủ file mà catalog khai báo.
4. Cài sáu skill core và bốn owned-reference vào `.agents/skills` nếu Cursor phải đọc được chúng.

## Unresolved Questions

- Message `OSError` cụ thể của skip symlink không có trong log non-verbose.
- Workspace chưa cài hook native, nên không có bằng chứng Cursor thật sự gọi hook lúc session chạy.
