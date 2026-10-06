"""Reconcile failed current baseline and verified exit-state evidence without marking native delivery complete."""
import hashlib
import importlib.util
import json
import re
from datetime import datetime,timezone
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
PRIOR=RUN.parent / "nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51"
PLAN=WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT=WORK / "plans/reports/delivery-261006-0423-r37-cursor-posttool-baseline-failure.md"
JOURNAL=WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read=lambda path:json.loads(path.read_text(encoding="utf-8-sig"))
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
bind=lambda path:{"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
def save_new(path,value):
    with path.open("x",encoding="utf8") as stream:stream.write(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
verified=read(RUN / "verified-baseline-failure-observation.json")
assert verified["status"] == "verified-failed-native52-baseline-observation" and verified["dependent_cases_unstarted"] == 6
assert verified["frozen_byte_oracle"] == "failed-preserved" and verified["owned_processes_live"] == 0
spec=importlib.util.spec_from_file_location("final_posttool_source",RUN / "cursor-posttool-runtime.py")
probe=importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
save_new(RUN / "final-source-check.json",{"status":"verified-unchanged-r37-canonical-source-lock",
    "timestamp_utc":datetime.now(timezone.utc).isoformat(),"source_revision":37,"source_lock_hash":probe.EXPECTED,
    "guard_source":bind(RUN / "cursor-posttool-runtime.py"),"broad_tests_rerun":False})
paths=[PLAN / "plan.md",PLAN / "phase-03-portable-hooks.md",PLAN / "native-evidence-history.md",JOURNAL]
contents={path:path.read_text(encoding="utf8") for path in paths}
before={str(path):sha(path) for path in paths}
preimages=RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    with (preimages / path.name).open("xb") as stream:stream.write(path.read_bytes())
text=contents[paths[0]]
old='[Grep faults51](../reports/delivery-261006-0420-r37-cursor-grep-faults.md)'
new=old+', [PostToolUse baseline52](../reports/delivery-261006-0423-r37-cursor-posttool-baseline-failure.md)'
assert text.count(old) == 1
text=text.replace(old,new)
old='Latest native51:5 directory-Grep fault turns/21 callbacks/14 receipts, each native permission_denied and unchanged fixture. Native exit0/monitor exit1; original oracle failed, scoped observations verified. Cleanup27/preserved938. Ownership correction preserves27 preexisting applications in raw union2968; current qualified owned-live0, historical raw zero-live claims need qualification. Six controller-capture checks passed. Source r37/protected global hashes unchanged; full native task remains unchecked.'
new=('Latest native52:1 actual Write/5 callbacks/5 receipts; expected CRLF became CRCRLF and PostToolUse returned pending/stale bytes. '
     'Frozen baseline failed; six dependent cases unstarted. Native exit0/monitor exit1 at root close; creation time alone proved insufficient for liveness by a real process-state control. '
     'Cleanup33/preserved991/qualified temporal union612/owned-live0;27 preexisting apps preserved, raw historical zero-live claims need qualification. '
     'Source r37/protected global hashes unchanged; full native task remains unchecked.')
assert text.count(old) == 1
updates={paths[0]:text.replace(old,new)}
summary=("[Cursor PostToolUse baseline52](../reports/delivery-261006-0423-r37-cursor-posttool-baseline-failure.md) records one Grok4.7/500k/xhigh/fastfalse turn/one actual Write on CLI2026.09.15-d2fe57e:"
    "five callbacks/five receipts, marker already changed at PostToolUse; expected CRLF differs from actual CRCRLF. "
    "Post policy pending/artifact-final-bytes-missing-or-stale; frozen baseline failed/six dependent cases unstarted/no retry or regrade. "
    "Native exit0/monitor exit1 at root close. Real owned Python process control proves creation times stay queryable after exit0; actual exit state must qualify liveness. "
    "Cleanup33/preserved991/qualified temporal union612/zero owned-live;27 preexisting apps preserved and legacy raw union not used as ownership. "
    "Next input-content diagnostic/exit-state monitor route is causally different; normalization origin remains unqualified. "
    "Source r37 unchanged;44/45/P3 active.")
for path in paths[1:]:
    assert "Cursor PostToolUse baseline52" not in contents[path]
    updates[path]=contents[path].rstrip()+"\n\n## Cursor PostToolUse baseline and root exit state\n\n"+summary+"\n"
for path,value in updates.items():
    assert sha(path) == before[str(path)]
    path.write_text(value,encoding="utf8")
todo=read(PRIOR / "native-continuation-todo.json")
todo["latest_scoped_evidence"]=bind(RUN / "verified-baseline-failure-observation.json")
todo["final_process_audit"]=bind(RUN / "process-final-audit.json")
todo["process_state"]="native52 terminal29583 exit0/monitor5099 exit1 at root close; qualified temporal union612/owned-live0;27 preexisting apps preserved; no process stop; continuous monitor unqualified"
todo["source_final_check"]=bind(RUN / "final-source-check.json")
todo["Cursor_current_Write_PostToolUse"]={
    "verification":bind(RUN / "verified-baseline-failure-observation.json"),"report":bind(REPORT),
    "status":"baseline oracle failed-preserved; one genuine Write exposes pending/stale bytes",
    "expected_tail":"CRLF","actual_tail":"CRCRLF","remaining_cases_unstarted":6,
    "normalizer_origin":"unqualified; actual native content body not retained",
}
todo["controller_exit_state"]={
    "helper":bind(RUN / "native-process-state.py"),"verification":bind(RUN / "verified-process-exit-state-control.json"),
    "fact":"creation time can stay queryable for terminated process; use actual GetExitCodeProcess status",
    "native_usage":"not-yet-performed; native52 monitor failure retained",
}
todo["controller_capture_repair"]["native_usage"]="temporal capture actually used52;252 captured identities; root-close liveness failure retained"
todo["controller_capture_repair"]["next_liveness_requirement"]="read actual active/terminated/absent/unobservable state with exact creation generation"
todo["current_verified_Cursor_scopes"].append("Write PostToolUse52 failed baseline: actual CRCRLF vs expected CRLF; current pending stale-byte guard observed; six controls unstarted")
todo["next_authorized_native_cell"]=("Prepare causally different Write contract separating LF native content argument and CRLF on-disk expectation; bounded content hash/tail observation on exact synthetic marker only. "
    "Use actual exit-state monitor and temporal/precision audit. Preserve native52 failed CRLF request/oracle; no identical prompt retry. "
    "Claude selection/cache authority/direct-app gaps remain pending.")
todo["current_turn_classification"]="progress: one genuine current Write/PostToolUse baseline failure changes next input contract; native cleanup verified; actual terminal-versus-creation-time control"
save_new(RUN / "native-continuation-todo.json",todo)
counts={}
for path in sorted(PLAN.glob("phase-*.md")):
    items=re.findall(r"^\s*- \[([ xX])\]",path.read_text(encoding="utf8"),re.MULTILINE)
    counts[path.name]={"done":sum(item.lower()=="x" for item in items),"total":len(items)}
assert [(value["done"],value["total"]) for value in counts.values()] == [(13,13),(9,9),(10,11),(12,12)]
links=0
for path in [*sorted(PLAN.glob("*.md")),REPORT,JOURNAL]:
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)",path.read_text(encoding="utf8")):
        if reference.startswith(("http:","https:","#","mailto:","codex:")):continue
        assert (path.parent / reference.split("#",1)[0]).resolve().exists(),str(path)+" missing link "+reference
        links+=1
save_new(RUN / "plan-reconciliation.json",{"timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "status":"in-progress","tasks":"44/45","phases":counts,"full_native_gate":"unchecked","source_revision":37,
    "source_lock_hash":verified["source_lock_hash"],"report":bind(REPORT),"todo":bind(RUN / "native-continuation-todo.json"),
    "docs":[{"path":path.relative_to(WORK).as_posix(),"before_sha256":before[str(path)],"after_sha256":sha(path),"preimage":bind(preimages/path.name)} for path in paths],
    "source_final_check":bind(RUN / "final-source-check.json"),"native52_oracle":"failed-preserved",
    "local_links_checked":links,"link_evidence_class":"structural only","broad_tests_rerun":False,"index_reindex_performed":False,
    "current_goal_turn":"progress","reconciler":bind(Path(__file__))})
print(json.dumps({"status":"in-progress","tasks":"44/45","local_links":links,"qualified_union":612,"owned_live":0,"native52_oracle":"failed-preserved"}))
