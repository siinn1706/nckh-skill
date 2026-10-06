"""Bind factual prose corrections to retained cleanup evidence without rewriting history."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
read = lambda path: json.loads(path.read_text(encoding="utf8"))
target = RUN / "report-correction.json"
assert not target.exists()
evidence = []
for name in ("nckh-native-261005-1257-r36-cursor-prompt-stop-faults-attempt-07",
             "nckh-native-261005-1340-r36-cursor-direct-interactive-attempt-08"):
    cleanup_path = WORK / "plans/runs" / name / "cleanup.json"
    cleanup = read(cleanup_path)
    assert cleanup["status"] == "pass" and cleanup["global_direct_write"] is False
    assert cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"]
    assert all(row["sha256"] == row["current_sha256"] for row in cleanup["protected_global_config"])
    evidence.append({"cleanup": bind(cleanup_path), "global_direct_write": False,
                     "protected_config_hashes_unchanged": True,
                     "cli_state_hash_before": cleanup["global_cli_hash_before"],
                     "cli_state_hash_after": cleanup["global_cli_hash_after"],
                     "cli_state_hash_equal": False, "exact_changed_fields": "unknown-no-full-before-image"})
documents = []
for preimage in sorted((RUN / "report-correction-preimages").glob("*.md")):
    if preimage.name.startswith("phase-"):
        current = PLAN / preimage.name
    elif preimage.name.startswith("delivery-"):
        current = WORK / "plans/reports" / preimage.name
    else:
        current = WORK / "plans/journals" / preimage.name
    assert sha(preimage) != sha(current)
    text = current.read_text(encoding="utf8")
    assert "CLI-owned state" in text and ("changed" in text or "differ" in text)
    documents.append({"preimage": bind(preimage), "corrected": bind(current)})
assert len(documents) == 5
previous = WORK / "plans/runs/nckh-native-261005-1340-r36-cursor-direct-interactive-attempt-08/plan-finalization.json"
record = {"status": "verified-factual-prose-correction", "recorded_at": datetime.now(timezone.utc).isoformat(),
          "facts": evidence, "documents": documents, "previous_finalization": bind(previous),
          "previous_document_bindings": "historical-stale-after-correction; refresh-in-new-reconciliation",
          "source_modified": False, "model_turns": 0, "full_native_gate": "unchecked", "verifier": bind(Path(__file__))}
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "documents_corrected": len(documents)}))
