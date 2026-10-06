"""Preserve the incomplete terminal attempt and remove only its owned hooks."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_interactive_runtime", RUN / "cursor-interactive-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
assert not (RUN / "native-interactive-summary.json").exists()
preparation = probe.read(RUN / "preparation.json")
terminal = probe.read(RUN / "terminal-observations.json")
assert terminal[-1]["response"]["exit_code"] == 1
assert "session_id" not in terminal[-1]["response"]
assert sum(row.get("operation") == "submit-one-prepared-prompt" for row in terminal) == 1
assert any("Grok 4.7 500K Extra High" in row["response"]["output"] for row in terminal)
assert any("Press Ctrl+C again to exit" in row["response"]["output"] for row in terminal)
stop = probe.read(RUN / "process-stop-force.json")
assert stop["exit_code"] == 0 and stop["root_pid"] == 47492
assert all(row["expected"] == row["current"] for row in stop["identity_checks"])
fixture = probe.contained(probe.PROJECT, preparation["fixture_relative"])
assert probe.digest_file(fixture) == preparation["fixture_sha256"]
callbacks = sorted((probe.EVIDENCE / "observations").rglob("*.json"))
policies = sorted((probe.EVIDENCE / "policy-receipts").rglob("*.json"))
assert len(callbacks) == 1 and probe.read(callbacks[0])["event"] == "sessionStart"
assert len(policies) == 1
record = {
    "status": "incomplete-interactive-prompt-submission-not-observed",
    "source_revision": 36,
    "source_lock_hash": probe.EXPECTED,
    "source_modified": False,
    "surface": "cursor-cli-interactive-terminal",
    "model_requested": probe.MODEL,
    "effort_requested": "xhigh",
    "native_model_label": "Grok 4.7 500K Extra High · MAX",
    "native_permission_label": "Run Everything",
    "prepared_model_turns": 1,
    "model_turns_verified": 0,
    "native_prompt_submission": "not-observed",
    "native_tool_attempt": "not-observed",
    "callback_bindings": [{**probe.bind(path), "receipt": probe.read(path)} for path in callbacks],
    "policy_receipts": [{**probe.bind(path), "receipt": probe.read(path)} for path in policies],
    "definition": probe.bind(RUN / "definitions/interactive-public-read.json"),
    "fixture": {"path": preparation["fixture_relative"], "sha256": preparation["fixture_sha256"], "unchanged": True},
    "terminal": probe.bind(RUN / "terminal-observations.json"),
    "process_tree": probe.bind(RUN / "process-tree-before-turn.json"),
    "graceful_stop": probe.bind(RUN / "process-stop-graceful.json"),
    "force_stop": probe.bind(RUN / "process-stop-force.json"),
    "terminal_exit_code": 1,
    "process_cleanup": "owned-tree-force-stopped-after-graceful-refusal",
    "backend_attestation": "not-observed",
    "billing": "not-observed",
    "full_native_gate": "unchecked",
    "verifier": probe.bind(Path(__file__)),
}
probe.cleanup()
record["cleanup"] = probe.bind(RUN / "cleanup.json")
probe.atomic_json(RUN / "native-interactive-summary.json", record)
print(json.dumps({"status": record["status"], "model_turns_verified": 0, "callbacks": 1}))
