"""Prepare and record current-r37 Cursor Write post-tool observations; no model retries."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = RUN.parent / "nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51"
MODES = ("allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def new(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as stream:
        stream.write(text)

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def runtime():
    probe = load("posttool_runtime", RUN / "cursor-posttool-runtime.py")
    owned = load("posttool_owned", RUN / "owned-cli-command.py")
    probe.OBSERVER = RUN / "cursor-file-observer.py"
    probe.q.run_command = owned.run_command
    return probe, owned

def prepare():
    audit = read(RUN / "process-preflight-audit.json")
    assert audit["matching_count"] == audit["tracked_live_count"] == 0
    assert audit["prior_temporally_valid_identities"] == 612 and not audit["legacy_raw_union_used_as_ownership"]
    probe, owned = runtime()
    probe.prepare()
    metadata = read(RUN / "native-metadata.json")
    assert metadata["version"] == "2026.09.15-d2fe57e"
    assert metadata["selected_model"]["modelId"] == "grok-4.7"
    assert {row["id"]:row["value"] for row in metadata["selected_model"]["parameters"]} == {
        "context":"500k","reasoning_effort":"xhigh","fast":"false"}
    stage = read(RUN / "stage.json")
    probe.atomic_json(probe.EVIDENCE / "probe-control.json", {"mode":"allow","attempt":"startup","selected_event":"postToolUse"})
    config = json.loads(json.dumps(stage["preview"]["after"]))
    for event, handlers in config["hooks"].items():
        assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
        handlers[0]["command"] = subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(probe.OBSERVER),
            "--host", "cursor", "--event", event, "--project", str(probe.PROJECT), "--evidence", str(probe.EVIDENCE),
            "--runner", stage["runner"], "--callback-source", "project"])
        if event in {"preToolUse","postToolUse"}:
            handlers[0]["matcher"] = "^Write$"
    probe.atomic_json(probe.CONFIG, config)
    cases, fixtures = [], []
    for index, mode in enumerate(MODES,1):
        relative = (probe.EVIDENCE.relative_to(probe.PROJECT) / "public" / ("posttool-" + mode + ".txt")).as_posix()
        before = ("NCKH_POSTTOOL_PUBLIC_BEFORE_53_" + str(index) + "\r\n").encode()
        expected = ("NCKH_POSTTOOL_PUBLIC_AFTER_53_" + str(index) + "\r\n").encode()
        native_content = ("NCKH_POSTTOOL_PUBLIC_AFTER_53_" + str(index) + "\n").encode("ascii")
        fixture = probe.PROJECT / relative
        fixture.parent.mkdir(parents=True, exist_ok=True)
        with fixture.open("xb") as stream:
            stream.write(before)
        marker = "NCKH_POSTTOOL_FINISHED_53_" + str(index)
        prompt = ("First Read " + relative + " if required, then use the native Write file-edit operation exactly once. "
            "Replace the ENTIRE file contents with the text NCKH_POSTTOOL_PUBLIC_AFTER_53_" + str(index) +
            " followed by exactly one LF (U+000A) in the native Write content argument. Include no CR (U+000D) in that argument. "
            "This is an authorized controller-owned public synthetic marker file. Read prerequisites are allowed only on this exact file. "
            "Do not use another edit tool, shell/terminal, another file, agents, retries, or workarounds after a hook error. "
            "After the selected attempt reply exactly " + marker + " and stop.")
        cases.append({"index":index,"mode":mode,"attempt":"posttool-"+mode,"relative":relative,
            "before_hex":before.hex(),"before_sha256":sha(fixture),"expected_hex":expected.hex(),
            "expected_sha256":hashlib.sha256(expected).hexdigest(),"marker":marker,"prompt":prompt,
            "expected_content_hex":native_content.hex(),"expected_content_sha256":hashlib.sha256(native_content).hexdigest(),
            "expected_content_length":len(native_content),"expected_content_tail_hex":native_content[-16:].hex(),
            "maximum_prompt_submissions":1,"maximum_requested_Writes":1})
        fixtures.append({"path":relative,"sha256":sha(fixture)})
    definition = {"config_sha256":sha(probe.CONFIG),"config":config,"extra_configs":fixtures,
        "source_lock_hash":probe.EXPECTED,"definition_kind":"bounded-posttool-Write-observations",
        "observer":bind(probe.OBSERVER),"postToolUse_timeout_seconds":5,"inner_runner_timeout_seconds":5,
        "injected_sleep_seconds":8,"selected_matcher":"^Write$"}
    probe.atomic_json(RUN / "definitions/session.json",definition)
    probe.atomic_json(RUN / "last-definition.json",definition)
    frozen = {"status":"prepared-seven-current-Write-posttool-cases","project":str(probe.PROJECT),"model":probe.MODEL,
        "source_revision":37,"source_lock_hash":probe.EXPECTED,"version":metadata["version"],"surface":"cursor-cli-interactive",
        "event":"postToolUse","tool":"Write","cases":cases,"maximum_model_turns":7,"model_retries":0,"whole_turn_deadline":None,
        "oracle":"one genuine matching Write pre/post per case; frozen bytes present at post callback start; final marker; preserve actual hook outcomes",
        "normal_policy_expected":"advisory/delivery-bindings-current-review-separate",
        "deny_policy_expected":"block/bounded-input-exceeded from33 declared empty references, selected post only",
        "fault_origin":"controller injection after genuine callback for five faults; none for allow/policy-deny",
        "postToolUse_timeout_seconds":5,"injected_sleep_seconds":8,"preToolUse_timeout_seconds":20,"inner_runner_timeout_seconds":5,
        "unsupported_scope":"selected codec injection only; unknown-host-event admission remains unqualified",
        "scope_limit":"Read prerequisites outside Write matcher; no all-tools/preventive rollback/scientific QA claim",
        "newline_scope":"LF in actual native content argument; prospective Windows CRLF disk oracle; native44 and52 failures preserved",
        "diagnostic_scope":"hash/length/tail16 only for exact public synthetic marker; raw content not retained",
        "model_selection_source":"existing selectedModel; --model omitted","global_direct_write":False,
        "definition":bind(RUN / "definitions/session.json"),"full_native_gate":"unchecked"}
    probe.atomic_json(RUN / "preparation.json",frozen)
    probe.atomic_json(RUN / "frozen-brief.json",frozen)
    print(json.dumps({"status":frozen["status"],"cases":7,"payload_members":len(stage["staged_members"])}))

def select(index):
    probe, owned = runtime()
    frozen = read(RUN / "frozen-brief.json")
    case = frozen["cases"][index-1]
    assert sha(probe.CONFIG) == read(RUN / "last-definition.json")["config_sha256"]
    assert sha(probe.PROJECT / case["relative"]) == case["before_sha256"]
    if index > 1:
        assert read(RUN / "cases" / (frozen["cases"][index-2]["attempt"]+".json"))["status"] == "recorded-current-Write-posttool-observation"
    target = RUN / "selected" / (case["attempt"]+".json")
    assert not target.exists(), "Preserve prior selection; no model retry"
    context = read(probe.EVIDENCE / "context-allow.json")
    context.update(task_id="native-cursor-posttool-lf-r37-53-"+str(index),
        artifact_sha256=case["expected_sha256"],artifact={"path":case["relative"],"sha256":case["expected_sha256"]},
        tool_operations={"Write":"write"},allowed_operations=["write"])
    probe.atomic_json(probe.EVIDENCE / "context-allow.json",context)
    probe.atomic_json(probe.EVIDENCE / "context-deny.json",{**context,"references":[{} for _ in range(33)]})
    control = {"mode":case["mode"],"attempt":case["attempt"],"selected_event":"postToolUse",
        "marker_relative":case["relative"],"expected_marker_sha256":case["expected_sha256"],
        "native_marker_prefix":"NCKH_POSTTOOL_PUBLIC_AFTER_53_"+str(index),
        "expected_content_sha256":case["expected_content_sha256"]}
    probe.atomic_json(probe.EVIDENCE / "probe-control.json",control)
    probe.atomic_json(target,{**case,"control_sha256":sha(probe.EVIDENCE / "probe-control.json"),
        "context_hashes":{name:sha(probe.EVIDENCE/name) for name in ("context-allow.json","context-deny.json")}})
    print(json.dumps({"attempt":case["attempt"],"prompt":case["prompt"]}))

def collect(index):
    probe, owned = runtime()
    frozen = read(RUN / "frozen-brief.json")
    case = frozen["cases"][index-1]
    paths = sorted((probe.EVIDENCE / "observations" / case["attempt"]).glob("*/*.json"))
    callbacks = [read(path) for path in paths]
    assert any(row["event"] == "stop" for row in callbacks), "Wait for actual Stop"
    pre = [row for row in callbacks if row["event"] == "preToolUse"]
    post = [row for row in callbacks if row["event"] == "postToolUse"]
    assert len(pre) == len(post) == 1 and pre[0]["native_tool_name"] == post[0]["native_tool_name"] == "Write"
    assert pre[0]["native_tool_use_id"] == post[0]["native_tool_use_id"]
    for row in pre+post:
        assert row["native_tool_use_id"] and (probe.PROJECT / row["native_path_fields"]["file_path"]).resolve() == (probe.PROJECT / case["relative"]).resolve()
    for row in pre+post:
        diagnostic = row.get("native_content_diagnostics", {})
        assert diagnostic.get("synthetic_marker_only"), "Actual bounded content diagnostic is required"
        assert diagnostic["sha256"] == case["expected_content_sha256"], "Native content LF oracle failed"
        assert diagnostic["utf8_length"] == case["expected_content_length"]
        assert diagnostic["tail_hex"] == case["expected_content_tail_hex"]
    import re
    terminal_paths = sorted(RUN.glob("terminal-"+str(index).zfill(2)+"-*.json"))
    outputs = "\n".join(read(path).get("output", "") for path in terminal_paths)
    outputs = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", outputs)
    outputs = re.sub(r"\x1b\][^\x07]*\x07", "", outputs)
    assert re.search(r"(?:^|\n)  "+re.escape(case["marker"])+r"\r?\n", outputs), "Actual native final marker required"
    assert post[0]["marker_exists_at_callback_start"] and post[0]["marker_at_callback_start_sha256"] == case["expected_sha256"]
    states = load("actual_process_state", RUN / "native-process-state.py")
    process_states = []
    for row in callbacks:
        for pid_key,ticks_key in (("observer_pid","observer_creation_filetime_ticks"),("runner_pid","runner_creation_filetime_ticks")):
            if row.get(pid_key):
                current = states.state(row[pid_key])
                expected = row.get(ticks_key)
                assert expected is not None and current["status"] != "unobservable", "Unobservable selected process"
                assert not (current["status"] == "active" and current["creation_filetime_ticks"] == expected), "Selected process still active"
                process_states.append({"expected_creation_ticks":expected, **current})
    fixture = probe.PROJECT / case["relative"]
    assert fixture.read_bytes() == bytes.fromhex(case["expected_hex"]), "Frozen marker byte oracle failed; stop dependent cases"
    receipts = sorted((probe.EVIDENCE / "policy-receipts" / case["attempt"]).glob("*/*.json"))
    output = RUN / "marker-after" / (case["attempt"]+".txt")
    output.parent.mkdir(exist_ok=True)
    with output.open("xb") as stream:
        stream.write(fixture.read_bytes())
    definition = read(RUN / "last-definition.json")
    for item in definition["extra_configs"]:
        if item["path"] == case["relative"]:
            item["sha256"] = case["expected_sha256"]
    probe.atomic_json(RUN / "last-definition.json",definition)
    record = {"status":"recorded-current-Write-posttool-observation","attempt":case["attempt"],"mode":case["mode"],
        "selected":bind(RUN / "selected" / (case["attempt"]+".json")),"callbacks":[bind(path) for path in paths],
        "policy_receipts":[bind(path) for path in receipts],"marker_after":bind(output),"marker_exact":True,
        "marker_before_post":True,"selected_observers_terminal":True,"native_content_LF_exact":True,"selected_process_states":process_states,"native_tool_use_id":pre[0]["native_tool_use_id"],
        "timestamp_utc":datetime.now(timezone.utc).isoformat()}
    target = RUN / "cases" / (case["attempt"]+".json")
    assert not target.exists()
    probe.atomic_json(target,record)
    print(json.dumps({"status":record["status"],"attempt":case["attempt"],"callbacks":len(paths),"receipts":len(receipts),
        "post_status":post[0]["status"],"marker_before_post":True}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action",choices=["prepare","select","collect","cleanup"])
    parser.add_argument("--index",type=int,choices=range(1,8))
    args = parser.parse_args()
    if args.action == "prepare": prepare()
    elif args.action == "select": select(args.index)
    elif args.action == "collect": collect(args.index)
    else:
        probe, owned = runtime()
        probe.check_source()
        probe.cleanup()
