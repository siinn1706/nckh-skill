"""Bind native model/tool observations without broadening their qualification scope."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = RUN / "projects/codex-model"
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record

REPORT = WORK / "plans/reports/delivery-261004-1707-r30-model-tools.json"
MARKDOWN = REPORT.with_suffix(".md")
if REPORT.exists() or MARKDOWN.exists():
    raise RuntimeError("Preserve previous model/tool report")


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


lock = verify_source_lock(ROOT)
source_hash = digest_record(lock)
if source_hash != "55a4b60779228f3be3ae42d7691a49dec1df1b4e6f26139a32435aa1914562e1":
    raise RuntimeError("Source drifted from frozen r30")
registration = read(PROJECT / "tool-probe-registration.json")
grant = read(RUN / "model-medium-grant.json")
if grant["reasoning_effort"] != "medium" or registration["source_lock_hash"] != source_hash:
    raise RuntimeError("Source/grant binding differs")
definition = "sha256:f26dcc9290135bcf225d52cdff4a72130753dc33758b46a5ebf2a5b314e71206"
expected = {"allow": ("completed", True), "policy-deny": ("blocked", False),
            "malformed-input": ("blocked", False), "malformed-output": ("failed", True),
            "timeout": ("failed", True), "crash": ("failed", True),
            "unsupported-codec": ("failed", True), "uncovered-tool": ("completed", True)}
cases = []
usage_totals = {}
bindings = [RUN / "model-medium-grant.json", RUN / "native-grant.json", RUN / "owner-feedback.json",
            RUN / "codex-model-tool-probe.py", RUN / "codex-tool-failure-observer.py",
            PROJECT / "tool-probe-registration.json", PROJECT / "tool-probe-cleanup.json",
            RUN / "host-model-grant-prerequisites.json", RUN / "process-audit-model-tools-final.json"]
for mode, (status, exists) in expected.items():
    path = PROJECT / f"tool-probe-{mode}-attempt-01.json"
    record = read(path)
    thread = record["thread"]["result"]
    hooks = record["hooks"]
    if record["status"] != "completed" or (thread["model"], thread["reasoningEffort"]) != ("gpt-5.6-luna", "medium"):
        raise RuntimeError("Model turn did not complete under the exact grant: " + mode)
    if len(hooks) != 1 or (hooks[0]["currentHash"], hooks[0]["trustStatus"], hooks[0]["enabled"]) != (definition, "trusted", True):
        raise RuntimeError("Native definition/trust differs: " + mode)
    observations = record["native_observations"]
    if len(observations) != 1 or observations[0]["reported_event"] != "PreToolUse" or observations[0]["native_tool_name"] != "Bash":
        raise RuntimeError("No exact native model tool callback: " + mode)
    if observations[0]["native_model"] != "gpt-5.6-luna":
        raise RuntimeError("Native hook model differs")
    notifications = record["notifications"]
    runs = [row["params"]["run"] for row in notifications if row.get("method") == "hook/completed"]
    commands = [row["params"]["item"] for row in notifications if row.get("method") == "item/completed"
                and row.get("params", {}).get("item", {}).get("type") == "commandExecution"]
    turns = [row for row in notifications if row.get("method") == "turn/completed"]
    if len(runs) != 1 or runs[0]["status"] != status or len(turns) != 1 or turns[0]["params"]["turn"]["status"] != "completed":
        raise RuntimeError("Native hook/turn status differs: " + mode)
    marker = Path(record["marker"])
    if marker.is_file() != exists or record["marker_exists"] != exists:
        raise RuntimeError("Native side-effect oracle differs: " + mode)
    if exists:
        if len(commands) != 1 or commands[0]["exitCode"] != 0 or digest_file(marker) != record["marker_sha256"]:
            raise RuntimeError("Successful native tool/oracle binding differs: " + mode)
        bindings.append(marker)
    elif commands:
        raise RuntimeError("Denied native tool has a completed command item")
    config = record["effective_config"]["result"]["config"]
    if config["model_reasoning_effort"] != "medium" or any(row["enabled"] for area in ("plugins", "mcp_servers") for row in config[area].values()):
        raise RuntimeError("Invocation configuration differs")
    raw = RUN / f"commands/codex-tool-probe-{mode}-attempt-01.stdout.jsonl"
    messages = [json.loads(line) for line in raw.read_text(encoding="utf8").splitlines()]
    listings = [row["result"] for row in messages if isinstance(row.get("result"), dict) and "data" in row["result"]
                and any("hooks" in item for item in row["result"]["data"])]
    if len(listings) != 1:
        raise RuntimeError("Actual hooks/list response is missing")
    globals_ = [row for area in listings[0]["data"] for row in area.get("hooks", [])
                if row.get("sourcePath", "").casefold() == str(Path(r"C:/Users/USER\.codex\hooks.json")).casefold()]
    if len(globals_) != 27 or any(row.get("enabled") for row in globals_):
        raise RuntimeError("User hooks were not isolated for the native turn")
    usage = [row["params"]["tokenUsage"] for row in notifications if row.get("method") == "thread/tokenUsage/updated"]
    total = usage[-1]["total"] if usage else {}
    for name, value in total.items():
        usage_totals[name] = usage_totals.get(name, 0) + value
    cases.append({"name": mode, "callbacks": 1, "native_hook_status": status, "native_feedback": runs[0]["entries"],
                  "native_tool": "Bash", "tool_use_id": observations[0]["native_tool_use_id"],
                  "model_requested": "gpt-5.6-luna", "native_thread_effort": "medium", "turn_completed": True,
                  "completed_command_items": len(commands), "marker_created": exists, "marker_sha256": record["marker_sha256"],
                  "policy_receipts": record["policy_receipts"], "reported_token_usage_total": total,
                  "fault_after_real_callback": mode in {"malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"},
                  "controller_uncovered_route": mode == "uncovered-tool"})
    bindings.append(path)
metadata = {number: read(PROJECT / f"model-metadata-attempt-{number:02d}.json") for number in (1, 2, 3)}
project_rows = [[row for area in metadata[number]["hook_list"].get("result", {}).get("data", []) for row in area.get("hooks", [])
                 if row.get("sourcePath", "").casefold() == str(PROJECT / ".codex/hooks.json").casefold()] for number in (1, 2, 3)]
if project_rows[0] or project_rows[2] or len(project_rows[1]) != 1 or project_rows[1][0]["enabled"]:
    raise RuntimeError("Before/after native hook cleanup state differs")
cleanup = read(PROJECT / "tool-probe-cleanup.json")
audit = read(RUN / "process-audit-model-tools-final.json")
if cleanup["status"] != "pass" or not cleanup["config_absent"] or not cleanup["runtime_absent"] or len(cleanup["removed_members"]) != 26:
    raise RuntimeError("Matching native cleanup is incomplete")
if audit["matching_count"] != 0 or not cleanup["unrelated_hook_state_unchanged"]:
    raise RuntimeError("Process/native state cleanup differs")
process_receipts = sorted((RUN / "commands").glob("codex-tool-probe-*.json"))
process_receipts += sorted((RUN / "commands").glob("codex-model-metadata-*.json"))
process_receipts += [PROJECT / f"tool-probe-tui-process-{number:02d}.json" for number in (1, 2)]
process_receipts += [RUN / f"commands/{name}.json" for name in ("cursor-auth-status-model-grant-01", "agy-models-help-model-grant-01", "agy-models-model-grant-01")]
if any(not read(path).get("process_exited") for path in process_receipts):
    raise RuntimeError("An owned process lacks terminal exit evidence")
bindings += process_receipts
bindings += [PROJECT / f"model-metadata-attempt-{number:02d}.json" for number in (1, 2, 3)]
bindings += sorted((RUN / "commands").glob("codex-tool-probe-*.stdout.jsonl"))
bindings += sorted((RUN / "commands").glob("codex-tool-probe-*.stderr.txt"))
bindings += sorted((PROJECT / "tool-observations").glob("*/*.json"))
bindings += sorted((PROJECT / "tool-policy-receipts").glob("*/*.json"))
result = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
          "status": "native-model-tool-denial-and-fail-open-observed-full-qualification-pending", "goal_turn_classification": "progress",
          "source_revision": lock["revision"], "source_lock_hash": source_hash, "source_pins": len(lock["files"]),
          "source_changed": False, "full_suite_build_rerun": False, "plan_progress": {"done": 44, "total": 45},
          "host": "Codex CLI", "version": "0.154.0", "event": "PreToolUse", "model": "gpt-5.6-luna", "reasoning_effort": "medium",
          "execution_route": "installed-CLI-app-server-stdio-thread-start-turn-start-native-model-unifiedExecStartup",
          "trust_route": "normal-CLI-TUI-exact-single-project-definition", "native_definition_hash": definition,
          "callbacks": 8, "completed_model_turns": 8, "policy_receipts": sum(len(row["policy_receipts"]) for row in cases),
          "oracle_files_created": sum(row["marker_created"] for row in cases), "cases": cases,
          "fail_open_cases": [row["name"] for row in cases if row["native_hook_status"] == "failed"],
          "reported_token_usage_totals": usage_totals, "provider_billing_receipt": "not-observed", "gateway_backend_model_attestation": "not-observed",
          "model_grant_resolved": True, "other_host_prerequisites": read(RUN / "host-model-grant-prerequisites.json"),
          "coverage_limits": ["one Windows native model shell route only; no direct TUI/desktop/IDE inference coverage",
              "fault injection follows genuine callback; no claim host generated malformed/unsupported event",
              "controller-uncovered case uses real Bash with its context mapping omitted; no native unsupported-tool oracle",
              "Bash payload has command field and no file_path/path; this experiment does not prove protected-path extraction or blocking",
              "Codex project/plugin duplicate and remaining events/surfaces still unverified"],
          "cleanup": {"config_removed": True, "staged_payload_members_removed": 26, "project_hooks_after": 0,
                      "new_project_test_state_keys_disabled": 1, "total_historical_and_new_test_state_keys_disabled": 4,
                      "unrelated_hook_state_unchanged": True, "matching_run_processes": 0, "oracle_evidence_preserved": True},
          "evidence_bindings": [{"path": str(path.relative_to(WORK)), "sha256": digest_file(path)} for path in dict.fromkeys(bindings)]}
atomic_json(REPORT, result)
labels = {"allow": "Allow", "policy-deny": "Policy deny", "malformed-input": "Malformed runner input (injected)",
          "malformed-output": "Malformed output (injected)", "timeout": "Timeout 2 giây / sleep 8 giây", "crash": "Observer crash exit17",
          "unsupported-codec": "Unsupported selected codec", "uncovered-tool": "Bash thiếu controller mapping"}
table = "\n".join(f"| {labels[row['name']]} | `{row['native_hook_status']}` | {'Có' if row['marker_created'] else 'Không'} | {', '.join(receipt['decision'] for receipt in row['policy_receipts']) or 'Không có policy receipt'} |" for row in cases)
MARKDOWN.write_text(f"""# NCKH r30 — native model/tool checkpoint

