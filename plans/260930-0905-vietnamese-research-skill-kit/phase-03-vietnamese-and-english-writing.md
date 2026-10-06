---
title: "Phase 3: Việt ngữ và English scientific writing"
status: pending
---

# Phase 3: Việt ngữ và English scientific writing

## Overview

**Priority:** P1 · **Estimate:** 2–3 ngày, ước tính không cam kết · **Status:** pending.

Phase này xây ba domain module còn thiếu của lớp ngôn ngữ: `vi-writing`,
`vi-taste` và `en-scientific-writing`. Writer nhận evidence-bound input từ P2,
không tự tìm citation để hợp thức hóa bản nháp; taste là critic có rubric,
không phải AI detector; English có thể draft trực tiếp hoặc chuyển từ VI theo
brief, nhưng phải giữ modality, số, đơn vị, terminology, scope và limitation.
Instruction/metadata/adapter của cả ba module viết bằng English; output vẫn theo
`output_language`/style profile. Mọi file ở đây là **CREATE tương lai; hiện chưa
tồn tại** và chỉ phase này sở hữu.

**Context:** [design proposal](../reports/brainstorm-260930-0905-skill-kit-contract.md),
[synthesis](../reports/synthesis-260930-0905-skill-kit-selection.md),
[blueprint](../../vietnamese-writing-research-skills-blueprint.md),
[evidence contract](./phase-02-evidence-and-research.md),
[scoped writing standards](./standards-and-failure-catalog.md).

## Key insights and requirements

- Gu cá nhân không thể suy từ generic Vietnamese/technical register. Cần sample
  có quyền dùng, bad/good pairs và người dùng/native reviewer; self-score chỉ là
  diagnostic. Chưa có corpus thì gọi là neutral experimental register.
- `vi-writing` tách new draft, edit/minimal-diff, rewrite và polish. Polish
  không được đổi certainty, facts, terminology hay protected region.
- Không cấm tuyệt đối một danh sách sáo ngữ. Critic nêu chức năng cụ thể, độ
  trừu tượng, nhịp, lặp, dịch-khó chịu và đề xuất sửa gắn claim/evidence.
- `en-scientific-writing` không biến “native-like” thành scientific correctness,
  không áp IMRaD cho mọi genre, không tự thêm method/result/citation, và phải
  báo khi translation làm mất sắc thái.
- Evidence-first governs factual claims. A pure-prose/creative task with no
  factual change may use the writing/taste path without a full P2 evidence
  package, but supplied facts still receive fidelity checks and the writer may
  not invent citations or present fiction as research.
- English-authored instruction là lựa chọn của người dùng, không phải bằng chứng
  tự nó nâng output. Giữ instruction English cố định trong matched evaluation;
  không tự thêm thí nghiệm A/B ngôn ngữ chỉ dẫn.

## Architecture and data flow

| Stage | Input | Transform and gate | Output |
|---|---|---|---|
| Style lock | user brief, reader, genre, voice/style profile, protected regions | validate register/locale/terminology and permissions; choose `factual`, `pure-prose` or `creative`; no venue defaults | hashed style profile + edit scope |
| VI writer | P2 claims/evidence/limits when factual, or prose brief when no factual change | compose or minimal-diff; mark `UNVERIFIED`; preserve allowed wording and citations | VI draft + claim/fidelity diff |
| Taste critic | anonymized VI draft + rubric + source facts | flag cliché/abstraction/rhythm/register issues without fact edits; separate critic from writer | critique, alternatives, unresolved taste decisions |
| EN writer | evidence-bound VI or direct EN brief + terminology ledger + venue profile | rhetorical moves by genre; translate/draft; compare modality, numbers, units, negation, terminology | EN draft + translation/fact-fidelity diff |
| Handoff | VI/EN outputs + receipts + human-review status | require human/native/domain gate for sensitive claims and personal voice | `draft`, `evidence-pending`, `human-review-required`, never auto `ready` |

The writer may consume source IDs and locators but cannot create evidence. A
critic using the same model/runtime must be labeled non-independent. Protected
sections and author decisions are never silently rewritten.

<!-- Updated: approved red-team findings 4 and 5; user approval 2026-09-30. -->

