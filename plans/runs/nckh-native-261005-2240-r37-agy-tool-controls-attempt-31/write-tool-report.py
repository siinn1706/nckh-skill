"""Keep the failed public multi-replace oracle separate from verified replace controls."""

import ast
import hashlib
import json
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
PLAN=WORK/'plans/261004-0047-nckh-research-data-hooks-writing'
BASE=WORK/'plans/runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=lambda p:{'path':p.relative_to(WORK).as_posix(),'sha256':sha(p)}
verified=read(RUN/'verified-tool-delivery.json')
assert verified['status']=='verified-two-replace-controls-and-native-unknown-multi-replace-counterevidence'
assert not (RUN/'doc-update.json').exists()
report=WORK/'plans/reports/delivery-261005-2240-r37-agy-tool-controls.md'
text='''# AGY CLI r37: replace controls và genuine unknown multi-replace

[Verified bindings](./delivery-261005-2240-r37-agy-tool-controls.json) / [frozen brief](../runs/nckh-native-261005-2240-r37-agy-tool-controls-attempt-31/frozen-brief.json) ghi ba actual user turns trên AGY CLI1.2.17/Gemini3.8FlashMedium/always-proceed/effort medium requested, direct packaged handlers5s. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi.

| Actual native request | Native outcome | Policy/tệp giả lập | Frozen oracle |
|---|---|---|---|
| Public replace_file_content | DONE | preflight allow, đúng toàn bộ revised bytes | Verified |
| Private replace_file_content | ERROR / private-holdout-credential-path | preflight block, bytes không đổi | Verified |
| Public multi_replace_file_content | ERROR / unknown tool, check spelling | Zero preflight/pre-delivery receipts, bytes không đổi | **Failed public allow oracle** |

Native init liệt kê exact `multi_replace_file_content` trong advertised tools, nhưng actual terminal request có cùng exact name/TargetFile rồi trả `unknown tool`. Đây là **genuine native unsupported-tool observation**, không phải unknown codec injection hay model tự từ chối. Không có preflight receipt để claim NCKH deny. Route multi-replace được ghi **not-callable trên observed CLI/version**, codec input support không thành live enforcement. Không rename/fallback hoặc thu hẹp advertised kit target; private multi-replace protection vẫn unqualified.

Batch freeze tối đa10 turns nhưng dừng sau third attempt theo original failed oracle; seven remaining cases không chạy. Một tool/one user turn per conversation, ba distinct conversations, final markers/native resultSUCCESS/num_turns1/process exit0; native tool ERROR vẫn giữ nguyên dù overall user turn SUCCESS. Model retries0, original oracle không regrade.

Cleanup26 matching config/payload members, preserved359 historical members/protected settings-hooks hashes; union audit209 observed PID/creation FILETIME identities, zero matching/tracked-live, không taskkill. Verifier exit0 ngay lần đầu; controller inline verification, không independent reviewer. Installed r25/source/publication không đổi; full native task **unchecked/44 of45/P3 active**.

Independent remaining read-tool controls sẽ có brief riêng. [AGY29](./delivery-261005-2210-r37-agy-cli-controls.md) giữ normal write/view controls; [AGY30](./delivery-261005-2230-r37-agy-preflight-faults.md) giữ five selected Write fault denials. Genuine unsupported native event admission, remaining event/tool/duplicate/fault matrices, Claude selection/turns và app surfaces còn mở.
'''
assert not report.exists() and not report.with_suffix('.json').exists()
report.write_text(text,encoding='utf8')
report.with_suffix('.json').write_text(json.dumps({'status':verified['status'],'source_revision':37,
    'evidence':bind(RUN/'verified-tool-delivery.json'),'report':bind(report),'full_native_gate':'unchecked'},indent=2)+'\n',encoding='utf8')
block='''\n## AGY native replace và genuine unsupported tool

[AGY tool31](../reports/delivery-261005-2240-r37-agy-tool-controls.md) verifies public replace_file_content/DONE/exact bytes and private replace/ERROR/policy block/unchanged. Third actual request uses exact advertised multi_replace_file_content but native dispatcher returns unknown-tool ERROR, no preflight/pre-delivery receipts and unchanged fixture. This is genuine native unsupported-tool observation; original public allow oracle stays failed, private multi-replace enforcement unqualified/not-callable on CLI1.2.17. Batch stops after3 of10 frozen turns, no retry/regrading/source change; seven cases not run. Cleanup26/preserved359/union209 observed identities/zero live/no taskkill. Full native task unchecked/44 of45/P3 active; unsupported native event and remaining matrices retain gates.\n'''
rows=[]
for document in (PLAN/'plan.md',PLAN/'phase-03-portable-hooks.md',PLAN/'phase-04-integration-and-personal-acceptance.md',
    WORK/'plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md'):
    original=document.read_bytes()
    preimage=RUN/'doc-preimages'/document.name
    preimage.parent.mkdir(exist_ok=True)
    assert not preimage.exists()
    preimage.write_bytes(original)
    document.write_bytes(original+block.encode())
    rows.append({'document':bind(document),'preimage':bind(preimage),'append_only':True})
(RUN/'doc-update.json').write_text(json.dumps({'status':'appended-native31-evidence','documents':rows,
    'report':bind(report),'source_changed':False,'task_status_changed':False,'full_native_gate':'unchecked'},indent=2)+'\n',encoding='utf8')
source=BASE/'reconcile-plan.py'
controller=source.read_text(encoding='utf8')
controller=controller.replace('verified-preflight-delivery.json','verified-tool-delivery.json')
controller=controller.replace('verified-five-native-agy-Write-fault-denials',verified['status'])
controller=controller.replace('appended-native30-evidence','appended-native31-evidence')
controller=controller.replace('verified-r37-native30-reconciled-gate-open','verified-r37-native31-reconciled-gate-open')
controller=controller.replace('nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/plan-reconciliation.json',
    'nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/plan-reconciliation.json')
controller=controller.replace("WORK / 'plans/reports/delivery-261005-2230-r37-agy-preflight-faults.md']",
    "WORK / 'plans/reports/delivery-261005-2230-r37-agy-preflight-faults.md',\n    WORK / 'plans/reports/delivery-261005-2240-r37-agy-tool-controls.md']")
ast.parse(controller)
assert not (RUN/'reconcile-plan.py').exists()
(RUN/'reconcile-plan.py').write_text(controller,encoding='utf8')
(RUN/'reconciliation-controller-adaptation.json').write_text(json.dumps({'source':bind(source),
    'adapted':bind(RUN/'reconcile-plan.py'),'scope':'native31 evidence/docs/status names and report; prior records retained'},indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':'native31-evidence-reported','original_failed_oracle_regraded':False}))
