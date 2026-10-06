"""Retain the failed direct5s effect oracle without inventing a native failure cause."""

import importlib.util
import json
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_direct_sequence_delivery", RUN / "cursor-direct-sequence-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1523-r36-cursor-direct-sequence.json"
assert not REPORT.exists() and not (RUN / "native-direct-sequence-summary.json").exists()
record = probe.read(RUN / "sequence-observation.json")
preparation = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/session.json")
submission = probe.read(RUN / "submission.json")
assert preparation["maximum_prompt_submissions"] == preparation["maximum_model_turns"] == 1
assert submission["prompt"] == preparation["prompt"] and submission["prompt_write"]["session_id"] == submission["enter_write"]["session_id"] == 39922
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
assert definition["timeout_seconds"] == 5 and not definition["observer_invoked"]
assert record["model_final_marker_observed"] and not record["expected_effect_observed"] and not record["bytes_changed"]
assert len(record["policies"]) == 3 and sorted(row["receipt"]["phase"] for row in record["policies"]) == ["advisory", "preflight", "stop"]
assert len(record["event_diagnostic"]) == 1 and record["event_diagnostic"][0]["neutral_tool_matches"] == ["Read"]
assert record["event_diagnostic"][0]["policy"]["receipt"]["decision"] == "allow"
for binding in record["policies"] + record["terminal"] + [record["control"], record["submission"], record["fixture_after"]]:
    assert probe.digest_file(probe.WORK / binding["path"]) == binding["sha256"]
fixture = probe.contained(probe.PROJECT, preparation["relative"])
assert fixture.read_bytes() == (RUN / "fixture-preimage.txt").read_bytes() == (RUN / "fixture-after.txt").read_bytes()
assert probe.digest_file(fixture) == record["before_sha256"] == record["after_sha256"]
exit_record = probe.read(RUN / "terminal-final-observation.json")
assert "exit_code" in exit_record["response"] and "session_id" not in exit_record["response"]
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
forced = probe.read(RUN / "process-stop-force.json")
assert forced["root_pid"] == 19948 and forced["exit_code"] == 0
assert all(row["current"] is None or datetime.fromisoformat(row["current"]) == datetime.fromisoformat(row["expected"]) for row in forced["identity_checks"])
assert all(not probe.read(probe.WORK / binding["path"])["response"]["output"].startswith("Warning: truncated output") for binding in record["terminal"])
doc_note = {"url": "https://cursor.com/docs/hooks", "observed_date": "2026-10-05",
            "facts": {"timeout_unit": "seconds", "failClosed": "hook failures can block the action",
                      "permission_response_validation": "invalid permission JSON/schema can block independently of failClosed"},
            "scope": "current documentation; does not establish failure cause for installed CLI2026.09.15",
            "native_failure_response": "not-retained-in-this-direct-observation"}
probe.atomic_json(RUN / "timeout-doc-note.json", doc_note)
probe.cleanup()
cleanup = probe.read(RUN / "cleanup.json")
summary = {"status": "verified-direct5s-sequence-observation-write-oracle-failed", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "surface": "cursor-cli-interactive-terminal",
    "version": probe.read(RUN / "native-metadata.json")["version"], "model_requested": probe.MODEL, "effort_requested": "xhigh",
    "model_turns": 1, "prompt_submissions": 1, "timeout_seconds": 5, "observer_invoked": False,
    "policy_receipt_count": 3, "inferred_pre_tool": "Read", "actual_effect": "fixture-byte-identical-to-preimage",
    "write_oracle": "failed", "Write_preflight": "not-observed", "pre_delivery_receipts": 0,
    "native_tool_binding": "bounded-neutral-hash-reconstruction; raw native fields unavailable",
    "native_tool_use_id_bound": "unverified-direct-receipts-do-not-retain-native-ID", "native_failure_cause": "unverified",
    "current_documentation": probe.bind(RUN / "timeout-doc-note.json"), "sequence": probe.bind(RUN / "sequence-observation.json"),
    "preparation": probe.bind(RUN / "preparation.json"), "definition": probe.bind(RUN / "definitions/session.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": exit_record["response"]["exit_code"],
    "historical_members_preserved": cleanup["historical_members_unchanged"], "protected_global_configs_unchanged": True,
    "cli_state_hash_before": cleanup["global_cli_hash_before"], "cli_state_hash_after": cleanup["global_cli_hash_after"],
    "cli_state_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"], "global_direct_write": False,
    "full_native_gate": "unchecked", "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-direct-sequence-summary.json", summary)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "policy_receipts": 3, "actual_write": False,
                  "historical_preserved": cleanup["historical_members_unchanged"]}))
