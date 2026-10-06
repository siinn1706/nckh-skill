"""Verify bounded vendor observations and record the unresolved runtime route."""

import hashlib
import json
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
source_record = read(RUN / "workspace-hook-source-excerpts.json")
vendor = Path(source_record["source"])
assert sha(vendor) == source_record["source_sha256"]
source = vendor.read_text(encoding="utf8")
locations = {}
for row in source_record["rows"]:
    matches = [match.start() for match in re.finditer(re.escape(row["term"]), source)]
    assert len(matches) == row["match_count"]
    locations[row["term"]] = matches
    for snippet in row["snippets"]:
        actual = source[snippet["start"]:snippet["end"]]
        assert actual == snippet["text"]
        assert hashlib.sha256(actual.encode()).hexdigest() == snippet["sha256_utf8"]
assert len(locations["workspaceOpen"]) == 5 and len(locations["pluginPaths"]) == 7
assert all(4008000 <= position <= 4022000 for term in ("workspaceOpen", "pluginPaths") for position in locations[term])
last = locations["pluginPaths"][-1]
snippet = source[last-300:last+650]
with (RUN / "last-plugin-paths-snippet.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps({"start": last-300, "end": last+650, "text": snippet,
        "sha256_utf8": hashlib.sha256(snippet.encode()).hexdigest()}, ensure_ascii=False, indent=2) + "\n")
record = {
    "status": "verified-readonly-source-route-observation-not-native-qualification",
    "source_revision": 37, "source_lock_hash": "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb",
    "vendor_version": "2026.09.15-d2fe57e", "vendor_source_sha256": source_record["source_sha256"],
    "literal_locations": locations,
    "observed_region": "Shared event-name normalization, response validation and response aggregation",
    "runtime_invocation_route": "not-established by the bounded inspection; literal searches do not prove native unsupported status",
    "hypothesis": "workspaceOpen returning pluginPaths may provide a different loading route according to current docs",
    "hypothesis_status": "native trigger and successful loading remain unqualified in the installed CLI",
    "previous_missing_callback_cases": [
        bind(WORK / "plans/reports/delivery-261005-1930-r37-cursor-plugin-alias-controls.json"),
        bind(WORK / "plans/runs/nckh-native-261005-1923-r37-cursor-plugin-routing-inspection-attempt-20/routing-hypothesis.json"),
    ],
    "followup_boundary": "A future distinct native startup observation must establish workspaceOpen and plugin-path delivery before treating the route as a fix or sending model prompts",
    "vendor_source_modified": False, "vendor_code_evaluated": False, "model_prompts": 0,
    "CLI_processes_started": 0, "hook_callbacks_observed": 0, "full_native_gate": "unchecked",
    "source_observation": bind(RUN / "workspace-hook-source-excerpts.json"),
    "additional_snippet": bind(RUN / "last-plugin-paths-snippet.json"), "verifier": bind(Path(__file__)),
}
with (RUN / "verified-workspace-route-inspection.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "workspaceOpen_literals": 5, "pluginPaths_literals": 7, "model_prompts": 0}))
