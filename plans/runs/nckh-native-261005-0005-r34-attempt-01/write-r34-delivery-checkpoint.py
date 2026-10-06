"""Bind completed local delivery to native receipts without closing unobserved gates."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
OLD = RUN.parent / "nckh-native-261004-1707-attempt-01"
R31 = RUN.parent / "nckh-native-261004-2112-r31-attempt-01"
R32 = RUN.parent / "nckh-native-261004-2112-r32-attempt-01"
R33 = RUN.parent / "nckh-native-261004-2112-r33-attempt-01"
REPORT = WORK / "plans/reports/delivery-261005-0005-r34-cursor-agy"
EXPECTED = "8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34"


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind(path):
    return {"path": str(path.relative_to(WORK)), "sha256": sha(path)}


if REPORT.with_suffix(".json").exists() or REPORT.with_suffix(".md").exists():
    raise RuntimeError("Preserve the existing delivery report")
names = ("deterministic-r34-attempt-01.json", "archive-summary.json", "smoke-summary.json",
         "installer-previews.json", "final-preservation.json", "agy-native-file-summary.json")
components = {name: read(RUN / name) for name in names}
assert all(item["status"] == "pass" and item["source_lock_hash"] == EXPECTED for item in components.values())
context = read(RUN / "delivery-context.json")
assert context["status"] == "built" and context["source_revision"] == "34" and context["source_lock_hash"] == EXPECTED
assert len(context["artifacts"]) == len(components["archive-summary.json"]["artifacts"]) == 16
assert len(components["installer-previews.json"]["surfaces"]) == 8
assert all(item["entries"] == 45 and item["project_unchanged"] for item in components["installer-previews.json"]["surfaces"])
suite = components["deterministic-r34-attempt-01.json"]
assert suite["source_unchanged"] and suite["deterministic"]["successful"]
assert (suite["source_files_pinned"], suite["identities"], suite["skill_cases"], suite["required_families"]) == (281, 39, 156, 19)
plugin = read(RUN / "agy-native-workspace-plugin-summary.json")
assert plugin["status"] == "observed-qualified-duplicate" and plugin["source_lock_hash"] == EXPECTED
event_faults = read(RUN / "agy-native-event-fault-summary.json")
assert event_faults["status"] in {"recorded-genuine-callbacks", "incomplete"} and event_faults["source_lock_hash"] == EXPECTED
event_timing = read(RUN / "agy-native-event-timing.json")
assert event_timing["raw_summary_sha256"] == sha(RUN / "agy-native-event-fault-summary.json")
if event_faults["status"] == "recorded-genuine-callbacks":
    assert len(event_faults["results"]) == 25 and all(item["selected_event_observed"] for item in event_faults["results"])
chains = read(RUN / "native-package-chains.json")
assert chains["source_lock_hash"] == EXPECTED
for item in chains["packages"]:
    artifact = next(row for row in context["artifacts"] if row["host"] == item["host"] and row["variant"] == "on-standalone")
    assert artifact["closure_hash"] == item["bundle_closure_hash"]
    assert sha(Path(item["archive"])) == item["archive_sha256"]

cleanup_paths = [R31 / "projects/cursor-model/cleanup.json", R31 / "projects/agy-model/cleanup.json",
                 R33 / "projects/agy-model/cleanup.json", RUN / "projects/cursor-model/cleanup.json",
                 RUN / "projects/agy-model/cleanup.json", RUN / "projects/agy-event-faults/cleanup.json"]
cleanups = [read(path) for path in cleanup_paths]
assert all(not row["config_callable"] and all(item["unchanged"] for item in row["protected_native_config"])
           for row in cleanups)
audit = read(RUN / "final-process-audit.json")
assert audit["matching_task_processes"] == []

current_cursor = []
cursor_project = RUN / "projects/cursor-model"
stage = read(cursor_project / "stage.json")
for mode in ("allow", "duplicate"):
    path = cursor_project / "attempts" / (mode + "-01.json")
    attempt = read(path)
    command = read(Path(attempt["command_receipt"]))
    stdout_path = RUN / "commands" / ("cursor-native-" + mode + "-01.stdout.txt")
    frames = [json.loads(line) for line in stdout_path.read_text(encoding="utf8").splitlines()]
    callbacks = [(cursor_project / relative, read(cursor_project / relative)) for relative in attempt["observations"]]
    pretool = [item for _, item in callbacks if item["event"] == "preToolUse"]
    policies = sorted((cursor_project / "policy-receipts" / (mode + "-01") / "preToolUse").glob("*.json"))
    terminal = [frame["tool_call"]["shellToolCall"] for frame in frames
                if frame.get("type") == "tool_call" and frame.get("subtype") == "completed"
                and "shellToolCall" in frame.get("tool_call", {})]
    reasons = [item["result"]["rejected"].get("reason", "") for item in terminal if "rejected" in item.get("result", {})]
    assert attempt["exit_code"] == 0 and attempt["process_exited"] and attempt["invalid_stdout_lines"] == 0
    assert len(terminal) == 1 and len(policies) == 1
    assert all(item["runner_exit_code"] == 0 and item["runner_exited"] and item["runner_output"] == {}
               and item["runner_sha256"] == stage["payload"]["members"]["hooks/runner.py"] for item in pretool)
    assert all(read(item)["decision"] == "allow" for item in policies)
    if mode == "allow":
        assert len(pretool) == 1 and attempt["oracle_created"] and not reasons
        qualification = "observed-allow-with-native-shell-oracle"
    else:
        assert len(pretool) == 2 and not attempt["oracle_created"]
        assert len({(item["native_session_hash"], item["native_tool_use_id"], item["native_command_sha256"])
                    for item in pretool}) == 1
        assert any("Hook script timed out after 20000ms" in reason for reason in reasons)
        qualification = "observed-duplicate-callbacks-native-timeout-unverified"
    current_cursor.append({**bind(path), "qualification": qualification, "mode": mode,
        "source_revision": 34, "source_lock_hash": EXPECTED, "command": bind(Path(attempt["command_receipt"])),
        "stdout": bind(stdout_path), "exit_code": command["exit_code"], "oracle_created": attempt["oracle_created"],
        "native_rejection_reasons": reasons, "pretool_callback_count": len(pretool),
        "policy_receipt_count": len(policies), "callbacks": [bind(item) for item, _ in callbacks],
        "policy_receipts": [bind(item) for item in policies], "model_requested": attempt["model_requested"],
        "native_system_model": [frame.get("model") for frame in frames if frame.get("type") == "system"],
        "observed_events": sorted({item["event"] for _, item in callbacks}),
        "native_outcome_is_independent_of_cli_exit": True})

historical_rows = []
for host in ("cursor", "agy"):
    for mode in ("allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash",
                 "unsupported-codec", "uncovered-tool", "duplicate"):
        path = R31 / "projects" / (host + "-model") / "attempts" / (mode + "-01.json")
        row = read(path)
        historical_rows.append({**bind(path), "host": host, "mode": mode, "source_revision": 31,
            "status": row["status"], "exit_code": row["exit_code"], "oracle_created": row["oracle_created"],
            "callback_count": row["callback_count"], "fault_origin": row["fault_origin"],
            "duplicate_kind": row.get("duplicate_kind"), "current_revision_equivalence": "not-claimed"})

totals = {key: sum(item[key] for item in components["smoke-summary.json"]["bundles"])
          for key in ("resource_reads", "writer_disabled_observations", "hook_projections_exercised")}
open_gates = [
    {"host": "claude", "surface": "claude-code", "version": "2.1.272", "source_revision_observed": 30,
     "observed": "SessionStart matrix only", "pending": "model/tool oracle and remaining selected events",
     "model_route": "no configured approved-GPT route observed; no other model grant"},
    {"host": "codex", "surface": "codex-cli", "version": "0.154.0", "source_revision_observed": 30,
     "observed": "prompt admission/failure and eight GPT-medium tool turns",
     "pending": "duplicate, other events, protected tool paths and latest revision observations; four failure cases fail open"},
    {"host": "cursor", "surface": "cursor-cli-print", "version": "2026.09.15-d2fe57e", "source_revision_observed": [31, 34],
     "observed": "sessionStart/preToolUse/postToolUse; r34 allow shell oracle and duplicate callbacks",
     "pending": "beforeSubmitPrompt/stop and per-event failure coverage; r34 duplicate repeats unexplained native timeout"},
    {"host": "agy", "surface": "agy-cli-print", "version": "1.2.16", "source_revision_observed": [31, 33, 34],
     "observed": "five selected events historically; r34 native file allow/denies and project/workspace-plugin duplicate",
     "event_fault_status": event_faults["status"], "recorded_event_fault_cases": len(event_faults["results"]),
     "pending": "remaining native tools/surfaces and production timing qualification; event faults are recorded observations"},
    *[{"host": host, "surface": surface, "version": "unobserved", "pending": "direct application event receipts"}
      for host, surface in (("codex", "codex-desktop"), ("codex", "codex-ide"),
                            ("cursor", "cursor-ide"), ("agy", "agy-ide"))],
]
history_paths = [R32 / "deterministic-r32-attempt-01.json", R33 / "deterministic-r33-attempt-01.json",
    R33 / "receipt-parent-resolution-diagnostic-01.json", R33 / "r34-source-checkpoint.json",
    R33 / "source-receipt-parent-review.json", R32 / "source-native-path-review.json",
    R31 / "projects/agy-model/attempts/protected-file-before-01.reconciliation.json",
    R33 / "agy-native-file-summary.json", R33 / "agy-native-workspace-plugin-summary.json"]
record = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
    "status": "local-delivery-pass-native-surface-gate-open", "source_revision": 34, "source_lock_hash": EXPECTED,
    "source_pins": 281, "identities": 39, "base_cases": 156, "families": 19, "resources": 9,
    "deterministic": suite["deterministic"], "components": {name: bind(RUN / name) for name in names},
    "delivery_artifacts": context["artifacts"], "archive_chain": components["archive-summary.json"]["artifacts"],
    "native_package_chains": bind(RUN / "native-package-chains.json"), "extracted_totals": totals,
    "installer_previews": components["installer-previews.json"]["surfaces"],
    "preservation": components["final-preservation.json"], "native_r34_cursor": current_cursor,
    "native_r34_agy_files": components["agy-native-file-summary.json"], "native_r34_agy_workspace_plugin": plugin,
    "native_r34_agy_event_faults": {**bind(RUN / "agy-native-event-fault-summary.json"), **event_faults},
    "native_r34_agy_event_timing": {**bind(RUN / "agy-native-event-timing.json"), **event_timing},
    "historical_r31_native": historical_rows, "history": [bind(path) for path in history_paths],
    "cleanup": [bind(path) for path in cleanup_paths], "cleanup_files_total": sum(len(item["removed"]) for item in cleanups),
    "cleanup_current_revision_files": sum(len(item["removed"]) for item in cleanups[-3:]),
    "process_audit": bind(RUN / "final-process-audit.json"),
    "native_model_grant": bind(RUN / "cursor-agy-model-dangerous-grant.json"),
    "owner_feedback": bind(OLD / "owner-feedback.json"), "owner_scope": "two exact displayed r29 writer samples",
    "review": "inline; no independent reviewer claimed", "source_review": bind(R33 / "source-receipt-parent-review.json"),
    "native_gate": "incomplete", "open_gates": open_gates, "installed_revision": 25,
    "installed_update": "not-performed", "stable_release": "not-performed", "scientific_qualification": "pending",
    "backend_model_attestation": "not-observed", "billing": "not-observed",
    "plan_progress": {"done": 44, "total": 45, "native_checkbox": "unchecked"}}
REPORT.with_suffix(".json").write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
history_table = "\n".join("| " + mode + " | " + ("Có" if next(row for row in historical_rows if row["host"] == "cursor" and row["mode"] == mode)["oracle_created"] else "Không")
    + " | " + ("Có" if next(row for row in historical_rows if row["host"] == "agy" and row["mode"] == mode)["oracle_created"] else "Không") + " |"
    for mode in ("allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec", "uncovered-tool", "duplicate"))
event_fault_table = "\n".join("| " + event + " | " + str(sum(item["event"] == event for item in event_faults["results"]))
    + " | " + str(sum(item["event"] == event and item["oracle_created"] for item in event_faults["results"])) + " |"
    for event in event_faults["requested_events"])
md = f"""# Delivery r34 và native Cursor/AGY

