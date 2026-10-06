"""Freeze the reviewed event-specific timing change and preserve source history."""

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from core.build import freeze_sources, verify_source_lock
from core.hook_config import _definition
from core.paths import atomic_json, digest_file, digest_record

old_path = RUN / "source-preimages/core/registry/source-lock/source-lock.json"
old = json.loads(old_path.read_text(encoding="utf8"))
assert old["revision"] == "36" and digest_record(old) == "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"
assert digest_file(old_path) == digest_file(ROOT / "core/registry/source-lock/source-lock.json")
assert not (RUN / "source-checkpoint.json").exists()
expected_changed = {"core/hook_config.py", "hooks/templates/cursor.json", "docs/installation.md"}
assert {p for p, row in old["files"].items() if digest_file(ROOT / p) != row["sha256"]} == expected_changed
for p in expected_changed:
    assert digest_file(RUN / "source-preimages" / p) == old["files"][p]["sha256"]
argv = [sys.executable, "-I", "controller-owned-runner", "--event", "preToolUse"]
pre = _definition("cursor", "preToolUse", argv)
assert pre["timeout"] == 20 and pre["failClosed"] is True
template = json.loads((ROOT / "hooks/templates/cursor.json").read_text(encoding="utf8"))
assert template["config"]["hooks"]["preToolUse"][0]["timeout"] == pre["timeout"]
assert not any(template[k] for k in ("enabled", "registered", "trusted"))
assert all(_definition("cursor", event, argv)["timeout"] == 5 for event in ("sessionStart", "beforeSubmitPrompt", "postToolUse", "stop"))
assert all(_definition(host, "PreToolUse", argv)["hooks"][0]["timeout"] == 5 for host in ("claude", "codex", "agy"))
review = {"status": "inline-reviewed", "scope": sorted(expected_changed), "findings_requiring_fix": [],
    "primary_basis": "actual native5s timeout; direct20s Read and public Write/plan-only prevention controls",
    "review_limits": "not-independent-review; full native matrix and remaining app surfaces are still unqualified",
    "checks": {"Cursor_preToolUse20s_failClosed_true": True, "template_matches_preview": True,
               "other_events_and_hosts5s": True, "inactive_registration_trust_state": True},
    "base_failure": "plans/reports/delivery-261005-1550-r36-cursor-direct-failure-observer.json",
    "read_control": "plans/reports/delivery-261005-1610-r36-cursor-direct-timeout-control.json",
    "mutation_controls": "plans/reports/delivery-261005-1620-r36-cursor-direct-mutation-control.json"}
atomic_json(RUN / "inline-review.json", review)
lock = freeze_sources(ROOT)
assert lock["revision"] == "37" and len(lock["files"]) == len(old["files"]) == 281
assert set(lock["files"]) == set(old["files"])
changed = {p for p in lock["files"] if lock["files"][p] != old["files"][p]}
assert changed == expected_changed and digest_record(verify_source_lock(ROOT)) == digest_record(lock)
atomic_json(RUN / "source-checkpoint.json", {"status": "frozen-reviewed-cursor-preToolUse-timeout", "source_revision": 37,
    "source_lock_hash": digest_record(lock), "previous_source_revision": 36, "previous_source_lock_hash": digest_record(old),
    "pins": len(lock["files"]), "changed_pins": sorted(changed), "review": "inline-review.json",
    "source_preimages": [{"path": p, "sha256": digest_file(RUN / "source-preimages" / p)} for p in sorted(expected_changed)],
    "native_scope": "r36 packaged runtime controls; fresh r37 payload qualification remains separate",
    "installed_update": "not-performed", "stable_release": "pending", "publication": "not-performed"})
print(json.dumps({"status": "frozen-reviewed-cursor-preToolUse-timeout", "source_revision": 37,
                  "source_lock_hash": digest_record(lock), "pins": len(lock["files"]), "changed_pins": sorted(changed)}))
