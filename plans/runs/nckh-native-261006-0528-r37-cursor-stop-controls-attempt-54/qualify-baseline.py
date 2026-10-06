"""Require actual normal Stop behavior before selecting any dependent fault case."""
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
case = read(RUN / "cases/stop-allow.json")
assert case["status"] == "recorded-current-Write-Stop-observation" and case["Stop_count"] == 1
assert case["native_content_LF_exact"] and case["marker_before_Stop"] and case["marker_exact"]


def bound(reference):
    path = WORK / reference["path"]
    assert sha(path) == reference["sha256"]
    return read(path)


callbacks = [bound(reference) for reference in case["callbacks"]]
stops = [row for row in callbacks if row["event"] == "stop"]
assert len(stops) == 1
stop = stops[0]
assert stop["status"] == "completed" and stop["runner_exit_code"] == 0 and stop["runner_exited"]
assert stop["runner_output"] == {} and stop["mode"] == "allow" and stop["fault_origin"] == "none"
policies = [bound(reference) for reference in case["policy_receipts"] if "/stop/" in reference["path"]]
assert len(policies) == 1 and policies[0]["phase"] == "stop"
assert policies[0]["decision"] == "advisory" and policies[0]["reason_codes"] == ["writing-resource-advice-only"]
assert stop["native_version"] == read(RUN / "native-metadata.json")["version"]
record = {"status":"qualified-current-native-Stop-baseline", "case":bind(RUN / "cases/stop-allow.json"),
    "Stop_count":1,"native_loop_count":stop["native_stop_loop_count"],"native_status":stop["native_stop_status"],
    "wire":stop["runner_output"],"policy":policies[0]["decision"],"model_retries":0,
    "repeated_reminder_behavior":"unqualified; one actual callback only","source_kit_modified":False}
with (RUN / "verified-baseline.json").open("x",encoding="utf8",newline="\n") as stream:
    stream.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":record["status"],"Stop_count":1,"loop_count":record["native_loop_count"],"wire":{}}))
