"""Append verified evidence, back up the index, then reconcile plan and journal."""

import importlib.util
import json
import os
import re
import shutil
import sqlite3
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORTS = ["delivery-261005-0905-r35-cursor-template-controls",
    "delivery-261005-1021-r35-cursor-timing-diagnostic", "delivery-261005-1021-r35-codex-template-controls"]
records = [json.loads((WORK / "plans/reports" / (name + ".json")).read_text(encoding="utf8")) for name in REPORTS]
assert all(r["source_revision"] == 35 and r["full_native_gate"] == "unchecked" for r in records)
assert [r["native_turns"] for r in records] == [4, 1, 3]
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md"]
before = {p: p.read_text(encoding="utf8") for p in targets}
assert "- [ ] Record host evidence per surface/version/event" in before[targets[1]]
assert not (RUN / "plan-reconciliation.json").exists()
preimages = RUN / "plan-preimages"
preimages.mkdir()
for path in targets:
    shutil.copyfile(path, preimages / path.name)
paragraph = ('[Cursor direct template controls](../reports/delivery-261005-0905-r35-cursor-template-controls.md) '
    'bind four genuine timeout5s failures; collector sửa đúng `errorMessage`, giữ failed preimage/raw evidence. '
    '[Immediate timing diagnostic](../reports/delivery-261005-1021-r35-cursor-timing-diagnostic.md) '
    'flush allow3.076ms và Python atexit3.695ms nhưng native vẫn timeout5s, không gọi policy/runner; exact host cause unresolved. '
    '[Codex direct template5s](../reports/delivery-261005-1021-r35-codex-template-controls.md) '
    'xác minh three canonical add-file allow/plan-only/private controls với actual native denial, không observer/injection. '
    'Các batches đã cleanup và final audits zero matching; source r35 không đổi.')
needle = '\n| Check | Retained completed r34 result |'
assert needle in before[targets[0]]
targets[0].write_text(before[targets[0]].replace(needle, '\n' + paragraph + '\n' + needle, 1), encoding="utf8", newline="\n")
detail = ('\n\nCursor four direct failures không thay bằng production PASS; diagnostic riêng chỉ loại giả thuyết policy runtime là nguyên nhân duy nhất. '
    'Codex direct template5s đạt expected outcome cho ba canonical add-file turns; pre-delivery QA vẫn pending. '
    'Không có callback telemetry từ direct Codex runner nên model/effort là requested command binding. '
    'AGY app access đã human-approved và user báo unlocked; fresh capture vẫn hiển thị lock screen, không UI input/hook registration. '
    'Full native checkbox giữ unchecked; remaining routes/surfaces và Claude model/effort grant còn mở.\n')
targets[1].write_text(before[targets[1]] + '\n## Current continuation — direct template timing controls\n\n' + paragraph + detail,
    encoding="utf8", newline="\n")
targets[2].write_text(before[targets[2]] + '\n## Additional evidence — direct template timing controls\n\n' + paragraph
    + '\n\nP4 giữ12/12; owner sample acceptance, installed r25 và scientific/stable/release lanes giữ riêng. P3 full native task chưa complete.\n',
    encoding="utf8", newline="\n")
spec = importlib.util.spec_from_file_location("native_plan_command_helper", WORK / "plans/runs/nckh-native-261004-1707-attempt-01/qualification-run.py")
commands = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands)
commands.RUN = RUN
env = os.environ.copy()
env["AGENTKIT_HOME"] = str(WORK / "plans/.agentkit-runtime")
AK = r"C:/Users/USER\bin\ak.exe"
backup = RUN / "before-checkpoint-reindex.sqlite"
assert not backup.exists()
database = WORK / "plans/.agentkit-runtime/plans/plans.db"
with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
    source.backup(target)


def invoke(name, argv, body=b""):
    outcome, stdout, stderr = commands.run_command("checkpoint-" + name, argv, cwd=WORK, timeout=60, env=env, stdin=body)
    assert outcome["exit_code"] == 0, (name, stderr.decode("utf8"))
    return json.loads(stdout.decode("utf8"))


