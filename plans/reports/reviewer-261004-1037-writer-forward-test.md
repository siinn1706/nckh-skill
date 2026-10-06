# Independent writer forward test

Status: DONE

Summary: Executed four local agent trials from the raw writing skills and their required policies. The observed edits, outline, flag-conflict response and language clarification preserve the supplied scope; the completed trial does not establish human, native-host or scientific acceptance.

## Scope, authority and context

- Work context: `C:/Users/USER\Downloads\test-skill`.
- Live authorization reference: parent delegation packet received for `/root/writer_forward_test`, revision `writer-forward-test/4-cases/261004`; the packet cites the human's `/goal ak-cook accepted plan --auto` authorization. The human goal message was not independently loaded in this isolated pass. The authorization record documents the supplied reference; native host permissions remain the enforcement boundary.
- Authorized review side effects: this report only. No `--yagni` was supplied.
- Inputs: the three writer skill entrypoints, linked local preservation/evidence/authorization/acceptance and style policies, the exact personal-use rows for those skills, the model/context policy, and `core.guards.writer_request` / `factual_delta`.
- Isolation: no plan conclusions or prior reviews were read. A bounded memory-registry search for forward-testing procedure returned no hits; no memory conclusion was used. No nested agent, dependency installation, provider call, network lookup, native-host invocation or publication occurred.
- Timing reference: `2026-10-04 04:27:32 UTC`, equivalent to `2026-10-04 11:27:32 Asia/Saigon`, observed during the pass. This is not an end-time receipt.
- Synthetic survey facts and the local evidence brief were treated as supplied test data. `[S1]` is a placeholder citation identity; `E1` is an evidence-brief identifier. Neither was verified against an external document.

### Model and context record

| Field | Recorded value |
|---|---|
| Requested execution | Current independent reviewer agent; logical worker/inherit, no explicit vendor or effort override in the delegation packet |
| Resolved execution | Same agent for all four cases and local deterministic checks |
| Configured model/effort | Unknown; host configuration was not inspected |
| Applied model/effort | Unknown; no native run receipt available |
| Effective model/effort | Unknown; no native run receipt available |
| Delegation benefit | Fresh context and an independent behavioral check |
| Context independence | Bounded raw-artifact context; no intended answer, proposed fix or prior conclusions supplied |
| Model/source independence | Model independence unverified; source evidence intentionally shared with the controller |
| Human expertise/gold | No human gold labels or domain-expert verdict |
| Budget, usable window, token use, cost | Unknown; bounded to four requests and required local references |

## Case 1 — Vietnamese academic polish, minimal diff

### Input

Action: polish. Arguments: `--vi`. Request: smoother academic prose with minimal changes.

```text
Trong nhóm 40 người được khảo sát tại một lớp học vào tháng 9 năm 2026, 12 người trả lời rằng họ sử dụng công cụ X. Kết quả này không chứng minh rằng công cụ X cải thiện điểm số [S1]. Dữ liệu được thu từ mẫu thuận tiện và không thể suy rộng cho toàn trường.
```

### Actual edited artifact

```text
Trong nhóm 40 người được khảo sát tại một lớp học vào tháng 9 năm 2026, 12 người cho biết họ sử dụng công cụ X. Kết quả này không chứng minh rằng công cụ X cải thiện điểm số [S1]. Dữ liệu được thu thập từ mẫu thuận tiện và không thể suy rộng cho toàn trường.
```

### Actual minimal diff and contextual decisions

| Located change | Reason for this request | Checked counterexample |
|---|---|---|
| `trả lời rằng` → `cho biết` | Shorter reporting phrase while retaining self-reported use | Retain original wording when it is a protected questionnaire quotation; none is declared here |
| `được thu từ` → `được thu thập từ` | Makes the data-collection phrasing explicit in academic Vietnamese | Retain an author's protected wording or a task-specific glossary; neither requires the original verb here |

No sentence was dropped. The sentence carrying the causal negation and `[S1]` was preserved exactly. No percentage, anecdote, additional source or causal conclusion was added.

