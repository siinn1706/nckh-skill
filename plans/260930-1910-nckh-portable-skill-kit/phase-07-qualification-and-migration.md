---
title: "Phase 7: Qualification and migration"
status: in-progress
---

# Phase 7: Qualification, migration và release gates

<!-- Updated: Validation Session 1 - Plan supersession recorded; package migration and release gates remain pending. -->

## Overview

Priority P1. Qualification scaffolding đang tích hợp theo [cook --auto được duyệt](plan.md); depends on P1–P6. Effort ban đầu 4–7 ngày công, không gồm chờ reviewer/native environments. Đã hoàn tất lượt agent-authored development cho 37 skills trong project. Human corpus/reviewers, protected holdout, matched baselines và full native/OS/model/cost acceptance vẫn thiếu. Local technical delivery và agent review không thành stable qualification.

## Context Links

- [Eval/migration contract và 19 case families](installer-evaluation-migration.md).
- [Catalog](skill-catalog.md), [runtime matrix](runtime-compatibility.md), [workflow/model](workflow-and-model-routing.md), [architecture](architecture.md).
- [Old red-team invariants](../reports/red-team-260930-0905-adjudication.md) và [old holdout/eval](../260930-0905-vietnamese-research-skill-kit/phase-05-evaluation-and-packaging.md): hồ sơ lịch sử; chỉ kế thừa theo migration map đã duyệt.

## Key Insights / Architecture

Test artifact presence khác real outcome. Synthetic fixtures test guards, không human gold/native behavior. Compare no-skill/upstream/NCKH same-agent/selective-delegation ở cùng scope/rights/quality floor; không forced best-of-N. Stable scope là skill + host/surface/version + mode/profile.

## Requirements

- Cả 37 identity đã chốt phải có positive/negative/outcome/failure eval, traceable source rights, evaluator và expected model/delegation.
- Advertised runtime surfaces gồm đủ four-host tracks; cell unsupported/unverified không xóa để làm đẹp bảng. Reduced scope cần user quyết định.
- Independent deterministic verification, agent behavior trace và human/domain acceptance tách riêng; holdout labels protected khỏi writer scope khi host enforce được.
- Freeze metrics, case families, sample/rights/reviewer/budget và acceptable economics trước paid/human run. Development tối đa ba vòng; holdout không lặp tuning.
- Migration preserves 11 invariants và maps old names. Supersession tài liệu đã được user duyệt/ghi ngày 01/10/2026; package promotion hoặc thay installed state vẫn cần acceptance và quyền tương ứng. User-owned installed state phải re-inventory, không assume còn trống.
- Source/license/private-data checks và recoverable install/uninstall required before release candidate; publish/distribution needs separate permission.

## File ownership — Create/integrate after P1–P6

| Absolute path / bounded subtree | Files/content owned |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/protocols/` | Frozen behavioral/human/native protocol, split/exposure lineage và stop conditions. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/rubrics/` | Outcome/VI taste/EN fidelity/scientific visual/domain rubrics; human-approved where required. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/baselines/` | Baseline manifests/source pins/aggregate nonprivate results, not raw corpus. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/run-evals.py` | Case validation + authorized deterministic/agent runner adapters; provider execution opt-in. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/release/` | All-skill case coverage, license/private-data/migration/manifest consistency checks. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/qualification.md` | Observed pass/fail/pending by skill/host/version with receipt references. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/migration.md` | Old-to-new authority/name/contract mapping, rollback and preserved user decisions. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/release-checklist.md` | Release gates, package checksums, permissions and known limitations. |

P7 reads all test/case directories. Defects go back to the original phase owner; no parallel silent fixes to core/adapters. Compatibility/source-lock status updates integrated sequentially after actual evidence. Raw receipts, corpora and reviewer identities remain private.

## Implementation Steps

1. Re-inventory built artifacts and all 37 identities; verify each required case family maps to an actual test/protocol, not only title in a document.
2. Freeze protocol, licensed sources, human reviewers, holdout partitions and cost authorization; no real paid runs before this gate.
3. Run deterministic suites in dependency order; repair cause in owning phase. Never delete/weaken acceptance to get green.
4. Run authorized host/agent cases including simple/deep/same-model, auto/interactive feedback/resume, permission bypass, stale receipt, config override, actual model and cleanup.
5. Run human VI/EN/domain/native visual review and matched baselines. Record failures/pending and raw counts; unknown token/cost coverage stays unknown, zero accepted denominator is undefined.
6. After at most three authorized development rounds, freeze candidate and evaluate protected holdout once. Exposure moves a set to development; replace/re-authorize holdout rather than pretending blind.
7. Execute migration rehearsal + owned transaction rollback/uninstall. If installed predecessor now exists, inventory real ownership and obtain scope; do not invent migration from nonexistent package.
8. Produce qualification decision, not publish. Giữ baseline làm lịch sử và authority của plan đã duyệt ngày 01/10/2026; chỉ promote package/installed state sau scoped acceptance và quyền tương ứng, retain rollback. Không trì hoãn hoặc đảo lại supersession tài liệu vì package chưa qualification.

## Todo

- [x] Validate 37 identity coverage and all 19 required case families.
- [ ] Freeze protocol/rights/reviewers/budget and protected holdout.
- [ ] Run deterministic + authorized agent/native/human suites.
- [x] Record quality/cost/evidence coverage, failures and unsupported cells.
- [x] Rehearse migration/rollback and issue scoped release decision.

Rehearsal ở owned Windows fixtures; không là migration host thật. [Candidate checkpoint](../reports/implementation-261001-nckh-candidate.md) ghi 65 actual tests pass, four-host reproducible artifacts, checksums và NO-GO cho stable/public distribution. 148 skill cases, 224 native cells và 10 installer/OS scenarios vẫn not-run; cost unknown, accepted count zero. Năm rubrics vẫn proposal/pending.

