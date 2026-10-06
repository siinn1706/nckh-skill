---
title: "Phase 4: Slides và scientific visuals"
status: pending
---

# Phase 4: Slides và scientific visuals

## Overview

**Priority:** P1 · **Estimate:** 2–3 ngày, ước tính không cam kết · **Status:** pending.

Phase này biến evidence-bound claims và text đã kiểm thành storyboard, chart,
scientific mechanism diagram hoặc artwork đúng loại, với source truth,
provenance, accessibility, editability và render inspection. `research-visuals`
không tạo dữ liệu; không nhận một raster/AI image là PPTX editable hay scientific
evidence. Kết quả có thể là draft/pending nếu venue policy, asset license,
font/viewer hoặc source data chưa đủ.

**Context:** [nature report](../reports/researcher-260930-0905-nature-skills.md),
[ecosystem report](../reports/researcher-260930-0905-skill-ecosystem.md),
[synthesis](../reports/synthesis-260930-0905-skill-kit-selection.md),
[writing handoff](./phase-03-vietnamese-and-english-writing.md),
[selected policy and visual checks](./standards-and-failure-catalog.md).
Mọi file dưới đây là **CREATE tương lai; hiện chưa tồn tại** và chỉ phase này sở hữu.

## Key insights and requirements

- Phân biệt ba artifact: chart từ dữ liệu thật (giữ đơn vị/uncertainty), diagram
  cơ chế/quan hệ (kiểm topology/nhãn/ký hiệu), và artwork minh họa (ghi rõ
  illustrative, không đại diện measurement/mechanism đã xảy ra).
- Native runtime presentations và các module có interface thật có thể được gọi
  qua P1 adapter; không copy runtime package hay nhầm HTML/PDF với PPTX.
- `nature-paper2ppt`/Orchestra cung cấp storyboard, source labels, speaker notes,
  text budget và PPTX QA để chọn lọc. K-Dense scientific-slides mặc định thiên
  image-per-slide/PDF nên **không đạt editability contract ở route đó**; route
  PowerPoint thay thế có tồn tại nhưng phải qualify riêng, chưa được coi là đã
  chạy/đạt. Anthropic Office skill là reference-only vì license file proprietary.
- OpenAI visualization references chỉ đóng góp model/geometry/provenance; tính
  đúng cơ chế khoa học, số liệu và policy venue do package này chịu trách nhiệm.
- Ảnh sinh hoặc asset third-party chỉ dùng khi provider/venue/license cho phép;
  confidential source không được upload mặc định.

## Architecture and data flow

| Stage | Input | Transform and gate | Output |
|---|---|---|---|
| Visual brief | audience, duration, artifact type, venue/profile, editability target | lock chart/diagram/artwork kind, dimensions, fonts, language and egress | hashed visual brief |
| Truth mapping | P2 claims/evidence/data + P3 text | map each mark/label/arrow/numeric value to source ID, unit, uncertainty and inference flag | visual source manifest |
| Authoring | manifest + allowed native worker/tool | build editable shapes/tables/charts/SVG/PPTX or clearly labeled raster draft; keep notes/citations | source artifact + provenance |
| QA | source + rendered pages/slides + contract | semantic/topology checks, collision/readability, font/contrast, panel alignment and editability inspection | audit report + failures |
| Handoff | artifact, render, manifest, receipt | human/domain/venue/asset review; preserve pending gates | `draft`, `human-review-required`, `accepted` |

No chart value may appear without a source/derivation record. Inferred arrows,
illustrative styling and manual corrections must be labeled separately from
observed/source-truth elements.
Visual `accepted` ở phase này chỉ là acceptance cục bộ trong receipt; nghiệm thu
toàn scope vẫn phải qua aggregate gate P5, không che fail/pending của phần khác.

<!-- Updated: approved red-team finding 9; user approval 2026-09-30. -->

Mỗi QA run gắn `qa_run_id`, source/data/render/manifest hashes, contract/profile
revision, viewer/render engine và font versions. Sửa source, dữ liệu, labels,
font hay render làm stale đúng phép kiểm bị ảnh hưởng; không dùng báo cáo pass
của file cũ cho file mới. Trước handoff kiểm artifact khớp QA receipt; giữ
originals và failed renders để truy nguyên, không tự overwrite nguồn.

Storyboarding và semantic mapping đi trước image generation. Dựng slide pilot
đại diện trong ngân sách rồi mới mở rộng deck; tái dùng template/assets được phép
và render lại phần ảnh hưởng. Chi phí image/vision và số lần sửa nằm trong pool
P1, không gọi image model để thay một chart/vector deterministic đã đáp ứng brief.

## Requirements

1. `research-visuals` must route by artifact kind and target format (PowerPoint,
   SVG/PDF/native canvas or other user-approved format), not by filename alone.
2. Slide contract must specify hierarchy, text budget, source/caveat/alt text,
   speaker notes, editable objects, font/contrast and render viewer requirements.
3. Diagram contract must specify entities/relations, direction, grouping,
   labels, units, source IDs, inferred-vs-observed flags and accessibility text.
4. Charts must preserve raw values, aggregation, denominator, uncertainty,
   axis units, missingness and rounding; no image-only chart may be labeled data.
5. Artwork must carry `illustrative`/synthetic provenance and cannot stand in for
   an experiment, clinical observation, citation, mechanism or Q1/Q2 evidence.
6. Visual review must inspect both native/source layer and rendered output; a
   script pass is not human/domain acceptance. Venue AI/figure policy is loaded
   only for the selected venue and revision.

## Related files — ownership (future, not existing)

