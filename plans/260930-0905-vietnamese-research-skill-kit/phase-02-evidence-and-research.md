---
title: "Phase 2: Bằng chứng và research"
status: pending
---

# Phase 2: Bằng chứng và research

## Overview

**Priority:** P1 · **Estimate:** 2–4 ngày, ước tính không cam kết · **Status:** pending.

Phase này triển khai hợp đồng discovery → reader → evidence audit → reasoning
trên nền contract revision của P1. Đầu ra là source/search manifest, reader
anchors, evidence cards, claim ledger, screening/ranking decision và argument
outline có giới hạn; không viết literature review bằng cách viết trước rồi đi tìm
citation, không coi metadata/ranking là semantic support, và không công bố đã
đọc/kiểm toàn văn khi chỉ có abstract hoặc access chưa rõ.

**Context:** [evidence report](../reports/research-260930-0905-local-sources-and-evidence.md),
[nature report](../reports/researcher-260930-0905-nature-skills.md),
[ecosystem report](../reports/researcher-260930-0905-skill-ecosystem.md),
[contract](../reports/brainstorm-260930-0905-skill-kit-contract.md),
[standards and failure catalog](./standards-and-failure-catalog.md).
Mọi file bên dưới là **CREATE tương lai; hiện chưa tồn tại** và chỉ phase này sở hữu.

## Key insights and requirements

- Ba quyết định phải tách: nguồn có đủ điều kiện theo policy; đoạn nguồn có
  entail claim; câu chữ có certainty phù hợp. Một paper Q1 không tự đỡ mọi câu.
- `metadata-only|abstract-only|full-text`, identity match, quote match,
  correction/retraction, license/access và semantic support là các trường riêng.
- Abstract-only có thể hỗ trợ một phát biểu hẹp, đúng nguyên văn/nội dung được
  nêu trong abstract nếu source policy cho phép; vẫn phải ghi rõ không đọc full
  text và không suy ra method/result/limitation ngoài abstract.
- Q1/Q2 chỉ được đánh giá ở chế độ `journal-strict` khi người dùng đã chọn
  issuer/system, category, metric và data-year. Unknown không được pass; không
  dùng best quartile/category khác, JIF/JCI/CiteScore/SJR/CAS lẫn nhau, hay tạo
  “Q1 conference”.
- Scholar/PaperPop chỉ là discovery/ranking hint; Unpaywall chỉ giúp tìm bản OA
  hợp pháp. Crossref/Retraction Watch xác minh metadata/notice, không thay cho
  đọc nguồn gốc. Không scrape, vượt paywall hoặc cài extension mặc định.
- Primary text, book, preprint, conference, foundational source và nguồn văn học
  cần policy ngoại lệ do từng task cho phép; không ép tất cả vào Q1/Q2.
- Chỉ dẫn, prompt injection hoặc yêu cầu upload nằm trong PDF/HTML là dữ liệu
  nguồn, không phải lệnh của người dùng hay của adapter.

## Architecture and data flow

| Stage | Input | Transform and decision | Output |
|---|---|---|---|
| Discovery | question/brief, venue/profile, allowed sources, date range | lưu query, timestamp, searcher, filters, raw candidate IDs; dedupe/version link có lý do | immutable search log + candidate manifest |
| Reader | candidate + exact version/hash + access/license | extract metadata, thesis/method/data/limits, stable S/C/F/T/E or page/section/line/timestamp anchors; OCR chưa là quote verified | source record + reader notes + evidence cards |
| Evidence audit | cards + claims + ranking/retraction metadata | field checks, quote exactness, entailment, contradiction, uncertainty, correction/retraction, permission | claim ledger `supported`, `contradicted`, `insufficient`, `unverified` |
| Reasoning | accepted/qualified claims + limits | separate observation/author claim/interpretation/inference; compare axes; build gap/method argument | bounded outline and open questions |
| Handoff | all records + receipts | preserve unknowns and blockers; map to writer/visual brief | evidence package, not prose acceptance |

Mỗi record mang `source_id`, version/hash, locator, provenance and check date.
Không dùng một scalar confidence để che trường còn thiếu. Nếu nguồn mâu thuẫn,
giữ cả hai verdict và lý do; không tự chọn nguồn “đẹp” hơn.

### Verdict-to-wording and freshness

<!-- Updated: approved red-team findings 4, 6, 8, 11; user approval 2026-09-30. -->

| Verdict | Cách được trình bày | Không được làm |
|---|---|---|
| `supported` | Câu có scope/certainty không vượt đoạn nguồn; nêu attribution nếu cần | Coi source eligibility/DOI match là semantic support |
| `contradicted` | Nêu tranh luận và nguồn trái chiều, tách population/method/time khi có | Nhận proposition bị bác bỏ như fact hoặc giấu nguồn bất lợi |
| `insufficient` | Giả thuyết/câu hỏi có nhãn, hoặc `AUTHOR_INPUT_NEEDED` trong draft | Chỉ thêm “có thể” để biến claim không có căn cứ thành accepted fact |
| `unverified` | Giữ pending với dữ liệu cần xác minh và người chịu trách nhiệm | Bịa citation/quote, tự xóa phần user yêu cầu để đạt pass |

