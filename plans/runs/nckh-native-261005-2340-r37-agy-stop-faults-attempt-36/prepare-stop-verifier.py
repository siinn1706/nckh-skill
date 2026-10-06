"""Reuse verified binding rules for the four newly completed Stop cases."""

import ast
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
source = WORK / "plans/runs/nckh-native-261005-2320-r37-agy-event-controls-attempt-34/verify-event-delivery.py"
text = source.read_text(encoding="utf8")
text = text.replace("event-controls-34", "stop-faults-36").replace("verified-event-delivery.json", "verified-stop-delivery.json")
text = text.replace('summary = read(RUN / "native-event-recovery.json")', 'summary = read(RUN / "native-event-summary.json")')
text = text.replace('recorded-24-native-event-cases-with-original-child-wait-failure', 'recorded-native-agy-event-controls')
text = text.replace('== 24 and len(brief["cases"]) == 28', '== 4 and len(brief["cases"]) == 4')
text = text.replace('brief["maximum_model_turns"] == 28', 'brief["maximum_model_turns"] == 4')
text = text.replace('case["name"] == "postinvocation-timeout"', 'case["name"] == "stop-timeout"')
old = '''    if child_receipt.exists():
        assert read(child_receipt)["same_process_live"] == 0
    else:
        assert case["name"] == "stop-malformed-input" and read(RUN / "orphan-inspection.json")["count"] == 0'''
assert old in text
text = text.replace(old, '    assert child_receipt.exists() and read(child_receipt)["same_process_live"] == 0')
text = text.replace('== 24\ncleanup', '== 4\ncleanup').replace('"model_turns": 24', '"model_turns": 4')
old = '''"summary": bind(RUN / "native-event-recovery.json"),
    "original_summary": bind(RUN / "native-event-summary.json"), "original_failure": bind(RUN / "native-event-failure.json"),
    "original_collection_exit": 1, "not_run_cases": summary["not_run_cases"],
    "timing_correction": "original PostInvocation summary label does not establish per-tool timing; raw summary retained"'''
assert old in text
text = text.replace(old, '"summary": bind(RUN / "native-event-summary.json"), "previous_partial_batch_retained": True')
text = text.replace('verified-native-agy-event-observations', 'verified-four-native-agy-Stop-fault-observations')
ast.parse(text)
target = RUN / "verify-event-delivery.py"
assert not target.exists()
target.write_text(text, encoding="utf8")
with (RUN / "verifier-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"source": str(source.relative_to(WORK)), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "source_modified": False,
        "scope": "bind four fresh Stop cases; retain original partial batch and Windows serialization repair"}, stream, indent=2)
