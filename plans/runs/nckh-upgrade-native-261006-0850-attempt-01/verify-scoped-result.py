"""Bind the completed native observation without regrading its failed mutation oracle."""
import ctypes
import hashlib
import importlib.util
import json
import sys
from ctypes import wintypes
from pathlib import Path

sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parent
ACTUAL = RUN / 'corrected-cli-02'
PROJECT = ACTUAL / 'project'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p): return {'path':str(p), 'sha256':sha(p)}
def save(p, value): p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

monitor_path = RUN.parents[2] / 'plans/runs/nckh-native-261006-0125-r37-codex-patch-faults-attempt-40/owned-cli-command.py'
spec = importlib.util.spec_from_file_location('scoped_final_monitor',monitor_path)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)
monitor.kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
monitor.kernel.GetExitCodeProcess.restype = wintypes.BOOL
def live(row):
    if monitor.creation_ticks(row['pid']) != row['creation_filetime_ticks']: return False
    handle=monitor.kernel.OpenProcess(0x1000,False,row['pid'])
    if not handle: return False
    try:
        code=wintypes.DWORD()
        assert monitor.kernel.GetExitCodeProcess(handle,ctypes.byref(code))
        return code.value==259
    finally: monitor.kernel.CloseHandle(handle)

callback_path = PROJECT/'evidence/native-callback.json'
callback=read(callback_path)
receipt_path=next((PROJECT/'evidence/policy-receipts').glob('*.json'))
receipt=read(receipt_path)
command=read(ACTUAL/'commands/codex-native-advisory.json')
stderr_path=ACTUAL/'commands/codex-native-advisory.stderr.txt'
stdout_path=ACTUAL/'commands/codex-native-advisory.stdout.txt'
stderr=stderr_path.read_text(encoding='utf8')
frames=[json.loads(line) for line in stdout_path.read_text(encoding='utf8').splitlines()]
assert callback['native_event']=='PreToolUse' and callback['native_tool']=='apply_patch'
assert callback['native_model']=='gpt-5.6-luna'
assert callback['native_command_sha256']==read(ACTUAL/'request.json')['patch_sha256']
assert callback['runner_exit_code']==0 and callback['runner_output']=={}
assert receipt['decision']=='block' and receipt['hook_mode']=='advisory' and receipt['reason_codes']==['plan-only-mutation']
assert command['exit_code']==0 and any(f.get('type')=='turn.completed' for f in frames)
assert not (PROJECT/'advisory-marker.txt').exists()
assert 'patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings' in stderr
assert read(ACTUAL/'protected-before.json')==read(ACTUAL/'protected-after.json')
assert read(ACTUAL/'cleanup.json')['protected_unchanged']
protected_before=read(ACTUAL/'protected-before.json')
current_protected={p:sha(Path(p)) for p in protected_before}
assert protected_before==current_protected
save(RUN/'final-protected-check.json', {'status':'pass','files':len(current_protected),
    'hashes_equal_to_preflight':True,'protected_members':current_protected})
identities={}
for root in (RUN, ACTUAL):
    for p in (root/'commands').glob('*.process-tree.json'):
        control=read(p.with_name(p.name.replace('.process-tree.json','.json')))
        for row in read(p)['processes']:
            if row['creation_filetime_ticks']>=control['creation_filetime_ticks']:
                identities[(row['pid'],row['creation_filetime_ticks'])]=row
    for p in (root/'commands').glob('native-*.json'):
        row=read(p)
        if 'creation_filetime_ticks' in row:
            assert row['process_exited'] and row['exit_code']==0
            identities[(row['pid'],row['creation_filetime_ticks'])]=row
active=[r for r in identities.values() if live(r)]
assert not active
save(RUN/'final-process-audit.json', {'status':'pass','qualified_known_identities':len(identities),'owned_live':active,
    'scope':'exact observed PID and creation-time identities; actual GetExitCodeProcess state','system_wide_inventory':'not-claimed'})
effective=read(ACTUAL/'native-trusted-preflight.effective.json')['result']['config']
assert effective['model']=='gpt-5.6-luna' and effective['model_reasoning_effort']=='medium'
summary={
    'status':'DONE_WITH_CONCERNS','surface':'codex-cli-exec','host_version':read(ACTUAL/'host-version.json')['version'],
    'source_revision':38,'source_lock_hash':read(ACTUAL/'frozen-brief.json')['source_lock_hash'],
    'native_model_turns':1,'native_tool_callbacks':1,'model_requested':'gpt-5.6-luna','model_effective_callback':callback['native_model'],
    'reasoning_effort_native_config':'medium','backend_model_attestation':'unobserved','cost':'unknown',
    'advisory_callback':'observed-non-denial','policy_verdict':receipt['decision'],'policy_reason_codes':receipt['reason_codes'],
    'runner_exit_code':0,'wire_output':{},'native_cli_exit_code':0,'native_turn_completed':True,
    'benign_mutation_oracle':'blocked-by-native-read-only-sandbox','marker_absent':True,
    'overall_quick_acceptance':'blocked-for-tool-side-effect; callback-advisory-observation-supported',
    'full_native_qualification':'unchanged-unchecked','historical_44_45_gate':'unchanged',
    'protected_files_unchanged':791,'qualified_known_process_identities':len(identities),'owned_live':0,
    'cleanup':{'project_hooks_removed':True,'staged_runtime_removed':True,'private_host_configs_removed':True,'raw_evidence_preserved':True},
    'earlier_failures':['controller encoding setup error before native launch','sandbox CIM query failure before native launch','CLI option parser exit2 before inference'],
    'bindings':{'callback':bind(callback_path),'policy_receipt':bind(receipt_path),'command_receipt':bind(ACTUAL/'commands/codex-native-advisory.json'),
        'stdout':bind(stdout_path),'stderr':bind(stderr_path),'trusted_preflight':bind(ACTUAL/'native-trusted-preflight.json'),
        'effective_config':bind(ACTUAL/'native-trusted-preflight.effective.json'),'cleanup':bind(ACTUAL/'cleanup.json'),
        'protected_before':bind(ACTUAL/'protected-before.json'),'protected_after':bind(ACTUAL/'protected-after.json'),
        'observer':bind(RUN/'native-observer.py'),'controller':bind(RUN/'quick-native.py'),'verifier':bind(Path(__file__)),
        'final_process_audit':bind(RUN/'final-process-audit.json'),'final_protected_check':bind(RUN/'final-protected-check.json')}
}
save(RUN/'verification-summary.json',summary)
print(json.dumps({k:summary[k] for k in ('status','native_model_turns','native_tool_callbacks','advisory_callback','benign_mutation_oracle','protected_files_unchanged','owned_live')},indent=2))
