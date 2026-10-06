"""Reconcile the executed plan with retained evidence, leaving human/run gates open."""

import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent
PLAN = PROJECT / "plans/261002-0832-nckh-skill-resource-quality"
lock = json.loads((PROJECT / "nckh-kit/core/registry/source-lock/source-lock.json").read_text(encoding="utf-8"))
revision = lock["revision"]


def passed(name):
    path = EVIDENCE / name
    return path.is_file() and json.loads(path.read_text(encoding="utf-8")).get("status") == "pass"


technical = all(passed("verification-" + group + "-r" + revision + ".json") for group in ["deterministic", "reproducibility", "artifacts"])
smoke = passed("extracted-smoke-r" + revision + ".json")
matched_path = EVIDENCE / "matched-integrity.json"
matched = ((EVIDENCE / "matched-manifest.json").is_file() and matched_path.is_file()
           and json.loads(matched_path.read_text(encoding="utf-8")).get("integrity") == "pass")
index = '''---
title: "NCKH skill resource quality — thực thi chọn lọc"
description: "Tài nguyên có consumer cho 37 identities; integrity, lịch sử và qualification được ghi riêng."
status: in-progress
priority: P1
effort: "8–14 ngày công; chưa gồm thời gian chờ corpus, reviewer và runtime gates"
branch: "none (workspace không có Git repository)"
tags: [nckh, resources, provenance, evaluation, portability]
created: 2026-10-02
---

# NCKH skill resource quality

## Outcome và boundary

Thực thi theo `/goal ak-codex-goal ak-cook plan.md --auto` ngày 2026-10-02. Giữ đúng **37 identities / 148 package cases / 19 required families / 224 native cells**. Markdown là mặc định; bốn snapshot có reader, provenance và license riêng đã qua staging/promotion. Các identity khác giữ MD-only. Không tạo corpus tổng hợp mới; VI/EN corpus và chart measurements thật còn `blocked-input`.

Source revision 18 và installed revision 14 là baseline lịch sử bất biến. Revision mới không kế thừa verdict cũ. [Initial freeze](../evaluation/resource-quality/initial-freeze.json), [evaluator freeze](../evaluation/resource-quality/evaluator-freeze.json), [direct linkage](../evaluation/resource-quality/direct-linkage.json) và [promotion receipt](../evaluation/resource-quality/promotion-receipt.json) ghi từng lane. Một answer round-1 của `nckh-cook` thiếu, linkage vẫn pending. Rollback phải khớp source + schema + lock.

## Phases và dependency

| # | Phase | Depends on | Trạng thái / chi tiết |
|---|---|---|---|
| 1 | Test/provenance freeze | Không | Evaluator/linkage/guards đã triển khai; [phase 1](./phase-01-start.md) |
| 2 | Chọn, review và stage resources | P1 freeze | 4 resources, 3 nguồn, quyết định đủ 37 identities; [phase 2](./phase-02-domain-resources.md) |
| 3 | Format/rights/closure, promote, build | P2 packet → P3 support → P1 freeze | PHASE3_STATE; [phase 3](./phase-03-resource-packaging.md) |
| 4 | Matched comparison và qualification | P1–P3; inputs/human/runtime grants | Checker đã có; behavioral/human run còn pending; [phase 4](./phase-04-behavioral-qualification.md) |

## Ownership và quyết định

- [Resource map](./resource-map.md) ghi đủ 37 identities và disposition; một registry cho bốn resources, không tạo 37 manifest.
- P2 content → P3 support → P1 freeze đã theo đúng thứ tự. Staging, thất bại kỹ thuật và lịch sử được giữ để review.
- Người dùng chọn **mở rộng CRO để kiểm tra canonical/noindex**; [scope amendment](../evaluation/resource-quality/cro-scope-amendment.json) giữ failure lịch sử. Broader crawl/search analysis vẫn theo SEO.
- Package/native/human/provider/OS/release là các gate riêng. Protected holdout vẫn `pending/NOT_CALLABLE`, current runner development-only; không có tổng deadline 15 phút hay route mới cho case quá 900 giây.

## Measurable acceptance

- [x] Resources có consumer, artifact, source/version/hash, rights, read checks và rollback; đủ 37 disposition.
- [x] Không thêm synthetic dataset; bytes gốc và per-record provenance được giữ, không manufacture missing records hay mix namespaces.
- [TECH] Candidate/extracted smoke và full deterministic suite có receipt khớp revision cuối; private/unpinned/uncleared data bị chặn.
- [ ] Sáu condition được pin đầy đủ khi có subject/run thật; same-base off/on giữ wrapper/model/budget. Preparation không chứng minh resource benefit; revision 14 migration riêng.
- [ ] Actual corpus/rights/reviewer/threshold/host/model/budget và các gate native/human được duyệt, chạy và review. Stable/public còn **NO-GO**.

## Đầu vào còn thiếu

Corpus VI/EN và phép sử dụng; reviewer cho taste/fidelity/domain/visuals; threshold và coverage; host/OS/model; provider/process budget và economics. Upstream baseline cần skill subject thật được pin và route có phép. Không cấp thêm development round hoặc dựng gold từ model.

## Historical plan review

[Skill review](../reports/review-261002-0832-nckh-skill-quality.md), [shortlist](../reports/researcher-261002-0832-source-shortlist.md), [runtime audit](../reports/code-reviewer-261002-0832-nckh-runtime-evals.md) và [red-team review](../reports/red-team-261002-0832-nckh-resource-plan.md) là hồ sơ trước thực thi. Bảy Accept R1/R2/R4/R5/R6/R7/R10 đã được áp dụng ở mức plan; R3/R8/R9 giữ Reject. Hai review độc lập và một self-audit không được gọi là ba review độc lập. [Validation trước thực thi](../reports/validation-261002-0832-nckh-resource-plan.md) chỉ chứng minh integrity của plan cũ.

<!-- slug: nckh-skill-resource-quality -->
'''
index = index.replace("PHASE3_STATE", "Hoàn tất kỹ thuật trên revision " + revision if technical and smoke else "Đang hoàn tất kiểm tra candidate revision " + revision)
index = index.replace("[TECH]", "[x]" if technical and smoke else "[ ]")
(PLAN / "plan.md").write_text(index, encoding="utf-8", newline="\n")

