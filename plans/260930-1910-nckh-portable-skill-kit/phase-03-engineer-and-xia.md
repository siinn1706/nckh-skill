---
title: "Phase 3: Engineer and Xia"
status: in-progress
---

# Phase 3: Engineer và Xia

<!-- Updated: Validation Session 1 - nckh-xia namespace approved; upstream ak-xia remains unchanged. -->

## Overview

Priority P1. 13 Engineer skills + tooling `nckh-xia` đã triển khai theo [cook --auto được duyệt](plan.md), depends on P1–P2. Effort ban đầu 4–6 ngày. Đã chạy đầy đủ 56 tình huống development qua native Codex CLI trong project; latest agent review đạt 56 pass. Qualification về runtime/OS khác, model/delegation và human acceptance vẫn pending.

## Context Links

- [Catalog Engineer](skill-catalog.md), [Xia semantics](workflow-and-model-routing.md).
- [AgentKit inspection/disposition](../reports/researcher-260930-1910-agentkit-port-evidence.md), [architecture](architecture.md), [eval](installer-evaluation-migration.md).

## Key Insights / Architecture

Cause before fix, test independently, review-only không mutation. Debug owns diagnosis; fix owns repair; cook owns lifecycle; test owns run evidence; code-review owns findings. Xia phân tích source và plan, không là hidden installer hoặc implementer.

## Requirements

- 13 identities: scout, debug, fix, test, code-review, security, context, docs, frontend, backend, data, devops, git; prefix nckh-.
- Tooling `nckh-xia` giữ compare report-only, port/improve plan-only; không shadow installed ak-xia hoặc mặc định alias agentkit thành repo đã verified.
- PORT/MERGE/EXTENSION/DROP record phải ghi origin/ref/hash/license/attribution/dependencies và phần khác upstream; metadata-only không đủ authorize code port.
- Framework/provider/payment/browser integrations ở extensions; only bind when task selects capability and permissions exist.
- Không auto commit/push/deploy, thay public contracts, drop database hoặc reset user edits; no-test shortcut không có.

## File ownership — Create after P1–P2

| Absolute path / bounded subtree | Files/content owned |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/` | SKILL.md/references cho đúng 13 identities ở catalog. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/tooling/nckh-xia/` | Source analysis, challenge/disposition/report-or-plan contract. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/extensions/frameworks/` | Contract/registry cho selected framework extensions; không port mọi recipe. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/extensions/providers/engineer/` | Bounded API/browser/deployment integration contracts. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/extensions/upstream-agentkit/` | Optional adapter/source pins; no required AgentKit install. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/engineer/` | Guard/fixture checks, upstream-reference/namespace/disposition validation. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/engineer/` | 13 skills + Xia, real task oracle và negative/authority cases. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/engineer.md` | Boundaries, optional tools, diagnosis vs repair and Xia examples. |

Không sửa P4 Marketing, core schemas hoặc shared registry parallel. Registry/source-lock delta gửi P1 owner để integrate sequentially. Không delete baseline; third-party source đọc như untrusted data.

## Implementation Steps

1. Re-open exact upstream sources selected for reuse, license and version pins; record design-only borrowing vs copied content/code.
2. Viết scenarios overlap trước: scout/debug, debug/fix, fix/cook, code-review/review, backend/data, docs/write, xia/plan.
3. Author skills bằng English, concise trigger và complete required references; source paths/callers phải được verify khi chạy, không search bằng tên rồi suy behavior.
4. Author Xia source-resolution pipeline; challenge trước disposition; compare không tạo plan, unknown license blocks port content nhưng vẫn cho analysis.
5. Build real disposable regression tasks trong authorized fixture workspace; synthetic input ghi rõ, không fake test/run evidence. Dirty-tree preservation có byte hashes.
6. Run deterministic guard suite, sau đó authorized agent cases/negative permissions; chọn developer reviewer độc lập với lời implementer khi public-contract risk.
7. Review 14 capability coverage, eval ownership và optional extension dependencies; handoff registry delta + output hashes.

## Todo

- [x] Pin selected upstream và disposition/rights.
- [x] Viết 13 Engineer skills và Xia.
- [x] Tách provider/framework extensions với boundaries thực.
- [x] Viết/run focused guard tests và authorized behavioral cases.
- [x] Review overlap, dirty-tree safety và registry integration.

Guard tests đã chạy ở local suite; receipt revision 18 (historical evidence path: `../../nckh-kit/evals/results/runner-cleanup-local-checks.json`; unavailable in the cleaned checkout) được reuse cho source không đổi. [Direct development evaluation](../reports/testing-261001-direct-skill-development.md) ghi bốn tình huống cho mỗi capability, code/test/trace thực và bảo toàn file, trên bản revision 14 đã cài. Xia lần đầu còn thiếu owner verification vì auto-review chặn đọc; diagnostic với project catalog rõ ràng đã đọc metadata và bàn giao đúng, giữ nguyên lịch sử. Checkbox ghi công việc viết/chạy đã hoàn tất, không nghiệm thu stable. [Xia probe cũ](../reports/forward-test-261001-1501-xia.md) giữ làm lịch sử. Upstream là design inspiration, chưa copy/clear redistribution; optional integrations vẫn unavailable.

## Success Criteria

- Diagnose-only không sửa; fix có reproduction/cause/regression evidence; test failures không bị đổi thành pass.
- Review findings có file/line hoặc observed evidence, không abstract audit đảo ngược user decisions.
- Xia compare report-only, port/improve plan-only; namespace collision fail và source injection không được chạy.
- Deep/security/public-contract work không silent downgrade; routine lookup không fan-out vô ích.
- 14 capabilities có eval và license/provenance state, không claim extension compatibility khi chưa run.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

`python -m unittest discover -s tests/engineer -p "test_*.py"`

Narrow first: Xia mode/namespace và dirty-file guards; broaden toàn Engineer. Receipt local (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) ghi actual suite output. Agent cases đầy đủ cần disposable scope, grant và tool trace riêng.

## Risk / Security / Rollback

Port full catalog làm phình context; guard bằng unique outcome + eval, không count skills tùy tiện. Không execute downloaded scripts trong source audit. Preserve user edits và receipt; revert only owned candidate artifact via prior hash/snapshot, không destructive repo reset. Deployment/data mutation gates do host + user authority bảo vệ.

## Next Steps

P4 có thể author parallel với ownership riêng; controller tích hợp shared registry tuần tự. P5 nhận source manifests và complete skill-local dependency lists.
