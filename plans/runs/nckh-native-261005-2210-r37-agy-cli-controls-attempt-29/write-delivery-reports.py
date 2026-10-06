"""Publish local evidence reports and reconcile their plan pointers without closing the native gate."""

import hashlib
import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / 'plans/261004-0047-nckh-research-data-hooks-writing'
REPORTS = WORK / 'plans/reports'
PREVIOUS = WORK / 'plans/runs/nckh-native-261005-2155-r37-agy-cli-controls-attempt-28'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {'path': p.relative_to(WORK).as_posix(), 'sha256': sha(p)}
verified = read(RUN / 'verified-cli-delivery.json')
assert verified['status'] == 'verified-five-direct-agy-controls-with-previous-byte-failure-retained'
assert not (RUN / 'doc-update.json').exists()

failure_report = REPORTS / 'delivery-261005-2155-r37-agy-cli-byte-failure.md'
success_report = REPORTS / 'delivery-261005-2210-r37-agy-cli-controls.md'
failure_text = '''# AGY CLI r37: public Write có thêm LF, exact-byte oracle thất bại

[Verified bindings](./delivery-261005-2155-r37-agy-cli-byte-failure.json) giữ một actual `write_to_file`/DONE, preflight allow, selected TargetFile và final marker/native exit0 trên AGY CLI1.2.17/Gemini3.8FlashMedium/dangerous. Brief yêu cầu không newline; actual bytes bằng requested bytes cộng một LF. **Exact-byte oracle vẫn failed**, không regrade hoặc sửa raw evidence.

Batch28 freeze tối đa năm turns nhưng dừng sau turn đầu; bốn case còn lại không chạy. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi. Native tool frames không có CodeContent, nên chưa chứng minh newline được thêm bởi model hay host. [Batch29](./delivery-261005-2210-r37-agy-cli-controls.md) là brief riêng yêu cầu JSON decoded content kết thúc bằng đúng một LF, không thay grade của batch28.

Lượt tra models trong sandbox exit1 do log access và proxy bị chặn, zero model prompts; không phải kết luận authentication. Lượt elevated models inventory exit0, alias `gemini-3.8-flash-medium` hiện diện. CLI báo1.2.16 trước admission và1.2.17 khi prepare; controller không gọi update, nguyên nhân drift chưa verified.

Direct packaged handlers đều5s; no instrumented callback observer. Neutral policy receipts giữ advisory/preflight/pre-delivery/stop; advisory phase không phân biệt PreInvocation và PostInvocation. Post-delivery artifact QA còn pending. Native init ghi exact model alias và `always-proceed`; effort medium có trong command, backend/billing attestation chưa có. Không claim shared hook/tool ID hoặc full event matrix.

Cleanup26 matching config/payload members, preserved231 historical members và protected settings/hooks hashes. Union audit64 identities, zero matching/tracked-live, không taskkill. Source/install/publication không thay đổi; full native task **unchecked/44 of45/P3 active**.
'''
success_text = '''# AGY CLI r37: năm direct packaged controls verified

[Verified bindings](./delivery-261005-2210-r37-agy-cli-controls.json) / [frozen brief](../runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/frozen-brief.json) ghi năm distinct conversations, mỗi conversation một turn/một actual selected tool, trên **AGY CLI1.2.17**, `gemini-3.8-flash-medium`, effort medium requested, dangerous. Native init xác nhận exact model alias, selected workspace và `permission_mode=always-proceed`; backend/billing attestation chưa observed.

## Kết quả

| Case | Actual native tool/state | Policy preflight | Tệp giả lập |
|---|---|---|---|
| Public Write | write_to_file / DONE | allow | Đúng toàn bộ requested bytes, một LF cuối |
| Private Write | write_to_file / ERROR | block / private-holdout-credential-path | Không đổi |
| Public Read | view_file / DONE | allow | Không đổi |
| Private Read | view_file / ERROR | block / private-holdout-credential-path | Không đổi |
| Plan-only Write | write_to_file / ERROR | block / plan-only-mutation | Không đổi |

Mỗi case đủ native result/SUCCESS/num_turns1/final marker/process exit0. Terminal frames giữ actual TargetFile/AbsolutePath, conversation ID và step index. Verifier correlate policy session hash theo actual conversation và exact context file SHA256; native policy/tool shared-ID hay CodeContent attestation không có. Direct handlers gọi verified extracted r37 package, broad `.*` tool matcher và producer timeout5s, không observer injection hoặc model retry.

Neutral receipts có preflight/pre-delivery/advisory/stop; phase-only advisory receipts không xác định separately PreInvocation/PostInvocation và có thể deduplicate. PostInvocation native coverage chưa qualified. Public post-delivery artifact QA giữ pending. Các ca normal allow/deny không chứng minh failure-path enforcement hoặc default-all-tools coverage.

## Failure preservation

[Batch28](./delivery-261005-2155-r37-agy-cli-byte-failure.md) giữ failed no-newline byte oracle, một turn và dừng batch. Batch29 freeze JSON decoded content với một LF trước first submission; không sửa/regrade batch28 hoặc suy nguyên nhân LF từ tool frames thiếu CodeContent. CLI version drift1.2.16→1.2.17 observed; controller không gọi update. Trước batch28 freeze, exact plan-only reason được align theo source `plan-only-mutation`, có controller preimage và historical admission binding.

Hai verifier failures được giữ: collector final record không giữ running prompt_hash, và verifier ban đầu dùng canonical context digest thay raw file SHA256. Repairs bind immutable command argv và đúng `runner.load_context` byte-hash contract; không đổi oracle/native records hoặc resubmit model. Final verifier exit0. Review là controller inline raw-artifact verification, chưa independent reviewer.

## Cleanup và gates

Cleanup26 matching members, preserved243 historical project members và hai protected global settings/hooks hashes. Union audit109 exact PID/creation FILETIME identities: zero matching/tracked-live, không taskkill. CLI tự quản listener ports; controller không tạo service/port riêng. R37 source, installed r25 và previous receipts không đổi.

[Owner CLI route](../runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/cli-route-user-decision.json) tiếp tục AGY CLI/Gemini và Cursor CLI/Grok dangerous. [Inventory26](./delivery-261005-2120-r37-agy-window-inventory.md) là historical IDE identity gap; yêu cầu bring-to-front đã được trả lời bằng lựa chọn CLI, controller không chờ thao tác phục hồi IDE. IDE vẫn unverified.

Plan **44/45/P3 active/full native task unchecked**. [Cursor Write faults27](./delivery-261005-2125-r37-cursor-write-faults.md) giữ riêng same-source Write fault evidence. AGY failure/event/tool/duplicate matrices, Cursor plugin prompt/stop duplicates, genuine unsupported native observations, Claude model/effort/turns và app surfaces còn cần evidence. Exact r29 VI/EN owner acceptance và scientific/stable/release/publication gates giữ riêng.
'''
for document, content, binding in ((failure_report, failure_text, {'status': 'verified-recorded-failed-exact-byte-oracle',
    'source_revision': 37, 'full_native_gate': 'unchecked', 'evidence': bind(RUN / 'verified-cli-delivery.json'),
    'failed_summary': bind(PREVIOUS / 'native-cli-summary.json'), 'original_grade': 'failed-frozen-oracle-retained'}),
    (success_report, success_text, {'status': 'verified-five-direct-agy-controls-with-previous-byte-failure-retained',
    'source_revision': 37, 'full_native_gate': 'unchecked', 'evidence': bind(RUN / 'verified-cli-delivery.json')})):
    assert not document.exists() and not document.with_suffix('.json').exists()
    document.write_text(content, encoding='utf8')
    document.with_suffix('.json').write_text(json.dumps({**binding, 'report': bind(document)}, indent=2) + '\n', encoding='utf8')

