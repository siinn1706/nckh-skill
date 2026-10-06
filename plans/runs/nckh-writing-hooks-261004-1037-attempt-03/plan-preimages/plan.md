---
title: "NCKH research-first writing, visuals và hooks"
description: "Thực thi candidate cục bộ cho hai writer, scientific visuals và portable hooks; các gate native/human giữ riêng."
status: in-progress
priority: P1
effort: 4 phases / 5-8 ngày công
branch: unverified-no-git-worktree
tags: [nckh, research, writing, visuals, hooks, provenance]
created: 2026-10-04
---

# NCKH research-first writing, visuals và hooks

## Outcome và đường biên

Thực thi candidate có thể kiểm chứng: writer tách nhiệm vụ, visual chỉ cho mục đích nghiên cứu, và checker/hook deterministic portable. Lệnh `/goal ak-cook plan.md --auto` ngày 04/10/2026 cấp quyền sửa source, kiểm tra và build cục bộ. Native activation/trust, cập nhật installation đang dùng và human/scientific acceptance vẫn cần gate riêng. Baseline trước sửa: r26 và installed doctor (historical evidence path: `../reports/checks-261004-1037-starting-baseline.json`; unavailable in the cleaned checkout), static evaluation (historical evidence path: `../reports/checks-261004-1037-starting-evaluation.json`; unavailable in the cleaned checkout).

Baseline độc lập: source lock r26, 243 pinned files, 37 identities, 9 resources (`plans/reports/checks-261004-0047-source-baseline.json:5-12`); installed candidate r25 và doctor read-only 43 items/current, không conflict (`plans/reports/review-261004-0047-current-kit.md:12-16`, `plans/reports/checks-261004-0047-installed-doctor.json`); cả bốn adapter `hooks.state=not-installed`, coverage unverified (`nckh-kit/adapters/claude/adapter.json:42-45`, `nckh-kit/adapters/codex/adapter.json:54-57`). Bốn pin khác revision chỉ được reconcile ở P4 sau approval, không auto-update.

## Quyết định đã duyệt

Theo quyền lựa chọn người dùng giao ngày 04/10/2026, dùng hai identity `nckh-humanwrite` và `nckh-paperwrite`, mỗi skill có `--en` hoặc `--vi`; không tách bốn skill theo ngôn ngữ. Target catalog là 39, chưa triển khai. Giữ `nckh-write` tương thích và route theo action; `nckh-taste` vẫn là critic. Quy tắc ngôn ngữ (historical evidence path: `../reports/decision-261004-0047-writer-language-options.md`; unavailable in the cleaned checkout) dùng chung preservation nhưng nạp riêng style VI/EN. Giữ toàn bộ engineer/marketing identities; visual gate áp dụng direct/indirect nhưng không xoá 27 skills.

## Phases và dependencies

| Phase | Kết quả chính | Phụ thuộc | Owner/file boundary |
|---|---|---|---|
| [P1 Start](./phase-01-start.md) | Hai writer + `--en`/`--vi`, target 39 IDs, policies/data/cases | Quyết định language đã chốt; implementation chưa được cấp quyền | Catalog, writer skills, acceptance/eval writer files |
| [P2 Scientific visuals](./phase-02-scientific-visuals.md) | research-purpose guard, measured/computed/simulation plots và source→mark QA | P1 contract; dữ liệu hoặc đầu ra tính toán thật, provenance/rights rõ | Visual skill/contracts/guards/cases; instruction và enforcement tách biệt |
| [P3 Portable hooks](./phase-03-portable-hooks.md) | neutral policy, 4 codecs, portable closure, preview/apply/remove | P2 semantics; official schemas; mặc định không đăng ký | Hook/config/build owners; native activation cần grant riêng |
| [P4 Integration & acceptance](./phase-04-integration-and-personal-acceptance.md) | single-owner freeze, persistent build→extract→smoke→preview | P1–P3; implementation/install authority riêng | Source lock, matrix, receipts và docs; không ghi đè lịch sử |

## Acceptance, risks và rollback