Sau mỗi lần polish/rewrite/translation, so factual delta giữa input và output:
claim mới, attribution, số/đơn vị, phủ định, modality, population, time và causal
language. Nếu thêm/đổi factual claim, chuyển riêng phần đó về P2 hoặc đánh dấu
`evidence-pending`; nhãn “chỉ sửa văn” trong brief không thay phép kiểm đầu ra.
Pure fiction không bị ép có citation; dữ kiện về thế giới thật được chèn vào một
bài nonfiction vẫn phải kiểm. Receipt trỏ đúng input/output hash và claim ledger.

Nguồn đại học uy tín cung cấp heuristic về lập luận, cohesion, rõ nghĩa và
hedging; profile người dùng mới quyết định gu. Không cấm toàn bộ passive voice,
nominalization, từ Hán–Việt hay cụm chuyển đoạn. Không sao chép phrasebank thành
corpus không rõ quyền; không dịch máy máy móc quy tắc tiếng Anh sang tiếng Việt.
Đọc rule cards thích hợp theo genre, không nạp cả kho style vào context.

## Requirements

1. Future `SKILL.md` files are English and use progressive disclosure; examples,
   quotes and Vietnamese corpus retain original language and provenance.
2. Style profile fields cover audience, genre, register, pronouns, formality,
   rhythm, vocabulary, desired/undesired traits, approved examples and reason;
   style cannot override facts, evidence or certainty.
3. VI output supports natural Vietnamese, explicit concrete claims and varied
   rhythm while reporting unsupported/overbroad/AI-like phrasing as critique,
   not treating a heuristic list as law.
4. EN output supports direct drafting and `vi-to-en` as distinct routes; keeps
   citation/quote unchanged unless an approved translation is supplied; preserves
   equations, units, CI/SD/SE, denominators, conditions and limitations.
5. Terminology ledger records source term, VI/EN form, definition, allowed
   variants, protected forms and decision owner; no synonym swap merely to avoid
   repetition.
6. Pure-prose/creative routes may omit scholarly evidence when the task and
   output factual-delta check confirm no new or changed factual assertion; facts
   supplied in the brief still require fidelity checks and fiction stays labeled.
   Human review is required for
   personal taste gold, claim-sensitive translation,
   terminology disputes and any venue-facing compliance decision.

## Related files — ownership (future, not existing)

| Action | Absolute path | Ownership / purpose |
|---|---|---|
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\vi-writing\SKILL.md` | Vietnamese draft/edit/polish modes |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\vi-taste\SKILL.md` | Independent taste critique and rubric |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\en-scientific-writing\SKILL.md` | English scientific draft/translation |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\style\vi-register.md` | Register, rhythm, diction and locale heuristics |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\style\taste-rubric.md` | Precision, concreteness, rhythm, naturalness, cliché risk |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\style\terminology-ledger.schema.yaml` | Schema/template only; task/project-scoped term decisions |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\style\translation-fidelity.md` | Claim/modality/number/unit fidelity checks |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\profiles\style\generic-draft.yaml` | Neutral generic profile, not personal gold |

P3 consumes P1/P2 contracts and outputs; P5 owns all evaluation fixtures and
release checks. P4 may consume the final text but must not edit P3 files.

## Implementation steps (future execution)

1. Freeze the evidence-bound input/output fields and protected-region semantics;
   require P2 claim/evidence status for factual content, while allowing an
   explicitly marked pure-prose/creative path with no factual-change claim.
2. Define generic and personal style profile loading, including sample license,
   provenance, author preference and expiry/review fields.
3. Write VI writer modes with minimal-diff, rewrite, polish and new-draft rules;
   retain uncertainty and surface missing evidence rather than filling it.
4. Write taste critic rubric and independent-review protocol; include concrete
   diagnostic categories (empty abstraction, fake depth, translationese, rhythm,
   repetition) without absolute banned-word rules.
5. Write EN direct and VI→EN routes with rhetorical moves selected by genre,
   terminology lock, source-linked diff and `AUTHOR_INPUT_NEEDED` fallback.
6. Define locale checks for NFC/diacritics, numbers/dates and code-switching
   where relevant; warnings cannot assert scientific truth.
7. Add human-review handoff and disagreement capture; do not merge reviewer
   scores into a single “gold” without identity and rubric provenance.
8. Run only authorized workers after P1 resolution; record model/runtime and
   whether writer/critic share a model so independence is not overstated.
