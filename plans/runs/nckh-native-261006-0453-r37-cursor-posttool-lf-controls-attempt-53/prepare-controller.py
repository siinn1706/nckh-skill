"""Create a new, bounded LF-content experiment while preserving every prior attempt."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def replace_once(text, old, new):
    assert text.count(old) == 1, "The retained source no longer matches the bounded adaptation"
    return text.replace(old, new)


def create(name, text):
    target = RUN / name
    assert target.resolve().is_relative_to(WORK.resolve())
    if name.endswith(".py"):
        compile(text, str(target), "exec")
    with target.open("x", encoding="utf8", newline="\n") as stream:
        stream.write(text)


for name in ("owned-cli-command.py", "native-process-capture.py", "native-process-state.py", "select-native-root.ps1"):
    create(name, (PRIOR / name).read_text(encoding="utf8"))
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write((PRIOR / "cursor-agy-model-dangerous-grant.json").read_bytes())

audit = (PRIOR / "audit-owned-processes.ps1").read_text(encoding="utf8")
audit = replace_once(audit,
    "plans\\runs\\nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51\\process-ownership-correction.json",
    "plans\\runs\\nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52\\process-final-audit.json")
begin = audit.index("foreach ($taskKey in $taskPrior.owned_identity_keys)")
end = audit.index("if (Test-Path", begin)
audit = audit[:begin] + '''foreach ($taskRow in $taskPrior.tracked) {
    $taskKey=([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks
    $taskExpected[$taskKey]=$taskRow
}
if ($taskExpected.Count -ne 612) {throw 'Qualified prior identity set changed'}
''' + audit[end:]
audit = audit.replace("prior_temporally_valid_identities=358", "prior_temporally_valid_identities=612")
create("audit-owned-processes.ps1", audit)

runtime = (PRIOR / "cursor-posttool-runtime.py").read_text(encoding="utf8")
runtime = runtime.replace(".nckh-native-r37-cursor-posttool-controls-52", ".nckh-native-r37-cursor-posttool-lf-controls-53")
runtime = runtime.replace("native-cursor-posttool-r37-52", "native-cursor-posttool-lf-r37-53")
create("cursor-posttool-runtime.py", runtime)

observer = (PRIOR / "cursor-file-observer.py").read_text(encoding="utf8")
needle = '        command = fields.get("command", fields.get("CommandLine"))'
diagnostics = '''        if record["native_tool_name"] == "Write" and control.get("marker_relative"):
            native_path = fields.get("file_path")
            if isinstance(native_path, str) and (args.project / native_path).resolve() == marker:
                content = fields.get("content")
                if isinstance(content, str):
                    content_bytes = content.encode("utf8")
                    prefix = control["native_marker_prefix"].encode("ascii")
                    suffix = content_bytes[len(prefix):]
                    synthetic = (len(content_bytes) <= 256 and content_bytes.startswith(prefix)
                        and len(suffix) <= 8 and all(byte in {10,13} for byte in suffix))
                    record["native_content_diagnostics"] = {
                        "sha256":sha(content_bytes), "utf8_length":len(content_bytes),
                        "synthetic_marker_only":synthetic,
                        "tail_hex":content_bytes[-16:].hex() if synthetic else None,
                        "expected_LF_content_sha256":control["expected_content_sha256"],
                        "raw_content_retained":False,
                        "scope":"exact controller-owned public synthetic marker path"}
                else:
                    record["native_content_diagnostics"] = {"status":"content-argument-not-observed"}
''' + needle
observer = replace_once(observer, needle, diagnostics)
create("cursor-file-observer.py", observer)

controller = (PRIOR / "control-posttool.py").read_text(encoding="utf8")
begin = controller.index("def setup():")
end = controller.index("def prepare():", begin)
controller = controller[:begin] + controller[end:]
controller = controller.replace(".nckh-native-r37-cursor-posttool-controls-52", ".nckh-native-r37-cursor-posttool-lf-controls-53")
controller = controller.replace("native-cursor-posttool-r37-52", "native-cursor-posttool-lf-r37-53")
controller = controller.replace("_52_", "_53_")
controller = controller.replace('audit["prior_temporally_valid_identities"] == 358', 'audit["prior_temporally_valid_identities"] == 612')
controller = replace_once(controller,
    '        fixture = probe.PROJECT / relative',
    '        native_content = ("NCKH_POSTTOOL_PUBLIC_AFTER_53_" + str(index) + "\\n").encode("ascii")\n        fixture = probe.PROJECT / relative')
controller = replace_once(controller,
    '" followed by exactly one Windows CRLF line ending (carriage return then line feed). "',
    '" followed by exactly one LF (U+000A) in the native Write content argument. Include no CR (U+000D) in that argument. "')
controller = replace_once(controller,
    '"expected_sha256":hashlib.sha256(expected).hexdigest(),"marker":marker,"prompt":prompt,',
    '"expected_sha256":hashlib.sha256(expected).hexdigest(),"marker":marker,"prompt":prompt,\n            "expected_content_hex":native_content.hex(),"expected_content_sha256":hashlib.sha256(native_content).hexdigest(),\n            "expected_content_length":len(native_content),"expected_content_tail_hex":native_content[-16:].hex(),')
controller = replace_once(controller,
    '"newline_scope":"frozen CRLF contract from prior native44 observation; original44 LF failure preserved",',
    '"newline_scope":"LF in actual native content argument; prospective Windows CRLF disk oracle; native44 and52 failures preserved",\n        "diagnostic_scope":"hash/length/tail16 only for exact public synthetic marker; raw content not retained",')
controller = replace_once(controller,
    '"marker_relative":case["relative"],"expected_marker_sha256":case["expected_sha256"]}',
    '"marker_relative":case["relative"],"expected_marker_sha256":case["expected_sha256"],\n        "native_marker_prefix":"NCKH_POSTTOOL_PUBLIC_AFTER_53_"+str(index),\n        "expected_content_sha256":case["expected_content_sha256"]}')
controller = replace_once(controller,
    '    assert post[0]["marker_exists_at_callback_start"]',
    '''    for row in pre+post:
        diagnostic = row.get("native_content_diagnostics", {})
        assert diagnostic.get("synthetic_marker_only"), "Actual bounded content diagnostic is required"
        assert diagnostic["sha256"] == case["expected_content_sha256"], "Native content LF oracle failed"
        assert diagnostic["utf8_length"] == case["expected_content_length"]
        assert diagnostic["tail_hex"] == case["expected_content_tail_hex"]
    import re
    terminal_paths = sorted(RUN.glob("terminal-"+str(index).zfill(2)+"-*.json"))
    outputs = "\\n".join(read(path).get("output", "") for path in terminal_paths)
    outputs = re.sub(r"\\x1b\\[[0-?]*[ -/]*[@-~]", "", outputs)
    outputs = re.sub(r"\\x1b\\][^\\x07]*\\x07", "", outputs)
    assert re.search(r"(?:^|\\n)  "+re.escape(case["marker"])+r"\\r?\\n", outputs), "Actual native final marker required"
    assert post[0]["marker_exists_at_callback_start"]''')
controller = replace_once(controller,
    '    for row in callbacks:\n        for pid_key,ticks_key',
    '''    states = load("actual_process_state", RUN / "native-process-state.py")
    process_states = []
    for row in callbacks:
        for pid_key,ticks_key''')
controller = replace_once(controller,
    '''                current = owned.creation_ticks(row[pid_key])
                expected = row.get(ticks_key)
                assert current is None or (expected is not None and current != expected), "Selected process still live or unqualified; retain control"''',
    '''                current = states.state(row[pid_key])
                expected = row.get(ticks_key)
                assert expected is not None and current["status"] != "unobservable", "Unobservable selected process"
                assert not (current["status"] == "active" and current["creation_filetime_ticks"] == expected), "Selected process still active"
                process_states.append({"expected_creation_ticks":expected, **current})''')
controller = replace_once(controller,
    '"marker_before_post":True,"selected_observers_terminal":True,',
    '"marker_before_post":True,"selected_observers_terminal":True,"native_content_LF_exact":True,"selected_process_states":process_states,')
controller = controller.replace('["setup","prepare","select","collect","cleanup"]', '["prepare","select","collect","cleanup"]')
controller = controller.replace('    if args.action == "setup": setup()\n    elif args.action == "prepare": prepare()', '    if args.action == "prepare": prepare()')
create("control-posttool.py", controller)

monitor = (PRIOR / "monitor-native-session.py").read_text(encoding="utf8")
monitor = replace_once(monitor, 'read = lambda path:', '''state_spec = importlib.util.spec_from_file_location("native_exit_state", RUN / "native-process-state.py")
states = importlib.util.module_from_spec(state_spec)
state_spec.loader.exec_module(states)
read = lambda path:''')
monitor = replace_once(monitor,
    'assert ticks is not None and abs(ticks-selected["creation_cim_ticks"]) <= 9',
    'assert ticks is not None and abs(ticks-selected["creation_cim_ticks"]) <= 9\nassert states.active_generation(selected["pid"], ticks)')
monitor = replace_once(monitor, 'try:\n    while capture.creation_ticks(root) == ticks:', '''def actual_state():
    observed = states.state(root)
    if observed["status"] == "unobservable":
        raise RuntimeError("Owned root exit state is unobservable; preserve failure")
    return observed

def same_active(observed):
    return observed["status"] == "active" and observed["creation_filetime_ticks"] == ticks

closing_messages = {
    "Owned root identity changed before snapshot", "Owned root identity changed during snapshot",
    "Owned root identity changed or is not observable"}
try:
    observed = actual_state()
    while same_active(observed):''')
monitor = replace_once(monitor,
    '''        except ValueError:
            if capture.creation_ticks(root) != ticks:
                break
            raise''',
    '''        except ValueError as error:
            observed = actual_state()
            if str(error) in closing_messages and not same_active(observed):
                break
            raise''')
monitor = replace_once(monitor, '        time.sleep(0.25)', '        time.sleep(0.25)\n        observed = actual_state()')
monitor = monitor.replace('"temporal_parent_identity":True,"captured_at"', '"temporal_parent_identity":True,"actual_exit_state_used":True,"root_state":observed,"captured_at"')
create("monitor-native-session.py", monitor)

verifier = (PRIOR / "verify-posttool-observations.py").read_text(encoding="utf8")
verifier = verifier.replace(".nckh-native-r37-cursor-posttool-controls-52", ".nckh-native-r37-cursor-posttool-lf-controls-53")
verifier = replace_once(verifier,
    'assert monitor["status"] == "root-exited-or-reused"',
    'assert monitor["actual_exit_state_used"] and monitor["root_state"]["status"] in {"terminated","absent","active"}\nassert not (monitor["root_state"]["status"] == "active" and monitor["root_state"]["creation_filetime_ticks"] == monitor["root_creation_filetime_ticks"])\nassert monitor["status"] == "root-exited-or-reused"')
verifier = replace_once(verifier,
    '    assert pre["marker_at_callback_start_sha256"] == case["before_sha256"]',
    '''    for row in (pre,post):
        diagnostic = row["native_content_diagnostics"]
        assert diagnostic["synthetic_marker_only"] and not diagnostic["raw_content_retained"]
        assert diagnostic["sha256"] == case["expected_content_sha256"]
        assert diagnostic["utf8_length"] == case["expected_content_length"]
        assert diagnostic["tail_hex"] == case["expected_content_tail_hex"]
    assert record["native_content_LF_exact"]
    assert pre["marker_at_callback_start_sha256"] == case["before_sha256"]''')
verifier = replace_once(verifier,
    '"native_exit_code":0,"monitor_exit_code":0,"temporal_process_capture":True,',
    '"native_exit_code":0,"monitor_exit_code":0,"temporal_process_capture":True,"actual_exit_state_used":True,\n    "newline_scope":"actual native content LF / actual disk CRLF; vendor-internal attribution unqualified",')
create("verify-posttool-observations.py", verifier)

record = {"timestamp_utc":datetime.now(timezone.utc).isoformat(), "source_kit_modified":False,
    "native_model_prompts":0, "native52_oracle":"failed-preserved; no regrade or identical retry",
    "changes":["explicit LF in native content vs CRLF disk oracle", "bounded synthetic content diagnostics",
               "actual GetExitCodeProcess liveness and generation checks", "final reply required before next case"],
    "prior_inputs":[bind(PRIOR/name) for name in ("control-posttool.py","cursor-file-observer.py",
        "monitor-native-session.py","native-process-state.py","verified-process-exit-state-control.json","process-final-audit.json")],
    "created":[bind(path) for path in sorted(RUN.iterdir()) if path.is_file()],
    "controller":bind(Path(__file__))}
create("controller-adaptation.json", json.dumps(record, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({"status":"prepared-distinct-LF-content-controller","files":len(record["created"]),"model_prompts":0}))
