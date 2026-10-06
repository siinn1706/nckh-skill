"""Preserve failed verification and bind exact native event-specific identifiers."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
source = RUN / "verify-uncovered-search-delivery.py"
text = source.read_text(encoding="utf8")
old = 'assert obs["native_version"] == metadata["version"] and obs["native_model"] == "grok-4.7-xhigh"'
new = ('assert obs["native_version"] == metadata["version"]\n'
    '    assert obs["native_model"] == ("grok-4.7" if obs["event"] in {"preToolUse", "postToolUse"} else "grok-4.7-xhigh")\n'
    '    assert obs["native_model_id"] is None and obs["native_model_params"] is None')
assert text.count(old) == 1
text = text.replace(old, new)
old = '"model_turns": 1, "prompt_submissions": 1, "model_prompt_retries": 0, "fault_origin": "none",'
new = (old + '\n    "native_model_fields_by_event": {c["observation"]["event"]:c["observation"]["native_model"] for c in case["callbacks"]},\n'
    '    "native_model_parameter_attestation": "absent model_id/model_params; granted selection confirmed by config and CLI display only",\n'
    '    "failed_verifier_attempt_01": probe.bind(RUN / "verifier-attempt-01-failure.json"),\n'
    '    "model_field_correction": probe.bind(RUN / "verifier-attempt-02-adaptation.json"),')
assert text.count(old) == 1
text = text.replace(old, new)
target = RUN / "verify-uncovered-search-delivery-attempt-02.py"
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
with (RUN / "verifier-attempt-02-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"status":"exact-native-model-field-binding-correction", "source_sha256":sha(source), "target_sha256":sha(target),
        "original_verifier_retained":True, "frozen_search_oracle_changed":False, "original_case_changed":False,
        "model_prompt_retries":0, "reason":"Actual tool event model fields omit effort suffix; lifecycle fields retain suffix. No raw model parameter attestation is present."},stream,indent=2)
    stream.write("\n")
print(json.dumps({"status":"prepared-verifier-attempt-02", "frozen_oracle_changed":False}))
