---
title: "Phase 2: Selective domain resources"
status: completed
---

# Phase 2: Selective domain resources

## Overview

<!-- Historical plan amendments: R6/R10, 2026-10-02; execution authorized 2026-10-02 -->

Chọn tài nguyên theo consumer và gap đã đo; review quyền, stage bytes/content ngoài pinned source/dist và kiểm consumer ở source level. P2 không promote data chưa được hỗ trợ vào source-lock hay distribution. P3 phải bổ sung schema/rights/closure trước candidate build/extracted smoke. Không port nguyên Nature/AgentKit/K-Dense, không biến mọi prose thành CSV/JSON; giữ `SKILL.md` mỏng và progressive disclosure.

## Requirements

- [x] Duyệt toàn bộ 37 dòng và decision matrix cụ thể trong [resource-map.md](./resource-map.md); không identity nào bị loại. Mỗi lựa chọn ghi `candidate-staged`, `MD-only`, `blocked-rights` hoặc `blocked-input` với lý do; không có candidate promotion trong P2.
- [x] Không tự bịa dataset/resource rows. Nếu cần dữ liệu, lập shortlist tối đa ba nguồn mạnh theo **domain fit, consumer fit, provenance/revision, license/redistribution và evidence depth**; gọi đây là shortlist có tiêu chí, không tuyên bố top 1–2–3 toàn cầu. Mỗi record phải giữ upstream path/full SHA/as-of/license/rights và source locator.
- [x] Chỉ mix các nguồn khi schema/semantics/license tương thích; ghi per-record provenance, dedup/conflict policy và missing-record policy. Không điền hàng còn thiếu, không dùng CSV có `TODO`/placeholder như dataset (đó chỉ là template), không gọi metadata hợp lệ là evidence hợp lệ.
- [x] Core ưu tiên: reader-card/research-log templates, claim/evidence locator, factual-slot contract và honest chart-data/source-map. VI/EN genre corpus hiện **missing/blocked-input**: reporting registry/publisher profiles/Nature references không lấp được gap này. Glossary CSV hay fact-slots JSON + thin CLI chỉ được chọn khi có nguồn thật và lookup/read-write consumer.
- [x] Engineer/Marketing chỉ nhận references/templates có scope: schema/provenance/test/failure matrix, source disposition, metric/experiment ledger, SEO ownership và CRO friction. Không thêm provider/native engine ngoài route được chọn và verified.
- [x] Mọi ví dụ VI/EN/corpus phải là real sourced/user-supplied/rights-cleared material. Fixture kỹ thuật nếu được duyệt riêng chỉ dùng test, không thay source corpus. 148 synthetic development cases giữ nhãn diagnostic, không phải dataset nguồn/human gold; không tự tạo synthetic dataset để lấp gap.
- [x] Nature/AgentKit pattern chỉ là design inspiration; nếu dùng byte/asset upstream, pin full SHA (Nature candidate full HEAD `84880815fb37317b3766bff2c2abba395b8993c3` phải re-check), LICENSE/NOTICE và redistribution. Clean-room re-authoring được ưu tiên.

## Verified shortlist input (not a global ranking)

Chi tiết bytes, readers và giới hạn ở [source shortlist](../reports/researcher-261002-0832-source-shortlist.md); quyết định resource → consumer → output/test ở [resource map](./resource-map.md). Đây là tối đa ba nguồn xem xét theo domain/consumer fit, không dùng popularity để chứng minh chất lượng. Đã review selected-file ancestry/license/NOTICE, stage bốn snapshot và chạy consumer thật; promotion sau P3 support. Release và semantic/human applicability vẫn pending.