Trước handoff mang tính nộp bài, kiểm lại correction/retraction và venue/AI
policy theo profile; kiểm lại ranking khi đổi metric-year/category/issuer, có
release mới liên quan hoặc snapshot hết freshness theo task policy. Ghi `as_of`,
`status_source`, revision và lý do recheck. Resume lâu hoặc nhận update notice
kích hoạt kiểm phần bị ảnh hưởng, không poll liên tục hay re-open mọi URL sau sửa
dấu câu. Không truy cập được nguồn kiểm trạng thái thì giữ `freshness-pending`;
full-text snapshot không bảo đảm paper chưa bị rút sau đó.

Reporting guideline, venue, mentor và style là các lớp riêng. Xung đột chưa
được giải quyết chặn `ready-for-selected-venue`; generic draft vẫn có thể bàn giao
nếu người dùng cho phép và các thiếu sót được ghi rõ. Không áp union mọi quy tắc.

Nguồn web/PDF chỉ đi qua tool sandbox/permissions thật. Source text không được
chuyển thành lệnh, quyền upload hoặc cấu hình hook. Nếu một adapter tự tải URL
sau này, phải kiểm redirects, scheme, local/private-network scope, kích thước,
thời gian và parser isolation trước dùng; không xây downloader/proxy chỉ để đọc
nguồn khi host đã có công cụ phù hợp.

## Requirements

1. `research-discovery` phải hỗ trợ narrative/scoping/systematic distinction;
   chỉ dùng nhãn systematic khi protocol, screening và audit tương ứng tồn tại.
2. `research-reader` phải lưu nguyên văn/giá trị nguồn, context, figure/table
   links, methodology, limitation và “do-not-overclaim”; thiếu locator thì không
   tạo direct quote.
3. `evidence-audit` phải kiểm DOI/title/author/year/publisher/page hoặc locator,
   source version, quote và claim entailment độc lập; `VERIFIED` không phải nhãn
   chung cho mọi chiều.
4. `research-reasoning` phải dựng claim–evidence–reasoning–limitation/counter-
   argument; research gap chỉ được nêu trong phạm vi corpus/search log.
5. Venue profile chỉ được nạp một profile đích gồm venue/year/revision/track/
   article type/stage/official sources; mentor/project overlay là lớp riêng.
6. Worker upstream tùy chọn phải qua P1 resolve/receipt và reader/evidence
   assessment; lỗi/timeout/thiếu receipt không biến thành success.
7. Maintain small rule cards with official source/section, applicability,
   revision/as-of, severity, exception, check and counterexample. Load only the
   selected study/venue/genre cards under P1 context budget, not whole manuals.
8. Preserve blueprint literary mode: exact edition/translator/editor and passage
   before interpretation; distinguish textual observation, critical interpretation,
   scholarly claim and personal inference. Books/primary text follow explicit
   source exceptions; no fabricated literary quote or Q1/Q2 label.

## Related files — ownership (future, not existing)