[Discovery/repeat/spec audit trước runner checkpoint](../reports/audit-261001-1813-native-progress-and-runner-gap.md) ghi một native catalog observation và actual Windows project-copy repeat, không coi chúng là full case/native acceptance. Tại thời điểm audit, `run-evals.py` mới validate/run deterministic và còn thiếu opt-in agent adapters. Gap này được xử lý ở checkpoint kế tiếp; các human/native/provider gates giữ nguyên.

[Runner checkpoint mới](../reports/implementation-261001-nckh-agent-runner-candidate.md) đã triển khai opt-in adapter, source/input/driver/budget checks, private command/trace records và owned lifecycle. Final deterministic discovery đạt 79/79 ở revision 17; four-host artifacts build lặp khớp và được giữ riêng tại `dist-runner`. Đây là local implementation/fixture evidence; 148 skill cases, 224 full native cells, human reviews và provider runs vẫn chưa nghiệm thu. Giữ nguyên các Todo chưa đủ bằng chứng và bản revision 14 đã cài.

[Journal-repair và whole-plan completion audit](../reports/implementation-261001-nckh-runner-journal-repair.md) ghi hai fault paths đã reproduce/fix: case-read sau preview và lỗi chờ lifecycle. Final revision 18 đạt 81/81 local tests; new build/reproducibility receipts giữ tại `runner-cleanup-*.json`, candidate `candidate-runner-cleanup.json`, artifacts `dist-runner-cleanup`. Revision 14/17 và installed state được recheck giữ nguyên; human/native/provider gates vẫn pending.

[Direct development checkpoint ngày 02/10/2026](../reports/testing-261001-direct-skill-development.md) theo grant mới đã chạy/chấm đủ 148 prompt tổng hợp do agent soạn: first round 137 pass, 4 fail, 7 pending; latest sau sáu diagnostic/10 request là 147 pass, một fail. 42 phiên native hoàn tất, một cook timeout trước khi bỏ deadline được giữ. Cook mới chạy hơn 20 phút; không tự cắt sau 15 phút. Native CLI explicit invocation, controller review và metadata/file hashes không là human gold, baseline improvement, full native matrix hay role/effective-model proof. Bản đã cài revision 14 và source revision 18 giữ nguyên; 43 owned items current. Hai Todo qualification tổng hợp phía trên vẫn mở vì còn human/holdout/full native acceptance.

## Success Criteria

- No stable skill without eval and acceptance evidence; full four-runtime claim requires all advertised cells, not one host success.
- Critical finite fault suite has zero accepted fabricated evidence, unauthorized side effect, wrong interactive boundary or lost user edit; this is not a universal guarantee outside the suite.
- Human/native evidence actually exists for claimed taste/scientific/visual quality; neither self-score nor content hash closes those gates.
- At most three development rounds unless new authorization; holdout exposure lineage and sample rights auditable.
- All 11 old invariants mapped and preserved; installed user data/config untouched outside authorized migration; release/publish permissions separate.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

1. Rerun phase-owned unit suites, narrow failures first.
2. `python -m unittest discover -s tests/release -p "test_*.py"`
3. `python evals/run-evals.py --validate-only` checks manifests/coverage/rights states **without** provider/human execution.
4. `python evals/run-evals.py --run-deterministic --output evals/results/NEW-REVISION-local-checks.json` retains actual suite output and failures; choose a fresh revision-bound name and preserve prior receipts. Timeout is unknown.

Tests/runner hiện tồn tại; root discovery đã quan sát 63 tests ở revision trước và receipt lịch sử được giữ. Installed-candidate local receipt (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) phải khớp candidate revision 14 tương ứng. [Rubrics](../../nckh-kit/evals/rubrics/catalog.json) là proposals chưa human-approved. Behavioral/native/human/OS acceptance có grants và receipts riêng; empty suite là failure.

Receipt `local-checks.json` và `candidate.json` thuộc bản revision 14 đã cài. Nguồn runner revision 17 dùng new local receipt (historical evidence path: `../../nckh-kit/evals/results/runner-local-checks.json`; unavailable in the cleaned checkout) và new candidate (historical evidence path: `../../nckh-kit/evals/results/candidate-runner.json`; unavailable in the cleaned checkout), cùng `runner-reproducibility.json`/`runner-build.json`. Không dùng receipt cũ để xác nhận source mới. `--prepare-agent-run` chỉ preview; `--run-agent` cần recipe đã review, sáu freeze references, quyền provider riêng và exact plan hash như [qualification contract](../../nckh-kit/docs/qualification.md).

Nguồn hiện hành revision 18 dùng cleanup local receipt (historical evidence path: `../../nckh-kit/evals/results/runner-cleanup-local-checks.json`; unavailable in the cleaned checkout) và cleanup candidate (historical evidence path: `../../nckh-kit/evals/results/candidate-runner-cleanup.json`; unavailable in the cleaned checkout), cùng `runner-cleanup-reproducibility.json`/`runner-cleanup-build.json`. Chỉ reuse checks khi source/inputs/environment không đổi; không chạy lại hoặc ghi đè receipts chỉ để lặp status.

## Risk / Security / Rollback

Largest risk is promoting a technical check to scientific quality or cross-host readiness. Keep evidence classes and open gates visible. No private corpus/holdout/customer/credential material in dist. Roll back candidate promotion/owned install transaction, never erase failed runs or user review. Missing input produces pending with exact owner/action, not fabricated results.

## Next Steps

Handoff factual qualification and explicit blockers. Only user can authorize installing into their real project/global scope, external release, paid expansion or further tuning. Completion of this phase does not authorize publish.