## Trạng thái

Candidate **r34** đạt local delivery. Plan giữ **in-progress, 44/45**; task native evidence theo event/version/surface vẫn unchecked. Hai mẫu VI/EN của r29 đã được owner chấp nhận. [Structured evidence](./delivery-261005-0005-r34-cursor-agy.json) bind hashes, archived packages, callbacks, tool outcomes, cleanups và historical failures.

Source có **281 pins**, đúng **39 identities / 156 base cases / 19 families / 9 resources**; canonical hash `{EXPECTED}`. Public resource access giữ ON; OFF chỉ dùng internal comparison. Installed r25 chưa update; stable/scientific/release chưa qualified.

## Native evidence dẫn tới sửa lỗi

- r31 sửa AGY permission shape: non-blocking dùng `ask`, block/pending dùng `deny`; native permission checks vẫn thuộc host. R32 sửa closure-test expectation tương ứng; [full r32](../runs/nckh-native-261004-2112-r32-attempt-01/deterministic-r32-attempt-01.json) đạt 183 tests và một skip.
- [Native protected-write trước sửa](../runs/nckh-native-261004-2112-r31-attempt-01/projects/agy-model/attempts/protected-file-before-01.reconciliation.json) thực sự tạo marker 19 bytes vì codec bỏ native `TargetFile`. Giữ marker, collector failure và callback evidence; không ghi thành deny.
- r33 kiểm `TargetFile`, `AbsolutePath`, `DirectoryPath`, `SearchDirectory`, `SearchPath`, các alias, target thiếu/sai kiểu; 21 subcase regressions trước sửa và 14 focused tests sau sửa được giữ trong [review](../runs/nckh-native-261004-2112-r32-attempt-01/source-native-path-review.json). Native file/plugin subset đạt ở r33.
- [Full r33](../runs/nckh-native-261004-2112-r33-attempt-01/deterministic-r33-attempt-01.json) thất bại: 186 tests, một concurrent receipt error, một skip. [Windows diagnostic](../runs/nckh-native-261004-2112-r33-attempt-01/receipt-parent-resolution-diagnostic-01.json) ghi child `Path.resolve` giữ extended prefix khi receipt parent xuất hiện đồng thời; root không có prefix. Đây là lỗi normalization/race thực, chưa phải path escape thực.
- r34 tạo contained receipt directory trước child resolution. Containment/no-links/kernel-lock/atomic-write guards giữ nguyên. [Review](../runs/nckh-native-261004-2112-r33-attempt-01/source-receipt-parent-review.json) ghi 15 focused passing tests, gồm 150 fresh directories × 6 concurrent calls và traversal rejection. Review inline; không claimed independent reviewer.

