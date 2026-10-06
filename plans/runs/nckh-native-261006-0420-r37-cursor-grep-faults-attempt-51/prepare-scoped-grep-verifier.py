"""Prepare a separate, explicitly scoped verifier; preserve the original failed oracle."""
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
original = RUN / "verify-grep-faults.py"
source = original.read_text(encoding="utf8")
replacements = {
    '"""Verify genuine Grep failures and keep declared fault/late receipt provenance."""':
    '"""Verify native Grep observations while preserving the failed continuous-monitor oracle."""',
    'assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == read(RUN / "monitor-exit.json")["exit_code"] == 0':
    'assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == 0\n'
    'assert read(RUN / "monitor-exit.json")["exit_code"] == 1\n'
    'assert read(RUN / "original-verification-result.json")["exit_code"] == 1\n'
    'correction = read(RUN / "process-ownership-correction.json")\n'
    'assert correction["status"] == "verified-scoped-native51-process-exit-with-historical-capture-correction"\n'
    'assert correction["current_scoped_owned_live"] == correction["current_project_command_matches"] == 0\n'
    'assert correction["raw_precision_live_matches"] == correction["preexisting_applications_preserved"] == 27\n'
    'assert not correction["continuous_monitor_success"]',
    'assert read(RUN / "commands/native-cursor-grep-faults.process-tree.json")["status"] == "root-exited-or-reused"':
    'assert read(RUN / "commands/native-cursor-grep-faults.process-tree.json")["status"] == "running"',
    '"status": "verified-five-current-native-directory-Grep-preflight-fault-observations"':
    '"status": "verified-five-native-directory-Grep-observations-with-monitor-gap"',
    '"native_exit_code": 0, "monitor_exit_code": 0':
    '"native_exit_code": 0, "monitor_exit_code": 1, "continuous_monitor_success": False,\n'
    '    "original_oracle": "failed and preserved; no regrading",\n'
    '    "original_verifier": bind(RUN / "verify-grep-faults.py"),\n'
    '    "original_verification": bind(RUN / "original-verification-result.json"),\n'
    '    "monitor_failure": bind(RUN / "monitor-exit.json"),\n'
    '    "process_ownership_correction": bind(RUN / "process-ownership-correction.json"),\n'
    '    "continuous_capture_after_failure": "unverified"',
    '"process_union_identities": len(audit["tracked"]), "processes_live": 0':
    '"raw_process_union_identities": len(audit["tracked"]),\n'
    '    "raw_precision_live_matches": 27, "preexisting_applications_preserved": 27,\n'
    '    "current_scoped_owned_live": 0,\n'
    '    "current_temporally_valid_captured_identities": correction["current_temporally_valid_captured_identities"]',
    'RUN / "verified-grep-faults.json"': 'RUN / "verified-grep-observations-with-monitor-gap.json"',
    '"native_failure_type": "permission_denied", "process_union": len(audit["tracked"]), "live": 0':
    '"native_failure_type": "permission_denied", "raw_process_union": len(audit["tracked"]),\n'
    '    "current_scoped_owned_live": 0, "monitor_exit_code": 1, "original_oracle": "failed-preserved"',
}
for old, new in replacements.items():
    assert source.count(old) == 1, old
    source = source.replace(old, new)
target = RUN / "verify-grep-observations-with-monitor-gap.py"
compile(source, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(source)
record = {
    "original_verifier": {"path": original.relative_to(WORK).as_posix(), "sha256": sha(original)},
    "scoped_verifier": {"path": target.relative_to(WORK).as_posix(), "sha256": sha(target)},
    "original_file_modified": False, "original_oracle": "failed-preserved",
    "causal_evidence": ["monitor-exit.json", "original-verification-result.json", "process-ownership-correction.json"],
    "scoped_claim": "native callbacks, policy receipts, actual denial metadata, marker integrity and corrected scoped process exit",
    "excluded_claim": "continuous monitor success, full original oracle, general historical zero-live claim",
    "behavior_checks_changed": False, "native_retry": False, "source_kit_modified": False
}
with (RUN / "scoped-verifier-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"prepared": target.name, "original_preserved": True, "native_retries": 0}))
