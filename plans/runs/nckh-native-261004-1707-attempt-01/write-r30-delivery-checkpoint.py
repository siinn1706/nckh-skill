"""Bind actual local checks, owner feedback and bounded native observations."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
REPORTS = WORK / "plans/reports"
STEM = "delivery-261004-1707-r30-native-checkpoint"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record


def read(name):
    return json.loads((RUN / name).read_text(encoding="utf8"))


def link(name, label):
    return f"[{label}](../runs/{RUN.name}/{name})"


lock = verify_source_lock(ROOT)
source_hash = digest_record(lock)
checks = read("deterministic-r30-attempt-02.json")
context = read("delivery-context.json")
archives = read("archive-summary.json")
smoke = read("smoke-summary.json")
previews = read("installer-previews.json")
preservation = read("final-preservation.json")
owner = read("owner-feedback.json")
native = read("native-r30-claude-summary.json")
cleanup = read("native-cleanup.json")
codex = read("codex-native-cleanup-observation.json")
repair = read("r30-source-checkpoint.json")
for item in (checks, context, archives, smoke, previews, preservation, native, repair):
    if item["source_lock_hash"] != source_hash:
        raise RuntimeError("Evidence does not bind the current source lock")
for item in (checks, archives, smoke, previews, preservation, cleanup):
    if item["status"] != "pass":
        raise RuntimeError("Checkpoint may not claim a failed required local check")
if len(archives["artifacts"]) != 16 or len(smoke["bundles"]) != 16 or len(previews["surfaces"]) != 8:
    raise RuntimeError("Missing host/variant evidence")
reads = sum(row["resource_reads"] for row in smoke["bundles"])
disabled = sum(row["writer_disabled_observations"] for row in smoke["bundles"])
projections = sum(row["hook_projections_exercised"] for row in smoke["bundles"])
if (reads, disabled, projections) != (216, 48, 24):
    raise RuntimeError("Extracted observations differ from the accepted contract")
for sample in owner["samples"]:
    if sample["feedback"] != "accepted":
        raise RuntimeError("Owner feedback not accepted")
    for path_field, hash_field in (("input_path", "input_sha256"), ("artifact_path", "artifact_sha256")):
        if digest_file(WORK / sample[path_field]) != sample[hash_field]:
            raise RuntimeError("Owner sample bytes changed")

tracks = [
    {"host": "claude", "surface": "claude-code", "version": "2.1.272", "source_revision": "30",
     "events": {"SessionStart": "observed-native-startup-only", "UserPromptSubmit": "not-exercised",
                "PreToolUse": "not-exercised", "PostToolUse": "not-exercised", "Stop": "not-exercised"},
     "limitations": ["no-provider-turn", "no-preventive-tool-side-effect-oracle"],
     "receipt": "native-r30-claude-summary.json"},
    {"host": "codex", "surface": "codex-cli", "version": "0.154.0", "source_revision": "29",
     "events": {name: "unobserved" for name in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop")},
     "observations": ["normal-workspace-trust", "two-exact-hook-trust-hashes", "specialized-local-shell-returned-no-callback",
                      "two-hooks-disabled-through-host-ui-before-project-config-removal"],
     "limitations": ["local-shell-path-does-not-qualify-model-tool-coverage"],
     "receipt": "codex-native-cleanup-observation.json"},
    {"host": "cursor", "surface": "cursor-cli", "version": "2026.09.15-d2fe57e", "source_revision": "29",
     "events": {name: "unobserved" for name in ("sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop")},
     "limitations": ["authentication-required-before-callback"], "receipt": "commands/cursor-native-pre-call.json"},
    {"host": "agy", "surface": "agy-cli", "version": "1.2.16", "source_revision": "29",
     "events": {name: "unobserved" for name in ("PreInvocation", "PostInvocation", "PreToolUse", "PostToolUse", "Stop")},
     "limitations": ["eligibility-check-blocked-by-loopback-proxy", "no-hook-support-inference-from-account-error"],
     "receipt": "commands/agy-native-local-probe.json"},
]
for host, surface in (("codex", "codex-desktop"), ("codex", "codex-ide"), ("cursor", "cursor-ide"), ("agy", "agy-ide")):
    names = ("PreInvocation", "PostInvocation", "PreToolUse", "PostToolUse", "Stop") if host == "agy" else (
        "sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop") if host == "cursor" else (
        "SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop")
    tracks.append({"host": host, "surface": surface, "version": "unobserved-in-this-run", "source_revision": "30",
                   "events": {name: "not-exercised" for name in names}, "limitations": ["exact-app-surface-run-required"],
                   "receipt": None})

receipt_names = ["owner-feedback.json", "native-grant.json", "r30-source-checkpoint.json", "source-review.json",
                 "deterministic-r30.json", "deterministic-r30-attempt-02.json", "delivery-context.json",
                 "archive-summary.json", "smoke-summary.json", "installer-previews.json", "final-preservation.json",
                 "native-r30-claude-summary.json", "codex-native-cleanup-observation.json", "native-cleanup.json",
                 "native-approval-review.json", "native-r30-claude-attempt-01-helper-failure.json"]
record = {
    "schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(), "status": "technical-pass-native-pending",
    "source_revision": lock["revision"], "source_lock_hash": source_hash, "source_pins": len(lock["files"]),
    "changed_from_r29": repair["changed"], "writer_instruction_pins_unchanged": True,
    "membership": {"skills": 39, "base_cases": 156, "families": 19, "resources": 9,
                   "historical_case_ids_preserved": 148, "historical_matrix_cells_preserved": 224},
    "local_checks": {"deterministic_tests": checks["deterministic"]["tests"], "skipped": len(checks["deterministic"]["skipped"]),
                     "seconds": checks["deterministic"]["seconds"], "archives": 16, "resource_reads": reads,
                     "writer_disabled_observations": disabled, "hook_projections": projections, "installer_surfaces": 8,
                     "protected_hashes": preservation["protected_hashes_checked"]},
    "owner_feedback": {"status": "accepted", "scope": owner["feedback_scope"], "sample_source_revision": owner["source_revision"],
                       "samples": owner["samples"], "propagation": "writer-instruction-bytes-unchanged; no-broader-human-qualification"},
    "native_tracks": tracks, "claude_session_start": native, "cleanup": cleanup,
    "global_residual": {"two_codex_definition_hashes": "trusted-disabled-no-project-config-or-payload",
                        "project_trust": "may-remain-for-disposable-project", "direct_trust_store_edits": 0},
    "prior_failures": [
        {"receipt": "deterministic-r30.json", "status": "timeout-unknown", "deadline_seconds": 900,
         "emitted_error_test": "tests.hooks.test_runner.HookRunnerTests.test_concurrent_duplicate_receipts_and_failed_attempts_are_preserved",
         "error_cause": "unknown-traceback-not-emitted-before-timeout", "later_same_source": "isolated-check-and-full-suite-pass",
         "fixture_or_test_weakening": False},
        {"receipt": "native-r30-claude-attempt-01-helper-failure.json", "cause": "helper-cleanup-relative-path-used-Windows-separators",
         "candidate_failure": False, "repair": "fresh-attempt-with-POSIX-relative-paths"},
        {"receipt": "native-approval-review.json", "action": "Codex-trust-all", "status": "auto-review-rejected",
         "reason": "could-include-unrelated-user-hooks", "executed": False, "replacement": "exact-project-definitions-reviewed-individually"},
    ],
    "plan_progress": {"completed_checkboxes": 44, "total_checkboxes": 45, "native_evidence_checkbox": "unchecked"},
    "authorization": {"routine_cook": "granted", "disposable_native_registration_trust": "granted",
                      "provider_spending": "not-granted-by-this-followup", "installed_r25_update": "not-performed",
                      "stable_scientific_release": "pending"},
    "archive_chain": archives["artifacts"], "receipt_hashes": {name: digest_file(RUN / name) for name in receipt_names},
    "review": {"scope": "three-r30-source-files-and-current-acceptance", "skill": "ak-code-review", "independent": False},
}
json_path = REPORTS / (STEM + ".json")
md_path = REPORTS / (STEM + ".md")
if json_path.exists() or md_path.exists():
    raise RuntimeError("Preserve existing checkpoint report")
atomic_json(json_path, record)
text = f"""# NCKH r30 — checkpoint sau xác nhận owner và thử native

