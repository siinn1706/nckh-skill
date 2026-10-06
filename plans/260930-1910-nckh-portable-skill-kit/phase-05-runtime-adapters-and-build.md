---
title: "Phase 5: Runtime adapters and closure build"
status: in-progress
---

# Phase 5: Runtime adapters và closure build

<!-- Updated: Validation Session 1 - Four-host design approved; native compatibility remains unverified. -->

## Overview

Priority P1. Four-host adapters và closure builder đã triển khai theo [cook --auto được duyệt](plan.md). Effort ban đầu 4–7 ngày. Candidate build depends on frozen P1–P4 inputs; native discovery/invocation/model/hook qualification vẫn unverified.

## Context Links

- [Runtime matrix và official sources](runtime-compatibility.md), [architecture/tree](architecture.md).
- [Model routing](workflow-and-model-routing.md), [runtime research](../reports/researcher-260930-1910-runtime-compatibility.md), [installer/eval](installer-evaluation-migration.md).

## Key Insights / Architecture

Surface/version là phần identity của capability. Codex desktop slash khác CLI/IDE documentation; Cursor IDE launcher khác standalone Agent CLI; Agy IDE/global khác CLI/global. Fresh context không tự tạo filesystem isolation; native config requested không chứng minh effective model.

Build resolve DAG/dependency closure, materialize shared references và host metadata, rồi emit content hashes/source/license manifest. Không runtime-home absolute links. Plugin packaging là optional projection của cùng source, không source authority thứ hai.

## Requirements

- Four adapters claude/codex/cursor/agy; discovery/invocation/config/hooks/permissions/effective model được map riêng theo surface.
- Same-agent fallback chỉ khi thỏa outcome; required capability unavailable/unverified thì pending/NOT_CALLABLE đúng lý do, không giả per-agent model bằng prompt.
- Native hook thiếu/crash/bypass không mở critical action; host permissions là boundary thật, không dùng coordinator prompt tự nhận enforcement.
- Deterministic build fail missing references, cycles, case-fold collisions, traversal/junction escapes, private/secret fixtures và unknown redistributability.
- Artifact self-contained; every source/reference dependency pin và hash; generated output không sửa tay.

## File ownership — Create after approved inputs

| Absolute path / bounded subtree | Files/content owned |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/adapters/claude/` | Claude skill/agent/plugin/hook projection + capability rules. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/adapters/codex/` | App/CLI/IDE-specific invocation/config projection, no hard-coded old dollar-only UX. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/adapters/cursor/` | Correct Agent CLI, compatibility roots/duplicate visibility, model parameters. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/adapters/agy/` | IDE/CLI paths, aliases, actual effort/permission limitations. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/registry/compatibility/` | Host/surface/version evidence records + advertised support cells. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/scripts/build-artifacts.py` | Stdlib closure builder; no download/install/agent run. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/build/` | DAG/path/hash/reproducibility/privacy deterministic tests. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/runtime/` | Adapter contract tests; no paid/native run in unit default. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/runtime/` | Native discovery/invoke/model/hook/mode/cleanup scenarios. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/dist/` | Generated claude/codex/cursor/agy artifacts only. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/runtime-support.md` | Evidence-scoped compatibility and invocation examples. |

Read skills/shared core; changes to source contract go through P1 owner. Do not edit user runtime config directly in builder. No baseline deletion.

## Implementation Steps

1. Refresh official docs/local help at execution time; compare drift to current research and record approved support matrix. No paid model discovery without authority.
2. Define adapter contract with supported/unsupported/unverified distinction, entrypoint×surface×invocation matrix, native auto permission preservation, model-resolution encoding/effective proof and same-agent fallback. Không phát sinh vendor bypass flags từ auto.
3. Write fixture-based tests for path resolution, duplicate discovery, field translation and safety; label fixtures as deterministic inputs, not live runtime proof.
4. Implement deterministic builder and four adapters; copy mandatory references into artifact-local locations where required; keep optional dependencies out of default closure. Shared-root artifacts phải neutral và qualified; conflicting projections fail before install, không last-writer-wins.
5. Build twice from frozen sources into isolated output directories; compare content/path/source manifests excluding declared volatile receipt fields. Both builds must resolve all links without source checkout.
6. Run authorized per-surface native probes separately for UI/menu/headless/implicit VI/EN invocation; fresh context, valid/invalid/overridden model+effort, parallel join, hooks allow/deny/failure and actual shell/file/MCP/web/egress permission coverage. Cell chưa probe giữ unverified.
7. Record limitations cell-by-cell, clean only owned temporary processes/files/config via receipts; hand self-contained artifacts + safe destinations to P6.

## Todo

- [x] Freeze host/surface capability schema và current source evidence.
- [x] Write four adapters + closure builder.
- [x] Run build/runtime contract tests và reproducibility check.
- [ ] Run native probes khi được phép; keep remaining cells pending.
- [x] Review generated manifest/privacy/namespace và handoff to installer.

## Success Criteria

- Same source generates four distinct host artifacts without manual edits or author-machine paths.
- No missing closure/cycle/collision/private material; reproducible hashes and source/license ledger.
- Correct Codex App vs CLI/IDE UX, correct Cursor CLI, correct Agy global roots.
- Config unsupported/overridden recorded honestly; requested model not labeled actual without evidence.
- Hooks tested against real tool coverage for claimed guards; no prompt-only enforcement claim. Missing authorized native runs remain pending, not pass.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

1. `python -m unittest discover -s tests/build -p "test_*.py"`
2. `python -m unittest discover -s tests/runtime -p "test_*.py"`
3. `python scripts/build-artifacts.py --all --check` validates/builds in temporary staging.
4. `python scripts/build-artifacts.py --all --plugin --check` includes optional plugin projections without registration/trust.

Source/tests/commands hiện tồn tại. Reproducibility receipt (historical evidence path: `../../nckh-kit/evals/results/reproducibility.json`; unavailable in the cleaned checkout) và candidate record (historical evidence path: `../../nckh-kit/evals/results/candidate.json`; unavailable in the cleaned checkout) ghi kết quả thực; không là native receipts. Native probes còn cần grant riêng.

## Risk / Security / Rollback

Host drift and shared discovery roots can create conflicting definitions; fail before installation. Source repos/frontmatter are untrusted; do not execute embedded install hooks. On failure keep candidate separate from last accepted artifact, preserve receipts, remove only verified owned staging paths. Do not downgrade declared security guarantees to make one runtime pass.

## Next Steps

P6 consumes built manifests and target map. P7 checks complete advertised cells; a partial native result cannot become “portable across all four” acceptance.
