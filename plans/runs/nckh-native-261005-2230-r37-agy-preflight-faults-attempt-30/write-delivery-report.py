"""Retain measured AGY failure semantics and append the scoped evidence checkpoint."""

import ast
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / 'plans/261004-0047-nckh-research-data-hooks-writing'
BASE = WORK / 'plans/runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {'path': p.relative_to(WORK).as_posix(), 'sha256': sha(p)}
evidence = read(RUN / 'verified-preflight-delivery.json')
assert evidence['status'] == 'verified-five-native-agy-Write-fault-denials'
assert not (RUN / 'doc-update.json').exists()
report = WORK / 'plans/reports/delivery-261005-2230-r37-agy-preflight-faults.md'
text = '''# AGY CLI r37: năm actual Write fault denials

[Verified bindings](./delivery-261005-2230-r37-agy-preflight-faults.json) / [frozen brief](../runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/frozen-brief.json) ghi năm distinct conversations trên AGY CLI1.2.17/Gemini3.8FlashMedium/always-proceed, effort medium requested. Mỗi conversation có một user turn, một genuine PreToolUse callback và một actual `write_to_file`/ERROR; actual session hash, step index2 và TargetFile correlate callback với native terminal frame. Native tool-use ID không reported. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi.

## Native outcomes

| Injection sau genuine PreToolUse/Write callback | Actual native error | Tệp giả lập |
|---|---|---|
| Malformed runner input | denied by pre-tool hook / hook-input-or-context-invalid | Không đổi |
| Malformed hook output | failed to unmarshal / invalid-native-hook-output | Không đổi |
| Sleeper8s | JSON hook command failure / exit status1 | Không đổi |
| Observer crash exit17 | JSON hook command failure / exit status17 | Không đổi |
| Unknown selected codec event | JSON hook command failure / exit status3 | Không đổi |

Outer handlers và inner runner đều configured5s; native timeout-injection tool duration **6.0395856s**, observer duration **8.140703s**. Observer sau đó trả ask và policy allow, nhưng native vẫn ERROR/unchanged; late policy không được dùng làm native permission. Host error chỉ báo exit status1, không giữ dedicated timeout reason. Đây là test instrumentation, không phải direct packaged handler; [normal direct controls29](./delivery-261005-2210-r37-agy-cli-controls.md) giữ riêng producer5s allow/private/plan-only evidence.

Malformed-input degraded receipt thiếu context_hash được giữ nguyên, correlate bằng genuine callback/session/step/path và native error. Unknown codec event là controller injection sau supported callback; không chứng minh genuine native unsupported-event admission. Không model retry/regrading/source patch. Native init/result quan sát model alias/permission/workspace; backend/billing attestation chưa có.

## Callback coverage và cleanup

Actual observer counts tổng cộng: PreInvocation10, PreToolUse5, PostInvocation10, Stop5, PostToolUse0. Mỗi denied tool không phát successful PostToolUse callback. PreInvocation/PostInvocation mỗi event hai callbacks mỗi conversation là lifecycle presence, không được coi là controlled project/plugin duplicate experiment hoặc failure matrix cho các event đó.

Đủ năm final markers/resultSUCCESS/num_turns1/process exit0. Exact initial/after fixture hashes bằng nhau. Child reconciliation giữa turns đối chiếu Win32 PID/creation FILETIME, không dừng process. [Cleanup](../runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/cleanup.json) gỡ26 matching config/payload members, giữ285 historical members và protected settings/hooks hashes. [Union final audit](../runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/process-final-audit.json)179 observed identities, zero matching/tracked-live, không taskkill.

Verifier exit0 ngay lần đầu; controller inline raw-artifact verification, không independent reviewer. CLI tự quản listener ports, không controller service/port riêng. Installed r25/publication/source/owner exact r29 VI/EN samples không đổi.

Plan **44/45/P3 active/full native task unchecked**. Remaining: other event/tool/fault/duplicate matrices, genuine unsupported native observations, Claude model/effort/native turns và IDE/app surfaces. Owner tiếp tục CLI dangerous route; IDE recovery không chờ bring-to-front, qualification vẫn unverified.
'''
assert not report.exists() and not report.with_suffix('.json').exists()
report.write_text(text, encoding='utf8')
report.with_suffix('.json').write_text(json.dumps({'status': evidence['status'], 'source_revision':37,
    'evidence':bind(RUN / 'verified-preflight-delivery.json'), 'report':bind(report), 'full_native_gate':'unchecked'}, indent=2)+'\n',encoding='utf8')
block = '''\n## Additional AGY native failure evidence

[AGY Write faults30](../reports/delivery-261005-2230-r37-agy-preflight-faults.md) verifies five genuine PreToolUse/Write callbacks with corresponding native ERRORs, exact unchanged fixtures and final marker/process exit0. Faults: malformed input/output, sleeper8s, crash17, unknown injected codec event. Outer/inner configured5s; timeout case native duration6.0395856s, observer8.140703s and late ask/allow retain separate status. Match actual conversation hash/step index2/TargetFile; no reported tool-use ID. Lifecycle counts PreInvocation10/PostInvocation10/Stop5 demonstrate presence, not controlled duplicates or their own failure matrices. Cleanup26/preserved285/protected settings-hooks unchanged, union179 observed identities/zero live/no taskkill. Source r37 unchanged, full native task unchecked/44 of45/P3 active.\n'''
documents = [PLAN/'plan.md', PLAN/'phase-03-portable-hooks.md', PLAN/'phase-04-integration-and-personal-acceptance.md',
    WORK/'plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md']
rows = []
for document in documents:
    original = document.read_bytes()
    preimage = RUN/'doc-preimages'/document.name
    preimage.parent.mkdir(exist_ok=True)
    assert not preimage.exists()
    preimage.write_bytes(original)
    document.write_bytes(original+block.encode())
    rows.append({'document':bind(document),'preimage':bind(preimage),'append_only':True})
(RUN/'doc-update.json').write_text(json.dumps({'status':'appended-native30-evidence','documents':rows,
    'report':bind(report),'source_changed':False,'task_status_changed':False,'full_native_gate':'unchecked'},indent=2)+'\n',encoding='utf8')
source = BASE/'reconcile-plan.py'
controller = source.read_text(encoding='utf8')
controller = controller.replace('verified-cli-delivery.json','verified-preflight-delivery.json')
controller = controller.replace('verified-five-direct-agy-controls-with-previous-byte-failure-retained','verified-five-native-agy-Write-fault-denials')
controller = controller.replace('appended-native26-29-evidence','appended-native30-evidence')
controller = controller.replace('verified-r37-native26-29-reconciled-gate-open','verified-r37-native30-reconciled-gate-open')
controller = controller.replace('nckh-native-261005-2055-r37-cursor-selected-write-attempt-25/plan-reconciliation.json',
    'nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/plan-reconciliation.json')
controller = controller.replace("WORK / 'plans/reports/delivery-261005-2210-r37-agy-cli-controls.md']",
    "WORK / 'plans/reports/delivery-261005-2210-r37-agy-cli-controls.md',\n    WORK / 'plans/reports/delivery-261005-2230-r37-agy-preflight-faults.md']")
ast.parse(controller)
assert not (RUN/'reconcile-plan.py').exists()
(RUN/'reconcile-plan.py').write_text(controller,encoding='utf8')
(RUN/'reconciliation-controller-adaptation.json').write_text(json.dumps({'source':bind(source),
    'adapted':bind(RUN/'reconcile-plan.py'),'scope':'native30 receipt/doc/status names and additional report; previous checkpoint retained'},indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':'native30-report-and-docs-updated','full_native_gate':'unchecked'}))
