"""Bind finished delivery and native observations without closing open surface gates."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
R31 = RUN.parent / "nckh-native-261004-2112-r31-attempt-01"
R32 = RUN.parent / "nckh-native-261004-2112-r32-attempt-01"
OLD = RUN.parent / "nckh-native-261004-1707-attempt-01"
REPORT = WORK / "plans/reports/delivery-261004-2112-r33-cursor-agy"


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind(path):
    return {"path": str(path.relative_to(WORK)), "sha256": sha(path)}


if REPORT.with_suffix(".json").exists() or REPORT.with_suffix(".md").exists():
    raise RuntimeError("Preserve existing delivery report")
component_names = ["deterministic-r33-attempt-01.json", "archive-summary.json", "smoke-summary.json",
                   "installer-previews.json", "final-preservation.json", "agy-native-file-summary.json"]
components = {name: read(RUN / name) for name in component_names}
assert all(row["status"] == "pass" for row in components.values())
context = read(RUN / "delivery-context.json")
assert context["status"] == "built" and context["source_revision"] == "33"
source_hash = context["source_lock_hash"]
assert all(row["source_lock_hash"] == source_hash for row in components.values())
suite = components["deterministic-r33-attempt-01.json"]
smoke = components["smoke-summary.json"]
preservation = components["final-preservation.json"]
plugin = read(RUN / "agy-native-workspace-plugin-summary.json")
assert plugin["status"] == "observed-qualified-duplicate" and plugin["source_lock_hash"] == source_hash
cleanup_paths = [R31 / "projects/cursor-model/cleanup.json", R31 / "projects/agy-model/cleanup.json",
                 RUN / "projects/agy-model/cleanup.json"]
cleanups = [read(path) for path in cleanup_paths]
assert all(not row["config_callable"] and all(item["unchanged"] for item in row["protected_native_config"])
           for row in cleanups)
process_audit = read(RUN / "final-process-audit.json")
assert process_audit["matching_native_processes"] == []
native_rows = []
for host in ("cursor", "agy"):
    for mode in ("allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash",
                 "unsupported-codec", "uncovered-tool", "duplicate"):
        path = R31 / "projects" / (host + "-model") / "attempts" / (mode + "-01.json")
        row = read(path)
        native_rows.append({**bind(path), "host": host, "mode": mode, "source_revision": 31,
                            "status": row["status"], "exit_code": row["exit_code"],
                            "oracle_created": row["oracle_created"], "callback_count": row["callback_count"],
                            "fault_origin": row["fault_origin"], "duplicate_kind": row.get("duplicate_kind")})
totals = {key: sum(row[key] for row in smoke["bundles"]) for key in
          ("resource_reads", "writer_disabled_observations", "hook_projections_exercised")}
open_gates = [
    {"host": "claude", "surface": "claude-code", "version": "2.1.272",
     "observed": "historical r30 SessionStart matrix only", "pending": "model/tool prevention and remaining events"},
    {"host": "codex", "surface": "codex-cli", "version": "0.154.0",
     "observed": "historical r30 prompt and eight GPT-medium local-tool cases",
     "pending": "four failure cases fail open; duplicate and other event routes remain unverified"},
    {"host": "cursor", "surface": "cursor-cli-print", "version": "2026.09.15-d2fe57e",
     "observed": "r31 SessionStart/PreToolUse/PostToolUse; allow/deny/fault cases",
     "pending": "beforeSubmitPrompt/stop absent on this route; uncovered/duplicate have native hook timeout anomalies"},
    {"host": "agy", "surface": "agy-cli-print", "version": "1.2.16",
     "observed": "r31 five selected events and shell cases; r33 protected native file paths and workspace-plugin duplicate",
     "pending": "failure matrix per other selected event and other surfaces remains incomplete"},
    {"host": "codex", "surface": "codex-desktop", "version": "unobserved", "pending": "direct app event receipts"},
    {"host": "codex", "surface": "codex-ide", "version": "unobserved", "pending": "direct IDE event receipts"},
    {"host": "cursor", "surface": "cursor-ide", "version": "unobserved", "pending": "direct IDE event receipts"},
    {"host": "agy", "surface": "agy-ide", "version": "unobserved", "pending": "direct IDE event receipts"},
]
record = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
          "status": "local-delivery-pass-native-surface-gate-open", "source_revision": 33,
          "source_lock_hash": source_hash, "source_pins": suite["source_files_pinned"],
          "identities": suite["identities"], "base_cases": suite["skill_cases"],
          "families": suite["required_families"], "resources": 9,
          "deterministic": suite["deterministic"], "components": [bind(RUN / name) for name in component_names],
          "delivery_artifacts": context["artifacts"], "archive_chain": components["archive-summary.json"]["artifacts"],
          "extracted_totals": totals, "installer_previews": components["installer-previews.json"]["surfaces"],
          "preservation": preservation, "native_r31_rows": native_rows,
          "native_r33_files": components["agy-native-file-summary.json"], "native_r33_workspace_plugin": plugin,
          "cleanup": [bind(path) for path in cleanup_paths], "process_audit": bind(RUN / "final-process-audit.json"),
          "native_model_grant": bind(R31 / "cursor-agy-model-dangerous-grant.json"),
          "model_selection_snapshot": bind(R31 / "cursor-agy-model-selection.json"),
          "source_review": bind(R32 / "source-native-path-review.json"),
          "runtime_source_equivalence": bind(RUN / "r31-runtime-r33-source-equivalence.json"),
          "native_before_failure": bind(R31 / "projects/agy-model/attempts/protected-file-before-01.reconciliation.json"),
          "owner_feedback": bind(OLD / "owner-feedback.json"), "owner_scope": "two exact displayed r29 writer samples accepted",
          "native_gate": "unverified/incomplete", "open_gates": open_gates,
          "installed_revision": 25, "installed_update": "not-performed", "stable_release": "not-performed",
          "scientific_qualification": "pending", "backend_model_attestation": "not-observed", "billing": "not-observed",
          "plan_progress": {"done": 44, "total": 45, "native_checkbox": "unchecked"}}
REPORT.with_suffix(".json").write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
rows = {host: {row["mode"]: row for row in native_rows if row["host"] == host} for host in ("cursor", "agy")}
table = "\n".join("| " + mode + " | " + ("Có" if rows["cursor"][mode]["oracle_created"] else "Không")
                    + " | " + ("Có" if rows["agy"][mode]["oracle_created"] else "Không") + " |"
                    for mode in rows["cursor"])
md = f"""# Delivery r33 và native Cursor/AGY