## Local delivery đã chạy

| Gate | Kết quả r34 |
|---|---|
| Full deterministic | {suite['deterministic']['tests']} tests, {len(suite['deterministic']['skipped'])} Windows symlink skip; successful, {suite['deterministic']['seconds']:.3f} giây |
| Reproducibility/build | Bốn variants, 16 bundles; mọi command exit0 |
| Archive/extraction | 16 archives giải nén ngoài source, closure/manifest verified |
| Extracted resource readers | {totals['resource_reads']} genuine local reads |
| OFF writer behavior | {totals['writer_disabled_observations']} disabled/no-read observations |
| Hook closure | {totals['hook_projections_exercised']} primary/reference projections |
| Installer previews | Tám surfaces, 39 skills + sáu agents, project bytes unchanged |
| Preservation | {components['final-preservation.json']['protected_hashes_checked']} protected hashes unchanged; installed r25 và bốn legacy bundles giữ nguyên |

[Full suite](../runs/nckh-native-261005-0005-r34-attempt-01/deterministic-r34-attempt-01.json), [archives](../runs/nckh-native-261005-0005-r34-attempt-01/archive-summary.json), [extracted observations](../runs/nckh-native-261005-0005-r34-attempt-01/smoke-summary.json), [previews](../runs/nckh-native-261005-0005-r34-attempt-01/installer-previews.json) và [preservation](../runs/nckh-native-261005-0005-r34-attempt-01/final-preservation.json) cùng bind current r34. Không có overall deadline tùy ý; individual test timeouts giữ nguyên.

