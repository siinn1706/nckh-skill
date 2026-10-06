"""Observe genuine prompt, stop, and read callbacks on the ACP route."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stage = load("r36_cursor_acp_runtime", RUN / "cursor-acp-runtime.py")
parameter_base = WORK / "plans/runs/nckh-native-261005-1118-r36-cursor-acp-parameters-attempt-03/acp-parameter-control.py"
acp = load("r36_cursor_acp_parameter_client", parameter_base)


def observe(label, prompt, fixture=None):
    stage.check_source()
    turn_dir = RUN / "attempts" / label
    turn_dir.mkdir(parents=True, exist_ok=False)
    target = turn_dir / "native-turn.json"
    definition = stage.register("allow", label)
    acp.RUN = turn_dir
    acp.probe.RUN = turn_dir
    argv = [str(p) for p in stage.q.installed_commands()["cursor"]] + [
        "--workspace", str(stage.PROJECT), "--model", stage.MODEL,
        "--force", "--trust", "--sandbox", "disabled", "acp"]
    record = {"status": "starting", "attempt": label, "owner": "/root", "port": None,
        "argv": argv, "cwd": str(stage.PROJECT), "source_revision": 36,
        "source_lock_hash": stage.EXPECTED, "model_requested": stage.MODEL,
        "effort_requested": "xhigh", "model_turns": 0, "started_at": acp.probe.now(),
        "definition": stage.bind(RUN / "definitions" / (label + ".json")),
        "prompt_sha256": acp.probe.hashlib.sha256(prompt.encode()).hexdigest(),
        "fault_origin": "none", "observer_invoked": False, "timeout_seconds": 5,
        "surface": "cursor-cli-acp", "backend_attestation": "not-observed", "billing": "not-observed"}
    stage.atomic_json(target, record)
    process = None
    try:
        with (turn_dir / "native-transcript.jsonl").open("x", encoding="utf8") as transcript:
            with (turn_dir / "native.stderr").open("xb") as stderr:
                with acp.probe.owned_process(argv, stage.PROJECT, subprocess.PIPE, stderr) as (process, job):
                    record.update(pid=process.pid, status="running")
                    stage.atomic_json(target, record)
                    client = acp.ParameterClient(process, transcript)
                    initialized = client.request("initialize", {"protocolVersion": 1,
                        "clientInfo": {"name": "nckh-bounded-acp-observer", "version": "1"},
                        "clientCapabilities": {"fs": {"readTextFile": False, "writeTextFile": False},
                            "terminal": False}}, timeout=45)
                    record["initialize"] = initialized
                    assert not initialized.get("error"), "ACP initialization rejected"
                    session = client.request("session/new", {"cwd": str(stage.PROJECT), "mcpServers": []}, timeout=90)
                    record["session_new"] = session
                    assert not session.get("error"), "ACP session creation rejected"
                    selection = stage.read(turn_dir / "parameter-selector-result.json")
                    assert selection["exact_granted_parameters_verified"]
                    record["parameter_selector"] = stage.bind(turn_dir / "parameter-selector-result.json")
                    stage.check_source()
                    assert stage.digest_file(stage.CONFIG) == definition["config_sha256"]
                    record["model_turns"] = 1
                    stage.atomic_json(target, record)
                    result = client.request("session/prompt", {"sessionId": session["result"]["sessionId"],
                        "prompt": [{"type": "text", "text": prompt}]}, timeout=270)
                    record["prompt_response"] = result
                    process.stdin.close()
                    try:
                        process.wait(timeout=5)
                        record["native_exit_after_stdin_close"] = True
                    except subprocess.TimeoutExpired:
                        record["native_exit_after_stdin_close"] = False
                    record.update(status="recorded-native-acp-turn")
    except Exception as error:
        record.update(status="failed-native-acp-turn", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record.update(ended_at=acp.probe.now(), process_exited=process.poll() is not None if process else None,
            exit_code=process.returncode if process else None, process_cleanup="owned-process-group-closed")
        policies = sorted((stage.EVIDENCE / "policy-receipts" / label).glob("*.json"))
        record["policy_receipts"] = [{**stage.bind(p), "receipt": stage.read(p)} for p in policies]
        record["fixture"] = {"path": fixture.relative_to(stage.PROJECT).as_posix(),
            "sha256": stage.digest_file(fixture), "content_unchanged": fixture.read_bytes() == b"NCKH_ACP_SYNTHETIC_READ_FIXTURE\n"} if fixture else None
        record["transcript"] = stage.bind(turn_dir / "native-transcript.jsonl")
        record["stderr"] = stage.bind(turn_dir / "native.stderr")
        record["source_unchanged"] = acp.probe.digest_record(acp.probe.verify_source_lock(WORK / "nckh-kit")) == stage.EXPECTED
        stage.atomic_json(target, record)
    print(json.dumps({"attempt": label, "status": record["status"], "model_turns": record["model_turns"],
        "policy_phases": [p["receipt"].get("phase") for p in record["policy_receipts"]],
        "process_exited": record["process_exited"]}), flush=True)
    return stage.bind(target)


if __name__ == "__main__":
    summary_path = RUN / "native-acp-summary.json"
    assert not summary_path.exists()
    stage.atomic_json(RUN / "preparation.json", {"maximum_model_turns": 2,
        "source_revision": 36, "source_lock_hash": stage.EXPECTED, "source_modified": False,
        "scope": "Fresh no-tool and public Read ACP sessions with direct packaged-runner hooks",
        "timeout_seconds": 5, "fault_origin": "none", "observer_invoked": False,
        "parameter_client": stage.bind(parameter_base), "controller": stage.bind(Path(__file__))})
    stage.prepare()
    summary = {"status": "running", "results": [], "source_revision": 36,
        "source_lock_hash": stage.EXPECTED, "full_native_gate": "unchecked"}
    stage.atomic_json(summary_path, summary)
    try:
        no_tool = observe("acp-no-tool", "Reply exactly NCKH_ACP_SYNTHETIC_REPLY and stop. Do not call any tool, inspect files, run commands, use agents, or change any file.")
        summary["results"].append({"attempt": "acp-no-tool", "receipt": no_tool})
        stage.atomic_json(summary_path, summary)
        fixture = stage.contained(stage.PROJECT, "oracles/r36-acp-public-read-04.txt")
        assert not fixture.exists()
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_bytes(b"NCKH_ACP_SYNTHETIC_READ_FIXTURE\n")
        read_control = observe("acp-public-read", "Use the native Read tool exactly once to read oracles/r36-acp-public-read-04.txt in this authorized scratch project. This file contains a synthetic test marker only. Do not call another tool, shell, agents, inspect other files, retry, or work around a tool or hook denial. After the single attempted Read, say ORACLE_ATTEMPT_FINISHED and stop.", fixture)
        summary["results"].append({"attempt": "acp-public-read", "receipt": read_control})
        summary.update(status="recorded-native-acp-controls", source_modified=False)
        stage.atomic_json(summary_path, summary)
    except Exception as error:
        stage.atomic_json(RUN / "native-acp-failure.json", {"error_type": type(error).__name__,
            "error": str(error), "raw_running_summary_preserved": True, "completed_attempts": len(summary["results"])})
        raise
    finally:
        stage.cleanup()
