"""Bind native CLI event evidence and retain source/trust/surface limits."""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = RUN / "project"
DELIVERY = RUN.parent / "nckh-native-261005-0005-r34-attempt-01"
REPORT = WORK / "plans/reports/delivery-261005-0052-r34-codex-events"
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import digest_record

read = lambda path: json.loads(path.read_text(encoding="utf8"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": str(path.relative_to(WORK)), "sha256": sha(path)}
EXPECTED = "8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34"
if REPORT.with_suffix(".json").exists() or REPORT.with_suffix(".md").exists():
    raise RuntimeError("Preserve the existing native addendum")
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
baseline = read(RUN / "native-baseline-summary.json")
faults = read(RUN / "native-fault-summary.json")
assert faults["status"] == "recorded-genuine-callbacks" and len(faults["results"]) == 25
cleanup = read(PROJECT / "cleanup.json")
assert cleanup["status"] == "pass" and not cleanup["config_callable"] and cleanup["unrelated_global_config_unchanged"]
audit = read(RUN / "final-process-audit.json")
assert audit["status"] == "pass" and not audit["matching_task_processes"]
rows = []
for item in faults["results"]:
    path = PROJECT / "attempts" / (item["attempt"] + ".json")
    record = read(path)
    assert record["source_lock_hash"] == EXPECTED and record["process_exited"] and record["invalid_stdout_lines"] == 0
    callbacks = [row for row in record["native_callbacks"] if row["event"] == item["event"]]
    assert callbacks and all(row["fault_origin"] == "controller-after-genuine-callback" for row in callbacks)
    commands = [frame["item"] for frame in record["native_json_frames"] if frame.get("type") == "item.completed"
                and frame.get("item", {}).get("type") == "command_execution"]
    errors = [frame["item"].get("message") for frame in record["native_json_frames"]
              if frame.get("type") == "item.completed" and frame.get("item", {}).get("type") == "error"]
    usage = [frame.get("usage") for frame in record["native_json_frames"] if frame.get("type") == "turn.completed"]
    decisions = [receipt["decision"] for receipt in record["policy_receipts"] if item["event"] in receipt["path"]]
    rows.append({**item, **bind(path), "exit_code": record["exit_code"], "command_receipt": bind(Path(record["command_receipt"])),
        "model_requested": record["model_requested"], "effort_requested": record["effort_requested"],
        "native_models": sorted({row["native_model"] for row in record["native_callbacks"] if row.get("native_model")}),
        "selected_callback_outcomes": [{"status": row["status"], "runner_exit_code": row.get("runner_exit_code"),
            "runner_output": row.get("runner_output"), "started_at": row["started_at"]} for row in callbacks],
        "selected_policy_decisions": decisions, "native_completed_command_items": [
            {key: command.get(key) for key in ("id", "status", "exit_code", "aggregated_output")} for command in commands],
        "native_error_items": errors, "native_usage": usage, "callbacks": record["callback_bindings"],
        "marker_path": record["marker_path"], "marker_sha256": record["marker_sha256"]})

native_status = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
    "status": "recorded-native-cli-events-full-surface-gate-open", "source_revision": 34, "source_lock_hash": EXPECTED,
    "source_unchanged": True, "host": "codex", "version": "0.154.0", "surface": "codex-cli-exec",
    "model_requested": "gpt-5.6-luna", "effort_requested": "medium", "permission_route": "native dangerous flags",
    "configuration": "sessionFlags inline hooks, matching project file absent for the 25-case matrix",
    "backend_model_attestation": "not-observed", "billing": "not-observed",
    "baselines": baseline, "faults": rows, "cleanup": bind(PROJECT / "cleanup.json"),
    "process_audit": bind(RUN / "final-process-audit.json"),
    "metadata_failures_and_reconciliations": [bind(path) for path in (
        PROJECT / "metadata.json", PROJECT / "metadata-invocation-only-02.json", PROJECT / "metadata-invocation-only-03.json",
        RUN / "metadata-initial-reconciliation.json", RUN / "native-project-trust-auto-review-rejection.json",
        RUN / "app-server-allow-01-reconciliation.json", RUN / "helper-amendments.json")],
    "prior_delivery": bind(WORK / "plans/reports/delivery-261005-0005-r34-cursor-agy.json"),
    "open_gates": ["persisted project-trust path needs approval after automatic reviewer rejection",
        "project plus plugin duplicate", "protected-path/native other tool qualification",
        "Claude model/tool and other events", "Cursor missing events and timeout anomaly",
        "Codex Desktop/IDE, Cursor IDE, AGY IDE direct application receipts", "production timing and scientific/stable/release"],
    "native_project_trust_change": "not-performed", "public_activation": "inactive/manual",
    "plan_progress": {"done": 44, "total": 45, "native_checkbox": "unchecked"}}
REPORT.with_suffix(".json").write_text(json.dumps(native_status, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
table = "\n".join("| " + event + " | " + " | ".join(
    "Có" if next(row for row in rows if row["event"] == event and row["fault"] == fault)["marker"] else "Không"
    for fault in ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")) + " |"
    for event in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"))
md = f"""# Codex CLI native event addendum — r34

## Current scope

Current r34 source/build/archives giữ nguyên hash `{EXPECTED}`. [Main delivery](./delivery-261005-0005-r34-cursor-agy.md) ghi full local checks. Addendum này ghi Codex CLI `0.154.0` **exec** route; [structured bindings](./delivery-261005-0052-r34-codex-events.json) chứa actual callbacks, native tool items, markers, failed discovery/collector receipts, cleanup và process audit. Plan vẫn **in-progress, 44/45**.

GPT-5.6 Luna medium và native dangerous flags thuộc direct human grant. Model ID ghi trong actual callbacks; effort được yêu cầu qua invocation. Native metadata/arguments chưa là backend attestation/billing. Global MCP/plugins và 27 unrelated hook definitions được disable riêng cho invocation trước inference; global file không được edit.

## Permission/discovery history

- App-server discovery không nhận new project hooks vì project chưa trusted, dù invocation có project trust override. Metadata failure giữ nguyên.
- Automatic approval review từ chối normal native UI project-trust step vì persistent global trust addition nằm ngoài retained authorization theo reviewer. Action chưa chạy, global trust không đổi. New specific approval request đã được gửi cho owner; không suy elapsed time là approval.
- Safer route dùng inline **sessionFlags** definitions cùng `--dangerously-bypass-hook-trust`, không lưu project trust. Actual native source enum là `sessionFlags`; initial collector expectation `session` đã fail rồi được sửa từ native metadata, không nới scope theo tên bất kỳ.
- App-server model allow attempt tạo marker nhưng **không có hook callbacks** trên route đó; collector còn có encoding alias typo. [Reconciliation](../runs/nckh-native-261005-0052-r34-codex-attempt-01/app-server-allow-01-reconciliation.json) giữ native process/marker/error bindings. Không gọi turn này là hook qualification.
- CLI exec supports dangerous flags trực tiếp. Matching project config có hai callbacks/event; sau preserve/removal file đó, cùng inline definitions có một callback/event. Differential này support file-sensitive project+inline multiplicity trên CLI route; chưa attest persisted trust hoặc plugin support.

Official [Codex hook documentation](https://learn.chatgpt.com/docs/hooks) describes invocation-only hook-trust bypass and separates explicit tool deny from hook failure behavior. Current metadata và actual native calls ở đây giữ riêng với docs capability claims.

## Native baselines

[Baseline receipts](../runs/nckh-native-261005-0052-r34-codex-attempt-01/native-baseline-summary.json):

- Allow: five genuine selected events; một shell execution và marker đúng bytes.
- Policy deny: genuine PreToolUse policy block, marker absent; model không retry hoặc đổi write route.
- Hai inline groups: hai same-tool PreToolUse callbacks, một idempotent policy receipt, một completed shell item và marker. Plugin route vẫn unobserved.

## Event fault matrix

Twenty-five native attempts có actual selected callbacks; fault được chèn bởi owned observer sau host invocation. Không gọi đây là malformed events tự phát bởi host. Từng model/native outcome giữ nguyên trong [raw summary](../runs/nckh-native-261005-0052-r34-codex-attempt-01/native-fault-summary.json).

| Selected event | Malformed input | Malformed output | Timeout | Crash | Unsupported selected codec |
|---|---:|---:|---:|---:|---:|
{table}

Bảng ghi **marker được tạo hay không**, không phải bảng pass/fail chung. Pre events xảy ra trước tool; PostToolUse/Stop sau side effect. Hook failure có thể fail-open; callback hoặc CLI exit0 không thay actual command items. Unsupported selected codec là controller gọi unknown event cho packaged runner sau callback thật. Harness timeout2s/sleeper8s chưa qualify public template5s hoặc production timing.

## Cleanup và phần còn mở

[Cleanup](../runs/nckh-native-261005-0052-r34-codex-attempt-01/project/cleanup.json) gỡ 26 matching payload members; matching project config đã park vào evidence trước matrix và không callable. Không thêm persisted native project trust; unrelated global config hash unchanged. [Final audit](../runs/nckh-native-261005-0052-r34-codex-attempt-01/final-process-audit.json) zero matching task processes. All oracles, native conversations/logs, callbacks, policy receipts và failures giữ nguyên.

Required native task vẫn unchecked: persisted project-trust route đang chờ explicit owner approval sau auto-review rejection; project/plugin duplicate và protected-path/other tools chưa qualified. Claude model/tool, Cursor events/timeouts, direct Desktop/IDE observations còn mở. Installed r25 chưa update; stable/scientific/release lanes riêng. Source/structural validation không đóng các gates này.
"""
REPORT.with_suffix(".md").write_text(md, encoding="utf8", newline="\n")
print(json.dumps({"status": native_status["status"], "report": str(REPORT.with_suffix(".md")), "fault_cases": len(rows)}))
