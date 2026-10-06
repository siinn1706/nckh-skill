"""Verify native bindings and write a limited Cursor event delivery record."""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
REPORT = WORK / "plans/reports/delivery-261005-0128-r34-cursor-events"
PRIOR = WORK / "plans/reports/delivery-261005-0005-r34-cursor-agy.json"
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import digest_record

read = lambda path: json.loads(path.read_text(encoding="utf8"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
expected = "8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34"
if REPORT.with_suffix(".md").exists() or REPORT.with_suffix(".json").exists():
    raise RuntimeError("Preserve the current report")
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == expected
summary = read(RUN / "native-summary.json")
assert summary["status"] == "recorded-native-cursor-events" and len(summary["results"]) == 20
assert summary["unobserved_events"] == ["beforeSubmitPrompt", "stop"]
assert summary["source_lock_hash"] == expected
audit = read(RUN / "final-process-audit.json")
assert audit["status"] == "pass" and not audit["matching_task_processes"]
rows = []
for result in summary["results"]:
    assert result["process_exited"] and result["invalid_stdout_lines"] == 0
    row = dict(result)
    native_models = set()
    for binding in [result["attempt_binding"], result["command_binding"], *result["callbacks"], *result["selected_policy_receipts"]]:
        target = RUN / binding["path"]
        assert sha(target) == binding["sha256"], "Native binding changed: " + str(target)
        if binding in result["callbacks"]:
            callback = read(target)
            if callback.get("native_model"):
                native_models.add(callback["native_model"])
    if result["oracle_created"]:
        assert sha(Path(result["oracle_retained"])) == result["oracle_sha256"]
    row["native_legacy_model_values"] = sorted(native_models)
    rows.append(row)
cleanups = []
removed = 0
for project in sorted((RUN / "projects").iterdir()):
    path = project / "cleanup.json"
    cleanup = read(path)
    assert not cleanup["config_callable"] and all(item["unchanged"] for item in cleanup["protected_native_config"])
    assert not (project / ".cursor/hooks.json").exists()
    for member in cleanup["removed"]:
        assert not (project / member["path"]).exists()
    removed += len(cleanup["removed"])
    cleanups.append(bind(path))
assert removed == 82
faults = [row for row in rows if row["mode"] in {"malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"}]
assert len(faults) == 15
for row in faults:
    assert row["selected_callback_count"] == 1
    assert all(callback["fault_origin"] == "controller-injection-after-genuine-callback" for callback in row["callbacks"]
               if callback["event"] == row["event"])
pretool = [row for row in faults if row["event"] == "preToolUse"]
assert len(pretool) == 5 and all(not row["oracle_created"] and row["completed_tool_items"][0]["result_keys"] == ["rejected"] for row in pretool)
duplicates = [row for row in rows if row["mode"] == "duplicate"]
for row in duplicates:
    selected = [callback for callback in row["callbacks"] if callback["event"] == "preToolUse"]
    assert len(selected) == 2 and len({callback["native_tool_use_id"] for callback in selected}) == 1
    assert len(row["selected_policy_receipts"]) == 1 and row["oracle_created"] and len(row["completed_tool_items"]) == 1
distinct = next(row for row in duplicates if "distinct" in row["attempt"])
assert {callback["callback_source"] for callback in distinct["callbacks"] if callback["event"] == "preToolUse"} == {"project", "plugin"}
report = {"schema_version": 1, "status": "recorded-native-cursor-events-full-surface-gate-open",
    "recorded_at": datetime.now(timezone.utc).isoformat(), "source_revision": 34, "source_lock_hash": expected,
    "source_unchanged": True, "host": "cursor", "version": "2026.09.15-d2fe57e", "surface": "cursor-cli-print",
    "model_requested": summary["model_requested"], "effort_requested": "xhigh", "context_requested": "500k",
    "native_model_observation": "legacy model strings present; model_id/model_params absent in callbacks",
    "backend_model_attestation": "not-observed", "billing": "not-observed",
    "attempts": rows, "fault_cases": 15, "configured_events": ["sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop"],
    "unobserved_events": summary["unobserved_events"], "summary": bind(RUN / "native-summary.json"),
    "ownership": bind(RUN / "ownership.json"), "native_selection": bind(RUN / "cursor-agy-model-selection.json"),
    "cleanup": cleanups, "removed_members": removed, "process_audit": bind(RUN / "final-process-audit.json"),
    "global_hooks": summary["global_hooks"], "prior_delivery": bind(PRIOR),
    "duplicate_anomaly": "Both new native duplicate cases succeed; historical 20s timeout remains retained and root cause unresolved",
    "fault_timing": "2s selected handler timeout / 8s sleeper; observer may complete after native host timeout; callback success alone is not native success",
    "open_gates": ["beforeSubmitPrompt and stop on this CLI route", "file/protected-path and other native tools",
        "Cursor IDE direct receipts", "historical intermittent duplicate timeout diagnosis", "production timing", "full four-host native evidence"],
    "public_activation": "inactive/manual", "plan_progress": {"done": 44, "total": 45, "native_checkbox": "unchecked"}}
REPORT.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
fault_names = ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")
table = "\n".join("| " + event + " | " + " | ".join(
    "Có" if next(row for row in faults if row["event"] == event and row["mode"] == mode)["oracle_created"] else "Không"
    for mode in fault_names) + " |" for event in ("sessionStart", "preToolUse", "postToolUse"))
md = f"""# Cursor CLI native event addendum — r34

## Scope và source

Unchanged r34 source hash `{expected}`; [main delivery](./delivery-261005-0005-r34-cursor-agy.md) giữ full local tests/build/archive evidence. [Bindings](./delivery-261005-0128-r34-cursor-events.json) ghi 20 completed native turns trên Cursor CLI `2026.09.15-d2fe57e`, gồm ba baselines, 15 injected faults và hai project + transient-plugin duplicates. Plan vẫn **in-progress, 44/45**.

Direct grant chọn `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]` với `--force --trust --sandbox disabled`. Native config và command selector bind đúng lựa chọn; callbacks chỉ có legacy model `grok-4.7-xhigh`/`grok-4.7`, không có `model_id`/`model_params`. Chưa có backend/billing attestation. Existing global hooks giữ enabled và bytes unchanged; observed CLI help không có flag isolation tương ứng. Đây là evidence trong configured native environment.

## Native event coverage

Project definitions có đủ năm selected events; actual callbacks chỉ gồm `sessionStart`, `preToolUse`, `postToolUse`. `beforeSubmitPrompt` và `stop` có zero callbacks trong các turns này. Không gọi hai events universally unsupported hoặc bỏ chúng khỏi advertised contract; CLI route giữ unobserved và các surface khác pending.

Allow tạo marker và một completed Shell item. Policy deny trả native `rejected` với `plan-only-mutation`, marker absent. Controller deliberately bỏ tool mapping trả `manual`, host vẫn thực thi Shell/tạo marker; đây là uncovered controller route, không phải native unknown-tool injection.

## Fault observations

Faults được chèn sau genuine native callbacks. Bảng ghi **marker được tạo**, không phải universal PASS:

| Selected event | Malformed input | Malformed output | Timeout | Crash | Unsupported selected codec |
|---|---:|---:|---:|---:|---:|
{table}

Cả năm `preToolUse` faults có native rejected tool và marker absent với `failClosed=true`. Post-tool faults xảy ra sau marker creation. `sessionStart` faults không ngăn Shell trong các lượt này. Timeout handler2s/sleeper8s: observer có thể vẫn hoàn tất sau khi native host đã báo timeout; callback exit0 không thay host/tool result. Public template5s và production timing chưa qualified. Official [Cursor hook docs](https://cursor.com/docs/hooks) có timeout/failClosed contract; actual receipts quyết định kết luận cho version/surface này.

## Project + plugin duplicate

Hai new cases đều có hai same-tool pretool callbacks, một idempotent policy receipt, một Shell success và một marker. Case command giống nhau chạy thành công; case thêm owned `--callback-source plugin` cũng chạy thành công và cho explicit project/plugin provenance. Không có global plugin installation.

Historical [r34 duplicate timeout](./delivery-261005-0005-r34-cursor-agy.md) vẫn được giữ: runners exit0 nhưng native host từ chối vì 20s timeout. Hai successes mới xác nhận route có thể chạy; chưa xác định root cause hoặc chứng minh timeout đã biến mất ổn định. Không sửa source hay tăng timeout để che failure.

## Cleanup và gates

Ba owned projects gỡ **82 matching files**, config/payload/plugin không callable. Protected native config hashes unchanged; [process audit](../runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/final-process-audit.json) zero matching task processes. Kênh exec cũ không còn handle khi recovery; completed command receipts, cleanup artifacts và read-only process inventory được kiểm trước tiếp tục, không restart batch.

Native checkbox còn unchecked: missing CLI prompt/stop callbacks, protected paths/other tools, intermittent timeout diagnosis, direct Cursor IDE receipts và production timing. Full four-host/surface contract, installed r25 và scientific/stable/release gates giữ riêng.
"""
REPORT.with_suffix(".md").write_text(md, encoding="utf8", newline="\n")
print(json.dumps({"status": report["status"], "native_turns": len(rows), "faults": len(faults), "removed": removed,
    "report": str(REPORT.with_suffix(".md"))}))