Quyền mới cho phép `gpt-5.6-luna` hoặc `gpt-6.1-sol`, mức `medium`, được lưu trong [model grant](../runs/nckh-native-261004-1707-attempt-01/model-medium-grant.json). Cả hai xuất hiện trong native `model/list`; lượt kiểm chứng này dùng `gpt-5.6-luna/medium`. [Structured evidence](delivery-261004-1707-r30-model-tools.json) bind source, definition, callbacks, completed turns, oracle và cleanup.

## Quan sát thực

Codex CLI **0.154.0**, Windows, route `app-server --stdio → thread/start → turn/start → native model exec_command/unifiedExecStartup`, event **PreToolUse**, matcher/native tool **Bash**. Có **8 completed model turns, 8 genuine callbacks, 5 policy receipts và 6 tệp oracle**. Native thread và payload cùng báo đúng model, effort `medium`; không có fallback sang model khác trong thread. Đây là runtime metadata, chưa có gateway/backend model attestation hoặc hóa đơn provider.

| Ca | Native hook | Tệp oracle được tạo | Policy |
|---|---|---|---|
{table}

`allow` thực sự chạy shell exit0 và tạo tệp; `policy-deny` nhận callback với cùng kiểu action, trả deny `plan-only-mutation`, native hook `blocked`, không có completed command item và không có tệp. Malformed runner input được inject sau callback cũng chặn. Đây là preventive evidence cho đúng route/event/version đã thử.

