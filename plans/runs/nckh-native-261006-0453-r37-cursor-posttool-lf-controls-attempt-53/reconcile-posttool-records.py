"""Record the qualified LF-content observations without closing broader native gates."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0453-r37-cursor-posttool-lf-controls.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}


def new_json(path, value):
    with path.open("x", encoding="utf8", newline="\n") as stream:
        stream.write(json.dumps(value,ensure_ascii=False,indent=2)+"\n")


verified = read(RUN / "verified-posttool-observations.json")
source = read(RUN / "final-source-check.json")
audit = read(RUN / "process-final-audit.json")
cleanup = read(RUN / "cleanup.json")
ownership = read(RUN / "native-process-ownership.json")
assert verified["status"] == "verified-seven-current-native-Write-posttool-observations"
assert verified["model_turns"] == verified["requested_native_Writes"] == 7
assert verified["callback_count"] == 29 and verified["policy_receipt_count"] == 27
assert verified["native_exit_code"] == verified["monitor_exit_code"] == 0
assert source["verified_pins"] == 281 and source["source_lock_hash"] == verified["source_lock_hash"]
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and len(audit["tracked"]) == 1542
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 33 and not cleanup["config_callable"]
timeout = next(row["timeout_observation"] for row in verified["results"] if row["mode"] == "timeout")
assert timeout["observed_callback_elapsed_seconds"] > timeout["declared_hook_bound_seconds"]
assert timeout["effective_native_deadline"] == "unqualified"
assert read(PRIOR / "verified-baseline-failure-observation.json")["frozen_byte_oracle"] == "failed-preserved"
reference = "../runs/"+RUN.name+"/"
report = f'''# Cursor CLI r37: nội dung LF và các quan sát PostToolUse/Write

[Bằng chứng đã xác minh]({reference}verified-posttool-observations.json) ghi **7 lượt model / 7 Write thật / 29 callbacks / 27 receipts** trên Cursor CLI **{verified['version']}**, Grok4.7/500k/xhigh/fast=false, Run Everything. Native terminal và monitor đều exit0. Source r37/281 pins/hash `{verified['source_lock_hash']}` giữ nguyên; full native task vẫn **unchecked / 44 of45 / P3 active**.

## Hợp đồng nội dung và byte

[Brief đóng băng]({reference}frozen-brief.json) tách **LF trong argument `content`** và **CRLF dự kiến trên đĩa**. Hash, độ dài32 byte và tail16 hex của argument thật khớp cả PreToolUse/PostToolUse cho từng marker. Hash tệp khớp bytes33 trên đĩa và đã hiện diện khi callback sau ghi bắt đầu. Mỗi lượt có một cặp pre/post Write cùng tool ID/session/path/version, một câu trả lời kết thúc đúng và không retry model.

Observer chỉ giữ hash/length/tail của đúng marker ASCII công khai do controller tạo; không lưu body native `content`. Việc đổi LF sang CRLF được quan sát trên tuyến Write này; hàm chuẩn hóa cụ thể bên trong vendor chưa được xác lập.

[Oracle52 thất bại]({"../runs/"+PRIOR.name+"/verified-baseline-failure-observation.json"}) giữ nguyên: yêu cầu CRLF nhưng nhận CRCRLF, policy pending/stale bytes, monitor exit1. Oracle LF44 cũng giữ nguyên thất bại. Ca53 có hợp đồng argument khác và diagnostics mới; không regrade hai ca cũ.

## Kết quả từng ca

| Ca | Observer sau Write | Policy/wire đã quan sát |
|---|---|---|
| allow | completed/exit0 | advisory; `delivery-bindings-current-review-separate` |
| policy-deny | completed/exit0 | block; `bounded-input-exceeded` trong additional_context |
| malformed-input | completed/exit0 | degraded block; `hook-input-or-context-invalid` |
| malformed-output | intentional invalid JSON | Không có selected policy receipt |
| timeout | completed/exit0 sau {timeout['observed_callback_elapsed_seconds']:.6f}s | advisory receipt sau mức khai báo5s; effective native deadline unqualified |
| crash | injected `os._exit(17)` sau callback thật | Không có selected policy receipt |
| unsupported-codec | completed/exit3 | degraded block receipt; native wire `{{}}` |

Năm lỗi là injection do controller sau callback native thật. Codec không hỗ trợ là selector thử; không chứng minh host giao một unknown event. Tệp đã thay đổi trước PostToolUse và còn đúng bytes ở cuối cả7 lượt; enforcement ngăn ghi/rollback/scientific QA vẫn unqualified.

Timeout có độ trễ khai báo8s, callback thực tế{timeout['observed_callback_elapsed_seconds']:.6f}s và receipt. Native timeout message quan sát: **{str(timeout['explicit_native_timeout_message_observed']).lower()}**; selected terminal retention complete: **{str(timeout['selected_terminal_retention_complete']).lower()}**. Mức timeout5s trong definition không tự chứng minh deadline hiệu lực của host. [Preimage và refinement]({reference}observation-scope-refinement.json) giữ đúng phạm vi này; byte/content oracles và điều kiện exit0 không đổi.

## Tiến trình và cleanup

[Ownership]({reference}native-process-ownership.json) bind root PID{ownership['root_pid']}/FILETIME{ownership['root_creation_filetime_ticks']} với terminal78758, project thử, owner `/root`, port do native CLI quản lý. Monitor79098 dùng GetExitCodeProcess và exact generation, xử lý root close bằng trạng thái thật. Snapshot cuối ghi root absent, không capture errors; harness xác nhận cả hai handle terminal exit0. Kết quả không regrade monitor failures51/52.

[Audit cuối]({reference}process-final-audit.json): union1542 identities từ bộ612 đã qualified và capture mới; zero matching/tracked-live. Raw historical union2968 không dùng làm ownership. Giữ27 ứng dụng preexisting; không taskkill/Stop-Process. Sau native `/exit`, [cleanup]({reference}cleanup.json) gỡ33 matching config/payload/fixture members, giữ{cleanup['historical_members_unchanged']} historical members và protected global config hashes. Native CLI-owned state có thể còn; controller không direct-write global.

## Verification và giới hạn còn lại

Verifier exit0 ở [tool result]({reference}verification-tool-result.json) kiểm hashes, actual input diagnostics, pre/post identities, bytes trước hook, final replies, selected receipt outcomes, terminal/monitor exits, historical preservation và audit. Review inline; không có independent reviewer. Một poll baseline bị output truncation được giữ rõ; bytes/callback evidence và final marker có bindings riêng.

Sandbox CIM preflight và dependent prepare từng fail trước model; [failure record]({reference}sandbox-preflight-failure.json) giữ cả hai. Read-only inventory đã chạy qua quyền process reconciliation, rồi mới stage và gửi model. Không retry model, đổi source hoặc che lỗi.

[Source check]({reference}final-source-check.json) xác minh current source. Reuse checkpoint192 successful tests/one Windows skip và16 archives cho source/input không đổi; không chạy lại broad suite. Installed r25, publication và human acceptance của exact r29 samples giữ scope riêng.

Các ô native còn thiếu, effective timeout deadline, root/glob search, project/plugin và direct IDE qualification vẫn mở. Quyền cache/metadata Codex ngoài workspace và Claude model/effort đã được hỏi lại sau recovery, chưa có câu trả lời; chưa cài plugin hoặc gửi Claude model prompt. AGY/Gemini3.8FlashMedium/dangerous và Cursor/Grok4.7/500k/xhigh/dangerous grants tiếp tục được giữ.
'''
with REPORT.open("x", encoding="utf8", newline="\n") as stream:
    stream.write(report)

paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "native-evidence-history.md", JOURNAL]
contents = {path:path.read_text(encoding="utf8") for path in paths}
before = {path:sha(path) for path in paths}
preimages = RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    with (preimages / path.name).open("xb") as stream:
        stream.write(path.read_bytes())
text = contents[paths[0]]
old = '[PostToolUse baseline52](../reports/delivery-261006-0423-r37-cursor-posttool-baseline-failure.md)'
assert text.count(old) == 1
text = text.replace(old,old+', [PostToolUse LF53](../reports/delivery-261006-0453-r37-cursor-posttool-lf-controls.md)')
old_start = text.index('Latest native52:')
old_end = text.index('\n\n',old_start)
summary = ('Latest native53:7 actual Write turns/29 callbacks/27 receipts; native content LF and disk CRLF matched in every case. '
    'Allow/bounded block/five injected post-tool faults recorded after exact mutations. Timeout callback8.263741s exceeds declared5s; effective native deadline unqualified. '
    'Native/monitor exit0 using actual exit-state checks; cleanup33/preserved1010/qualified temporal union1542/owned-live0;27 preexisting apps preserved. '
    'Native44/52 failed oracles remain preserved. Source r37/protected global hashes unchanged; full native task remains unchecked.')
text = text[:old_start]+summary+text[old_end:]
updates = {paths[0]:text}
note = ('[Cursor PostToolUse LF53](../reports/delivery-261006-0453-r37-cursor-posttool-lf-controls.md) records seven '
    'Grok4.7/500k/xhigh/fastfalse turns/seven actual Write operations on CLI2026.09.15-d2fe57e:29 callbacks/27 receipts; '
    'bounded actual content diagnostics prove LF argument and CRLF disk bytes for each marker before selected post callback. '
    'Advisory/bounded block/five injected post faults retain completed mutations/final replies; prevention/rollback/scientific QA unqualified. '
    'Timeout observer completes8.263741s vs declared5s with advisory receipt; effective host deadline unqualified/no explicit native timeout message observed. '
    'Actual exit-state monitor and native terminal exit0; cleanup33/preserved1010/qualified temporal union1542/zero owned-live/protected hashes unchanged. '
    'Preserve27 preexisting apps and failed oracles44/52/no regrade. Source r37 unchanged;44/45/P3 active.')
for path in paths[1:]:
    assert "Cursor PostToolUse LF53" not in contents[path]
    updates[path] = contents[path].rstrip()+"\n\n## Cursor LF-content post-tool controls and actual exit state\n\n"+note+"\n"
for path,value in updates.items():
    assert sha(path) == before[path]
    path.write_text(value, encoding="utf8", newline="\n")

todo = read(PRIOR / "native-continuation-todo.json")
todo["latest_scoped_evidence"] = bind(RUN / "verified-posttool-observations.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["process_state"] = "native53 terminal78758 and monitor79098 exit0; actual exit-state capture/qualified union1542/owned-live0;27 preexisting apps preserved; no process stop"
todo["source_final_check"] = bind(RUN / "final-source-check.json")
todo["Cursor_current_Write_PostToolUse"] = {"verification":bind(RUN / "verified-posttool-observations.json"), "report":bind(REPORT),
    "status":"verified-seven-scoped-native-Write-posttool-observations", "native_content":"LF exact hashes/length32/tail16",
    "disk_bytes":"CRLF exact hashes/length33 before selected callback", "turns":7,"callbacks":29,"receipts":27,
    "native52_original_oracle":"failed-preserved; no regrade", "effective_native_timeout_deadline":"unqualified",
    "timeout_observation":timeout, "preventive_rollback":"unqualified", "normalizer_internal_origin":"unqualified"}
todo["controller_exit_state"]["native_usage"] = "qualified53: actual GetExitCodeProcess state/generation; native and monitor exit0, no capture errors; root absent at final snapshot"
todo["controller_exit_state"]["native_verification"] = bind(RUN / "verified-posttool-observations.json")
todo["controller_capture_repair"]["native_usage"] = "qualified53: temporal ancestry/928 captured native identities/actual exit-state checks; historical51/52 failures retained"
todo["controller_capture_repair"]["next_liveness_requirement"] = "reuse actual state and exact generation; audit1542 qualified identities rather than raw legacy2968"
todo["current_verified_Cursor_scopes"].append("Write PostToolUse53: seven scoped LF-content/CRLF-disk observations,29 callbacks/27 receipts/native-monitor0; timeout effective deadline remains unqualified")
todo["pending_or_unqualified"].append("Cursor effective native PostToolUse deadline: delayed observer53 finishes8.263741s after declared5s; no explicit native timeout response observed")
todo["next_authorized_native_cell"] = ("Current-r37 Cursor Stop fault observations after an actual Write using qualified53 LF content/CRLF disk diagnostics and actual exit-state monitor. "
    "Reconcile1542 qualified identities before start; preserve53 timing limits and failures44/52. Other event/tool/plugin/surface cells remain scoped; cache authority and Claude selection pending.")
todo["current_turn_classification"] = "progress: seven causally distinct current Write/post-tool observations qualify LF input/disk byte contract and actual exit-state monitor; cleanup verified; full native gate remains unchecked"
todo["pending_cache_permission"] = "reconfirmed asynchronously after current context recovery; no direct reply; native installation not performed"
todo["Claude_selection"] = "reconfirmed asynchronously after current context recovery; no direct reply; no Claude model prompt"
new_json(RUN / "native-continuation-todo.json", todo)

counts = {}
for path in sorted(PLAN.glob("phase-*.md")):
    items = re.findall(r"^\s*- \[([ xX])\]",path.read_text(encoding="utf8"),re.MULTILINE)
    counts[path.name] = {"done":sum(item.lower()=="x" for item in items),"total":len(items)}
assert [(value["done"],value["total"]) for value in counts.values()] == [(13,13),(9,9),(10,11),(12,12)]
links = 0
for path in [*sorted(PLAN.glob("*.md")), REPORT, JOURNAL]:
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)",path.read_text(encoding="utf8")):
        if reference.startswith(("http:","https:","#","mailto:","codex:")):
            continue
        assert (path.parent / reference.split("#",1)[0]).resolve().exists(), str(path)+" missing link "+reference
        links += 1
new_json(RUN / "plan-reconciliation.json", {"timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "status":"in-progress", "tasks":"44/45", "phases":counts,"full_native_gate":"unchecked", "source_revision":37,
    "source_lock_hash":verified["source_lock_hash"], "report":bind(REPORT), "todo":bind(RUN / "native-continuation-todo.json"),
    "docs":[{"path":path.relative_to(WORK).as_posix(),"before_sha256":before[path],"after_sha256":sha(path),"preimage":bind(preimages/path.name)} for path in paths],
    "source_final_check":bind(RUN / "final-source-check.json"),"native44_and52_oracles":"failed-preserved",
    "local_links_checked":links,"link_evidence_class":"structural only", "broad_tests_rerun":False,"index_reindex_performed":False,
    "qualified_process_union":len(audit["tracked"]),"owned_live":0,"current_goal_turn":"progress","reconciler":bind(Path(__file__))})
print(json.dumps({"status":"in-progress","tasks":"44/45","local_links":links,"qualified_union":len(audit["tracked"]),
    "owned_live":0,"source_revision":37,"native44_and52":"failed-preserved"}))
