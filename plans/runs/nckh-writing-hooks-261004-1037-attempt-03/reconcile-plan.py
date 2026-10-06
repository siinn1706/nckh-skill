import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[2]
PLAN = PROJECT / "plans/261004-0047-nckh-research-data-hooks-writing"
BACKUP = RUN / "plan-preimages"
if BACKUP.exists():
    raise RuntimeError("Preserve existing plan reconciliation preimages")
assert (RUN / "final-preservation.json").is_file()
assert (PROJECT / "plans/reports/delivery-261004-1037-r29-local-candidate.json").is_file()
BACKUP.mkdir()
for path in PLAN.glob("*.md"):
    (BACKUP / path.name).write_bytes(path.read_bytes())

for path in sorted(PLAN.glob("phase-*.md")):
    text = path.read_text(encoding="utf8")
    number = int(path.name.split("-")[1])
    text = text.replace("status: pending", "status: completed" if number < 3 else "status: in-progress", 1)
    if number == 1:
        text = text.replace("flag chỉ là giao diện dự kiến của skill", "flag là giao diện của skill")
        text = text.replace("Các test này chưa tồn tại và không chạy ở lượt lập plan.",
            "Các test đã có trong candidate và được chạy ở lượt cook; native/human gates vẫn riêng.")
    if number in (3, 4):
        keep = ("- [ ] Record host evidence",) if number == 3 else (
            "- [ ] Personal-use owner", "- [ ] Collect personal-use owner feedback")
        text = "\n".join(line.replace("- [ ]", "- [x]", 1)
            if line.startswith("- [ ]") and not line.startswith(keep) else line for line in text.splitlines()) + "\n"
    if number == 3:
        text = text.replace("Tên file/CLI mới là contract dự kiến, chưa tồn tại.",
            "CLI/schema/codecs đã có; full deterministic và extracted checks được ghi ở checkpoint bên dưới.")
        text = text.replace("Package closure implementation đã khai báo đủ và chờ P4 freeze/build/extracted verification; chưa coi là packaged PASS ở P3.",
            "Package closure r29 đã build/extract và gọi entrypoints từ outside CWD; evidence class là local portability observation.")
        text += "\n## Execution checkpoint — r29\n\n[Full deterministic](../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic.json) đạt 181 tests, một Windows symlink skip. [Extracted smoke](../runs/nckh-writing-hooks-261004-1037-attempt-03/smoke-summary.json) kiểm 24 primary/reference projections cho runner/manual/config preview, với disposable project bytes giữ nguyên. [Delivery](../reports/delivery-261004-1037-r29-local-candidate.md) ghi exact closure, config transaction tests/recovery và limits. Native event/version/surface failure-path evidence còn unchecked: official schema và codec fixture không thay actual host response; registration/activation/trust vẫn cần grant riêng.\n"
    if number == 4:
        text = text.replace("Plan execution vẫn pending dù review+plan đã được duyệt; triển khai/native/trust cần lệnh riêng.",
            "Technical execution r29 đã hoàn tất theo cook grant; native/trust và owner feedback vẫn cần grant/evidence riêng.")
        text += "\n## Execution checkpoint — r29\n\n[Delivery record](../reports/delivery-261004-1037-r29-local-candidate.md): 281 pins, 181 deterministic tests (`OK`, một symlink skip), 16 persistent ZIP/extracted bundles, 216 resource reads, 48 writer disabled/no-read observations, 24 hook projections và 8 installer previews (39 skills + 6 agents). [Preservation](../runs/nckh-writing-hooks-261004-1037-attempt-03/final-preservation.json) giữ 509 protected hashes và installed r25; bốn legacy schema-v1 bundles vẫn verify được. r27/r28 failures và source-lock history được giữ; [r29 delta review](../reports/review-261004-1037-r29-source.md) riêng với snapshot review trước freeze. Hai owner-feedback checkboxes chưa có evidence nên giữ unchecked. Supplemental writer matrix 256/20 và historical 224 cells vẫn không có native pass được tạo bởi local checks.\n"
    path.write_text(text, encoding="utf8")