for number, name in [(1, "start"), (2, "domain-resources"), (3, "resource-packaging"), (4, "behavioral-qualification")]:
    path = PLAN / f"phase-{number:02}-{name}.md"
    text = path.read_text(encoding="utf-8")
    state = "completed" if number in {1, 2} or number == 3 and technical and smoke else "in-progress"
    text = re.sub(r"^status: .+$", "status: " + state, text, count=1, flags=re.M)
    text = re.sub(r"<!-- Updated: approved red-team (.*?); plan only -->", r"<!-- Historical plan amendments: \1; execution authorized 2026-10-02 -->", text)
    text = text.replace("## File ownership (implementation later)", "## File ownership")
    if number == 1:
        text = text.replace("Lượt hiện tại chỉ author/review plan. Khi có yêu cầu thực thi riêng, P1 được sửa đúng source/contracts/tests bên dưới và freeze candidate tương ứng; không chạy provider/native/human, không cài skill và không đổi `not-run` thành pass.", "P1 đã triển khai evaluator/schema/holdout guards, lưu baseline 18 và evaluator freeze 19, tạo direct linkage riêng. Source candidate có revision mới; không chạy provider/native/human, cài skill hay đổi package `not-run` thành pass.")
        text = text.replace("## Evidence đã re-check", "## Evidence trước thực thi và runtime audit")
        text = text.replace("- [ ]", "- [x]")
    elif number == 2:
        text = text.replace("Chưa resource nào được phép import; per-file rights, consumer smoke và release disposition vẫn pending.", "Đã review selected-file ancestry/license/NOTICE, stage bốn snapshot và chạy consumer thật; promotion sau P3 support. Release và semantic/human applicability vẫn pending.")
        text = text.replace("## Proposed resource families (not all mandatory)", "## Resource families đã cân nhắc (không bắt buộc)")
        text = text.replace("Trong P2, mọi candidate edit nằm dưới staging được duyệt **ngoài pinned source/dist**, đề xuất `plans/evaluation/resource-quality/staging/`. Bảng dưới ghi owner và đích tương lai, không cho phép ghi ngay vào các đích đó. Chỉ sau P3 support/regressions, content owner mới promote nội dung đã duyệt và giao P1 freeze. Raw traces/holdout không nằm trong staging này.", "P2 đã stage dưới `plans/evaluation/resource-quality/staging/` ngoài pinned source/dist. Sau P3 support/regressions, content owner promote đúng bytes trong promotion receipt và giao P1 freeze. Bảng giữ trách nhiệm từng owner; raw traces/holdout không nằm trong staging này.")
        text = text.replace("Keep SEO canonical/index and CRO conversion-friction ownership separate; no automatic source/oracle edit.", "User selected CRO canonical/noindex inspection; broader SEO remains separate, and historical failure/oracle is preserved.")
        text = text.replace("**ĐỀ XUẤT**, chưa tồn tại: `python -m unittest tests.resource.test_consumers tests.resource.test_provenance` and `python scripts/search-resource.py --resource-id ID --query TEXT --json`; these are required only for a selected lookup resource.", "Implemented: `python -m unittest tests.resource.test_consumers tests.resource.test_closure`; reader requires `--resource-id ID --consumer SKILL --domain DOMAIN --genre GENRE --query TEXT --json` and resource-specific context. Per-file rights/hash regressions live in `test_closure`; no separate nonexistent `test_provenance` module is required.")
        text = text.replace("Keep the hash-bound CRO fail and add a separate SEO/handoff case only after user decision; never rewrite history.", "Keep the hash-bound CRO fail; the owner selected canonical/noindex inspection and a separate scope amendment. Never rewrite history.")
        text = text.replace("- [ ]", "- [x]")
    elif number == 3:
        text = text.replace("Hiện `build.py` chỉ nhận suffix giới hạn và lần theo Markdown links; target là resource đọc được từ extracted package độc lập với repository CWD/PYTHONPATH. Lượt hiện tại chỉ sửa plan.", "Build/bundle format 2 đã hỗ trợ registry/rights/explicit closure; format 1 local-only vẫn đọc đúng nghĩa lịch sử. Resource-off giữ reader/registry chung, bỏ copied bytes. Candidate và extracted checks có receipt riêng, không kế thừa lịch sử.")
        text = text.replace("## Verified current behavior", "## Baseline revision 18 trước thay đổi")
        text = text.replace("**ĐỀ XUẤT**, chưa tồn tại: `python -I scripts/resource-smoke.py --bundle EXTRACTED --cwd OUTSIDE_REPO --unset-pythonpath` and `python -m unittest tests.resource.test_closure tests.resource.test_extracted_smoke`; future script must emit resource-read evidence and preserve failed receipts.", "Implemented: `python -I scripts/resource-smoke.py --bundle EXTRACTED --cwd OUTSIDE_REPO --unset-pythonpath --output RECEIPT` and `python -m unittest tests.resource.test_closure tests.resource.test_extracted_smoke`; actual relocated reader runs with isolation and retained read hashes. Failed revision 21 and corrective freeze remain separate records.")
        if technical and smoke:
            text = text.replace("- [ ]", "- [x]")
    else:
        text = text.replace("Mọi provider/native run vẫn cần authority riêng; lượt này chỉ sửa plan.", "Preparation/checker đã được triển khai trong lượt cook; provider/native/human run chờ inputs và authority cho cấu hình thực tế.")
        text = text.replace("Preserve CRO `nckh-cro:positive` failure and hash-bound answer/native/trace match. `nckh-seo` owns canonical/index (`nckh-kit/skills/marketing/nckh-seo/SKILL.md:27-35`); require an explicit user decision before changing CRO scope or adding SEO handoff case.", "Preserve CRO `nckh-cro:positive` failure and hash-bound answer/native/trace match. The owner selected CRO canonical/noindex inspection; `cro-scope-amendment.json` records the decision using the original task with no historical rerun/regrade. Broader crawl/search analysis remains with SEO.")
        text = text.replace("Do not run provider/native/human in this plan turn. Future run requires actual host/OS/model/budget/right grants, compatible per-case route and independent receipt review.", "Complete actual host/OS/model/budget/right grants, compatible per-case route and independent receipt review before provider/native/human runs; these inputs remain pending.")
        text = text.replace("No real installation is authorized by this plan update.", "No real skill installation has been performed.")
        text = text.replace("Provider/native execution is **not authorized here**.", "Provider/native execution is **pending actual inputs and grants**.")
        text = text.replace("**ĐỀ XUẤT**, chưa tồn tại: `python scripts/compare-matched.py --manifest MATCHED_MANIFEST`; future tool must consume the full condition mapping, reject incomplete hashes/split/rights/reviewer/base pairing, preserve variant/pending status and emit no quality pass by itself. It is neither an existing runnable capability nor a route around timeout/holdout/grant limits.", "Implemented: `python scripts/compare-matched.py --manifest MATCHED_MANIFEST --work-context PROJECT --output RECEIPT`. It checks all six conditions, actual file-reference hashes, preserved historical rounds and within-pair base/wrapper/model/gates/config equality. Pending references stay explicit; output proves manifest integrity, with accepted count 0 and resource benefit unknown. It executes no host/provider or protected holdout.")
        lines = text.splitlines()
        requirement = 0
        for position, line in enumerate(lines):
            if line.startswith("- ["):
                requirement += 1
                complete = requirement in {4, 5, 6} or requirement == 1 and matched or requirement == 2 and technical
                lines[position] = re.sub(r"^- \[[ x]\]", "- [x]" if complete else "- [ ]", line)
        text = "\n".join(lines) + "\n"
    if "## Execution checkpoint" in text:
        text = text.split("## Execution checkpoint", 1)[0].rstrip() + "\n"
    checkpoints = {
        1: "Baseline 18/hash/snapshot được giữ. Evaluator freeze 19 khớp 46 members đã kiểm; 37 negative routes, 19 families và protocol được validate, protected helper bị chặn. Direct linkage có 158 review rows/148 IDs và giữ một answer thiếu. Candidate hiện revision " + revision + ". [Freeze](../evaluation/resource-quality/evaluator-freeze.json), [linkage](../evaluation/resource-quality/direct-linkage.json).",
        2: "Đã ghi quyết định đủ 37 identities, chọn bốn resources từ đúng ba nguồn. Source bytes/license/tree đã đọc ở pin; không clone repo hay chạy upstream code. VI/EN corpus/chart input vẫn blocked-input. [Staged packet](../evaluation/resource-quality/staged-packet.json), [source inspection](../evaluation/resource-quality/staging/source-inspection.json), [promotion](../evaluation/resource-quality/promotion-receipt.json).",
        3: "Format 2, shared verifier và installer-consumer regressions đã triển khai. Revision 21 có một off-closure failure do attribution link; snapshot và failure được giữ, sửa reader/registry closure ở revision " + revision + ". " + ("Full suite, hai lần build cho từng host/mode và extracted smoke đã pass theo receipts." if technical and smoke else "Current full suite/build/extracted receipts đang được hoàn tất.") + " Không cài skill hoặc chứng nhận native/plugin/OS.",
        4: "Matched checker và regression có thật; human queue/wrapper specifications chỉ là preparation. " + ("Manifest sáu conditions và actual references đã kiểm integrity." if matched else "Manifest sáu conditions chờ các candidate artifact receipts.") + " Không allocation round mới, không upstream subject giả, không effective model/output hash tự tạo. Actual corpus/reviewer/threshold/runtime/budget và native/human/holdout/release gates còn pending.",
    }
    text += "\n## Execution checkpoint\n\n" + checkpoints[number] + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")