| Source ID | Full repository pin / metadata | Actual structured candidate | Bounded use |
|---|---|---|---|
| S1 | `K-Dense-AI/scientific-agent-skills@154988403bb5a18e9d3c0ce4e6d5e2e4b184a298` (root MIT verified) | `skills/scientific-writing/assets/reporting_guidelines.json`, 15 records, SHA256 `215f8c55bd40bda0569f2e81556030ff575319e25276b1e1ae70e2cc7475ddcd`; `skills/scientific-visualization/assets/publisher_profiles.json`, 8 profiles, SHA256 `1e1b1b5a4e0e3dfc57877f2abf1e96888fe6b65617234b078f193b8f76e0ebe9` | Guideline lookup only for matching study design/domain, largely clinical/health; not generic CS. Publisher profiles are currency-labeled references, not automatic compliance. |
| S2 | `Yuan1z0825/nature-skills@84880815fb37317b3766bff2c2abba395b8993c3` (root Apache-2.0 verified at this pin) | `skills/nature-writing/manifest.yaml` and its routed references/MD; no CSV/JSON corpus claimed | Progressive-disclosure/router pattern and selective venue reference only; pin each selected reference/hash and review LICENSE/NOTICE/per-file rights before reuse. |
| S3 | `nextlevelbuilder/ui-ux-pro-max-skill@09170eec67eefd46a7ae85de61b40c194020f997` (MIT metadata) | `src/ui-ux-pro-max/data/ux-guidelines.csv`, 119 actual data rows, SHA256 `ff81ec613f70ba9fc3fcce52dbe4ae35d44b2079dbe6dc066d2d6e38c28facd5` | UI/frontend/CRO-owner-scoped lookup only; never scientific gold or universal NCKH guidance. |

Local AgentKit examples are consumer-pattern evidence, not a fourth source or independent corroboration of S3. K-Dense templates/placeholders with `TODO` remain templates, not a curated dataset. Any mix must retain S1/S2/S3 per-record provenance and compatibility/conflict decisions.

## Resource families đã cân nhắc (không bắt buộc)

| Family | Consumer | Format | Gate |
|---|---|---|---|
| Genre examples | `nckh-write`, `nckh-taste`, selected content/copy | MD with before/after/delta/limits | actual source/user rights, fidelity slots unchanged; human taste remains pending |
| Reader/research log | `nckh-research`, `nckh-docs`, `nckh-scout` | MD template; JSON only for repeated records | source/locator/status/hash fields complete; template is not dataset |
| Claim/evidence/fact slots | `nckh-evidence`, `nckh-method`, `nckh-write`, `nckh-experiment` | existing JSON schemas; optional JSONL records | validator + per-record provenance; no semantic self-certification |
| Glossary/source screening | `nckh-write`, `nckh-market-research` | CSV only with a stdlib lookup consumer | real rows/full source pin or explicit user material; stable header/version/owner |
| Honest visual QA | `nckh-visuals`, selected frontend/analytics | real sourced data JSON/CSV + source-map MD | data/metric source locators, mechanism links, hashes; editor/accessibility gate separate |
| Engineering references | `nckh-data`, `nckh-test`, `nckh-debug`, `nckh-code-review`, `nckh-security` | scoped MD/checklist; deterministic helper only if needed | malformed/negative fixture and no secret/provider action |
| Marketing references | `nckh-seo`, `nckh-cro`, `nckh-analytics`, `nckh-experiment` | scoped MD/metric ledger | ownership/handoff explicit; noindex remains CRO historical fail |

## File ownership

P2 đã stage dưới `plans/evaluation/resource-quality/staging/` ngoài pinned source/dist. Sau P3 support/regressions, content owner promote đúng bytes trong promotion receipt và giao P1 freeze. Bảng giữ trách nhiệm từng owner; raw traces/holdout không nằm trong staging này.

| Owner | Exact paths | Constraint |
|---|---|---|
| P2 staging | `plans/evaluation/resource-quality/staging/` (implemented) | Reviewed source bytes, content/adapters and source-level consumer receipts; immutable source locator/hash, not installed/released. |
| P2 Core | Future targets: `nckh-kit/skills/core/`; `nckh-kit/core/profiles/`; selected `nckh-kit/core/policies/` | Stage references/templates; re-author instructions, never invent source examples. No source-lock/eval-history edits. |
| P2 Engineer | Future target: `nckh-kit/skills/engineer/` | Stage selected UI lookup/references only; no blanket 13-skill expansion. |
| P2 Marketing | Future target: `nckh-kit/skills/marketing/` | User selected CRO canonical/noindex inspection; broader SEO remains separate, and historical failure/oracle is preserved. |
| P2 Tooling | Future target: `nckh-kit/skills/tooling/nckh-xia/` | Compare/disposition only; no upstream execution or global overwrite. |
| P3 / P1 handoff | P3 format/closure contracts; P1 `nckh-kit/core/registry/source-lock/` | P2 submits path/hash/rights packet; P3 supports candidate, P2 owner promotes content, then only P1 writes freeze/history. |