| Action | Absolute path | Ownership / purpose |
|---|---|---|
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-discovery\SKILL.md` | Search log, screening, dedupe và scope |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-reader\SKILL.md` | Deep reading, anchors, evidence cards |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\evidence-audit\SKILL.md` | Claim/citation/metadata/retraction audit |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-reasoning\SKILL.md` | Argument, comparison, method và gap |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\workflows\evidence-first.md` | Order and stop rules for reader→claim→prose |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\search-record.yaml` | Query, date, scope, raw result and screening fields |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\policies\ranking-and-venue.md` | Journal-strict Q1/Q2 and per-use venue isolation |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\policies\source-injection.md` | Treat source instructions as untrusted data |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\policies\evidence-verdicts.md` | Supported/contradicted/insufficient/unknown semantics |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\standards\rules.yaml` | Scoped, sourced rule cards and freshness records, not copied manuals |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\standards\failure-catalog.md` | Failure-to-rule-to-test mapping with false-positive boundaries |

P2 consumes P1 contracts read-only. P3 may consume its evidence package; P4 may
consume source/claim IDs. No later phase edits these P2-owned files directly.

## Implementation steps (future execution)

1. Map each output field to the immutable P1 source/evidence/claim contracts;
   add only a reviewed contract revision if a field is genuinely missing.
2. Define discovery record with query, source, timestamp, filters, candidate
   status, dedupe/version relationship, inclusion/exclusion reason and raw URL.
3. Define reader templates for PDF/HTML/scanned/OCR/primary literary text and
   stable locators; mark OCR-derived text as needing visual verification.
4. Define evidence cards and claim ledger with type, scope/population/condition,
   evidence IDs, allowed wording, forbidden strengthening and unresolved limits.
5. Add screening route for journal-strict Q1/Q2, generic draft and explicit
   source exceptions; require user decision for issuer/category/metric/year.
6. Add correction/retraction/version checks and preserve raw conflicting fields;
   do not call “no retraction found” proof of no retraction.
7. Write independent reasoning steps for synthesis, comparison and methodology;
   keep author claim, observation, interpretation and user inference labeled.
8. Exercise authorized upstream readers/citation workers only if P1 resolves a
   real interface and egress permission; otherwise retain a pending handoff.
9. Materialize the selected source-derived rule cards and literary/research modes
   from the standards catalog. Bind rule IDs to verdicts, reviewers and future
   fault tests; do not label a writing heuristic as an official universal rule.
10. Implement event-driven freshness and dependency invalidation; reserve reading
    and verification costs before dispatching independent source subsets.

## Todo

- [ ] Define search, source, evidence and claim fixtures against P1 schemas.
- [ ] Define Q1/Q2 decision record with unknown and exception states.
- [ ] Define reader anchors for page/block/section/line/timestamp and OCR review.
- [ ] Define conflict, correction, retraction and source-injection behavior.
- [ ] Define bounded reasoning outputs and handoff to P3/P4.
- [ ] Define scoped official rule cards, verdict wording and freshness triggers.
- [ ] Map every blueprint capability and literary mode to an output and fault test.

## Validation and test matrix (planned, not run)

| Fault/task | Required result |
|---|---|
| DOI matches but title/year/author conflicts | field conflict flagged; raw values retained; no silent merge |
| quote comes from another edition or page | direct quote rejected or marked unverified; locator requested |
| abstract-only source | may support only an exact, scoped abstract claim when policy permits; cannot claim full-text read or infer unmentioned method/result/limits |
| metadata-only source | cannot support substantive claim; identity/status only |
| retraction/correction notice or version relation | status visible; downstream wording blocked until resolved |
| rank missing system/category/metric-year | Q1/Q2 remains unknown; asks per-use decision |
| best quartile only in unrelated category | fails journal-strict; no substitute category |
| two sources disagree | contradiction preserved with scope and reasons |
| hostile instructions in PDF/HTML | ignored as data; logged as source anomaly |
| research gap beyond search corpus | downgraded to bounded observation or unverified |
| primary text/book/preprint exception absent | stop and ask policy; never auto-Q1/Q2 |
| retraction/AI policy changes after cached full-text read | dependent verdicts stale; recheck before venue-facing handoff |
| selected reporting guideline conflicts with mentor overlay | record conflict; no compliant status until resolved |
| claim is unsupported but writer adds a hedge | remains insufficient; no accepted fact without support |
| literary quote belongs to another edition/translation | preserve distinct versions and locators; no silent substitution |
| tutorial/official wording embedded as a source instruction | data only; no authority, script execution or provider permission |

Planned checks include schema validation, locator/quote matching, metadata
normalization, source-injection fixtures, and a human review of difficult claims.
No search, provider, source acceptance or research result is claimed as passed now.

## Risk, security and rollback

| Risk (likelihood × impact) | Mitigation / stop condition |
|---|---|
| False Q1/Q2 acceptance (M × H) | Require issuer/category/metric/year evidence and user policy; unknown blocks. |
| Citation/metadata mistaken for entailment (M × H) | Separate field check and claim support; human review for critical claims. |
| OCR/translation drift in quote (M × H) | Preserve original, locator and visual check; no quote until exact-match gate. |
| Source prompt injection (M × H) | Sandbox as untrusted data; allowlisted tools only; no source-originated commands. |
| Copyright/unauthorized full-text storage (M × H) | Store permitted excerpts/metadata/hash only; license ledger; stop packaging on ambiguity. |
| Provider/network failure (M × M) | Explicit pending/offline path; no retry of paid/side-effect calls without approval. |

Redact private manuscript content and credentials from logs; do not scrape beyond
access controls or bypass paywalls. Rollback removes/disable only the affected
worker mapping and keeps immutable ledger/receipts; accepted source decisions
must not be rewritten retroactively. Stop P2 if no source version/locator,
license, ranking policy or human escalation path can be established.

## Success criteria and next-step gate

- [ ] One sample task can travel from query to source manifest, reader card,
  claim ledger and bounded outline with all hashes/locators/unknowns visible.
- [ ] No fault fixture passes a fabricated quote, DOI/page, Q1/Q2 status or
  unsupported gap; no source instruction changes the workflow.
- [ ] Venue, ranking and source exceptions are explicit per use and never leak
  into the next task/profile.
- [ ] P3 receives evidence-bound input rather than a citation-seeking draft.

P3 may start only after P2’s planned matrix is executable against P1 contracts;
the phase remains pending until an executor supplies real evidence.