## Native r34: AGY

AGY CLI `1.2.16` dùng `gemini-3.8-flash-medium`, effort medium, `--dangerously-skip-permissions` trong project thử riêng theo human grant. [Verified native archive chain](../runs/nckh-native-261005-0005-r34-attempt-01/native-package-chains.json) có cùng bundle closure với final build.

[Ba native file cases](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-file-summary.json) đạt:

- Allowed `write_to_file`: tool DONE, marker được tạo, hook trả `ask`.
- Protected `write_to_file`: native tool ERROR `private-holdout-credential-path`, target vẫn absent.
- Protected `view_file`: native tool ERROR cùng reason; seeded test marker giữ nguyên hash.

[Project + workspace plugin](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-workspace-plugin-summary.json) có hai callbacks cùng session/step/tool, một policy receipt, một actual `run_command` DONE và một marker. Plugin nằm trong project thử, không cài global. Đây là các tool/version/surface observations trên; remaining native tools và IDE evidence còn thiếu.

[Event fault matrix r34](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-event-fault-summary.json) ghi **{len(event_faults['results'])}** attempts, status `{event_faults['status']}`. Mỗi fault được chèn sau callback thật; không claimed native host tự sinh malformed/unsupported events. Five faults: malformed input/output, timeout, crash, unsupported selected codec. Tệp thực và callbacks bind riêng từng attempt.