| Action | Absolute path | Ownership / purpose |
|---|---|---|
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-visuals\SKILL.md` | Slide, chart, diagram and artwork routing |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\visuals\slide-contract.md` | Editable deck/source/render contract |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\visuals\diagram-contract.md` | Topology, labels, evidence and accessibility |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\visuals\chart-contract.md` | Data/units/uncertainty/aggregation contract |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\visuals\asset-provenance.yaml` | Asset source, license, model/provider and manual changes |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\visuals\native-output.md` | Runtime/native output adapter boundary |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\profiles\visual\generic-draft.yaml` | Format-neutral visual profile, not venue compliance |

P4 consumes P1/P2/P3 records read-only. P5 owns visual regression fixtures and
packaging checks; it must not edit these contracts directly.

## Implementation steps (future execution)

1. Define visual brief and classify every request as chart, mechanism diagram,
   artwork or mixed deck; ask for format, viewer, font/template and venue policy.
2. Map claims/data/relationships to source IDs, locators, units, uncertainty,
   inferred flags and permitted transformations before authoring.
3. Select native worker/tool through P1; record capability, version/hash,
   provider, egress and output format. If only image/PDF route exists, keep it
   as non-editable draft and do not relabel it.
4. Build slide storyboard using audience/time/claim hierarchy, source labels,
   caveats, alt text, speaker notes and readable reduction; avoid Nature/CNS or
   ML conference rules unless a matching profile is selected.
5. Build diagrams from explicit entities/relations and test arrow direction,
   grouping, units and semantic consistency before styling.
6. Produce chart from supplied data or mark missing input; never infer `n`, p,
   error bar or result from visual appearance. Preserve rounding provenance.
7. Inspect native editability and renders in the user-approved viewer set; log
   collisions, clipping, overflow, contrast, font fallback and panel alignment.
8. Add human/domain/asset/license review and deliver source + preview + manifest,
   never preview-only when editability was requested.
9. Bind QA to exact artifact hashes and viewer/font versions, invalidate changed
   dependencies, and rerun affected checks before delivery. Load AI/figure rules
   only from the selected venue profile, including its stated exceptions.

## Todo

- [ ] Define slide, chart, diagram and asset-provenance contracts.
- [ ] Define native output routes and explicit non-editable fallback status.
- [ ] Define source/claim-to-mark mapping and inferred-vs-observed labels.
- [ ] Define render/viewer/editability and accessibility QA matrix.
- [ ] Define license/venue/egress gates for generated and third-party assets.
- [ ] Bind visual QA to artifact versions and define budgeted pilot/render reuse.

## Validation and test matrix (planned, not run)

| Scenario | Required result |
|---|---|
| chart missing `n`, units, aggregation or uncertainty | `AUTHOR_INPUT_NEEDED`; no invented values |
| chart value differs from source manifest | semantic check fails; block handoff |
| mechanism arrow/label/topology mismatch | diagram audit fails; domain review required |
| panel collision, clipped text, font fallback or low contrast | render audit fails; source remains editable for repair |
| raster image presented as editable PPTX/SVG | fail editability contract; label draft only |
| K-Dense default image/PDF route | record conditional/non-editable route; do not pass PPTX gate |
| conditional PowerPoint route | qualify with real runtime/output test before acceptance |
| confidential source or denied egress | no provider/image route; use approved local/native path or stop |
| third-party asset has unclear rights | exclude from distributable package; retain notice/pending |
| venue policy missing or stale | `HUMAN_REVIEW_REQUIRED`; no compliance claim |
| chart/diagram/artwork requested together | separate contracts/statuses; no type leakage |
| source changes after successful QA | stale QA; rerun affected checks before handoff |
| cheap image-only route proposed for editable request | reject substitution; ask budget/format decision without claiming completion |

Planned checks include source-to-mark mapping, deterministic SVG/PPTX inspection,
two-viewer render comparison, accessibility review and human scientific review.
No slide, figure or visual test is passed by this planning turn.

## Risk, security and rollback

| Risk (likelihood × impact) | Mitigation / stop condition |
|---|---|
| Scientific misrepresentation (M × H) | Source manifest, units/uncertainty, inferred flags and domain review; stop on mismatch. |
| Non-editable output mislabeled editable (M × H) | Inspect object layer and round-trip edit; fail closed on image-only result. |
| Confidential data sent to image/provider tool (M × H) | Egress allowlist, redaction/offline route and explicit permission; stop before call. |
| Asset/license or venue-policy breach (M × H) | Per-asset ledger and selected-venue policy version; reference-only until cleared. |
| Render drift across viewers (M × M) | Pin fonts/format, render comparison and source artifact retention. |
| Upstream visual worker drift (M × M) | P1 hash/receipt + P5 compatibility fixture; candidate is not accepted automatically. |

Do not log confidential raw figures or provider credentials. Do not include
`figures4papers` or Anthropic proprietary Office content without a separate
rights decision. Rollback by selecting the last accepted native route or
delivering a clearly labeled pending/non-editable artifact; never mutate source
data to make a render pass. Stop if editability, truth mapping, rights or
viewer acceptance cannot be demonstrated.

## Success criteria and next-step gate

- [ ] Every visual mark/value/arrow has a source or explicit illustrative/inferred
  flag; chart units and uncertainty survive the render.
- [ ] Requested editable format is delivered as editable native objects, or the
  result is explicitly blocked/draft with no false claim.
- [ ] Native/source and rendered inspections report no unresolved clipping,
  collision, semantic mismatch or missing provenance.
- [ ] P5 receives source artifact, preview, manifest, receipt and open gates.

P5 may start only when these are executable against real target formats and a
human/domain review path is identified; phase remains pending until then.