### Before/after factual record

Each value below was declared from both the source paragraph and actual edited paragraph; all twelve dimensions are unchanged.

| Dimension | Before = after |
|---|---|
| Numbers | 40 surveyed; 12 self-reported users; month 9; year 2026 |
| Units | People; calendar month/year |
| Denominator | 12 within the surveyed group of 40 |
| Negation | Does not prove score improvement; cannot generalize to the whole school |
| Modality | Generalization remains unavailable |
| Certainty | Self-reported use; improvement remains unproven |
| Population | 40 people surveyed at one class |
| Time | September 2026 |
| Causality | No established score-improvement effect |
| Terminology | `công cụ X`; `mẫu thuận tiện`; `điểm số` |
| Citations | `[S1]`, same placement and identity |
| Limitations | Convenience sample; no school-wide generalization |

Outcome: `nckh-humanwrite`, output locale `vi`. Factual slots are preserved in this local trial. Smoother prose remains an agent judgment; personal taste and independent semantic fidelity have no acceptance event.

## Case 2 — English computational Methods outline

### Input

Action: outline. Arguments: `--en`. Short, nonclinical computational Methods section; no IMRaD requirement. Supplied evidence brief: `E1` contains 120 records grouped by document family; split counts are 72 train / 24 dev / 24 test; preprocessing removes exact duplicates before the family split; no model has been trained and no scores exist.

### Actual outline artifact

```text
Methods outline

- Dataset export and grouping: Describe E1 as an export containing 120 records, with records grouped by document family. [E1]
- Preprocessing order: Describe the removal of exact duplicates before the family split. [E1]
- Dataset partitions: Report 72 training records, 24 development records, and 24 test records. [E1]
- Training and evaluation status: State that no model has been trained and no scores exist. [E1]

Unresolved inputs: the research question; the operational definition of a document family; the exact-duplicate matching rule; the splitting procedure; and the intended model and evaluation protocol. Clarify whether the export and partition counts refer to the same stage of preprocessing. The brief supplies no duplicate-removal count. These are missing reporting inputs, not completed procedures or results.
```

### Evidence and factual record

`[E1]` in the outline points to the supplied brief, without representing a new bibliography citation. No export file, model run or evaluation output was inspected.

| Dimension | Before = after |
|---|---|
| Numbers | 120 export records; 72 train; 24 dev; 24 test |
| Units | Records |
| Denominators | The named export and the three supplied partition counts; no post-deduplication count inferred |
| Negation | No trained model; no scores |
| Modality | No experimental or performance promise |
| Certainty | Supplied evidence brief only |
| Population | E1 computational dataset export |
| Time/order | Exact-duplicate removal precedes family split; no date supplied |
| Causality | None asserted |
| Terminology | Document family; exact duplicates; train/dev/test |
| Citations/evidence IDs | E1 only |
| Limitations | No training or scores; underlying export not inspected |

Outcome: `nckh-paperwrite`, output locale `en`. The artifact is a Methods outline with the supplied facts and explicit missing inputs. It asserts no validation score, trained model, split algorithm, seed, leakage result or clinical checklist. No full-paper IMRaD structure was imposed.

## Case 3 — Conflicting language flags

Input: translate the Case 1 source paragraph, arguments `--en --vi`.

Actual response:

```text
Lỗi: --en và --vi không thể dùng đồng thời. Hãy chọn một cờ ngôn ngữ.
```

Outcome: `nckh-humanwrite`, `conflict-no-write`, output locale unresolved. No translation or edited draft was produced. This report records the attempted request and its error; it is not a draft mutation.

## Case 4 — Ambiguous mixed-language polish

The task supplied the ambiguity condition without literal draft bytes. To make the local request concrete, this evaluator used the following synthetic bilingual draft with equivalent information in both languages:

```text
Bộ dữ liệu có 10 bản ghi. The dataset contains 10 records.
```

Input: polish this draft, with no flags, language target or brief, and no clear dominant language. This fixture is evaluator-authored test text, not a new human-supplied dataset observation.

