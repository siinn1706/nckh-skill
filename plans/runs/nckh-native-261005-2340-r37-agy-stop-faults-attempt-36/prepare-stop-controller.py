"""Prepare only the four Stop cases not run in the earlier frozen collection."""

import ast
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2320-r37-agy-event-controls-attempt-34"
PREVIOUS = WORK / "plans/runs/nckh-native-261005-2335-r37-agy-search-controls-attempt-35"
rows = []
for name in ("agy-cli-runtime.py", "owned-cli-command.py", "agy-tool-observer.py", "run-event-controls.py",
             "audit-owned-processes.ps1", "cursor-agy-model-dangerous-grant.json", "cli-route-user-decision.json"):
    source = BASE / name
    text = source.read_text(encoding="utf8")
    if name == "agy-cli-runtime.py":
        text = text.replace("event-controls-34", "stop-faults-36").replace("event-controls-r37-34", "stop-faults-r37-36")
    elif name == "run-event-controls.py":
        text = text.replace('MODES = ("allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")',
            'MODES = ("malformed-output", "timeout", "crash", "unsupported-codec")')
        text = text.replace('EVENTS = ("PreInvocation", "PostToolUse", "PostInvocation", "Stop")', 'EVENTS = ("Stop",)')
        text = text.replace("r37-agy-event34-", "r37-agy-stop36-").replace("native-agy-event34-", "native-agy-stop36-")
        text = text.replace('time.monotonic() - begin < 30', 'time.monotonic() - begin < 90')
        text = text.replace('"selected_callback_count": len(selected),',
            '"reconciled_callback_bindings": [probe.bind(p) for p in sorted((probe.EVIDENCE / "observations" / case["name"]).glob("*/*.json"))],\n                "selected_callback_count": len(selected),')
    elif name == "audit-owned-processes.ps1":
        text = text.replace("nckh-native-261005-2310-r37-agy-agent-inventory-attempt-33", PREVIOUS.name).replace(
            "prior native33 union audit", "prior native35 union audit")
    if name.endswith(".py"):
        ast.parse(text)
    target = RUN / name
    assert not target.exists()
    target.write_text(text, encoding="utf8")
    rows.append({"source": str(source.relative_to(WORK)), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                 "target": name, "adapted_sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
with (RUN / "controller-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"stage": "before model admission or native turns", "changes": rows,
        "scope": "four previously not-run Stop faults only, new fixtures and frozen brief",
        "original_partial_batch_retained": True, "original_oracles_regraded": False, "model_retries": 0,
        "process_supervision": "90-second descendant observation after native turn completion; no whole-turn deadline",
        "source_modified": False}, stream, indent=2)
