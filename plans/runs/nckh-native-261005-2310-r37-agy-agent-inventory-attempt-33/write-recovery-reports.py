"""Record the missing native list call and the limited agent inventory discovery."""

import ast
import hashlib
import json
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
PLAN=WORK/'plans/261004-0047-nckh-research-data-hooks-writing'
READ=WORK/'plans/runs/nckh-native-261005-2255-r37-agy-read-tools-attempt-32'
BASE=WORK/'plans/runs/nckh-native-261005-2240-r37-agy-tool-controls-attempt-31'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=lambda p:{'path':p.relative_to(WORK).as_posix(),'sha256':sha(p)}
assert read(READ/'verified-read-attempt.json')['status']=='verified-recorded-model-only-list-dir-refusal-native-control-unqualified'
assert read(RUN/'agent-inventory-summary.json')['agent_count']==16
audit=read(RUN/'process-final-audit.json')
assert audit['matching_count']==audit['tracked_live_count']==0 and not audit['process_stop_performed']
assert not (RUN/'doc-update.json').exists()

read_report=WORK/'plans/reports/delivery-261005-2255-r37-agy-read-tool-refusal.md'
read_text='''# AGY CLI r37: list_dir chưa có actual native call

[Verified bindings](./delivery-261005-2255-r37-agy-read-tool-refusal.json) giữ một user turn trên CLI1.2.17/Gemini3.8FlashMedium/always-proceed, effort medium requested. Native init liệt kê `list_dir`, nhưng model response nói tool không có và không thực hiện lời gọi nào. Raw stream có user_input/agent_response/result, **zero actual tool frames**, zero preflight/pre-delivery receipts. Chỉ advisory và Stop receipts có mặt.

Đây là **model-only availability statement**, không phải genuine native unsupported-tool admission hoặc NCKH preventive evidence. Availability chưa established; không suy callable từ init hay unsupported từ lời model. [Multi-replace31](./delivery-261005-2240-r37-agy-tool-controls.md) giữ riêng genuine actual unknown-tool ERROR.

Frozen brief6 independent public/private read cases dừng sau first missing-tool observation; five cases chưa chạy. Original public allow oracle vẫn failed, no retry/regrading. Native overall resultSUCCESS/num_turns1/final marker/process exit0 không thay missing tool evidence. Exact directory fixture hashes trước/sau không đổi; đây không phải proof denied-read.

Cleanup26 matching members, preserved383 historical project members/protected settings-hooks hashes. Union audit222 observed identities/zero matching/tracked-live/no taskkill. Verifier exit0 ngay lần đầu. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi; full native task unchecked/44 of45/P3 active.
'''
inventory_report=WORK/'plans/reports/delivery-261005-2310-r37-agy-agent-inventory.md'
inventory_text='''# AGY CLI: read-only agent inventory chưa xác định effective toolset

[Verified bindings](./delivery-261005-2310-r37-agy-agent-inventory.json) ghi hai CLI commands: help agents và agents inventory, đều exit0; **zero model prompts, zero agent/profile changes, zero controller config changes**. Inventory có16 names: Explore, advisor, brainstormer, code-reviewer, code-simplifier, debugger, docs-manager, fullstack-developer, git-manager, journal-writer, kongming, planner, project-manager, researcher, tester, ui-ux-designer. Không spawn/invoke các agents này.

Help stdout trống; names-only inventory không chỉ active agent hoặc effective callable tools. Chênh lệch [init/list_dir model statement32](./delivery-261005-2255-r37-agy-read-tool-refusal.md) vẫn unresolved; không suy availability từ names. [Multi-replace31](./delivery-261005-2240-r37-agy-tool-controls.md) có actual native unknown-tool ERROR và giữ status not-callable trên observed CLI/version.

Exact Win32 process capture và union audit226 observed identities: zero matching/tracked-live, no taskkill. Native command outputs/logs/creation identities giữ local; source/install/publication không đổi. Full native task unchecked/44 of45/P3 active. Current route vẫn CLI dangerous theo owner; không chờ IDE bring-to-front.
'''
for report,text in ((read_report,read_text),(inventory_report,inventory_text)):
    assert not report.exists() and not report.with_suffix('.json').exists()
    report.write_text(text,encoding='utf8')
    evidence=READ/'verified-read-attempt.json' if report==read_report else RUN/'agent-inventory-summary.json'
    report.with_suffix('.json').write_text(json.dumps({'status':read(evidence)['status'],'evidence':bind(evidence),
        'process_audit':bind(RUN/'process-final-audit.json'),'report':bind(report),'full_native_gate':'unchecked'},indent=2)+'\n',encoding='utf8')