path = PLAN / "resource-map.md"
previous = path.read_text(encoding="utf-8")
packet = json.loads((EVIDENCE / "promotion-receipt.json").read_text(encoding="utf-8"))
decisions = {row["identity"]: row for row in packet["identities"]}
rows = []
for match in re.finditer(r"^\| (\d+) \| `([^`]+)` \| (.*?) \| (.*?) \| (.*?) \|$", previous, re.M):
    number, identity, need, resource, acceptance = match.groups()
    decision = decisions[identity]
    selected = decision["resources"]
    resource = "promoted-local: " + ", ".join("`" + value + "`" for value in selected) if selected else "MD-only; existing references/contracts, no selected data consumer"
    if identity in {"nckh-write", "nckh-taste"}:
        resource += "; VI/EN genre corpus blocked-input"
    elif identity == "nckh-visuals":
        resource += "; actual chart measurements blocked-input"
    if identity == "nckh-cro":
        need = "conversion friction và owner-authorized canonical/noindex inspection"
        acceptance = "locate actual directives; live indexing unknown; retain historical fail and intentional directives"
    rows.append(f"| {number} | `{identity}` | {need} | {resource} | {acceptance} |")
if len(rows) != 37 or set(decisions) != {re.search(r"`([^`]+)`", row).group(1) for row in rows}:
    raise RuntimeError("resource matrix does not preserve exactly 37 approved identities")