invoke("validate", [AK, "plan", "validate", str(PLAN), "--json"])
invoke("parse", [AK, "plan", "parse", str(PLAN), "--json"])
invoke("reindex", [AK, "plan", "reindex", "--apply", "--path", str(WORK), "--json"])
phases = invoke("show", [AK, "plan", "show", "test-skill/261004-0047", "--json"])["data"]["phases"]
evidence = ["plans/reports/" + name + suffix for name in REPORTS for suffix in (".md", ".json")]
for number in (3, 4):
    phase = phases[number - 1]
    notes = (phase.get("notes") or "") + ('\nVerified continuation: Cursor4 template5s failures; immediate diagnostic timeout despite flushed allow and atexit under5ms; Codex3 direct template5s add-file controls with native denial. Source r35 unchanged; full native gate unchecked. AGY access granted; fresh capture still lock screen, no app input.')
    joined = (phase.get("evidence") or "") + "; " + "; ".join(evidence)
    invoke("phase-" + str(number), [AK, "plan", "phase", "update", "test-skill/261004-0047", str(number),
        "--evidence", joined, "--notes", notes, "--json"])
body = '''## Kết quả

Cursor4 direct template5s controls giữ native timeout failures. Collector bỏ sót error.errorMessage ở Read; failed preimage và raw native summary được bảo toàn trước repair. Verifier corrected đạt và bind toàn bộ four timeouts. Immediate Python callback trả allow trong3.076ms và atexit3.695ms nhưng host vẫn timeout5s, không NCKH policy/runner. Exact host transport/execution cause vẫn unresolved.

Codex3 direct packaged template5s canonical add-file turns đạt public allow, plan-only denial và private denial; actual native stderr/marker oracles đã verified. Pre-delivery artifact QA ở allow còn pending. Cleanup và final audits completed, source r35/281 pins và global protected hashes unchanged.

## Còn mở

AGY access approved và human báo unlocked; fresh capture tiếp tục lock screen. Không UI input. Plan in-progress44/45, full native checkbox unchecked; remaining tools/surfaces và Claude model/effort grant còn mở. Owner accepted đúng r29 VI/EN samples, installed r25 và scientific/stable/release gates giữ riêng. AgentWiki publish skipped.
'''
invoke("journal-create", [AK, "journal", "create", "NCKH r35 direct template timing controls",
    "--summary", "Verified Cursor timeout diagnostic and Codex direct template controls; native gate open",
    "--stdin", "--date", "2026-10-05", "--json"], body.encode("utf8"))
journal = WORK / "plans/journals/2026-10-05-nckh-r35-direct-template-timing-controls.md"
assert journal.is_file()
invoke("journal-validate", [AK, "journal", "validate", str(journal), "--json"])
status = invoke("status", [AK, "plan", "status", str(PLAN), "--json"])["data"]
assert (status["done_tasks"], status["total_tasks"], status["phases_done"]) == (44, 45, 3)
docs = [*targets, *(WORK / p for p in evidence if p.endswith(".md")), journal]
links = []
for path in docs:
    for reference in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("http://", "https://", "#")):
            continue
        assert (path.parent / reference.split("#", 1)[0]).exists(), (path, reference)
        links.append({"document": path.relative_to(WORK).as_posix(), "target": reference})
record = {"status": "pass", "evidence_class": "structure-state-links-only", "progress": status,
    "native_checkbox": "unchecked", "sqlite_preimage": str(backup.relative_to(WORK)),
    "sqlite_preimage_sha256": commands.sha(backup.read_bytes()), "local_links_checked": len(links), "links": links,
    "journal": str(journal.relative_to(WORK)), "AgentWiki_publish": "skipped",
    "documents": {str(p.relative_to(WORK)): commands.sha(p.read_bytes()) for p in docs}}
with (RUN / "plan-reconciliation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": "pass", "done": 44, "total": 45, "links_checked": len(links)}))