| Selected event | Recorded attempts | Attempts tạo marker |
|---|---:|---:|
{event_fault_table}

[Native tool states và actual callback order](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-event-timing.json) xác nhận five PreToolUse fault cases có actual tool ERROR và marker absent. Bốn PostToolUse faults (malformed output/timeout/crash/unsupported selected codec) có tool ERROR sau khi marker đã tạo; PostToolUse malformed input và fifteen PreInvocation/PostInvocation/Stop cases có tool DONE với marker được giữ. PreToolUse trước tool, PostToolUse sau tool. PreInvocation/PostInvocation bao quanh từng model invocation; trong các turns này có callbacks cả trước và sau tool. Stop sau final response. Mô tả `effect_timing` ban đầu trong raw summary quá rộng; diagnostic giữ original hash và sửa interpretation, không ghi đè raw receipts. [Initial collector assertion failure](../runs/nckh-native-261005-0005-r34-attempt-01/event-timing-collector-initial-failure.json) giữ việc giả định mọi non-pretool state DONE bị bác bỏ bằng actual stream. Marker tồn tại khi post hook lỗi không tự chứng minh prevention failure. Bảng không gọi mọi absence là policy deny hoặc mọi model exit0 là successful tool execution.

## Native r34: Cursor

Cursor CLI `2026.09.15-d2fe57e` dùng selector `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`, `--force --trust --sandbox disabled` trong project thử riêng. Historical native init xác nhận Grok 4.7 500K Extra High; callbacks hiện ghi base model `grok-4.7`. Metadata chưa là backend attestation hoặc billing receipt.

