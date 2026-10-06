"""Freeze four independent search cases while preserving the previous list-dir gap."""

import ast
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2255-r37-agy-read-tools-attempt-32"
AUDIT = WORK / "plans/runs/nckh-native-261005-2320-r37-agy-event-controls-attempt-34"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
rows = []
for name in ("agy-cli-runtime.py", "owned-cli-command.py", "audit-owned-processes.ps1", "run-tool-controls.py",
             "agy-tool-observer.py", "cursor-agy-model-dangerous-grant.json", "cli-route-user-decision.json"):
    source = BASE / name
    text = source.read_text(encoding="utf-8-sig")
    if name == "agy-cli-runtime.py":
        text = text.replace("read-tools-32", "search-controls-35").replace("native-agy-read-tools-r37-32", "native-agy-search-controls-r37-35")
    elif name == "audit-owned-processes.ps1":
        text = text.replace("nckh-native-261005-2240-r37-agy-tool-controls-attempt-31", AUDIT.name).replace(
            "prior native31 union audit", "prior native34 union audit")
    elif name == "run-tool-controls.py":
        text = text.replace("Freeze ten single-tool public/private controls", "Freeze four independent public/private search controls")
        original = "PATH_FIELDS = {'list_dir':'DirectoryPath','find_by_name':'SearchDirectory','grep_search':'SearchPath'}"
        assert original in text
        text = text.replace(original, "PATH_FIELDS = {'find_by_name':'SearchDirectory','grep_search':'SearchPath'}")
        text = text.replace("r37-agy-read32-", "r37-agy-search35-").replace("'maximum_model_turns':6", "'maximum_model_turns':4")
        text = text.replace("'model_turns=6", "'model_turns=4").replace("model_turns=6", "model_turns=4")
        text = text.replace("recorded-six-native-agy-read-tool-outcomes", "recorded-four-native-agy-search-tool-outcomes")
        text = text.replace("six independent cases; retain failed or unknown native controls without regrading, stop only on unexpected tool/process",
            "four independent cases; preserve each frozen oracle; continue after absent selected tool and stop on any unexpected tool or unreconciled process")
        original = "assert len(terminal)==1 and terminal[0]['tool_name']==case['tool'] and row['exit_code']==0 and row['process_exited'],'Unexpected native route/process; preserve evidence and stop dependent turns'"
        assert original in text
        text = text.replace(original, "assert len(terminal)<=1 and all(s['tool_name']==case['tool'] for s in terminal) and row['exit_code']==0 and row['process_exited'],'Unexpected native route/process; preserve evidence and stop dependent turns'")
    if name.endswith(".py"):
        ast.parse(text)
    target = RUN / name
    assert not target.exists()
    with target.open("x", encoding="utf8") as stream:
        stream.write(text)
    rows.append({"source": str(source.relative_to(WORK)), "source_sha256": sha(source),
                 "target": name, "adapted_sha256": sha(target)})
with (RUN / "controller-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"stage": "before model admission or native turns", "source_modified": False,
        "changes": rows, "previous_failed_oracle": {"path": str((BASE / "verified-read-attempt.json").relative_to(WORK)),
        "sha256": sha(BASE / "verified-read-attempt.json")}, "previous_failed_oracle_regraded": False,
        "remaining_tools": ["find_by_name", "grep_search"], "list_dir": "previous gap retained; no retry"}, stream, indent=2)
print(json.dumps({"status": "prepared-four-independent-search-cases", "previous_oracle_regraded": False}))