9. Apply the P2 verdict-to-wording matrix and selected writing rule cards; route
   newly introduced facts to evidence audit, without making every cosmetic edit
   pay for a new multi-agent literature search.

## Todo

- [ ] Define generic and personal style profile schemas and sample-rights fields.
- [ ] Define VI writer modes, protected regions and certainty-preservation diff.
- [ ] Define taste rubric, bad/good pair format and human/native review gate.
- [ ] Define EN direct/translation routes and terminology ledger behavior.
- [ ] Define locale/translation fault fixtures for P5 without treating them as gold.
- [ ] Define post-edit factual-delta checks and genre-scoped writing guidance.

## Validation and test matrix (planned, not run)

| Scenario | Required result |
|---|---|
| sentence has unsupported factual detail | writer marks/asks; does not invent citation or fact |
| pure prose/creative brief with no factual change | writing/taste route may proceed; supplied facts still get fidelity checks and fiction stays labeled |
| `suggests`/`may` rewritten as `proves` | fidelity gate fails; certainty must remain or weaken |
| changed number, unit, CI/SD/SE, denominator or negation | diff fails and blocks handoff |
| exact quote/term has no approved translation | preserve original or request author input; no invented quote |
| generic Vietnamese anti-cliché rule | critic explains local problem; no absolute banned-word deletion |
| personal sample license missing | personal profile blocked; neutral register only |
| direct EN vs VI→EN on same claims | route recorded; modality/term/number diff reviewed |
| genre is not a research article | no automatic IMRaD or “journal compliant” claim |
| writer and critic share model | receipt labels review non-independent; human gate remains |
| protected paragraph/mentor region | untouched unless explicit permission is recorded |
| polish inserts a date, mechanism or new causal claim | route delta to P2; evidence-pending until resolved |
| passive voice or Vietnamese formal diction is useful in context | preserve where justified; no universal banned-word/style rule |
| brief says creative but output invents a real quotation | quote gate still fails; creative label does not grant fabrication |

Planned tests include deterministic term/number diff, Vietnamese locale lint,
paired human rubric review and bilingual domain review. They are future test
design, not evidence that English instructions or style quality already passed.

## Risk, security and rollback

| Risk (likelihood × impact) | Mitigation / stop condition |
|---|---|
| Generic or culturally wrong Vietnamese voice (M × M) | Personal corpus + human gold; neutral fallback; do not claim personalization without review. |
| Translation changes scientific claim (M × H) | Claim-linked diff for modality/number/unit/term; human bilingual gate; block on mismatch. |
| Writer invents citation/evidence (M × H) | Writer cannot create source/evidence; P2 ledger required; unsupported state visible. |
| Taste critic becomes authority or detector (M × M) | Rubric is advisory; keep disagreement; no AI-detector/pass label. |
| Unauthorized personal sample/provider upload (M × H) | License/egress allowlist and redaction; offline path; stop before worker call. |
| Venue rule leaks into generic output (M × M) | Style and venue profiles separate; task-bound hash; reset between runs. |
| Mutable glossary leaks terms across tasks (M × M) | Use schema/template only; store term decisions with task/project lifetime, sources, approval and profile hash. |

Never store private samples or full drafts in shared diagnostics without explicit
permission. Keep raw quote and translated text traceable but redact sensitive
content. Rollback by disabling the affected route/profile or reverting to the
last accepted style/translation contract; do not silently rewrite existing
manuscript decisions. Stop if human approver, rights, source evidence or
translation fidelity cannot be established.

## Success criteria and next-step gate

- [ ] VI writer can produce a factual draft/minimal diff traceable to P2 records,
  or an explicitly pure-prose/creative draft without falsely claiming research;
  style choices remain explainable.
- [ ] Taste critic returns actionable, non-factual critique with human-review
  status; no self-score is labeled gold.
- [ ] EN direct and VI→EN routes preserve all tested quantities, modality,
  terminology and limitations, or stop with an explicit mismatch.
- [ ] No personal voice/venue compliance claim is made without rights/profile /
  human evidence; P4 receives a stable, reviewable text artifact.

P4 may start only after the writer/critic outputs and fidelity gate are specified
against immutable P1/P2 contracts; this phase remains pending until executed.