index = '''\n## Current CLI route and new native evidence

[Owner decision](../runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/cli-route-user-decision.json) selects AGY CLI/Gemini3.8FlashMedium and Cursor CLI/Grok4.7xhigh dangerous. IDE recovery request has been answered by that route selection; IDE qualification remains unverified. [Inventory26](../reports/delivery-261005-2120-r37-agy-window-inventory.md), [Cursor Write faults27](../reports/delivery-261005-2125-r37-cursor-write-faults.md), [AGY byte failure28](../reports/delivery-261005-2155-r37-agy-cli-byte-failure.md) and [AGY direct controls29](../reports/delivery-261005-2210-r37-agy-cli-controls.md) retain distinct evidence scopes. AGY29 verifies exact public Write, public Read, private Read/Write prevention and plan-only Write prevention at producer5s on CLI1.2.17; previous no-newline byte oracle remains failed. Cleanup26/preserved243/union109 identities/zero owned processes. R37/owner samples unchanged; full native task remains unchecked/44 of45.\n'''
phase = '''\n## Native CLI route, Write faults and AGY controls

[Inventory26](../reports/delivery-261005-2120-r37-agy-window-inventory.md) retains zero AGY-owned windows/no app input. Owner answered recovery request by selecting [CLI dangerous route](../runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/cli-route-user-decision.json); no IDE recovery action remains requested, but IDE coverage is unverified. [Cursor Write faults27](../reports/delivery-261005-2125-r37-cursor-write-faults.md) adds five genuine selected Write callbacks/five matching native failures and unchanged fixtures. Scope is test-only `^Write$`; faults are controller injection after supported callback, not genuine unsupported native admission. Cleanup26/preserved803/union53 exact identities/zero processes.\n\n[AGY28](../reports/delivery-261005-2155-r37-agy-cli-byte-failure.md) retains one public Write/DONE/allow and failed no-newline byte oracle; batch stops after one turn. [AGY29](../reports/delivery-261005-2210-r37-agy-cli-controls.md) freezes separate explicit one-LF content and verifies five direct5s normal controls: exact public Write/public Read allow, private Read/Write ERROR+policy block/unchanged, plan-only Write ERROR+plan-only-mutation/unchanged. Native init binds exact granted model/always-proceed/workspace; native terminal paths/conversations and raw context SHA256 correlate receipts. Raw CodeContent/shared hook-tool ID/backend attestation are absent; phase-only advisory receipts do not identify PreInvocation/PostInvocation separately. No failure-path coverage inferred.\n\nR37/281 pins/hash unchanged; previous byte failure/verifier binding failures retained with repairs and no resubmission/regrading. AGY29 cleanup26/preserved243/protected settings-hooks unchanged, union audit109 FILETIME identities/zero matching or tracked-live/no taskkill. Native event/tool/fault/duplicate matrices, Claude selection/turns and app surfaces remain open. Full task unchecked/44 of45/P3 active.\n'''
integration = '''\n## Additional native evidence — CLI route and AGY direct controls

[Cursor27](../reports/delivery-261005-2125-r37-cursor-write-faults.md) adds five selected Write fault denials; [AGY28](../reports/delivery-261005-2155-r37-agy-cli-byte-failure.md) preserves one failed exact no-newline byte oracle. [AGY29](../reports/delivery-261005-2210-r37-agy-cli-controls.md) verifies five direct producer5s normal file controls on CLI1.2.17/Gemini3.8FlashMedium/dangerous, exact explicit-LF public Write and private/plan-only prevention. Independent conversations, final markers/exit0, cleanup26/preserved243/union109 identities/zero owned processes. Owner selected CLI after inventory26; IDE qualification remains unverified. Source/local checkpoint/exact r29 owner VI/EN acceptance remain unchanged. P4 retains12/12; plan44/45/P3 native task unchecked.\n'''
journal = '''\n## Cursor Write failures and actual AGY CLI delivery

Owner selected AGY CLI/Gemini3.8FlashMedium and Cursor CLI/Grok4.7xhigh dangerous, then supplied the same AGY executable app mention. [Native26](../reports/delivery-261005-2120-r37-agy-window-inventory.md) IDE identity gap remains historical; no more bring-to-front recovery requested. [Native27](../reports/delivery-261005-2125-r37-cursor-write-faults.md) records five actual selected Write fault denials/unchanged fixtures. [AGY28](../reports/delivery-261005-2155-r37-agy-cli-byte-failure.md) stops after public Write produced one extra LF; original exact-byte oracle remains failed. [AGY29](../reports/delivery-261005-2210-r37-agy-cli-controls.md) is a separate explicit one-LF brief with five verified direct5s file controls. Native model/permission/workspace observed; actual paths/conversation hashes/context byte hashes bind normal allow/deny. CLI1.2.16→1.2.17 drift observed without controller update; cause unverified. Verifier prompt-field/context-digest errors retained then repaired without changing model evidence. R37 unchanged; cleanup26/preserved243/final union109 identities/zero live/no taskkill. Full matrix/Claude/app gates open; plan44/45/P3 active.\n'''
documents = [(PLAN / 'plan.md', index), (PLAN / 'phase-03-portable-hooks.md', phase),
    (PLAN / 'phase-04-integration-and-personal-acceptance.md', integration),
    (WORK / 'plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md', journal)]
records = []
for document, content in documents:
    original = document.read_bytes()
    preimage = RUN / 'doc-preimages' / document.name
    preimage.parent.mkdir(exist_ok=True)
    assert not preimage.exists()
    preimage.write_bytes(original)
    document.write_bytes(original + content.encode())
    records.append({'document': bind(document), 'preimage': bind(preimage), 'append_only': True})
(RUN / 'doc-update.json').write_text(json.dumps({'status': 'appended-native26-29-evidence',
    'documents': records, 'reports': [bind(failure_report), bind(success_report)], 'source_changed': False,
    'task_status_changed': False, 'full_native_gate': 'unchecked'}, indent=2) + '\n', encoding='utf8')
print(json.dumps({'status': 'reports-and-docs-updated', 'native_task': 'unchecked'}))
