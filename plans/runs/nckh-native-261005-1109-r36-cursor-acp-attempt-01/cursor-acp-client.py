"""Retain native ACP metadata before submitting an explicitly granted model turn."""

import argparse
import hashlib
import importlib.util
import json
import queue
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
MODEL = "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
EXPECTED = "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record
from core.processes import owned_process

spec = importlib.util.spec_from_file_location("cursor_acp_commands", WORK / "plans/runs/nckh-native-261004-1707-attempt-01/qualification-run.py")
commands = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands)
now = lambda: datetime.now(timezone.utc).isoformat()


def protected_snapshot():
    return {str(p): digest_file(p) if p.is_file() else None for p in [
        Path(r"C:/Users/USER") / relative for relative in (
            ".cursor/hooks.json", ".cursor/mcp.json", ".cursor/plugins/installed_plugins.json",
            ".cursor/plugins/settings.json")
    ]}


class Client:
    def __init__(self, process, transcript):
        self.process, self.transcript = process, transcript
        self.inbox = queue.Queue()
        self.next_id = 0
        self.lock = threading.Lock()
        self.responses = []
        self.reader_error = None
        self.thread = threading.Thread(target=self.read, daemon=True)
        self.thread.start()

    def log(self, direction, message):
        with self.lock:
            self.transcript.write(json.dumps({"recorded_at": now(), "direction": direction,
                "message": message}, ensure_ascii=False) + "\n")
            self.transcript.flush()

    def read(self):
        try:
            for line in self.process.stdout:
                try:
                    message = json.loads(line)
                except ValueError:
                    self.log("received-non-json", {"sha256": hashlib.sha256(line).hexdigest(), "length": len(line)})
                    continue
                self.log("received", message)
                self.inbox.put(message)
        except Exception as error:
            self.reader_error = str(error)
        finally:
            self.inbox.put({"reader_eof": True})

    def send(self, message):
        self.log("sent", message)
        self.process.stdin.write((json.dumps(message, ensure_ascii=False) + "\n").encode())
        self.process.stdin.flush()

    def server_request(self, message):
        method = message["method"]
        if method == "session/request_permission":
            options = message.get("params", {}).get("options", [])
            rejected = next((o.get("optionId") for o in options if o.get("kind") == "reject_once"), None)
            outcome = {"outcome": "selected", "optionId": rejected} if rejected else {"outcome": "cancelled"}
            self.send({"jsonrpc": "2.0", "id": message["id"], "result": {"outcome": outcome}})
        elif method == "cursor/ask_question":
            self.send({"jsonrpc": "2.0", "id": message["id"], "result": {
                "outcome": {"outcome": "skipped", "reason": "Bounded synthetic probe; no human answer is fabricated."}}})
        else:
            self.send({"jsonrpc": "2.0", "id": message["id"], "error": {
                "code": -32601, "message": "This read-only metadata client does not implement that capability."}})

    def request(self, method, params, timeout):
        self.next_id += 1
        identifier = self.next_id
        self.send({"jsonrpc": "2.0", "id": identifier, "method": method, "params": params})
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("ACP request did not complete: " + method)
            try:
                message = self.inbox.get(timeout=remaining)
            except queue.Empty:
                raise TimeoutError("ACP request did not complete: " + method)
            if message.get("reader_eof"):
                raise RuntimeError("Native ACP stream closed during " + method)
            if message.get("id") == identifier and "method" not in message:
                self.responses.append({"method": method, "message": message})
                return message
            if "method" in message and "id" in message:
                self.server_request(message)


def metadata():
    assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
    assert PROJECT.is_dir() and not (PROJECT / ".cursor/hooks.json").exists()
    target = RUN / "acp-metadata.json"
    assert not target.exists()
    before = protected_snapshot()
    argv = [str(p) for p in commands.installed_commands()["cursor"]] + [
        "--workspace", str(PROJECT), "--model", MODEL, "--force", "--trust", "--sandbox", "disabled", "acp"]
    record = {"status": "starting", "owner": "/root", "port": None, "command": argv,
        "cwd": str(PROJECT), "source_revision": 36, "source_lock_hash": EXPECTED,
        "model_requested": MODEL, "model_turns": 0, "hook_registration": "not-performed",
        "global_direct_write": False, "started_at": now()}
    atomic_json(target, record)
    process = None
    try:
        with (RUN / "metadata-transcript.jsonl").open("x", encoding="utf8") as transcript:
            with (RUN / "metadata-native.stderr").open("xb") as stderr:
                with owned_process(argv, PROJECT, subprocess.PIPE, stderr) as (process, job):
                    record.update(pid=process.pid, status="running")
                    atomic_json(target, record)
                    client = Client(process, transcript)
                    initialized = client.request("initialize", {"protocolVersion": 1,
                        "clientInfo": {"name": "nckh-bounded-acp-observer", "version": "1"},
                        "clientCapabilities": {"fs": {"readTextFile": False, "writeTextFile": False},
                            "terminal": False}}, timeout=45)
                    record["initialize"] = initialized
                    atomic_json(target, record)
                    if initialized.get("error"):
                        raise RuntimeError("Native ACP initialization rejected")
                    session = client.request("session/new", {"cwd": str(PROJECT), "mcpServers": []}, timeout=90)
                    record["session_new"] = session
                    atomic_json(target, record)
                    if session.get("error"):
                        raise RuntimeError("Native ACP session creation rejected; no inference submitted")
                    sid = session["result"]["sessionId"]
                    record["session_id"] = sid
                    capabilities = initialized["result"].get("agentCapabilities", {}).get("sessionCapabilities", {})
                    if "close" in capabilities:
                        record["session_close"] = client.request("session/close", {"sessionId": sid}, timeout=15)
                    process.stdin.close()
                    try:
                        process.wait(timeout=5)
                        record["native_exit_after_stdin_close"] = True
                    except subprocess.TimeoutExpired:
                        record["native_exit_after_stdin_close"] = False
                    record.update(status="recorded-native-acp-metadata-no-inference")
    except Exception as error:
        record.update(status="failed-native-acp-metadata-no-inference", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record.update(ended_at=now(), process_exited=process.poll() is not None if process else None,
            exit_code=process.returncode if process else None, protected_global_hashes_before=before,
            protected_global_hashes_after=protected_snapshot(), process_cleanup="owned-process-group-closed")
        record["protected_global_configs_unchanged"] = record["protected_global_hashes_before"] == record["protected_global_hashes_after"]
        record["source_unchanged"] = digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
        atomic_json(target, record)
    print(json.dumps({"status": record["status"], "model_turns": 0,
        "session_response_fields": sorted(record["session_new"]["result"]),
        "process_exited": record["process_exited"]}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["metadata"])
    parser.parse_args()
    metadata()