Trạng thái: **technical PASS; owner VI/EN accepted; native evidence còn pending, plan 44/45**.

Thực thi theo [plan](../261004-0047-nckh-research-data-hooks-writing/plan.md) và quyền trực tiếp của người dùng. Native grant chỉ áp dụng project thử riêng; gói đang dùng r25 chưa đổi. [Structured record]({STEM}.json) giữ source, input/artifact, archive và receipt hashes.

## Xác nhận đã hoàn tất

{link('owner-feedback.json', 'Owner feedback')} ghi đúng lời người dùng: `1. cho phép; Mẫu VI: chấp nhận; Mẫu EN: chấp nhận`. Hai mẫu bind r29/input/artifact hashes đã hiển thị trong [writer trial](reviewer-261004-1037-writer-forward-test.md). Writer instructions giữ nguyên bytes ở r30. Feedback này chỉ chấp nhận hai mẫu; scientific/stable, holdout, economics và native acceptance có hồ sơ riêng.

## Sửa từ bằng chứng native

Claude 2.1.272 trên Windows với Git Bash đã loại backslashes trong command string của r29, báo executable không tồn tại. r30 truyền executable và `args` trực tiếp. Chỉ ba pinned files đổi: `core/hook_config.py`, `tests/hooks/test_config.py`, `docs/installation.md`; focused hooks đạt 21/21. {link('source-review.diff', 'Diff')} / {link('source-review.json', 'Inline review')} / {link('r30-source-checkpoint.json', 'Freeze delta')}. Không có independent reviewer mới hoặc Git checkout.