- Mỗi phase phải tách static/deterministic/agent/native/human-scientific evidence; `37/148/19/224` hiện chỉ là structural coverage (`plans/reports/checks-261004-0047-source-structure.json`), không phải quality, native, scientific hay human acceptance.
- Candidate phải có đúng 39 identity = 37 ID baseline hợp hai writer và đúng 156 base cases; supplemental cases không làm đổi bốn case/identity. Giữ 148 case IDs, receipt và matrix 224 lịch sử; validator toàn source chỉ chạy trước sửa hoặc sau freeze P4.
- Visual positive nhận measurement thật, derived/computational/simulation output từ phép tính/run thật, sourced mechanism có nhãn inference, hoặc research illustration có nhãn non-evidentiary. Cấm ad/banner/logo (kể cả research logo), generic artwork và invented observations. Không xây simulation pipeline; purpose guard độc lập engine-integrity checker và không được quảng cáo bảo vệ host chưa qualify.
- Humanizer là Markdown policy cục bộ được humanwrite đọc trực tiếp, linked/pinned/tested; không AI-detection/evasion, blacklist tiếng Anh áp cho VI, hay fabricated anecdote. LanguageTool là English-only diagnostic tùy chọn, Java17/LGPL/nested-rights gate; thiếu nó không chặn core.
- Hooks không đọc full transcript/raw draft, chạy shell từ payload, network/provider/nested LLM hoặc tự cấp trust. Config merge phải preserve shared Codex/AGY `.agents`, invalid JSON untouched, owned blocks/receipts only; rollback chỉ revert bytes còn đúng hash.
- Critical risks: không copy source bị hạn chế quyền (L=2,I=5,R=10); migration target 39 không được sót consumer (L=3,I=5,R=15); native host schemas/trust phải qualify riêng (L=3,I=5,R=15). Không claim ready-to-cook hay human quality.

## Links và open gates

Chi tiết source→reader→artifact→test ở [source-adoption-map.md](./source-adoption-map.md). Plan authority/preservation/acceptance theo `nckh-kit/core/policies/{authorization,evidence,preservation,acceptance}-policy.md`; personal-use owner feedback vẫn độc lập. User đã duyệt A1–A9 bằng “duyệt 9 điều chỉnh”, tiếp đó “duyệt tất cả điều chỉnh”. Implementation authority, rights review, host/version/trust grant và native/human/scientific acceptance vẫn là gate riêng chưa được đóng.

## Red Team Review

Ba reviewer độc lập, 15 finding gốc → 12 nhóm sau gộp: **9 Accept đã duyệt và áp dụng vào plan, 3 Reject giữ nguyên**. Chi tiết ở adjudication (historical evidence path: `../reports/red-team-261004-0047-adjudication.md`; unavailable in the cleaned checkout). Đây là approval sửa kế hoạch, không phải lệnh cook/install/trust.

### Whole-Plan Consistency Sweep

Đã đồng bộ A1–A9 vào index, bốn phase và source map: sequencing/count/consumer, hook packaging/config transaction, output chain, writer matrix/Humanizer, computational scope và giới hạn enforcement. Kiểm lại sau sửa được ghi riêng trong hồ sơ áp dụng (historical evidence path: `../reports/validation-261004-1002-approved-plan-amendments.md`; unavailable in the cleaned checkout); không sửa lại snapshot review cũ.

## Validation Log

Kiểm cấu trúc ban đầu nhận diện 4 phase/41 tasks, sau language decision là 43 tasks; audit lịch sử (historical evidence path: `../reports/validation-261004-0047-research-data-hooks-writing.md`; unavailable in the cleaned checkout) giữ nguyên giới hạn của các snapshot đó. Sau A1–A9: validate/parse PASS, **4 phase/45 tasks/0 done**, 33 local links và 1 anchor hợp lệ. Mọi task triển khai vẫn unchecked; hoàn tất review+plan không có nghĩa đã chứng minh behavioral/native/human/scientific acceptance.

<!-- slug: nckh-research-data-hooks-writing -->
