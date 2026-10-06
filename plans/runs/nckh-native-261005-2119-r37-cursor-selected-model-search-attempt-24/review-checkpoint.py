"""Review current checkpoint claims and persisted bindings without replaying model turns."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda p: json.loads(p.read_text(encoding="utf8"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path":p.relative_to(WORK).as_posix(), "sha256":sha(p)}
aliases = WORK / "plans/runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21"
host = WORK / "plans/runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22"
admission = WORK / "plans/runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23"
summaries = [aliases/"native-alias-summary.json", host/"host-recovery-summary.json", admission/"native-admission-summary.json", RUN/"native-uncovered-summary.json"]
bindings_checked = []
def verify_bindings(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            target = WORK / value["path"]
            assert target.is_file() and sha(target) == value["sha256"], value["path"]
            bindings_checked.append(value["path"])
        for item in value.values():
            verify_bindings(item)
    elif isinstance(value, list):
        for item in value:
            verify_bindings(item)
for summary in summaries:
    value = read(summary)
    assert value["full_native_gate"] == "unchecked" and value["plan_tasks"] == "44/45"
    verify_bindings(value)
assert read(summaries[0])["unqualified_duplicate_events"] == ["beforeSubmitPrompt", "stop"]
assert read(summaries[1])["agy_owned_window_count"] == 0 and read(summaries[1])["new_processes"] == 0
assert read(summaries[2])["prompt_submissions"] == read(summaries[2])["native_model_turns"] == 0
assert read(summaries[3])["actual_native_tool"] == "Grep" and read(summaries[3])["model_prompt_retries"] == 0
union = read(RUN / "all-observed-process-audit.json")
assert [(row["observed_identity_count"],row["tracked_live_count"],row["matching_count"]) for row in union["runs"]] == [(9,0,0),(18,0,0)]
reconciliation = read(RUN / "plan-reconciliation.json")
assert reconciliation["done_tasks"] == 44 and reconciliation["total_tasks"] == 45
assert reconciliation["current_phase"] == 3 and reconciliation["state"] == "active"
assert reconciliation["index_bookkeeping_preserved"] and reconciliation["links_checked"] == 291
verify_bindings(reconciliation)
record = {"status":"inline-reviewed-native-progress-full-gate-open", "timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "review_kind":"controller inline; no new independent reviewer", "summaries":[bind(p) for p in summaries],
    "binding_count":len(bindings_checked), "unique_binding_count":len(set(bindings_checked)),
    "observed_process_audit":bind(RUN/"all-observed-process-audit.json"), "reconciliation":bind(RUN/"plan-reconciliation.json"),
    "findings":[
        {"finding":"Plugin prompt/stop callbacks absent after compatibility control", "disposition":"unqualified cells retained; no unsupported parity or new source patch"},
        {"finding":"AGY launch preserves process identities but exposes no owned target window", "disposition":"IDE proof pending; no input into Codex-attributed window"},
        {"finding":"Explicit Cursor model specifier rejected before prompt", "disposition":"failure retained; existing granted selection and CLI display verified before new single prompt"},
        {"finding":"Native tool event model fields omit effort suffix and raw parameters", "disposition":"exact event fields bound; failed verifier/preimage retained; selection proof separate from backend attestation"},
        {"finding":"Unmapped native Grep proceeds under manual policy", "disposition":"actual uncovered-route evidence; no preventive enforcement or native-unsupported claim"},
    ], "core_source_changes":0, "source_revision":37,
    "source_lock_hash":"629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb",
    "verification_reuse":"unchanged r37 local checks reused; not rerun or upgraded to native/scientific proof",
    "plan_tasks":"44/45", "full_native_gate":"unchecked", "goal_progress":True,
    "remaining_evidence":["actual private Write", "native plugin prompt/stop duplicates", "genuine native unsupported events/tools",
        "remaining per-host event/tool/fault matrices", "Desktop/IDE direct surfaces", "Claude model/effort selection and model turns"],
    "model_turns_replayed":0, "publication":"not-performed", "installed_update":"not-performed", "verifier":bind(Path(__file__))}
with (RUN / "inline-review.json").open("x",encoding="utf8") as stream:
    json.dump(record,stream,ensure_ascii=False,indent=2)
    stream.write("\n")
print(json.dumps({"status":record["status"],"bindings":len(bindings_checked),"links":291,"plan":"44/45", "new_independent_review":False}))
