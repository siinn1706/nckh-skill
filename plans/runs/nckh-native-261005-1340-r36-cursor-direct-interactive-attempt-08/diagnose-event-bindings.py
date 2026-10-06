"""Compare bounded synthetic event candidates with the retained neutral hashes."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_event_diagnostic", RUN / "cursor-direct-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
rows = []
for path in sorted((RUN / "attempts").glob("*.json")):
    attempt = probe.read(path)
    relative = attempt["relative"]
    path_candidates = [[], [relative], [relative.replace("/", "\\")]]
    candidates = sorted(set(attempt["context"]["context"]["tool_operations"]) | {"Bash", "Grep", "Glob"})
    for binding in attempt["policies"]:
        receipt = binding["receipt"]
        if receipt.get("phase") != "preflight":
            continue
        matches = []
        for tool in candidates:
            for paths in path_candidates:
                for stop_active in (False, True):
                    event = {"schema_version": 1, "phase": "preflight", "host": "cursor", "tool": tool,
                             "paths": paths, "session_key": receipt["session_key"], "task_key": receipt["task_key"],
                             "artifact_sha256": receipt["artifact_sha256"], "stop_active": stop_active}
                    if probe.digest_record(event) == receipt["event_hash"]:
                        matches.append({"tool": tool, "paths": paths, "stop_active": stop_active})
        rows.append({"index": attempt["index"], "requested_tool": attempt["kind"], "policy": binding,
                     "method": "bounded-candidate-reconstruction-from-neutral-event-hash; not-raw-native-payload",
                     "candidate_count": len(candidates) * len(path_candidates) * 2, "matches": matches})
result = {"status": "recorded-bounded-hash-diagnostic", "source_lock_hash": probe.EXPECTED,
          "model_turns": 0, "rows": rows, "diagnostic": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "event-binding-diagnostic.json", result)
print(json.dumps({"rows": [{"index": row["index"], "requested_tool": row["requested_tool"], "matches": row["matches"]} for row in rows]}))
