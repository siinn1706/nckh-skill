"""Record and repair a static global-target shadowing defect; no native rerun."""

import ast
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
HELPER = RUN / "codex-native-files.py"
PREIMAGE = RUN / "preimages/before-cleanup-target-shadow-repair.py"
RECEIPT = RUN / "cleanup-helper-review.json"
GLOBAL_HOOK = Path(r"C:/Users/USER\.codex\hooks.json")
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
if PREIMAGE.exists() or RECEIPT.exists():
    raise RuntimeError("Preserve the earlier review")
text = HELPER.read_text(encoding="utf8")
body = text.split("def cleanup():", 1)[1].split('if len(sys.argv)', 1)[0]
assert 'target = PROJECT / "cleanup.json"' in body
assert 'for target in (CONFIG,' in body and 'atomic_json(target,' in body
global_bytes = GLOBAL_HOOK.read_bytes()
global_value = json.loads(global_bytes)
assert sorted(global_value) == ["hooks"]
shutil.copyfile(HELPER, PREIMAGE)
replacement = body.replace('target = PROJECT / "cleanup.json"', 'receipt_path = PROJECT / "cleanup.json"')
replacement = replacement.replace('if target.exists():', 'if receipt_path.exists():')
replacement = replacement.replace('for target in (CONFIG,', 'for global_path in (CONFIG,')
replacement = replacement.replace('if target.is_file():', 'if global_path.is_file():')
replacement = replacement.replace('text = target.read_text(', 'text = global_path.read_text(')
replacement = replacement.replace('atomic_json(target,', 'assert receipt_path.resolve().is_relative_to(PROJECT.resolve())\n    atomic_json(receipt_path,')
new = text.replace(body, replacement)
ast.parse(new)
HELPER.write_text(new, encoding="utf8", newline="\n")
assert GLOBAL_HOOK.read_bytes() == global_bytes
record = {"status": "static-cleanup-target-defect-repaired", "recorded_at": datetime.now(timezone.utc).isoformat(),
    "classification": "owned helper repair; pinned kit/native receipts unchanged",
    "finding": "cleanup receipt variable was rebound by global config inspection loop; final atomic_json could target global hooks file",
    "before": bind(PREIMAGE), "after": bind(HELPER), "helper_invoked": False,
    "observed_global_hook_sha256": sha(GLOBAL_HOOK), "observed_global_hook_keys": sorted(global_value),
    "global_cleanup_overwrite_observed": False, "controller_global_write_attempt": "not proven by retained trace",
    "stalled_process_cause": "not proven; static defect is a concrete risk, not an execution trace",
    "retained_native_receipts": [bind(RUN / "native-global-trust-observation.json"), bind(RUN / "project-02/cleanup-reconciliation.json")],
    "retet_helper": "r35 helper uses receipt_path/global_path and checks raw config/hook hashes before cleanup"}
RECEIPT.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
print(json.dumps({"status": record["status"], "global_file_unchanged": True, "native_rerun": False}))