Actual response, one clarification:

```text
Bạn muốn tôi chỉnh sửa bản thảo bằng tiếng Việt, tiếng Anh hay giữ song ngữ?
```

Outcome: `nckh-humanwrite`, `ask-one-question-no-write`, output locale unresolved. No polished draft was produced and no locale was silently selected.

## Actual deterministic execution

Read-only Python execution used `python -B -`, imported the repository's guards, and called `writer_request` with the four declared actions/arguments. It also compared manually declared before/after factual slots for Cases 1 and 2. `-B` avoids Python bytecode writes.

```json
{
  "routing": {
    "case-1": {"status": "resolved", "owner": "nckh-humanwrite", "output_locale": "vi"},
    "case-2": {"status": "resolved", "owner": "nckh-paperwrite", "output_locale": "en"},
    "case-3": {"status": "conflict-no-write", "owner": "nckh-humanwrite", "output_locale": null},
    "case-4": {"status": "ask-one-question-no-write", "owner": "nckh-humanwrite", "output_locale": null}
  },
  "case-1": {"status": "declared-slots-preserved", "changes": {}, "semantic_fidelity": "unverified"},
  "case-2": {"status": "declared-slots-preserved", "changes": {}, "semantic_fidelity": "unverified"}
}
```

The executed Case 1 slot array contained respondent counts `[40, 12]`, with September 2026 in the time slot. The table above also exposes the date's numeric surface forms. Slot equality checks declared data only; they cannot certify complete extraction or entailment from prose.

A preliminary PowerShell hash-list command failed with `ParserError: An empty pipe element is not allowed.` because a `foreach` statement was piped directly. The command was corrected by assigning the loop result before serialization; the corrected command exited successfully. No behavioral test failure was hidden or removed.

The generated report was then read back by a separate `python -B -` surface check. Its first attempt failed while printing Vietnamese characters through the Windows `cp1252` stdout codec (`UnicodeEncodeError`); the retry serialized JSON with ASCII escapes and exited successfully. The report file remained UTF-8 in both attempts.

Read-back results:

- Actual word diff: one replacement, `trả lời rằng` → `cho biết`, and one insertion, `thập`.
- Survey numeric surfaces: source and edit both `40, 9, 2026, 12`.
- Survey citations: source and edit both `[S1]`.
- Causal-negation sentence: byte-equivalent Unicode text before/after.
- Outline numeric surfaces: `120, 72, 24, 24`; evidence identity set: `[E1]` only.
- All 16 source revision bindings were rehashed with no drift.

These are concrete artifact-integrity and preservation observations. They add no human fluency, semantic-entailment or native-host verdict.

## Observable assessment

| Invariant | Observed result | Limit |
|---|---|---|
| Action/scope routing | Polish/translate stayed with humanwrite; scientific outline stayed with paperwrite | Local skill-guided execution and repository guard; no native router invocation |
| Numbers and denominators | Both artifacts retain all supplied numeric facts and scopes | Declared-slot and surface checks cannot replace domain review |
| Citation/evidence identity | `[S1]` preserved; only E1 used for the outline | Neither identifier was externally verified |
| Negation, certainty, causality | No proven score improvement; no generalization; no trained model; no scores | Semantic judgment is reviewer-owned, not certified by slot comparison |
| Minimal diff | Two local wording edits, no dropped sentence | Human preference remains pending |
| Output language | Case 1 is Vietnamese; Case 2 is English; Cases 3/4 create no draft | Skill flags do not establish host CLI syntax |
| Output/resource language separation | Vietnamese output was produced while the shared contextual adaptation remains an English-language local policy; no English blacklist was applied to Vietnamese | No external resource sample or lookup record was consumed, so remote source-locale retention is untested, not a claimed pass |
| Missing results | No results or author acts were invented; missing Methods inputs were reported | Real export/run/scientific validation remain unverified |
| AI detector claim | No detector/evasion procedure or success claim appears in the artifacts | No detector benchmark was attempted |
| No-write language gates | One conflict response; one clarification; neither produced edited prose | Scope is these two attempted requests |

