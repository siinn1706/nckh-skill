"""Reconcile scoped observations and ownership counterevidence without changing the full native gate."""
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0400-r37-cursor-directory-denial-attempt-50"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0420-r37-cursor-grep-faults.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

verified = read(RUN / "verified-grep-observations-with-monitor-gap.json")
assert verified["status"] == "verified-five-native-directory-Grep-observations-with-monitor-gap"
assert verified["model_turns"] == verified["actual_native_tool_requests"] == 5
assert verified["callback_count"] == 21 and verified["policy_receipt_count"] == 14
assert verified["monitor_exit_code"] == 1 and verified["original_oracle"].startswith("failed")
correction = read(RUN / "process-ownership-correction.json")
assert correction["raw_identity_union"] == 2968 and correction["preexisting_applications_preserved"] == 27
assert correction["current_scoped_owned_live"] == 0 and not correction["continuous_monitor_success"]
helper = read(RUN / "verified-process-capture-checks.json")
assert len(helper["checks"]) == 6 and helper["model_prompts"] == 0
spec = importlib.util.spec_from_file_location("final_grep_source_guard", RUN / "cursor-grep-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
save_new(RUN / "final-source-check.json", {
    "status": "verified-unchanged-r37-canonical-source-lock",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": probe.EXPECTED,
    "guard": "check_source calls verify_source_lock and compares canonical digest",
    "guard_source": bind(RUN / "cursor-grep-runtime.py"), "broad_tests_rerun": False,
})
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "native-evidence-history.md", JOURNAL]
contents = {path: path.read_text(encoding="utf8") for path in paths}
before = {str(path): sha(path) for path in paths}
preimages = RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    with (preimages / path.name).open("xb") as stream:
        stream.write(path.read_bytes())
index = PLAN / "plan.md"
text = contents[index]
old = '[directory49/50](../reports/delivery-261006-0400-r37-cursor-directory-denial.md)'
new = old + ', [Grep faults51](../reports/delivery-261006-0420-r37-cursor-grep-faults.md)'
assert text.count(old) == 1
text = text.replace(old, new)
old = 'Latest native50:1 turn/1 private-directory Grep/5 callbacks/4 receipts; native permission_denied matches preflight tool ID/session/path/version. Cleanup27/preserved921/final union2592 zero live; source r37/protected global hashes unchanged. Full native task remains unchecked.'
new = (
    'Latest native51:5 directory-Grep fault turns/21 callbacks/14 receipts, each native permission_denied and unchanged fixture. '
    'Native exit0/monitor exit1; original oracle failed, scoped observations verified. Cleanup27/preserved938. '
    'Ownership correction preserves27 preexisting applications in raw union2968; current qualified owned-live0, '
    'historical raw zero-live claims need qualification. Six controller-capture checks passed. '
    'Source r37/protected global hashes unchanged; full native task remains unchecked.'
)
assert text.count(old) == 1
text = text.replace(old, new)
summary = (
    "[Cursor directory Grep faults51](../reports/delivery-261006-0420-r37-cursor-grep-faults.md) records five "
    "Grok4.7/500k/xhigh/fastfalse turns/five actual Grep requests on CLI2026.09.15-d2fe57e:21 callbacks/14 receipts, "
    "five matching native permission_denied responses, no successful post/unchanged fixture/final markers. "
    "Malformed input/output,20s timeout of24s sleeper,crash17 and unsupported selected codec are controller-injected "
    "after genuine preflight; late manual receipt does not override timeout denial. Native exit0/monitor exit1 WinError5; "
    "original full-run oracle failed and preserved, scoped behavioral verifier passed. Cleanup27/preserved938/protected hashes unchanged. "
    "Precision/ownership correction finds27 preexisting applications falsely included in raw union2968; bound snapshots prove "
    "their creation predates corresponding test roots. Preserve those apps/no process stop; current temporal captured358/owned-live0, "
    "continuous monitor and historical raw all-tracked-zero claims unqualified. New controller capture has six focused checks; "
    "native use of repaired helper still pending. Source r37 unchanged;44/45/P3 active."
)
updated = {index: text}
for path in paths[1:]:
    assert "Cursor directory Grep faults51" not in contents[path]
    updated[path] = contents[path].rstrip() + "\n\n## Cursor directory Grep faults and process ownership\n\n" + summary + "\n"
