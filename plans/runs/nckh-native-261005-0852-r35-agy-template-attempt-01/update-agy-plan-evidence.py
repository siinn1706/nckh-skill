"""Append verified AGY evidence with protected plan preimages."""

import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261005-0838-r35-agy-tools.json"
record = json.loads(REPORT.read_text(encoding="utf8"))
assert record["native_turns"] == 9 and record["full_native_gate"] == "unchecked"
assert record["classifications"] == {"native-write-completed": 2,
    "native-policy-denial-before-requested-write": 2, "native-cli-tool-unavailable-prevention-unverified": 3,
    "no-native-tool-attempt-prevention-unverified": 2}
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md"]
text = {path: path.read_text(encoding="utf8") for path in targets}
assert "- [ ] Record host evidence per surface/version/event" in text[targets[1]]
preimages = RUN / "plan-preimages-agy"
preimages.mkdir()
for path in targets:
    shutil.copyfile(path, preimages / path.name)
paragraph = '[AGY r35 tool/template addendum](../reports/delivery-261005-0838-r35-agy-tools.md) / [bindings](../reports/delivery-261005-0838-r35-agy-tools.json) ghi 9 native turns: replace public/private và two direct template5s write controls đúng expected outcome; three native unknown-tool và two no-tool turns giữ unverified prevention. Four cleanups gỡ104 matching members và final process audits zero matching; source r35 giữ nguyên.'
needle = '\n| Check | Retained completed r34 result |'
assert needle in text[targets[0]]
targets[0].write_text(text[targets[0]].replace(needle, '\n' + paragraph + '\n' + needle, 1), encoding="utf8", newline="\n")
targets[1].write_text(text[targets[1]] + '\n## Current continuation — r35 AGY tools và direct template controls\n\n' + paragraph + '\n\nActual TargetFile fields/hash bindings xác nhận replace allow/private denial và write allow/plan-only denial. Direct write controls dùng packaged runner/template5s, không observer/injection; không suy timing parity cho other routes. Unknown-tool responses ở multi_replace_file_content/list_dir/find_by_name đều trước PreToolUse; list_dir private và grep_search public không gọi tool, không prevention evidence. Raw running summaries và assertion failures giữ nguyên cùng terminal reconciliation. Four cleanups và protected global hashes đã verified; full native checkbox vẫn unchecked, AGY IDE chưa có direct receipts.\n', encoding="utf8", newline="\n")
targets[2].write_text(text[targets[2]] + '\n## Additional evidence — r35 AGY observations\n\n' + paragraph + '\n\nP4 giữ12/12 và source/local delivery không đổi; owner acceptance chỉ bind đúng hai r29 VI/EN samples. AGY direct write timing controls không thay full P3 event/version/surface qualification, artifact QA hoặc scientific/stable/release acceptance.\n', encoding="utf8", newline="\n")
print(json.dumps({"status": "updated-agy-plan-evidence", "native_checkbox": "unchecked", "progress": "44/45"}))
