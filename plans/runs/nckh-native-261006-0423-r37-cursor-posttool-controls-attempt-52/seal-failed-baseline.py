"""Seal the failed first baseline and authorize cleanup only for its observed owned bytes."""
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
spec = importlib.util.spec_from_file_location("failed_posttool_runtime", RUN / "cursor-posttool-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
frozen=read(RUN / "frozen-brief.json")
case=frozen["cases"][0]
observations=sorted((probe.EVIDENCE / "observations" / case["attempt"]).glob("*/*.json"))
rows=[read(path) for path in observations]
assert len(rows) == 4 and {row["event"] for row in rows} == {"beforeSubmitPrompt","preToolUse","postToolUse","stop"}
pre=next(row for row in rows if row["event"] == "preToolUse")
post=next(row for row in rows if row["event"] == "postToolUse")
stop=next(row for row in rows if row["event"] == "stop")
assert pre["native_tool_name"] == post["native_tool_name"] == "Write"
assert pre["native_tool_use_id"] == post["native_tool_use_id"]
assert (probe.PROJECT / pre["native_path_fields"]["file_path"]).resolve() == (probe.PROJECT / case["relative"]).resolve()
assert pre["marker_at_callback_start_sha256"] == case["before_sha256"]
marker=probe.PROJECT / case["relative"]
actual=marker.read_bytes()
assert len(actual) <= 256 and sha(marker) == post["marker_at_callback_start_sha256"] == stop["marker_at_callback_start_sha256"]
assert actual != bytes.fromhex(case["expected_hex"]) and actual.endswith(b"\r\r\n")
assert actual[:-3] == bytes.fromhex(case["expected_hex"])[:-2]
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == 0
assert read(RUN / "monitor-exit.json")["exit_code"] == 1
policies=sorted((probe.EVIDENCE / "policy-receipts" / case["attempt"]).glob("*/*.json"))
selected=[read(path) for path in policies if "/postToolUse/" in path.as_posix()]
assert len(selected) == 1 and selected[0]["decision"] == "pending" and selected[0]["reason_codes"] == ["artifact-final-bytes-missing-or-stale"]
out=RUN / "failed-marker-after.txt"
with out.open("xb") as stream: stream.write(actual)
for untouched in frozen["cases"][1:]:
    assert sha(probe.PROJECT / untouched["relative"]) == untouched["before_sha256"]
    assert not (RUN / "selected" / (untouched["attempt"]+".json")).exists()
before=RUN / "cleanup-definition-preimage.json"
with before.open("xb") as stream: stream.write((RUN / "last-definition.json").read_bytes())
definition=read(before)
for item in definition["extra_configs"]:
    if item["path"] == case["relative"]: item["sha256"]=sha(marker)
probe.atomic_json(RUN / "last-definition.json",definition)
record={"status":"recorded-failed-first-posttool-baseline","timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "source_revision":37,"source_lock_hash":frozen["source_lock_hash"],"model_turns":1,"native_Write_requests":1,
    "callbacks":[bind(path) for path in observations],"policy_receipts":[bind(path) for path in policies],
    "expected_marker_hex":case["expected_hex"],"actual_marker_hex":actual.hex(),"actual_marker":bind(out),
    "actual_post_policy":"pending/artifact-final-bytes-missing-or-stale","native_tool_use_id":pre["native_tool_use_id"],
    "full_frozen_oracle":"failed at baseline; six dependent cases unstarted","native_retry":False,"original_oracle_regraded":False,
    "monitor_exit_code":1,"native_exit_code":0,"monitor_failure":bind(RUN / "monitor-failure.json"),
    "normalizer_origin":"not-yet-established; native Write input content was not retained",
    "cleanup_adaptation":{"old_definition":bind(before),"new_definition":bind(RUN / "last-definition.json"),
        "reason":"same owned fixture matches genuine post/Stop hashes; permit removal of observed altered bytes without changing frozen oracle"},
    "sealer":bind(Path(__file__))}
with (RUN / "failed-baseline-observation.json").open("x",encoding="utf8") as stream:
    stream.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
probe.cleanup()
print(json.dumps({"status":record["status"],"model_turns":1,"dependent_cases_unstarted":6,"actual_tail":"CR CR LF","monitor_exit":1}))
