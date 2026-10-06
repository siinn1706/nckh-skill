"""Retain the failing verifier execution and inspect exact observer serialization."""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
spec = importlib.util.spec_from_file_location("owned_verifier_binding", RUN / "owned-cli-command.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
outcome, stdout, stderr = owned.run_command("event-verifier-before-newline-repair",
    [sys.executable, "-I", str(RUN / "verify-event-delivery.py")], timeout=60)
assert outcome["exit_code"] == 1 and "original_bytes" in stderr.decode("utf8")
rows = []
for path in sorted((RUN / "attempts").glob("*.json")):
    attempt = json.loads(path.read_text(encoding="utf8"))
    for snapshot, binding in zip(attempt["native_callbacks"], attempt["callback_bindings"]):
        encoded = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        native_path = WORK / binding["path"]
        lf = hashlib.sha256(encoded.encode()).hexdigest()
        crlf = hashlib.sha256(encoded.replace("\n", "\r\n").encode()).hexdigest()
        rows.append({"attempt": attempt["attempt"], "event": snapshot["event"], "path": binding["path"],
            "snapshot_lf_matches": lf == binding["sha256"], "snapshot_crlf_matches": crlf == binding["sha256"],
            "current_binding_matches": hashlib.sha256(native_path.read_bytes()).hexdigest() == binding["sha256"]})
assert rows and all(r["snapshot_crlf_matches"] for r in rows)
with (RUN / "verifier-newline-diagnosis.json").open("x", encoding="utf8") as stream:
    json.dump({"observed_failing_command": "commands/event-verifier-before-newline-repair.json", "exit_code": 1,
        "cause": "Path.write_text translates observer JSON newlines to Windows CRLF; LF-only replay is not the saved bytes",
        "callback_snapshots": len(rows), "rows": rows, "native_oracles_regraded": False}, stream, indent=2)
print(json.dumps({"status": "verified-Windows-CRLF-cause", "callback_snapshots": len(rows),
                  "late_changed_callback_files": sum(not r["current_binding_matches"] for r in rows)}))