| Case | Callback/receipt | Native tool và tệp |
|---|---|---|
| [Allow](../runs/nckh-native-261005-0005-r34-attempt-01/projects/cursor-model/attempts/allow-01.json) | sessionStart/preToolUse/postToolUse; một pretool/policy receipt | Shell completed, marker được tạo |
| [Project + transient plugin duplicate](../runs/nckh-native-261005-0005-r34-attempt-01/projects/cursor-model/attempts/duplicate-01.json) | Hai same-tool pretool callbacks, runner exit0/JSON hợp lệ, một policy receipt | Native host báo `Hook script timed out after 20000ms`, marker không tạo |

Duplicate timeout lặp lại từ r31 trên current r34. CLI exit0 và final response không chứng minh tool thành công; raw native tool rejection giữ nguyên. Chưa có nguyên nhân đủ evidence để sửa host hoặc gọi duplicate route qualified. `beforeSubmitPrompt`/`stop` chưa có callback trên print route này. Wrapper baseline 20s/fault2s/sleep8s là harness; public template5s chưa có production timing qualification.

## Historical r31 matrix

Các receipts dưới đây giữ đúng source r31; không regrade thành r34 sau runner repair.

| Case | Cursor tạo marker | AGY tạo marker |
|---|---:|---:|
{history_table}

Fault cases là controller injection sau genuine native callback, selected ở PreToolUse; host không tự phát malformed/unsupported events. Uncovered AGY ghi manual/ask rồi thực thi; uncovered Cursor có native timeout, owned process termination sau 270 giây. R31 AGY duplicate chỉ là hai project groups; project/workspace-plugin duplicate được quan sát ở r33/r34. Historical Claude/Codex evidence giữ trong [r30 checkpoint](./delivery-261004-1707-r30-native-checkpoint.md), [prompt faults](./delivery-261004-1707-r30-prompt-failures.md) và [model/tool observations](./delivery-261004-1707-r30-model-tools.md).

## Cleanup và gates còn mở

Current r34 gỡ **{record['cleanup_current_revision_files']}** matching config/payload/plugin files; cộng r31/r33 là **{record['cleanup_files_total']}**. Hai project hooks đều không callable, protected global config hashes unchanged. [Final process audit](../runs/nckh-native-261005-0005-r34-attempt-01/final-process-audit.json) không có matching task process. Native conversation/trust history, archived packages, callbacks, policy receipts, oracles và failures được giữ.

Task native vẫn unchecked. Claude còn model/tool oracle và các events khác; chưa có configured approved-GPT route quan sát được ở Claude. Codex còn duplicate/other-event/protected-path gaps và bốn observed failure cases fail-open. Cursor còn timeout anomaly và events thiếu; AGY event faults giữ actual status ở trên, remaining native tools/surfaces và production timing còn mở. Codex Desktop/IDE, Cursor IDE, AGY IDE chưa có direct application receipts. Advertised targets giữ nguyên. Owner acceptance chỉ bind hai mẫu r29 đã đọc; quality/scientific/stable/install/release gates không tự đóng bằng các kiểm tra cấu trúc hoặc subset native.
"""
REPORT.with_suffix(".md").write_text(md, encoding="utf8", newline="\n")
print(json.dumps({"status": record["status"], "report": str(REPORT.with_suffix(".md")),
                  "tests": suite["deterministic"]["tests"], "extracted_totals": totals,
                  "cleanup_files": record["cleanup_files_total"]}), flush=True)