source_map = PLAN / "source-adoption-map.md"
text = source_map.read_text(encoding="utf8")
first = text.splitlines()[2]
text = text.replace(first,
    "Ngày/as-of: 04/10/2026, Asia/Saigon. Map đã được thực thi trong candidate r29: 39 identities, 9 resources và 281 pins. [Starting r26 baseline](../reports/checks-261004-1037-starting-baseline.json) giữ lịch sử 243 pins; [delivery r29](../reports/delivery-261004-1037-r29-local-candidate.md) bind actual package/read/preview receipts. Hash xác nhận bytes/closure/access, không chứng minh upstream-current, semantic validity, human acceptance hoặc release quyền rộng hơn.")
text = text.replace("Artifact dự kiến", "Artifact/checkpoint")
text = text.replace("NEW candidate, bounded adaptation", "IMPLEMENTED, bounded adaptation")
text = text.replace("NEW candidate, selective reference", "IMPLEMENTED, selective reference")
text = text.replace("exact selected file/hash must be frozen before use", "exact selected file/hash recorded in the Xia source ledger")
text = text.replace("Đây là **target additive**, không mô tả current source đã có writer mới.",
    "Đây là **mapping additive đã triển khai**; consumer cũ vẫn nguyên vẹn và mỗi writer mới có ba required resource bindings.")
text = text.replace("Hook CLI mới có owner/contract P3, không được coi đang callable.",
    "Hook CLI của P3 đã callable cục bộ từ extracted package; không đồng nghĩa host registered/enabled/trusted/native-verified.")
text += "\n## Execution evidence — r29\n\n[Selected K-Dense paths/hashes/license và official schemas](../reports/researcher-261004-1037-hook-schemas-visual-source.md) là Xia comparison record; không copy whole skill hoặc restricted ClaudeKit/document resources. [Delivery](../reports/delivery-261004-1037-r29-local-candidate.md) kiểm 216 packaged resource reads và 48 direct writer disabled/no-read observations, cùng 16 archive chains. Humanizer linked Markdown và scientific visual QA nằm trong verified skill closure, không tăng resource registry lên 10. LanguageTool tiếp tục deferred; không install Java/service hoặc gọi public server. Source hash/lookup/closure không đóng scientific, human hoặc release rights gates.\n"
source_map.write_text(text, encoding="utf8")