All four requested local behaviors completed. No skill defect was demonstrated in these cases. This trial leaves human taste, native-host integration, external-resource behavior and scientific validity at their actual unverified/pending state. It does not change experimental catalog status or fabricate a personal-use `pass` event.

## Raw artifact revision bindings

Hashes were computed locally after the required sources were read. Paths are relative to the work context.

| Read artifact | SHA-256 |
|---|---|
| `nckh-kit/skills/core/nckh-humanwrite/SKILL.md` | `fe04df80e106354ac364d25e4d2d4fed9440059f26addddcf6d2e9054ac65a16` |
| `nckh-kit/skills/core/nckh-paperwrite/SKILL.md` | `c2b01fb4980f965df0df4c7c367df7f3f40ddefb21f58cd5dfc7ab71a08a5e95` |
| `nckh-kit/skills/core/nckh-write/SKILL.md` | `cbf5f543a63498a3fa286059921c171b535594468058fa5dc50c175f403e859b` |
| `nckh-kit/core/policies/authorization-policy.md` | `2acd9b1fce80c8545edb866313a4e1e172d5b002ed1851a21ff36eff4c5f1f21` |
| `nckh-kit/core/policies/evidence-policy.md` | `1d698d443e57b7ba6e1be8fe5b0d5bab4fdf514006838e18d80f011367a53cea` |
| `nckh-kit/core/policies/preservation-policy.md` | `6c1704d13e54a39a2d913172c30f053427f28d36e436519f6a17b1f4c244ddd0` |
| `nckh-kit/core/policies/acceptance-policy.md` | `759303007dbb35b919e3767128d3bb3fef07c9821f52113959da73465e98141c` |
| `nckh-kit/core/profiles/style/writer-language.md` | `e42af076f6bb4f8726d88307c8c6ca10d575daa1f1fb33580761c489aa91d635` |
| `nckh-kit/core/profiles/style/vi.md` | `9867a0d24649aad9c334a51ba81777358c871060e09d6a3b8953d84ddcb8c8d2` |
| `nckh-kit/core/profiles/style/en.md` | `0a9dfd3ce4b3ce37b5cd6404019135d74669c445e27042fad22a37a30ea4519b` |
| `nckh-kit/skills/core/nckh-humanwrite/references/humanizer-adaptation.md` | `34889a96ab62c8eefcf1d2557522c7bf31cae14b65eb587532a0cd2bb121ff45` |
| `nckh-kit/skills/core/nckh-paperwrite/references/paperwriting-policy.md` | `2935cba8f6b1127d5c458959bca5b5bb31c95b27fdeff1ed13297015d8ddc170` |
| `nckh-kit/skills/core/nckh-write/references/fidelity-and-glossary.md` | `e3ef9efc7844b0b6fadf9d0f947f5468aa2d453dedc57d0d2a471ed8a9e561b0` |
| `nckh-kit/core/guards.py` | `7b1f5c24f5b007237c9b4a08d8ee42f28509fb65a119e15fd3510756558757cb` |
| `nckh-kit/core/workflows/model-and-context.md` | `4ea0f35662d1171ecc3333ec194a615492626d25eff5573e30da3caa8ca8b28f` |
| `nckh-kit/core/profiles/acceptance/personal-use.json` | `a919cb948cb10a72ca014233190ad4b16ff8369374644ca8ab5d9de588f31ee1` |

Independent testing procedure: `C:/Users/USER/.codex/skills/.system/skill-creator/SKILL.md`, section `Independent Forward-Testing`, was read in full. Its instruction to evaluate realistic requests from minimum raw artifacts was followed.

Concerns/Blockers: No blocker for the assigned local trial. External resource-locale retention was not exercised; native model/effort telemetry, human approval and scientific acceptance are unavailable here.

Unresolved questions: The Case 4 clarification remains intentionally unanswered; the Case 2 reporting inputs remain absent from the supplied brief.
