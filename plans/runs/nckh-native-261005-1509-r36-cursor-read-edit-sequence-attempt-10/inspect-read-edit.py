"""Record bounded callback facts and exact fixture bytes, including unmet oracles."""

import argparse
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_read_edit_inspect", RUN / "cursor-read-edit-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
parser = argparse.ArgumentParser()
parser.add_argument("action", choices=("inspect", "record"))
args = parser.parse_args()
probe.check_source()
preparation = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/session.json")
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
observations, incomplete = [], []
for path in sorted((probe.EVIDENCE / "observations/read-edit-10").glob("*/*.json")):
    try:
        value = probe.read(path)
    except (ValueError, OSError):
        incomplete.append(path.relative_to(probe.PROJECT).as_posix())
        continue
    observations.append({**probe.bind(path), "observation": value})
policies = [{**probe.bind(path), "receipt": probe.read(path)} for path in
            sorted((probe.EVIDENCE / "policy-receipts/read-edit-10").glob("*/*.json"))]
terminal_paths = sorted((RUN / "terminal").glob("*.json"))
submission = probe.read(RUN / "submission.json")
response_text = "\n".join(probe.read(path)["response"]["output"] for path in terminal_paths)
response_text += "\n".join(submission[key]["output"] for key in ("prompt_write", "enter_write"))
rendered = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", response_text)
marker = bool(re.search(r"(?:^|\n)[ \t]*" + re.escape(preparation["marker"]) + r"[ \t]*\r?(?:\n|$)", rendered))
pre = sorted([row for row in observations if row["observation"]["event"] == "preToolUse"],
             key=lambda row: row["observation"]["started_at"])
post = sorted([row for row in observations if row["observation"]["event"] == "postToolUse"],
              key=lambda row: row["observation"]["started_at"])
stops = [row for row in observations if row["observation"]["event"] == "stop" and
         row["observation"].get("status") == "completed" and row["observation"].get("runner_exit_code") == 0]
fixture = probe.contained(probe.PROJECT, preparation["relative"])
after_bytes = fixture.read_bytes() if fixture.is_file() else None
expected = probe.read(RUN / "frozen-brief.json")["requested_after_text"].encode("utf8")
after_hash = hashlib.sha256(after_bytes).hexdigest() if after_bytes is not None else None
ready = bool(marker and stops and not incomplete and all(row["observation"].get("status") == "completed" for row in observations))
pairs = [{"tool_use_id": row["observation"].get("native_tool_use_id"),
          "pre_tool": row["observation"].get("native_tool_name"), "pre_callback": row["path"],
          "post_callbacks": [tail["path"] for tail in post if tail["observation"].get("native_tool_use_id") ==
                             row["observation"].get("native_tool_use_id") and row["observation"].get("native_tool_use_id") is not None
                             and tail["observation"].get("native_tool_name") == row["observation"].get("native_tool_name")]}
         for row in pre]
use_ids = sorted({row["observation"]["native_tool_use_id"] for row in pre if row["observation"].get("native_tool_use_id")})
all_ids_present = bool(pre) and all(row["observation"].get("native_tool_use_id") for row in pre)
record = {"status": "completed-sequence-observation" if ready else "observation-in-progress", "ready": ready,
          "recorded_at": datetime.now(timezone.utc).isoformat(), "source_revision": 36, "source_lock_hash": probe.EXPECTED,
          "model_final_marker_observed": marker, "native_observations": observations, "incomplete_observer_files": incomplete,
          "policies": policies, "preflight_callbacks": len(pre), "post_callbacks": len(post), "stop_callbacks": len(stops),
          "native_pre_tool_names_in_order": [row["observation"].get("native_tool_name") for row in pre],
          "native_tool_pairs": pairs, "distinct_native_tool_use_ids": use_ids,
          "distinct_native_tool_use_id_count": len(use_ids),
          "requested_tool_call_bound_respected": len(use_ids) <= 2 if all_ids_present else None,
          "call_count_scope": "distinct native tool_use_id; multiple hook tool names may share one native use identity",
          "raw_model_tool_call_frames": "not-captured",
          "before_sha256": preparation["before_sha256"], "after_sha256": after_hash,
          "expected_effect_observed": after_bytes == expected, "bytes_changed": after_hash != preparation["before_sha256"],
          "terminal": [probe.bind(path) for path in terminal_paths], "submission": probe.bind(RUN / "submission.json"),
          "preparation": probe.bind(RUN / "preparation.json"), "outer_timeout_seconds": 20,
          "packaged_runner_timeout_seconds": 5, "fault_origin": "none", "collector": probe.bind(Path(__file__))}
if args.action == "record":
    assert ready and not (RUN / "sequence-observation.json").exists()
    with (RUN / "fixture-after.txt").open("xb") as stream:
        stream.write(after_bytes if after_bytes is not None else b"")
    record["fixture_after"] = probe.bind(RUN / "fixture-after.txt")
    record["fixture_after_present"] = after_bytes is not None
    probe.atomic_json(RUN / "sequence-observation.json", record)
print(json.dumps({"ready": ready, "preflight_callbacks": len(pre), "post_callbacks": len(post), "stop_callbacks": len(stops),
                  "native_tools": record["native_pre_tool_names_in_order"], "effect_observed": record["expected_effect_observed"],
                  "bytes_changed": record["bytes_changed"], "bound_respected": record["requested_tool_call_bound_respected"]}))