Malformatted output, timeout, crash và unsupported selected codec có native `failed` rồi shell vẫn exit0/tạo tệp: **bốn failure cases fail-open**. Không nâng deterministic `block` receipt của unsupported codec thành host prevention. Observer cố ý crash exit17; Windows host command layer báo exit1. Native unsupported-event/tool vẫn chưa được chứng minh: test selected-codec khác event, còn uncovered case dùng Bash thật nhưng bỏ controller mapping.

## Phạm vi và isolation

Definition hash: `{definition}`. Normal native TUI review/trust/enable riêng đúng project hook, rồi disable. Mỗi lượt actual `hooks/list` xác nhận 27 user hooks disabled theo invocation; effective config xác nhận ba configured MCP servers và 13 plugins disabled. Hook runner/policy không gọi provider; model turn do controller gọi theo quyền mới. TUI trust/cleanup dùng endpoint refused-loopback, không chạy inference.

Bash payload có `tool_input.command`, không có structured `file_path/path`; phép thử này không xác nhận protected-path extraction/credential-path blocking. Hosted tools, shell continuations, Codex project/plugin duplicate, các event còn lại, direct TUI/desktop/IDE inference đều chưa có coverage từ tám cases này. Chưa activate production route như enforcement.

Source giữ **r30/281 pins**, hash `{source_hash}`. Full deterministic/build/extract evidence đã có cho cùng source nên không chạy lại. Hai mẫu owner VI/EN giữ acceptance/hashes ban đầu; installed r25 chưa đổi.

