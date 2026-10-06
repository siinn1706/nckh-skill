"""Adapt retained test controllers without modifying kit or installed host state."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2255-r37-agy-read-tools-attempt-32"
FAULT = WORK / "plans/runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30"
GRANT = WORK / "plans/runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29"
changes = []
for source, name in ((BASE / "agy-cli-runtime.py", "agy-cli-runtime.py"),
                     (BASE / "owned-cli-command.py", "owned-cli-command.py"),
                     (FAULT / "agy-tool-observer.py", "agy-tool-observer.py"),
                     (GRANT / "cursor-agy-model-dangerous-grant.json", "cursor-agy-model-dangerous-grant.json"),
                     (GRANT / "cli-route-user-decision.json", "cli-route-user-decision.json")):
    target = RUN / name
    assert not target.exists()
    original = source.read_bytes()
    content = original
    if name == "agy-cli-runtime.py":
        content = original.decode("utf8").replace("read-tools-32", "event-controls-34").replace(
            "native-agy-read-tools-r37-32", "native-agy-event-controls-r37-34"
        ).replace('"timeout": 20', '"timeout": 5').replace('5 if direct else 20', '5')
        content = content.encode("utf8")
    elif name == "agy-tool-observer.py":
        text = original.decode("utf8")
        text = text.replace('native_step_idx=native.get("stepIdx"),',
                            'native_step_idx=native.get("stepIdx"), execution_num=native.get("executionNum"),')
        old = 'context = "context-deny.json" if mode == "policy-deny" else "context-uncovered.json" if mode == "uncovered-tool" else "context-allow.json"'
        new = 'context = control["deny_context"] if fault and mode == "policy-deny" else control["allow_context"]'
        assert old in text
        content = text.replace(old, new).encode("utf8")
    with target.open("xb") as stream:
        stream.write(content)
    changes.append({"source": str(source.relative_to(WORK)), "target": name,
                    "original_sha256": hashlib.sha256(original).hexdigest(),
                    "adapted_sha256": hashlib.sha256(content).hexdigest()})
with (RUN / "controller-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"source_modified": False, "changes": changes,
               "changes_scope": "new test namespace, five-second outer handlers, selected-event context binding and native execution number"}, stream, indent=2)