index = """---
title: "NCKH research-first writing, visuals và hooks"
description: "Candidate r29 đã triển khai và kiểm chứng cục bộ; native/owner/scientific gates giữ riêng."
status: in-progress
priority: P1
effort: 4 phases / 5-8 ngày công
branch: unverified-no-git-worktree
tags: [nckh, research, writing, visuals, hooks, provenance]
created: 2026-10-04
---

# NCKH research-first writing, visuals và hooks

## Outcome và quyền thực thi

Candidate r29 gồm hai writer theo nhiệm vụ, scientific-purpose visual guard và portable deterministic hooks. Lệnh `/goal ak-cook plan.md --auto` ngày 04/10/2026 cấp quyền implementation, tests/build/extract/local checks và previews. Installation đang dùng r25, native registration/trust/activation và human/scientific/release acceptance có gate riêng. [Starting baseline](../reports/checks-261004-1037-starting-baseline.json) giữ r26/243 pins, 37 identities, 148 case IDs, 9 resources và installed r25/43 items.

## Quyết định và contract

Hai identity `nckh-humanwrite` và `nckh-paperwrite`, mỗi skill dùng `--en`/`--vi`; không tạo bốn locale identities. Current catalog đúng 39 = 37 cũ + hai writer, 156 base cases, 19 families và 9 resources. `nckh-write` giữ compatibility theo action; `nckh-taste` là critic. Output locale độc lập resource locale theo [language decision](../reports/decision-261004-0047-writer-language-options.md). Giữ 148 old IDs, historical 224 matrix/comparator/receipts; current visual prompt bytes đổi không được dùng receipt cũ để regrade.

Visual workflow chỉ nhận research purpose với source/mark/origin rõ; computed/simulation cần source/code/transform/output/run bindings và nhãn. Humanizer là owned linked Markdown policy, không detector/evasion hoặc fabricated anecdotes; LanguageTool vẫn optional/deferred English diagnostic. Hooks bounded, không payload shell/network/provider/nested LLM/full-transcript ingestion; manual/config transactions riêng, inactive mặc định. Purpose/hash/fixture pass không certify scientific truth hoặc native prevention.

## Phases và dependencies

| Phase | Kết quả/evidence | Phụ thuộc và owner |
|---|---|---|
| [P1 Writers](./phase-01-start.md) | 13/13 checkboxes; hai writer, locale/preservation/router, exact membership, source consumers và supplemental matrix | Language decision; catalog/writer/profile/eval owners |
| [P2 Scientific visuals](./phase-02-scientific-visuals.md) | 9/9 checkboxes; purpose/origin/mark guards, real local calculation và selective QA | P1 contract; guards/visual contracts/cases/instruction owners |
| [P3 Portable hooks](./phase-03-portable-hooks.md) | 10/11 checkboxes; policy/codecs/closure/config lifecycle và local extracted observations; native evidence còn mở | P2 + official schema ledger; hook/config/build owners |
| [P4 Integration](./phase-04-integration-and-personal-acceptance.md) | 10/12 checkboxes; r29 freeze/deterministic/build/extract/smoke/previews; hai owner-feedback items còn mở | P1–P3; single freeze owner `/root`, preservation và acceptance lanes |

## Technical checkpoint

[Delivery report và 16 archive links](../reports/delivery-261004-1037-r29-local-candidate.md) / [structured evidence](../reports/delivery-261004-1037-r29-local-candidate.json).

| Kiểm tra thực | Kết quả |
|---|---|
| Static/current source | r29, 281 pins, exact 39/156/19; writer matrix 256 planned native cells + 20 scenarios, unverified |
| Full deterministic | 181 tests, `OK (skipped=1)`; real-symlink fixture bị giới hạn quyền Windows |
| Packaging | 4 reproducibility variants; 16 persistent bundles đã nén/giải nén ngoài source và verify |
| Extracted behavior | 216 resource reads, 48 writer disabled/no-read observations, 24 primary/reference hook projections |
| Installer previews | 8 surfaces, mỗi preview 39 skills + 6 agents, disposable projects không đổi bytes |
| Preservation | 509 protected hashes không đổi; installed r25 chưa update; 4 legacy schema-v1 bundles verify được |

## Open gates, risk và rollback

Plan giữ **in-progress, 42/45 checkboxes**. Một task native host/version/surface/event evidence và hai owner-feedback items còn unchecked. Registration/trust/activation, update installation, stable/scientific/rights/reviewer/holdout/economics vẫn cần authority/evidence tương ứng. Four-case [independent writer trial](../reports/reviewer-261004-1037-writer-forward-test.md) là local agent evidence; không human gold, native pass hoặc scientific acceptance. Resource access ON giữ public contract, OFF chỉ là internal comparison; r29 chưa publish.

Critical risks: source rights/claim inflation; native uncovered/fail-open routes; config/user-byte conflicts. Giữ manual/unverified coverage, no-copy với restricted sources, separate transactions, preimages/postimage hashes và rollback/recover chỉ trên owned matching bytes; edited/shared user files được preserve. Chi tiết ở phase files và [source→reader→artifact→test map](./source-adoption-map.md).

## Review và validation history

User đã duyệt A1–A9; [red-team adjudication](../reports/red-team-261004-0047-adjudication.md) giữ 9 Accept/3 Reject và [plan amendments](../reports/validation-261004-1002-approved-plan-amendments.md) giữ historical 45 tasks/0 done. [Pre-freeze review](../reports/review-261004-1037-pre-freeze.md) là snapshot r27; [r29 delta review](../reports/review-261004-1037-r29-source.md) và [Xia source/schema ledger](../reports/researcher-261004-1037-hook-schemas-visual-source.md) giữ evidence mới riêng. r27/r28 failures, pre-freeze drift refusal và later passing receipts đều giữ trong [delivery history](../reports/delivery-261004-1037-r29-local-candidate.md).

Final reconciliation dùng validate/parse/reindex và link checks; [receipts](../runs/nckh-writing-hooks-261004-1037-attempt-03/) có log/JSON riêng. Những checks đó xác nhận cấu trúc/state/links; technical behavior theo actual run receipts ở trên, còn native/human/scientific gate không được đóng bằng parser/hash.

<!-- slug: nckh-research-data-hooks-writing -->
"""
(PLAN / "plan.md").write_text(index, encoding="utf8")
tasks = [line for path in PLAN.glob("phase-*.md") for line in path.read_text(encoding="utf8").splitlines()
    if re.match(r"^- \[[ x]\]", line)]
assert len(tasks) == 45 and sum(line.startswith("- [x]") for line in tasks) == 42
print("Reconciled plan: 42/45; three native/owner gates remain unchecked")