## Cleanup

[Matching cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex-model/tool-probe-cleanup.json) gỡ một config và 26 staged payload members sau native UI disable. [Native list sau cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex-model/model-metadata-attempt-03.json) không còn project hook callable. Một test key mới còn trusted/disabled; cộng ba key lịch sử là bốn test keys disabled, không phải bốn hash hiện hành của cùng UserPromptSubmit key. Unrelated native user-hook state không đổi. [Final process audit](../runs/nckh-native-261004-1707-attempt-01/process-audit-model-tools-final.json) có 0 matching run processes. Giữ six oracle files, contexts và receipts làm evidence.

## Điều kiện còn thiếu

[Host preflight mới](../runs/nckh-native-261004-1707-attempt-01/host-model-grant-prerequisites.json): Cursor CLI vẫn chưa đăng nhập. AGY `models` qua kết nối thật exit0, danh mục không có hai GPT models được cấp quyền; command này không xác nhận prompt eligibility hoặc native hook coverage. Claude Code chưa có configured route tới hai GPT models trong phần settings đã đọc; chưa gọi model khác. Không chuyển quyền GPT thành quyền dùng mặc định Claude/Gemini.

Codex CLI `plugin add` dùng marketplace selector; installed `PluginInstallParams` không có destination/scope field. [Official local marketplace guide](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo) mô tả repo marketplace và enabled state; [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) nói refresh có thể install/refresh cả khi disabled. Chưa xác định và thử route duplicate không ghi global plugin state; không cài plugin global để đóng gate.

Plan giữ **in-progress, 44/45**: native host/version/surface/event task còn unchecked. Model grant đã tháo điều kiện provider cho hai lựa chọn được nêu; các host/account/surface prerequisites và native cells còn thiếu được giữ riêng. Goal turn này là progress, chưa complete.
""", encoding="utf8")
print(json.dumps({"status": result["status"], "callbacks": 8, "completed_model_turns": 8, "oracle_files": 6,
                  "fail_open_cases": result["fail_open_cases"], "cleanup": "pass", "bindings": len(result["evidence_bindings"])}))