## Data flow and steps

1. Select a row from the matrix only when the consumer and expected artifact are named.
2. For data, choose at most three source candidates with the explicit criteria above; the shortlist above is the current input, not an automatic approval. Capture actual rows/content, source revision/path/full SHA/as-of, license/NOTICE/redistribution and exact permitted use before extraction.
3. Stage cleared source bytes/content outside pinned source/dist; annotate locale/genre, factual slots, source locators, limits and owner. Re-author instructions only; do not manufacture data/missing rows or silently mix incompatible records.
4. Draft the smallest route reference and named NCKH consumer/adapter in staging; distinguish upstream's existing reader from a proposed NCKH reader. Keep authoritative policy in Markdown.
5. After source/script review and execution authorization, run source-level checks through the staged consumer using real selected bytes and existing or separately approved negative fixtures. Record output hash/read evidence. This is not an extracted-package/candidate-build pass.
6. Reject resources that only add context, duplicate prose, hide private holdout, or require an unapproved provider/native engine. Hand the reviewed staged packet to P3; keep rights/input gaps pending and preserve failed receipts/staged material for rework.

## Validation

- Existing baseline-only syntax: `python evals/run-evals.py --validate-only` and `python -m unittest tests.evidence.test_guards tests.release.test_qualification tests.build.test_closure`; record the unchanged P1-frozen baseline revision/hash actually checked, not the staged resource candidate.
- Optional existing baseline build checks: `python scripts/build-artifacts.py --all --check` and `python scripts/build-artifacts.py --all --plugin --check`, only on that unchanged pinned baseline with authorized output. P2 does not require a new-resource candidate build to advance; candidate build/extracted smoke belongs to P3 after support and freeze.
- Implemented: `python -m unittest tests.resource.test_consumers tests.resource.test_closure`; reader requires `--resource-id ID --consumer SKILL --domain DOMAIN --genre GENRE --query TEXT --json` and resource-specific context. Per-file rights/hash regressions live in `test_closure`; no separate nonexistent `test_provenance` module is required.

## Risks and rollback

- High: invented/placeholder rows or incompatible mix appears as a real corpus. Mitigate source/full-SHA/per-record provenance and fail closed on missing rights; reject promotion without altering direct-history.
- High: examples silently change numbers, causality, quotation or venue rules. Mitigate factual-slot diff and source locators; quarantine staged candidate, retaining source bytes/pins and failed receipt for rework.
- High: license snapshot drift or third-party bytes. Mitigate full-SHA/NOTICE review; leave `blocked-rights`, do not relabel as owned.
- Medium: CRO/SEO oracle mismatch. Keep the hash-bound CRO fail; the owner selected canonical/noindex inspection and a separate scope amendment. Never rewrite history.
- Medium: P2 build depends on P3 support. Keep staged work out of source-lock/dist until P3 succeeds; no false owned-local label to pass. If P3 rejects the packet, return it to P2 with failed receipt, retaining staging/history.
- Medium: broad resource set reduces context fidelity. Gate by observed consumer read and artifact usefulness; exclude unconsumed candidate from promotion, retaining review evidence.

## Success criteria

Every selected resource has a staged decision packet: named consumer, actual domain fit, upstream existing reader versus proposed NCKH adapter, real sourced/user-provided content, provenance/rights status, expected output and source-level negative/failure check. A technical fixture never fills missing source data. VI/EN corpus stays missing/blocked-input until supplied and reviewed. No new resource has been promoted into pinned source/dist during P2; P3 owns the packaging gate. All 37 identities remain; unselected identities are MD-only. No writing/scientific/runtime/visual-editability improvement is claimed from this phase.

## Execution checkpoint

Đã ghi quyết định đủ 37 identities, chọn bốn resources từ đúng ba nguồn. Source bytes/license/tree đã đọc ở pin; không clone repo hay chạy upstream code. VI/EN corpus/chart input vẫn blocked-input. [Staged packet](../evaluation/resource-quality/staged-packet.json), [source inspection](../evaluation/resource-quality/staging/source-inspection.json), [promotion](../evaluation/resource-quality/promotion-receipt.json).