for path, value in updated.items():
    assert sha(path) == before[str(path)], "Document changed during reconciliation"
    path.write_text(value, encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["process_state"] = "native51 terminal52990 exit0/monitor90446 exit1 WinError5; raw union2968 has27 preexisting app matches; current temporal owned-live0; no stop; continuous monitor unqualified"
todo["latest_scoped_evidence"] = bind(RUN / "verified-grep-observations-with-monitor-gap.json")
todo["final_process_audit"] = bind(RUN / "process-ownership-correction.json")
todo["raw_final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["source_final_check"] = bind(RUN / "final-source-check.json")
todo["historical_process_audit_correction"] = {
    "verification": bind(RUN / "process-ownership-correction.json"),
    "raw_union": 2968, "preexisting_applications_preserved": 27,
    "current_temporally_valid_captured_identities": 358, "current_scoped_owned_live": 0,
    "legacy_raw_zero_live_claim": "not currently qualified; original records retained",
    "process_stop_performed": False,
}
todo["controller_capture_repair"] = {
    "helper": bind(RUN / "native-process-capture.py"),
    "verification": bind(RUN / "verified-process-capture-checks.json"),
    "expected_root_creation_ticks": "required",
    "atomic_commit": "6 attempts/0.775s bounded total delay; terminal failures retained",
    "native_usage": "not-yet-performed; wire into next owned controller instead of legacy parent-PID-only traversal",
}
todo["current_verified_Cursor_scopes"].append("directory Grep51: five actual fault permission denials/21 callbacks/14 receipts; scoped behavioral verification with preserved monitor1/full-run oracle failure")
todo["Cursor_directory_Grep"]["native51_verification"] = bind(RUN / "verified-grep-observations-with-monitor-gap.json")
todo["Cursor_directory_Grep"]["native51_report"] = bind(REPORT)
todo["Cursor_directory_Grep"]["native51_original_oracle"] = "failed-preserved; monitor exit1"
todo["current_turn_classification"] = "progress: five directory Grep faults recorded, monitor failure retained, temporal/precision ownership corrected and six controller checks"
todo["next_authorized_native_cell"] = (
    "Use repaired temporal capture with explicit root PID/creation and precision ownership audit before further native runs; "
    "inspect unchanged Cursor/Codex event records to choose a genuinely missing current-r37 fault/tool cell. "
    "Keep AGY search failures, unknown-host-event, direct-app and plugin gaps distinct. No repeated model prompt without causal evidence."
)
todo["pending_cache_permission"] = "context recovery reconfirmed asynchronously this turn; no direct answer at reconciliation"
todo["Claude_selection"] = "model/effort reconfirmed asynchronously this turn; no direct answer and no Claude model prompt"
save_new(RUN / "native-continuation-todo.json", todo)
counts = {}
for path in sorted(PLAN.glob("phase-*.md")):
    items = re.findall(r"^\s*- \[([ xX])\]", path.read_text(encoding="utf8"), re.MULTILINE)
    counts[path.name] = {"done": sum(item.lower() == "x" for item in items), "total": len(items)}
assert [(value["done"], value["total"]) for value in counts.values()] == [(13,13),(9,9),(10,11),(12,12)]
links = 0
for path in [*sorted(PLAN.glob("*.md")), REPORT, JOURNAL]:
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("http:", "https:", "#", "mailto:", "codex:")):
            continue
        assert (path.parent / reference.split("#",1)[0]).resolve().exists(), str(path) + " missing link " + reference
        links += 1
save_new(RUN / "plan-reconciliation.json", {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status":"in-progress", "tasks":"44/45", "phases":counts,
    "source_revision":37, "source_lock_hash":verified["source_lock_hash"], "full_native_gate":"unchecked",
    "docs":[{"path":path.relative_to(WORK).as_posix(),"before_sha256":before[str(path)],"after_sha256":sha(path),
             "preimage":bind(preimages / path.name)} for path in paths],
    "report":bind(REPORT), "todo":bind(RUN / "native-continuation-todo.json"),
    "original_oracle":"failed-preserved", "scoped_native_verification":bind(RUN / "verified-grep-observations-with-monitor-gap.json"),
    "process_ownership_correction":bind(RUN / "process-ownership-correction.json"), "source_final_check":bind(RUN / "final-source-check.json"),
    "local_links_checked":links, "link_evidence_class":"structural only", "broad_tests_rerun":False,
    "index_reindex_performed":False, "current_goal_turn":"progress", "reconciler":bind(Path(__file__)),
})
print(json.dumps({"status":"in-progress","tasks":"44/45","local_links":links,"raw_union":2968,
                  "preexisting_preserved":27,"current_scoped_owned_live":0,"original_oracle":"failed-preserved"}))