r30 có **281 pins**, canonical source-lock hash `{source_hash}`. Đúng 39 skills/156 base cases/19 families/9 resources; historical 148 IDs và 224 matrix cells giữ nguyên. r29 archives/receipts/history không bị ghi đè.

## Kiểm chứng r30

| Kiểm tra | Kết quả thực | Receipt |
|---|---|---|
| Full deterministic | 182 tests, `OK (skipped=1)`, 1222.501 giây theo unittest; symlink fixture bị giới hạn quyền Windows | {link('deterministic-r30-attempt-02.json', 'Complete unchanged suite')} |
| Reproducibility/build | 4 variants × 4 hosts, 16 persistent bundles | {link('delivery-context.json', 'Build context')} |
| Archive/extract | 16 ZIP thực, giải nén ngoài source rồi verify | {link('archive-summary.json', 'Archive chain')} |
| Resource/writer reads | 216 reads; 48 resource-OFF disabled/no-read observations | {link('smoke-summary.json', 'Extracted smoke')} |
| Hook portability | 24 primary/reference projections; runner/manual/config preview; disposable projects không đổi | {link('smoke-summary.json', 'Smoke receipts')} |
| Installer preview | 8 surfaces, mỗi preview 39 skills + 6 agents; không viết project | {link('installer-previews.json', 'Preview')} |
| Preservation | 509 protected hashes, installed r25 và 4 legacy schema-v1 bundles giữ nguyên | {link('final-preservation.json', 'Preservation')} |

Public package contract giữ resource access ON; OFF chỉ là internal comparison. [Đủ 16 archives](../runs/{RUN.name}/archives/) chưa được publish hoặc cập nhật installation.

## Native theo đúng surface/version/event