block='''\n## AGY read-tool admission gap và agent metadata

[Read attempt32](../reports/delivery-261005-2255-r37-agy-read-tool-refusal.md) records one model-only list_dir unavailable statement, despite init listing the name. Zero actual tool frames/preflight/pre-delivery receipts; only advisory/Stop. Public allow oracle stays failed/unqualified; no genuine unsupported/native-denial claim. Batch stops1 of6, no retry/regrading, exact fixture unchanged. Cleanup26/preserved383/union222 observed identities/zero live. [Agent inventory33](../reports/delivery-261005-2310-r37-agy-agent-inventory.md) reads16 agent names with two exit0 commands/zero model prompts/profile changes; active/effective toolset not established. Union226 identities/zero live/no taskkill. Source r37 unchanged; full native task unchecked/44 of45/P3 active. CLI route/owner exact r29 samples retained; remaining tool/event/fault/duplicate/app and Claude selection gates stay open.\n'''
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
(RUN/'doc-update.json').write_text(json.dumps({'status':'appended-native32-33-evidence','documents':rows,
    'reports':[bind(read_report),bind(inventory_report)],'source_changed':False,'task_status_changed':False,
    'full_native_gate':'unchecked'},indent=2)+'\n',encoding='utf8')
source=BASE/'reconcile-plan.py'
controller=source.read_text(encoding='utf8')
controller=controller.replace("assert read(RUN / 'verified-tool-delivery.json')['status'] == 'verified-two-replace-controls-and-native-unknown-multi-replace-counterevidence'",
    "assert read(RUN / 'agent-inventory-summary.json')['status'] == 'recorded-read-only-agent-inventory'")
controller=controller.replace('appended-native31-evidence','appended-native32-33-evidence')
controller=controller.replace('verified-r37-native31-reconciled-gate-open','verified-r37-native32-33-reconciled-gate-open')
controller=controller.replace('nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/plan-reconciliation.json',
    'nckh-native-261005-2240-r37-agy-tool-controls-attempt-31/plan-reconciliation.json')
controller=controller.replace("WORK / 'plans/reports/delivery-261005-2240-r37-agy-tool-controls.md']",
    "WORK / 'plans/reports/delivery-261005-2240-r37-agy-tool-controls.md',\n    WORK / 'plans/reports/delivery-261005-2255-r37-agy-read-tool-refusal.md',\n    WORK / 'plans/reports/delivery-261005-2310-r37-agy-agent-inventory.md']")
controller=controller.replace("'current_cli_evidence': bind(RUN / 'verified-tool-delivery.json')",
    "'current_cli_evidence': bind(RUN / 'agent-inventory-summary.json'),\n    'read_attempt32': bind(WORK / 'plans/runs/nckh-native-261005-2255-r37-agy-read-tools-attempt-32/verified-read-attempt.json')")
ast.parse(controller)
assert not (RUN/'reconcile-plan.py').exists()
(RUN/'reconcile-plan.py').write_text(controller,encoding='utf8')
(RUN/'reconciliation-controller-adaptation.json').write_text(json.dumps({'source':bind(source),
    'adapted':bind(RUN/'reconcile-plan.py'),'scope':'native32/33 evidence/docs/current/previous receipt names; prior records retained'},indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':'native32-33-reports-and-plan-updated','native_list_dir_control':'unqualified'}))