## Kết quả hiện tại

Candidate **r33** đạt local delivery; plan giữ **in-progress, 44/45** vì native event/surface gate chưa đủ. Hai mẫu VI/EN của r29 đã được owner chấp nhận. [Structured bindings](./delivery-261004-2112-r33-cursor-agy.json) giữ hashes và exact run paths. Installed r25 giữ nguyên; chưa có stable/scientific/release acceptance.

Source có {suite['source_files_pinned']} pins, canonical hash `{source_hash}`. Exact {suite['identities']} identities, {suite['skill_cases']} base cases, {suite['required_families']} families, 9 resources; historical 148 IDs/224 cells và writer sample bindings giữ nguyên. OFF chỉ là internal comparison; public resource contract vẫn ON.

## Sửa lỗi từ native evidence

- **r31:** AGY PreToolUse yêu cầu `decision`; codec trả `ask` cho policy không chặn, giữ native permission checks, và `deny` cho block/pending. Regression và actual shell allow/deny đã ghi riêng. Không dùng `allow`/`permissionOverrides` để ngầm cấp quyền.
- **r32:** sửa kỳ vọng closure test cũ từ `{{}}` thành `{{"decision":"ask"}}` riêng AGY. Full r32 đạt 183 tests, một Windows symlink skip. Các r31 failure receipts giữ nguyên.
- **r33:** [phép thử native trước sửa](../runs/nckh-native-261004-2112-r31-attempt-01/projects/agy-model/attempts/protected-file-before-01.reconciliation.json) đã tạo marker 19 bytes trong `private` vì codec bỏ `TargetFile`. Marker có newline; collector trước đó báo lỗi và giữ bytes. Không gọi việc tạo marker này là policy deny.
- Codec mới đọc các native path fields được [AGY công bố](https://antigravity.google/docs/hooks/#supported-tools), từ chối target thiếu/sai kiểu và kiểm mọi supplied alias. [Review/preimages/focused receipts](../runs/nckh-native-261004-2112-r32-attempt-01/source-native-path-review.json) giữ ba changed pins. Regression trước sửa có 21 subcase failures; sau sửa 14 focused tests đạt.

## Local delivery đã chạy thật

| Gate | Kết quả |
|---|---|
| Full deterministic r33 | {suite['deterministic']['tests']} tests, {len(suite['deterministic']['skipped'])} skip; successful; {suite['deterministic']['seconds']:.3f} giây |
| Reproducibility/build | 4 variants, 16 persistent host bundles |
| Archive/extraction | 16 archives giải nén ngoài source, manifest/closure verified |
| Extracted readers | {totals['resource_reads']} resource reads; {totals['writer_disabled_observations']} writer disabled/no-read observations |
| Hook closure | {totals['hook_projections_exercised']} primary/reference projections |
| Installer preview | 8 surfaces, 39 skills + 6 agents, project bytes unchanged |
| Preservation | {preservation['protected_hashes_checked']} protected hashes unchanged; installed r25 và four legacy schema-v1 bundles preserved |

Receipt entrypoints: [full suite](../runs/nckh-native-261004-2112-r33-attempt-01/deterministic-r33-attempt-01.json), [archives](../runs/nckh-native-261004-2112-r33-attempt-01/archive-summary.json), [smoke](../runs/nckh-native-261004-2112-r33-attempt-01/smoke-summary.json), [previews](../runs/nckh-native-261004-2112-r33-attempt-01/installer-previews.json), [preservation](../runs/nckh-native-261004-2112-r33-attempt-01/final-preservation.json). Source unchanged guards bind r33; r32's incomplete archive/smoke delivery được supersede bằng r33, không regrade r32.

## Native CLI matrix r31

Cursor CLI `2026.09.15-d2fe57e` nhận selector `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]` và native init báo **Grok 4.7 500K Extra High**. Hai selector errors/256K mismatch cũ giữ nguyên. Flags là `--force --trust --sandbox disabled`, chỉ dùng project thử riêng.

AGY CLI `1.2.16` dùng `gemini-3.8-flash-medium`, `--effort medium` và `--dangerously-skip-permissions`; native init báo `always-proceed`. Đây là native metadata, chưa là backend attestation hoặc billing receipt.

| Case | Cursor tạo oracle | AGY tạo oracle |
|---|---:|---:|
{table}

Hai host có genuine PreToolUse callbacks, policy deny trước shell side effect. Fault cases là controller injection sau callback thật; unsupported-codec không phải native host tự phát unsupported event. Uncovered bỏ controller mapping của tool thật: AGY ghi manual/ask rồi chạy shell; Cursor ghi manual nhưng host báo hook timeout, nên chưa có kết luận prevention từ policy.

Cursor uncovered bị owned runner terminate sau 270 giây. Duplicate project + transient CLI plugin có hai same-tool callbacks và một policy receipt, nhưng native host báo `Hook script timed out after 20000ms` và không tạo oracle. Hai observer runs exit0/JSON hợp lệ không giải thích được native timeout; giữ limitation. Cursor chỉ quan sát sessionStart/preToolUse/postToolUse ở print route; beforeSubmitPrompt/stop chưa có callbacks.

AGY r31 quan sát đủ năm selected event types; duplicate r31 là hai project groups. Fault selection chỉ ở PreToolUse. Wrapper baseline 20s/fault timeout 2s/sleep8s là test harness; public template vẫn 5s, chưa có production timing qualification. [Source equivalence](../runs/nckh-native-261004-2112-r33-attempt-01/r31-runtime-r33-source-equivalence.json): Cursor 25/25 runtime members không đổi so với r33; AGY 24/25, nên historical receipts giữ packaged r31 binding.

## Native file tools và workspace plugin r33

[Ba file-tool cases](../runs/nckh-native-261004-2112-r33-attempt-01/agy-native-file-summary.json) dùng verified archive/extracted r33 và model/quyền đã cấp:

- `write_to_file` ở đường dẫn được phép: actual tool DONE và marker được tạo; codec `ask` giữ native permission route.
- `write_to_file` trong `private`: codec/policy deny, native tool ERROR với `private-holdout-credential-path`, target vẫn absent.
- `view_file` trong `private`: codec/policy deny, native tool ERROR; seeded test marker giữ nguyên hash. Không dùng nội dung riêng thật.

[Workspace plugin duplicate](../runs/nckh-native-261004-2112-r33-attempt-01/agy-native-workspace-plugin-summary.json) dùng [documented project plugin location](https://antigravity.google/docs/plugins/#manual-plugin-installation) `.agents/plugins/`: project + plugin có hai callbacks cùng session/step/tool, một idempotent policy receipt, một actual terminal tool DONE và một oracle. Không gọi plugin installer/profile global.

Đây là tool/version/surface observations đúng các cases trên; chưa qualify mọi native tool, five-event failure matrix hoặc IDE surfaces. Chưa gọi production `configure-hooks.py apply`.

## Cleanup và phần còn mở

[r31 Cursor cleanup](../runs/nckh-native-261004-2112-r31-attempt-01/projects/cursor-model/cleanup.json), [r31 AGY cleanup](../runs/nckh-native-261004-2112-r31-attempt-01/projects/agy-model/cleanup.json), [r33 AGY cleanup](../runs/nckh-native-261004-2112-r33-attempt-01/projects/agy-model/cleanup.json) gỡ 82 matching config/payload/plugin files tổng cộng, giữ mọi native observations/commands/policy/oracles. Protected global configuration hashes unchanged. Native conversation/project trust state có thể còn lưu; không sửa trực tiếp trust store. [Final process audit](../runs/nckh-native-261004-2112-r33-attempt-01/final-process-audit.json) không có matching native test process.

Native task vẫn unchecked: Claude chưa có model/tool oracle; Codex có bốn hook failures fail-open và còn duplicate/other-event gaps; Cursor thiếu print-route events và có timeout anomalies; AGY còn per-event failure coverage. Codex Desktop/IDE, Cursor IDE và AGY IDE chưa có direct app receipts. Không thu hẹp advertised targets để đóng gate. Rights/stable/scientific/install/release vẫn là các lane riêng; owner feedback chỉ bind hai mẫu đã đọc.

## History

[r30 checkpoint](./delivery-261004-1707-r30-native-checkpoint.md) và [r30 model/tool addendum](./delivery-261004-1707-r30-model-tools.md) giữ nguyên. R31 initial failed suite, r32 full pass, r33 initial failed regression và preparation/helper failures đều được giữ; source-lock histories/preimages không bị ghi đè. Plan parser/hash/link checks xác nhận state/integrity, không thay native hoặc scientific evidence.
"""
REPORT.with_suffix(".md").write_text(md, encoding="utf8", newline="\n")
print(json.dumps({"status": record["status"], "report": str(REPORT.with_suffix(".md")), "tests": suite["deterministic"]["tests"],
                  "native_rows": len(native_rows), "extracted_totals": totals}), flush=True)