| Surface/version | Quan sát thực | Giới hạn |
|---|---|---|
| Claude Code 2.1.272, r30 | `SessionStart` gọi direct packaged runner; tám lượt instrumented entrypoints, tổng 10 callbacks gồm duplicate project/plugin hai callback | Chưa thử UserPromptSubmit, PreToolUse, PostToolUse, Stop; không có tool side-effect prevention oracle |
| Codex CLI 0.154.0, r29 | Host list nhận project definitions; hai hash được trust riêng; specialized local shell trả kết quả | Không có callback ở route đã thử, không suy model tool coverage |
| Cursor CLI 2026.09.15-d2fe57e, r29 | `Authentication required`, exit 1 trước callback | Cần phiên đăng nhập hợp lệ để chạy tiếp |
| AGY CLI 1.2.16, r29 | Eligibility check fail khi dùng loopback proxy, exit 1 trước callback | Không kết luận chưa đăng nhập hoặc không hỗ trợ hooks từ lỗi này; cần network/account eligibility được cấp quyền |
| Codex Desktop/IDE; Cursor IDE; AGY IDE | Chưa thử trong đúng app surface | Version/event native receipts vẫn pending, không đổi advertised targets |

{link('native-r30-claude-summary.json', 'Claude startup observations')} ghi direct, normal/advisory, bounded policy-block, malformed input, malformed output, injected sleeper, crash exit17, unsupported codec event và duplicate project/plugin. Các lượt `--init-only` đều host exit0. SessionStart là advisory; policy block được mã hóa thành context. Sleeper đã vào callback nhưng chưa hoàn tất khi host/job đóng; receipt không tự xác nhận host timeout prevention. Unsupported codec test đổi selected codec event, không giả host phát event lạ. Duplicate tạo hai callback, một policy receipt do idempotence. Các quan sát này không hoàn thành full native preventive failure matrix.

## Cleanup và trust còn lưu

{link('native-cleanup.json', 'Cleanup')} đạt: 14 project thử, bốn config còn lại và 362 staged payload members đã gỡ theo matching hashes, không conflict. Các config của lượt Claude r30 đã gỡ ngay sau mỗi run. Archives, extracted packages, context và evidence giữ lại. Owned process jobs đã đóng; không dừng tiến trình người dùng.

{link('codex-native-cleanup-observation.json', 'Codex cleanup observation')} xác minh PreToolUse và SessionStart thử đã tắt bằng normal UI. Host vẫn lưu hai trusted hashes, và project trust có thể còn lưu; không có config/payload project để gọi. Không sửa trực tiếp trust store/global user definitions để xóa những record này.

Automatic approval review đã từ chối `Codex /hooks trust all` vì có thể bao gồm hooks sẵn có của người dùng. Action đó không chạy. Đã review/trust riêng đúng hai project definitions; {link('native-approval-review.json', 'Rejection record')} giữ lý do và thay thế đã thực hiện.

## Failure history và công việc còn lại

- {link('deterministic-r30.json', 'Attempt 01')} timeout ở hạn 900 giây của existing eval wrapper, phát `E` ở concurrent receipt test trước khi có traceback. Nguyên nhân lỗi chưa xác định. Cùng source r30, isolated test và full 182-test run sau đó đều pass; không sửa/giảm/skip test để qua. Lượt đầy đủ mất hơn 900 giây, dùng direct unchanged unittest discovery với owned process tracking và không đặt hạn toàn suite. Per-test timeouts giữ nguyên.
- {link('native-r30-claude-attempt-01-helper-failure.json', 'Native helper failure')} là lỗi cleanup dùng Windows relative separators; direct packaged callback đã chạy. Giữ failure, gỡ matching config và tạo attempt mới; source không đổi.
- Native grant và owner VI/EN feedback đã hoàn tất. **Một checkbox P3 còn mở**: event/version/surface evidence đủ để quyết định từng route. Production hook activation vẫn inactive; không gọi production apply với evidence giả.
- Để thử PreToolUse/deny-side-effect matrix cần native model turns theo provider scope/budget riêng. Cursor cần login; AGY cần eligibility thành công qua kết nối thật. App/IDE tracks phải được thử trong đúng surface. Không lấy CLI evidence để đóng Desktop/IDE gate.

Gói r30 là candidate cục bộ đã kiểm chứng technical. Installed r25 update, public release và scientific/stable qualification chưa thực hiện.
"""
md_path.write_text(text, encoding="utf8", newline="\n")
print(json.dumps({"status": record["status"], "report": str(md_path), "source_revision": lock["revision"],
                  "tests": 182, "archives": 16, "owner": "accepted", "plan": "44/45"}), flush=True)
