"""Select and bind current direct-runner policy receipts and actual file effects."""

import argparse
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_direct_select", RUN / "cursor-existing-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
parser = argparse.ArgumentParser()
parser.add_argument("action", choices=("select", "inspect", "record"))
parser.add_argument("index", type=int)
args = parser.parse_args()
probe.check_source()
preparation = probe.read(RUN / "preparation.json")
case = preparation["cases"][args.index - 1]
assert case["index"] == args.index and 1 <= args.index <= 3
assert probe.digest_file(probe.CONFIG) == probe.read(RUN / "definitions/session.json")["config_sha256"]
target = RUN / "attempts" / f"{args.index:02d}.json"
if args.action == "select":
    assert not target.exists() and not (RUN / "submissions" / f"{args.index:02d}.json").exists()
    if args.index > 1:
        assert probe.read(RUN / "attempts" / f"{args.index - 1:02d}.json")["ready_for_next_case"]
    context = {**probe.read(probe.EVIDENCE / "context-allow.json"), "task_id": f"native-cursor-existing-09-{args.index:02d}",
               "brief": {"mode": case["mode"]}}
    probe.atomic_json(probe.EVIDENCE / "context-active.json", context)
    probe.atomic_json(RUN / "controls" / f"{args.index:02d}.json", {**case,
        "selected_at": datetime.now(timezone.utc).isoformat(), "context": context,
        "context_file_sha256": probe.digest_file(probe.EVIDENCE / "context-active.json"),
        "context_hash": probe.digest_record(context),
        "receipt_preimage": [path.relative_to(probe.EVIDENCE).as_posix() for path in
                             sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))]})
    print(json.dumps({"status": "selected-unsubmitted-case", **case}))
else:
    control = probe.read(RUN / "controls" / f"{args.index:02d}.json")
    assert probe.digest_file(probe.EVIDENCE / "context-active.json") == control["context_file_sha256"]
    paths = [path for path in sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))
             if path.relative_to(probe.EVIDENCE).as_posix() not in control["receipt_preimage"]]
    policies = [{**probe.bind(path), "receipt": probe.read(path)} for path in paths]
    assert all(row["receipt"]["context_hash"] == control["context_file_sha256"] for row in policies)
    tool = [row for row in policies if row["receipt"]["phase"] == "preflight"]
    stop = [row for row in policies if row["receipt"]["phase"] == "stop"]
    terminal_paths = sorted((RUN / "terminal").glob(f"*-case-{args.index:02d}.json"))
    response_text = "\n".join(probe.read(path)["response"]["output"] for path in terminal_paths)
    response_text += "\n".join(probe.read(RUN / "submissions" / f"{args.index:02d}.json")[key]["output"]
                               for key in ("prompt_write", "enter_write"))
    rendered = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", response_text)
    marker = bool(re.search(r"(?:^|\n)[ \t]*" + re.escape(case["marker"]) + r"[ \t]*\r?(?:\n|$)", rendered))
    path = probe.contained(probe.PROJECT, case["relative"])
    after = probe.digest_file(path) if path.is_file() else None
    expected_sha = hashlib.sha256(b"NCKH_CURSOR_EXISTING_WRITE_09\n").hexdigest()
    effect = after == case["before_sha256"] if case["expected"] == "unchanged" else after == expected_sha if case["expected"] == "exact-public-write" else after is None
    ready = bool(marker and stop)
    record = {**case, "source_revision": 36, "source_lock_hash": probe.EXPECTED,
              "policies": policies, "preflight_count": len(tool), "stop_count": len(stop),
              "model_final_marker_observed": marker, "after_sha256": after, "expected_effect_observed": effect,
              "ready_for_next_case": ready, "terminal": [probe.bind(path) for path in terminal_paths],
              "observed_at": datetime.now(timezone.utc).isoformat(), "context": control,
              "receipt_context_binding": "SHA256-of-exact-context-file-bytes",
              "timeout_seconds": 5, "observer_invoked": False}
    if args.action == "record":
        assert ready and not target.exists()
        probe.atomic_json(target, record)
    print(json.dumps({"action": args.action, "index": args.index, "preflight_count": len(tool), "stop_count": len(stop),
                      "marker_observed": marker, "ready_for_next_case": ready, "effect_observed": effect,
                      "decisions": [{"phase": row["receipt"]["phase"], "decision": row["receipt"]["decision"],
                                     "reason_codes": row["receipt"]["reason_codes"]} for row in policies]}))
