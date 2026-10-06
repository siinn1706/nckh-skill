"""Verify supported recovery limits and preserved process identities."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
def text_result(p):
    result = read(p)
    assert not result.get("isError")
    texts = [item["text"] for item in result["content"] if item["type"] == "text"]
    assert len(texts) == 1
    return json.loads(texts[0])

before = text_result(RUN / "agy-inventory-before-launch.json")
after = text_result(RUN / "agy-inventory-after-launch.json")
launch = text_result(RUN / "agy-launch-recovery.json")
app_id = "Google.Antigravity"
for inventory in (before, after):
    apps = [app for app in inventory["apps"] if app["id"] == app_id]
    assert len(apps) == 1 and apps[0]["isRunning"] and not apps[0]["windows"]
    assert not [window for window in inventory["windows"] if "antigravity" in window["app"].casefold()]
assert launch["app"] == app_id and launch["status"] == "launch-returned"
assert launch["workspace_input_sent"] is False and after["workspace_input_sent"] is False
assert after["agy_owned_candidate_count"] == 0
process_before = read(RUN / "agy-process-before-launch.json")
process_after = read(RUN / "agy-process-after-launch.json")
identity = lambda rows: sorted((row["pid"], row["parent_pid"], row["creation_utc"], row["executable"]) for row in rows)
assert identity(process_before["processes"]) == identity(process_after["processes"])
assert len(process_before["processes"]) == 6
roots = [row for row in process_after["processes"] if row["parent_pid"] not in {p["pid"] for p in process_after["processes"]}]
assert len(roots) == 1 and roots[0]["pid"] == 44132
assert roots[0]["creation_utc"] == "2026-10-05T02:09:07.8897790Z"
routing = read(RUN / "cursor-native-routing-contexts.json")
assert sha(Path(routing["source"])) == routing["source_sha256"]
assert not routing["vendor_code_evaluated"] and not routing["vendor_source_modified"]
assert not routing["native_callbacks_triggered"]
for row in routing["patterns"]:
    assert len(row["contexts"]) == row["retained_matches"] <= 8
    assert row["retained_matches"] <= row["total_matches"]
    for snippet in row["contexts"]:
        assert hashlib.sha256(snippet["text"].encode("utf8")).hexdigest() == snippet["sha256_utf8"]
summary = {"status": "verified-supported-recovery-native-window-still-unidentified",
    "agy_owned_window_count": 0, "launch_attempts": 1, "workspace_input_sent": False,
    "existing_agy_root_pid": roots[0]["pid"], "existing_agy_creation_utc": roots[0]["creation_utc"],
    "agy_process_count_before": 6, "agy_process_count_after": 6, "process_identities_preserved": True,
    "new_processes": 0, "process_stop_performed": False,
    "window_attribution_limit": "Antigravity-titled window remains assigned to OpenAI.Codex app; no input or capture used on that window",
    "computer_use_scope": "one fresh inventory, supported launch by returned app id, fresh inventory; stop on zero owned candidates",
    "access_and_unlock_grants": "retained-no-new-approval-required", "agy_ide_native_gate": "pending-unverified",
    "cursor_vendor_source_sha256": routing["source_sha256"], "vendor_code_evaluated": False,
    "source_inspection_scope": "bounded text contexts only; 8 of 10 executeHookForStep matches retained",
    "cursor_plugin_prompt_stop_cause": "unverified; missing regex matches do not establish absence or unsupported behavior",
    "artifacts": [bind(RUN / name) for name in (
        "agy-inventory-before-launch.json", "agy-launch-recovery.json", "agy-inventory-after-launch.json",
        "agy-process-before-launch.json", "agy-process-after-launch.json", "cursor-native-routing-contexts.json")],
    "verifier": bind(Path(__file__)), "plan_tasks": "44/45", "full_native_gate": "unchecked"}
with (RUN / "host-recovery-summary.json").open("x", encoding="utf8") as stream:
    json.dump(summary, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"status": summary["status"], "agy_windows": 0, "existing_agy_processes": 6, "new_processes": 0}))