text = '''---
title: "Resource map — 37 NCKH identities"
status: selected
---

# Resource map — 37 NCKH identities

Thực thi chọn lọc đã ghi đủ 37 disposition. Một registry chứa bốn resources với năm consumer identities; các identity khác giữ Markdown và contracts hiện hữu. `promoted-local` chỉ là trạng thái kỹ thuật sau staged support, không phải human/scientific acceptance hay stable release.

Không tạo dataset tổng hợp mới, không copy repository. Bytes gốc, license và source/hash/as-of được giữ; reader phát per-record provenance. Clinical, publisher, UI và English advice ở namespace riêng, không mix records. VI/EN prose corpus, chart measurements và human gold vẫn thiếu. Những template/glossary/log đề xuất trước đây chưa có input/consumer được chọn thì giữ MD-only.

| # | Identity | Consumer/need | Actual resource/disposition | Acceptance gate |
|---:|---|---|---|---|
'''
text += "\n".join(rows) + "\n"
text += '''
## Selected resources và consumers

| Resource | Consumer | Content/limit | Source rights |
|---|---|---|---|
| `R-reporting-lookup` | `nckh-method`, `nckh-write` | 15 clinical/health reporting entries; unmatched CS/domain returns no applicable record | K-Dense pinned MIT; unchanged source bytes |
| `R-publisher-profile` | `nckh-visuals` | 8 publisher snapshots; exact venue/year/track/article-type applicability unknown; Science historical and ACS legacy warnings retained | K-Dense pinned MIT; profile is planning reference |
| `R-ui-lookup` | `nckh-frontend` | 119 unchanged UX rows; bounded query; examples are untrusted data and never executed | UI UX Pro Max pinned MIT; UI-only |
| `R-nature-reference` | `nckh-write`, `nckh-taste` | Only manifest-routed `static/fragments/language/en.md`; optional English advice, no corpus/policy claim | Nature Skills pinned Apache-2.0 with retained license/attribution |

[Registry](../../nckh-kit/core/registry/catalog/resources.json) owns exact source paths, full commits/file hashes, license/NOTICE paths, requires, reader, expected artifacts and rollback. [Source inspection](../evaluation/resource-quality/staging/source-inspection.json) retains full tree and selected-file license evidence; [staged packet](../evaluation/resource-quality/staged-packet.json) and [promotion receipt](../evaluation/resource-quality/promotion-receipt.json) preserve the ordered P2 → P3 → P1 handoff. The earlier [shortlist](../reports/researcher-261002-0832-source-shortlist.md) remains historical research rather than a global ranking.

## Consumer và verification

`scripts/search-resource.py` is the reviewed NCKH stdlib reader, distinct from upstream readers. It checks rights/hash, consumer, domain/locale/genre and publisher context, returns source locators/read hashes and preserves unknown semantic applicability. Resource-off uses the same reader/registry with no copied bytes and returns disabled before any resource read. Shared verifier and extracted smoke inspect the candidate closure with external CWD, isolated Python and unset PYTHONPATH.

CRO canonical/noindex inspection follows the explicit owner decision in [scope amendment](../evaluation/resource-quality/cro-scope-amendment.json). Broader SEO remains separate; no historical verdict was changed. The amended task is a separate not-run record outside the unchanged 148 package identities/case IDs.

P4 preparation preserves no-skill, permitted upstream and two same-base off/on pairs for same-agent/selective delegation, with separate revision 14 migration history. A lookup, valid manifest, imported rows or successful extracted read establishes no causal benefit, human taste, scientific validity, native binding or stable release. Real samples/rights/reviewers/thresholds/host/model/budget remain required.
'''
path.write_text(text, encoding="utf-8", newline="\n")
print(json.dumps({"revision": revision, "technical_receipts_complete": technical and smoke,
                  "matched_preparation": matched, "identities": len(rows), "plan_status": "in-progress"}))
