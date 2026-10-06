"""Verify real observations and retain the failure to exercise a native mutation."""

import importlib.util
import json
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_existing_delivery", RUN / "cursor-existing-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1415-r36-cursor-existing-mutations.json"
assert not REPORT.exists() and not (RUN / "native-existing-summary.json").exists()
preparation = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/session.json")
metadata = probe.read(RUN / "native-metadata.json")
assert preparation["maximum_model_turns"] == preparation["maximum_prompt_submissions"] == 3
assert definition["timeout_seconds"] == 5 and not definition["observer_invoked"]
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
stage = probe.read(RUN / "stage.json")
for handlers in definition["config"]["hooks"].values():
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    assert stage["runner"] in handlers[0]["command"] and str(probe.OBSERVER) not in handlers[0]["command"]
submissions = sorted((RUN / "submissions").glob("[0-9][0-9].json"))
assert len(submissions) == 3
diagnostic = probe.read(RUN / "event-binding-diagnostic.json")
assert len(diagnostic["rows"]) == 3 and all(len(row["matches"]) == 1 for row in diagnostic["rows"])
inferred = {row["index"]: row["matches"][0] for row in diagnostic["rows"]}
cases = []
case_policy_paths = set()
for expected, submission_path in zip(preparation["cases"], submissions):
    index = expected["index"]
    submission = probe.read(submission_path)
    assert submission["case"]["index"] == index and submission["case"]["prompt"] == expected["prompt"]
    assert submission["prompt_write"]["session_id"] == submission["enter_write"]["session_id"] == 24065
    assert inferred[index] == {"tool": "Read", "paths": [expected["relative"]], "stop_active": False}
    path = RUN / "attempts" / f"{index:02d}.json"
    attempt = probe.read(path)
    assert attempt["ready_for_next_case"] and attempt["model_final_marker_observed"]
    assert attempt["preflight_count"] == attempt["stop_count"] == 1
    assert attempt["source_lock_hash"] == probe.EXPECTED
    for binding in attempt["policies"] + attempt["terminal"] + [expected["preimage"]]:
        assert probe.digest_file(probe.WORK / binding["path"]) == binding["sha256"]
    assert all(binding["receipt"]["context_hash"] == attempt["context"]["context_file_sha256"] for binding in attempt["policies"])
    assert sorted(binding["receipt"]["phase"] for binding in attempt["policies"]) == ["advisory", "preflight", "stop"]
    case_policy_paths.update(binding["path"] for binding in attempt["policies"])
    policy = next(binding["receipt"] for binding in attempt["policies"] if binding["receipt"]["phase"] == "preflight")
    assert policy["decision"] == ("block" if index == 3 else "allow")
    assert policy["reason_codes"] == (["private-holdout-credential-path"] if index == 3 else ["declared-route-checks-current"])
    current = probe.contained(probe.PROJECT, expected["relative"])
    assert current.read_bytes() == probe.contained(probe.WORK, expected["preimage"]["path"]).read_bytes()
    assert probe.digest_file(current) == attempt["after_sha256"] == expected["before_sha256"]
    assert attempt["expected_effect_observed"] == (index != 1)
    cases.append({"case": expected, "observation": probe.bind(path), "submission": probe.bind(submission_path),
                  "inferred_neutral_event": inferred[index], "preflight": policy,
                  "actual_sha256": probe.digest_file(current), "effect_oracle_matches": attempt["expected_effect_observed"],
                  "qualification": "requested-mutation-not-observed"})
extra_policies = [probe.bind(path) for path in sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))
                  if probe.bind(path)["path"] not in case_policy_paths]
assert len(extra_policies) == 1 and probe.read(probe.WORK / extra_policies[0]["path"])["phase"] == "advisory"
exit_record = probe.read(RUN / "terminal-final-observation.json")
assert "exit_code" in exit_record["response"] and "session_id" not in exit_record["response"]
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and not audit["matches"]
graceful = probe.read(RUN / "process-stop-graceful.json")
forced = probe.read(RUN / "process-stop-force.json")
assert graceful["root_pid"] == forced["root_pid"] == 30356 and graceful["exit_code"] == 128 and forced["exit_code"] == 0
assert all(row["current"] is None or datetime.fromisoformat(row["current"]) == datetime.fromisoformat(row["expected"])
           for row in forced["identity_checks"])
terminal = []
truncated = []
for path in sorted((RUN / "terminal").glob("*.json")):
    terminal.append(probe.bind(path))
    if probe.read(path)["response"]["output"].startswith("Warning: truncated output"):
        truncated.append(probe.bind(path))
assert len(truncated) == 1
probe.cleanup()
cleanup = probe.read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and not cleanup["config_callable"]
record = {"status": "verified-existing-file-observations-mutation-route-unqualified", "source_revision": 36,
          "source_lock_hash": probe.EXPECTED, "source_modified": False, "surface": "cursor-cli-interactive-terminal",
          "version": metadata["version"], "model_requested": probe.MODEL, "effort_requested": "xhigh",
          "selected_model": metadata["selected_model"], "model_turns": 3, "prompt_submissions": 3,
          "timeout_seconds": 5, "observer_invoked": False, "cases": cases,
          "inferred_tool_counts": {"Read": 3, "Write": 0}, "policy_receipt_count": 9,
          "additional_startup_policy_receipts": extra_policies, "observed_policy_phases": ["advisory", "preflight", "stop"],
          "pre_delivery_receipts": 0, "native_tool_binding_method": "bounded-hash-reconstruction; raw callback payload not retained",
          "actual_fixture_effects": "all-three-existing-fixtures-byte-identical-to-preimages",
          "public_write_oracle": "failed", "plan_only_mutation_denial": "unqualified-observed-Read-allow",
          "private_observation": "scoped-Read-block-with-unchanged-file; mutation-not-qualified",
          "raw_native_tool_results": "not-captured", "truncated_terminal_chunks": truncated,
          "terminal_transcript_scope": "bounded-harness-chunks; one chunk truncated; no full-transcript claim",
          "preparation": probe.bind(RUN / "preparation.json"), "definition": probe.bind(RUN / "definitions/session.json"),
          "event_diagnostic": probe.bind(RUN / "event-binding-diagnostic.json"), "terminal": terminal,
          "terminal_start": probe.bind(RUN / "terminal-start-observation.json"),
          "terminal_ready": probe.bind(RUN / "terminal-ready-observation-01.json"),
          "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"),
          "terminal_exit_code": exit_record["response"]["exit_code"], "process_audit": probe.bind(RUN / "final-process-audit.json"),
          "graceful_stop": probe.bind(RUN / "process-stop-graceful.json"), "force_stop": probe.bind(RUN / "process-stop-force.json"),
          "cleanup": probe.bind(RUN / "cleanup.json"), "historical_members_preserved": cleanup["historical_members_unchanged"],
          "protected_global_configs_unchanged": True, "global_direct_write": False,
          "cli_state_hash_before": cleanup["global_cli_hash_before"], "cli_state_hash_after": cleanup["global_cli_hash_after"],
          "cli_state_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"],
          "report_correction": probe.bind(RUN / "report-correction.json"),
          "agy_window_recovery": probe.bind(RUN / "agy-window-recovery-observation.json"),
          "full_native_gate": "unchecked", "backend_attestation": "not-observed", "billing": "not-observed",
          "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-existing-summary.json", record)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "model_turns": 3, "inferred_tools": record["inferred_tool_counts"],
                  "policy_receipts": 9, "historical_preserved": record["historical_members_preserved"],
                  "cli_state_hash_unchanged": record["cli_state_hash_unchanged"]}))
