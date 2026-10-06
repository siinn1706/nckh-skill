"""Keep canonical plan files honest while the frozen repair revalidation runs."""

import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
CHECKPOINT = WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-01/source-checkpoint.json"
record = json.loads(CHECKPOINT.read_text(encoding="utf8"))
assert record["source_revision"] == 36 and record["pins"] == 281
assert json.loads((RUN / "revalidation-summary.json").read_text(encoding="utf8"))["status"] == "running"
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md"]
before = {p: p.read_text(encoding="utf8") for p in targets}
assert "- [ ] Record host evidence per surface/version/event" in before[targets[1]]
images = RUN / "plan-preimages-running"
images.mkdir()
for p in targets:
    shutil.copyfile(p, images / p.name)
text = before[targets[0]]
text = text.replace('description: "R35 local delivery và native canonical patch repair verified; full native event/surface gate còn mở."',
    'description: "R36 shell-target guard frozen; latest revalidation/native retest pending, full native gate còn mở."', 1)
text = text.replace('Candidate hiện **r35**, local delivery và scoped native canonical patch repair đã có receipts; full native event/surface gate còn mở.',
    'Candidate hiện **r36**, shell-target guard đã frozen và focused checks đạt; full revalidation/native retest đang pending. R35 local delivery và scoped native canonical patch receipts được giữ là historical evidence; full native event/surface gate còn mở.', 1)
text = text.replace('bind current **r35/281 pins**', 'bind retained **r35/281 pins**', 1)
text = text.replace('Latest source repair placeholder', 'Latest source repair placeholder')
paragraph = ('\n## Current repair — r36 shell targets\n\n'
    '[R35 shell failure](../reports/delivery-261005-1042-r35-shell-target-failure.md) / '
    '[bindings](../reports/delivery-261005-1042-r35-shell-target-failure.json) verify actual private synthetic marker creation '
    'through Bash command-only payload with allow policy. [Reviewed repair](../reports/review-261005-1050-shell-target-guard.md) '
    'makes mapped shell routes pending when target coverage is unverifiable, without arbitrary shell parsing. '
    '[Frozen r36 checkpoint](../runs/nckh-native-261005-1050-r36-shell-guard-attempt-01/source-checkpoint.json) '
    'has281 pins/hash `' + record['source_lock_hash'] + '`; three pins changed (policy, adapter regressions, installation docs). '
    'Before repair21 subcase failures retained; after repair20 focused tests passed. '
    '[Current pipeline](../runs/nckh-native-261005-1050-r36-shell-guard-attempt-02/revalidation-summary.json) '
    'runs full deterministic/build/extract/smoke/previews/preservation with no overall deadline; current native retest pending. '
    'Earlier setup failure happened before any suite child start and is preserved separately. '
    'R35 metrics and scoped native passes remain revision-bound; owner samples bind r29 and installed r25 is unchanged.\n')
needle = '\n## Current candidate và retained acceptance\n'
assert needle in text
targets[0].write_text(text.replace(needle, paragraph + needle, 1), encoding="utf8", newline="\n")
targets[1].write_text(before[targets[1]] + paragraph + '\nSource repair does not close the native checkbox. Native shell targets and current direct file controls require retest against r36 payload; r35 source failures remain historical.\n', encoding="utf8", newline="\n")
targets[2].write_text(before[targets[2]] + paragraph + '\nP4 twelve checked items retain historical completion; latest r36 full delivery is pending until its own pipeline and native retest finish. No r35 result is regraded as r36.\n', encoding="utf8", newline="\n")
print(json.dumps({"status": "recorded-running-r36-checkpoint", "native_checkbox": "unchecked", "progress": "44/45"}))
