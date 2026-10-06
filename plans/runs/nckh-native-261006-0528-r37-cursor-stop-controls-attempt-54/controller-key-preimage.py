"""Freeze current Cursor Stop observations after the qualified LF-content Write route."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}


def once(text, old, new):
    assert text.count(old) == 1, "Retained controller differs from the bounded adaptation"
    return text.replace(old,new)


def create(name, text):
    target = RUN / name
    assert target.resolve().is_relative_to(WORK.resolve())
    if name.endswith(".py"):
        compile(text,str(target),"exec")
    with target.open("x",encoding="utf8",newline="\n") as stream:
        stream.write(text)


def scope(text):
    return (text.replace(".nckh-native-r37-cursor-posttool-lf-controls-53", ".nckh-native-r37-cursor-stop-controls-54")
        .replace("native-cursor-posttool-lf-r37-53", "native-cursor-stop-r37-54")
        .replace("NCKH_POSTTOOL_", "NCKH_STOP_").replace("_53_", "_54_")
        .replace("cursor-posttool-runtime.py", "cursor-stop-runtime.py")
        .replace("native-cursor-posttool.process-tree.json", "native-cursor-stop.process-tree.json"))


for name in ("owned-cli-command.py", "native-process-capture.py", "native-process-state.py", "select-native-root.ps1"):
    create(name,(PRIOR/name).read_text(encoding="utf8"))
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write((PRIOR / "cursor-agy-model-dangerous-grant.json").read_bytes())
audit = (PRIOR / "audit-owned-processes.ps1").read_text(encoding="utf8")
audit = once(audit,
    "plans\\runs\\nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52\\process-final-audit.json",
    "plans\\runs\\nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53\\process-final-audit.json")
audit = once(audit,"$taskExpected.Count -ne 612", "$taskExpected.Count -ne 1542")
audit = once(audit,"prior_temporally_valid_identities=612", "prior_temporally_valid_identities=1542")
create("audit-owned-processes.ps1",audit)
create("cursor-stop-runtime.py",scope((PRIOR / "cursor-posttool-runtime.py").read_text(encoding="utf8")))
create("monitor-native-session.py",scope((PRIOR / "monitor-native-session.py").read_text(encoding="utf8")))
create("seal-source-check.py",scope((PRIOR / "seal-source-check.py").read_text(encoding="utf8")))

observer = scope((PRIOR / "cursor-file-observer.py").read_text(encoding="utf8"))
needle = '    if isinstance(fields, dict):'
observer = once(observer,needle,'''    if args.event == "stop":
        loop_count = native.get("loop_count")
        record["native_stop_loop_count"] = loop_count if isinstance(loop_count,int) and not isinstance(loop_count,bool) else None
        status = native.get("status")
        record["native_stop_status"] = status if isinstance(status,str) and len(status.encode("utf8")) <= 64 else None
        for field in ("generation_id", "session_id"):
            value = native.get(field)
            record["native_"+field+"_sha256"] = sha(value.encode("utf8")) if isinstance(value,str) and value else None
        record["transcript_read_performed"] = False
''' + needle)
create("cursor-file-observer.py",observer)

controller = scope((PRIOR / "control-posttool.py").read_text(encoding="utf8"))
controller = controller.replace('audit["prior_temporally_valid_identities"] == 612', 'audit["prior_temporally_valid_identities"] == 1542')
controller = controller.replace('"selected_event":"postToolUse"', '"selected_event":"stop"')
controller = controller.replace('"posttool-"', '"stop-"').replace('posttool-cases', 'stop-cases')
controller = controller.replace('bounded-posttool-Write-observations', 'bounded-Stop-after-Write-observations')
controller = controller.replace('"event":"postToolUse"', '"event":"stop"')
controller = controller.replace('"postToolUse_timeout_seconds"', '"Stop_timeout_seconds"')
controller = controller.replace('advisory/delivery-bindings-current-review-separate', 'advisory/writing-resource-advice-only; Cursor Stop wire is empty object')
controller = controller.replace('selected post only', 'selected Stop only')
controller = controller.replace('"oracle":"one genuine matching Write pre/post per case; frozen bytes present at post callback start; final marker; preserve actual hook outcomes",',
    '"oracle":"one genuine matching Write pre/post per case; exact bytes at one actual Stop; actual poll final marker; bounded Stop loop_count/status/generation hash; preserve actual outcomes",')
controller = once(controller,
    '    assert any(row["event"] == "stop" for row in callbacks), "Wait for actual Stop"',
    '''    stops = [row for row in callbacks if row["event"] == "stop"]
    assert len(stops) == 1, "Frozen one-Stop oracle failed; preserve repeated/missing callback"
    stop = stops[0]
    assert stop["marker_exists_at_callback_start"] and stop["marker_at_callback_start_sha256"] == case["expected_sha256"]
    assert isinstance(stop["native_stop_loop_count"],int) and 0 <= stop["native_stop_loop_count"] <= 65535
    assert stop["native_stop_status"] and stop["native_generation_id_sha256"] and stop["native_session_id_sha256"]
    assert not stop["transcript_read_performed"]''')
controller = once(controller,
    'terminal_paths = sorted(RUN.glob("terminal-"+str(index).zfill(2)+"-*.json"))',
    'terminal_paths = sorted(RUN.glob("terminal-"+str(index).zfill(2)+"-poll-*.json"))')
controller = controller.replace('recorded-current-Write-posttool-observation', 'recorded-current-Write-Stop-observation')
controller = once(controller,
    '"marker_before_post":True,"selected_observers_terminal":True,',
    '"marker_before_post":True,"marker_before_Stop":True,"Stop_count":1,"native_stop_loop_count":stop["native_stop_loop_count"],\n        "native_stop_status":stop["native_stop_status"],"native_generation_id_sha256":stop["native_generation_id_sha256"],\n        "selected_observers_terminal":True,')
controller = once(controller,
    '"post_status":post[0]["status"],"marker_before_post":True',
    '"stop_status":stop["status"],"marker_before_Stop":True,"Stop_count":1,"loop_count":stop["native_stop_loop_count"]')
create("control-stop.py",controller)

verifier = scope((PRIOR / "verify-posttool-observations.py").read_text(encoding="utf8"))
verifier = verifier.replace('recorded-current-Write-posttool-observation','recorded-current-Write-Stop-observation')
verifier = verifier.replace('verified-seven-current-native-Write-posttool-observations','verified-seven-current-native-Write-Stop-observations')
verifier = verifier.replace('verified-posttool-observations.json','verified-stop-observations.json')
verifier = verifier.replace('"native_timeout_deadline_qualification"','"native_Stop_timeout_deadline_qualification"')
verifier = verifier.replace('"postToolUse_timeout_seconds"','"Stop_timeout_seconds"')
verifier = verifier.replace('if row["event"] == "postToolUse" and case["mode"]', 'if row["event"] == "stop" and case["mode"]')
verifier = verifier.replace('if row["event"] != "postToolUse":', 'if row["event"] != "stop":')
verifier = verifier.replace('"/postToolUse/" in ref["path"]', '"/stop/" in ref["path"]')
verifier = once(verifier,
    '    post = next(row for row in callbacks if row["event"] == "postToolUse")',
    '''    post = next(row for row in callbacks if row["event"] == "postToolUse")
    stop = next(row for row in callbacks if row["event"] == "stop")
    assert record["marker_before_Stop"] and record["Stop_count"] == 1
    assert stop["marker_at_callback_start_sha256"] == case["expected_sha256"]
    assert isinstance(stop["native_stop_loop_count"],int) and 0 <= stop["native_stop_loop_count"] <= 65535
    assert stop["native_stop_status"] and stop["native_generation_id_sha256"] and stop["native_session_id_sha256"]
    assert not stop["transcript_read_performed"]''')
begin = verifier.index('    mode = case["mode"]')
end = verifier.index('assert len(set(ids))',begin)
region = verifier[begin:end].replace('post[','stop[').replace('post.get(', 'stop.get(')
region = region.replace('delivery-bindings-current-review-separate', 'writing-resource-advice-only')
region = region.replace('"post_status":stop["status"]', '"Stop_status":stop["status"]')
region = region.replace('"post_callback_elapsed_seconds"', '"Stop_callback_elapsed_seconds"')
region = region.replace('"selected_policy_receipts":len(selected_receipts)',
    '"selected_policy_receipts":len(selected_receipts),"Stop_count":1,"native_loop_count":stop["native_stop_loop_count"],\n        "native_stop_status":stop["native_stop_status"],"native_generation_id_sha256":stop["native_generation_id_sha256"]')
# A host may terminate the selected sleeper before it produces a completed record.
region = once(region,
    'assert elapsed is not None and elapsed >= frozen["injected_sleep_seconds"]\n        assert elapsed > frozen["Stop_timeout_seconds"]',
    'if elapsed is not None:\n            assert elapsed >= frozen["injected_sleep_seconds"] and elapsed > frozen["Stop_timeout_seconds"]')
region = once(region,
    '"receipt_after_declared_bound":bool(selected_receipts)',
    '"receipt_after_declared_bound":bool(selected_receipts) and elapsed is not None and elapsed > frozen["Stop_timeout_seconds"]')
verifier = verifier[:begin]+region+verifier[end:]
verifier = once(verifier,
    '"all_markers_before_selected_post":True',
    '"all_markers_before_selected_Stop":True,"Stop_callback_counts":[row["Stop_count"] for row in results],\n+    "repeat_behavior":"unqualified; observe actual counts/loop_count only", "Stop_wire":"empty object for advisory/block/degraded codec outcomes"')
create("verify-stop-observations.py",verifier)

record = {"timestamp_utc":datetime.now(timezone.utc).isoformat(),"source_kit_modified":False,"model_prompts":0,
    "causal_scope":"current r37 Cursor Stop on interactive surface after native LF-content Write; native53 selected PostToolUse only",
    "changes":["select Stop faults only", "capture bounded Stop status/loop_count/generation/session hashes",
               "one native Stop per requested turn oracle", "final marker from actual poll outputs only", "actual exit-state monitor/1542 qualified prior identities"],
    "prior_inputs":[bind(PRIOR/name) for name in ("control-posttool.py","cursor-file-observer.py","verify-posttool-observations.py",
        "monitor-native-session.py","verified-posttool-observations.json","process-final-audit.json")],
    "created":[bind(path) for path in sorted(RUN.iterdir()) if path.is_file()], "controller":bind(Path(__file__)),
    "timeout_scope":"declared5s/injected8s; effective native deadline unqualified until an actual native witness"}
create("controller-adaptation.json",json.dumps(record,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":"prepared-distinct-current-Stop-controller","files":len(record["created"]),"model_prompts":0}))
