"""Bounded native r38 advisory observation with entirely disposable host state."""
import ctypes
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import tomllib
from ctypes import wintypes
from pathlib import Path

sys.dont_write_bytecode = True
CONTROLLER_RUN = Path(__file__).resolve().parent
RUN = CONTROLLER_RUN / 'corrected-cli-02'
WORK = CONTROLLER_RUN.parents[2]
PROJECT = RUN / 'project'
HOME = PROJECT / 'native-home'
ROOT = WORK / 'nckh-kit'
OLD = WORK / 'plans/runs/nckh-native-261004-1707-attempt-01'
sys.path.insert(0, str(ROOT))
from core.build import build_host, verify_source_lock
from core.hook_config import payload_from_bundle
from core.paths import digest_record

read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def toml(value):
    if isinstance(value, bool): return 'true' if value else 'false'
    if isinstance(value, str): return json.dumps(value)
    if isinstance(value, (int, float)): return str(value)
    if isinstance(value, list): return '[' + ','.join(toml(v) for v in value) + ']'
    if isinstance(value, dict): return '{' + ','.join(json.dumps(k) + '=' + toml(v) for k,v in value.items()) + '}'
    raise ValueError('Unsupported config value')
def protected():
    paths = {ROOT / 'core/registry/source-lock/source-lock.json'}
    lock = read(ROOT / 'core/registry/source-lock/source-lock.json')
    paths.update(ROOT / p for p in lock['files'])
    for host in ('.codex', '.cursor', '.claude', '.agents', '.gemini'):
        base = Path(r'C:/Users/USER') / host
        for relative in ('skills', 'agents', 'config/skills', 'config/agents', 'antigravity-cli/skills'):
            area = base / relative
            if area.is_dir():
                for item in area.iterdir():
                    if item.name.startswith('nckh-'):
                        paths.update(item.rglob('*') if item.is_dir() else [item])
    for area in (WORK / '.agents/skills', WORK / '.codex/agents'):
        if area.is_dir(): paths.update(area.rglob('*'))
    paths.update(Path(r'C:/Users/USER/.codex') / n for n in ('config.toml','hooks.json','auth.json'))
    return {str(p): sha(p) for p in sorted(paths) if p.is_file()}

monitor = load('quick_native_monitor', WORK / 'plans/runs/nckh-native-261006-0125-r37-codex-patch-faults-attempt-40/owned-cli-command.py')
monitor.RUN = RUN
monitor.kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
monitor.kernel.GetExitCodeProcess.restype = wintypes.BOOL
q = load('quick_native_rpc', OLD / 'qualification-run.py')
q.RUN = RUN
BIN = read(WORK / 'plans/runs/nckh-native-261006-0125-r37-codex-patch-faults-attempt-40/commands/codex-version.json')['command'][0]
q.installed_commands = lambda: {'codex': [BIN]}

class SafeRPC(q.CodexRPC):
    def read_stdout(self):
        for line in self.process.stdout:
            message = json.loads(line)
            result = message.get('result', {})
            if isinstance(result, dict) and 'config' in result:
                cfg = result['config']
                message = {**message, 'result':{'config':{k:cfg.get(k) for k in ('model','model_reasoning_effort','model_provider')}, 'private_fields':'omitted-before-recording'}}
            self.messages.append((json.dumps(message)+'\n').encode())
            self.inbox.put(message)

def live_identity(row):
    if monitor.creation_ticks(row['pid']) != row['creation_filetime_ticks']: return False
    handle = monitor.kernel.OpenProcess(0x1000, False, row['pid'])
    if not handle: return False
    try:
        code = ctypes.c_ulong()
        if not monitor.kernel.GetExitCodeProcess(handle, ctypes.byref(code)): raise ctypes.WinError(ctypes.get_last_error())
        return code.value == 259
    finally: monitor.kernel.CloseHandle(handle)
def listing(name):
    client = SafeRPC(name, PROJECT, isolated=True)
    client.record['creation_filetime_ticks'] = monitor.creation_ticks(client.process.pid)
    try:
        response = client.request('initialize', {'clientInfo': {'name':'nckh-quick-r38','version':'r38'}, 'capabilities':{'experimentalApi':True}})
        assert 'error' not in response
        client.process.stdin.write(b'{"method":"initialized","params":{}}\n')
        client.process.stdin.flush()
        effective = client.request('config/read', {'includeLayers':False})
        save(RUN / (name + '.effective.json'), effective)
        cfg = effective.get('result',{}).get('config',{})
        assert cfg.get('model')=='gpt-5.6-luna' and cfg.get('model_reasoning_effort')=='medium'
        result = client.request('hooks/list', {'cwds':[str(PROJECT)]})
        save(RUN / (name + '.json'), result)
        rows = [h for entry in result.get('result',{}).get('data',[]) for h in entry.get('hooks',[])]
        selected = [r for r in rows if Path(r.get('sourcePath','')).resolve() == (PROJECT / '.codex/hooks.json').resolve()]
        assert len(selected) == 1 and len(rows) == 1, 'Unexpected hook discovery; stop before inference'
        return selected[0]
    finally: client.close()

def main():
    assert not PROJECT.exists(), 'Preserve prior project'
    check = subprocess.run(['powershell.exe','-NoProfile','-Command', "Get-CimInstance Win32_Process -Filter \"Name='codex.exe'\" | Where-Object { $_.CommandLine -and $_.CommandLine.Contains('" + str(PROJECT) + "') } | Select-Object ProcessId,CreationDate | ConvertTo-Json"],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    save(RUN/'process-preflight.json', {'exit_code':check.returncode,'matching_native_processes':json.loads(check.stdout) if check.stdout.strip() else [],'project':str(PROJECT)})
    assert check.returncode==0 and not check.stdout.strip(), 'Existing project native process; preserve and stop'
    PROJECT.mkdir()
    HOME.mkdir()
    before = protected()
    save(RUN / 'protected-before.json', before)
    lock = verify_source_lock(ROOT)
    assert str(lock['revision']) == '38'
    save(RUN / 'frozen-brief.json', {'source_revision':38,'source_lock_hash':digest_record(lock),
        'model':'gpt-5.6-luna','effort':'medium','maximum_model_turns':1,'maximum_tool_requests':1,
        'event':'PreToolUse','tool':'apply_patch','oracle':'Policy block retained, advisory wire non-denying exit0, exact benign marker created',
        'permission_route':'workspace-write/never; no dangerous flags','global_trust_write':False,
        'full_native_gate':'unchecked','host_home':str(HOME)})
    config = tomllib.loads(Path(r'C:/Users/USER/.codex/config.toml').read_text(encoding='utf8'))
    provider = config['model_provider']
    settings = config['model_providers'][provider]
    assert settings.get('requires_openai_auth') is False, 'Auth copy is outside this quick route'
    local = {'model':'gpt-5.6-luna','model_provider':provider,'model_reasoning_effort':'medium',
        'features':{'hooks':True,'memories':False},'history':{'persistence':'none'},
        'model_providers':{provider:settings},'sqlite_home':str(HOME/'sqlite'),'log_dir':str(HOME/'logs'),
        'projects':{str(PROJECT).casefold():{'trust_level':'trusted'}}}
    private_config = HOME / 'config.toml'
    private_config.write_text('\n'.join(k+'='+toml(v) for k,v in local.items())+'\n', encoding='utf8')
    os.environ['CODEX_HOME'] = str(HOME)
    staged = []
    config_expected = sha(private_config)
    hook_path = PROJECT / '.codex/hooks.json'
    try:
        payload = payload_from_bundle(CONTROLLER_RUN/'bundle/codex')
        runtime = PROJECT / 'runtime'
        for relative, expected in payload['members'].items():
            target = runtime / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(CONTROLLER_RUN/'bundle/codex'/relative,target)
            assert sha(target) == expected
            staged.append({'path':str(target),'sha256':expected})
        (PROJECT/'evidence').mkdir()
        save(PROJECT/'evidence/context.json', {'schema_version':1,'task_id':'quick-native-advisory-r38',
            'brief':{'mode':'plan-only'},'tool_operations':{'apply_patch':'write'},'allowed_operations':['write']})
        runner = runtime / payload['runner']
        command = subprocess.list2cmdline([sys.executable,'-I',str(CONTROLLER_RUN/'native-observer.py'),'--project',str(PROJECT),'--runner',str(runner)])
        save(hook_path, {'hooks':{'PreToolUse':[{'matcher':'apply_patch','hooks':[{'type':'command','timeout':10,'command':command}]}]}})
        hook_hash = sha(hook_path)
        version, out, err = monitor.run_command('codex-version',[BIN,'--version'],cwd=PROJECT)
        assert version['exit_code']==0
        save(RUN/'host-version.json', {'binary':BIN,'binary_sha256':sha(Path(BIN)),'version':out.decode().strip()})
        row = listing('native-discovery')
        local['hooks'] = {'state':{row['key']:{'enabled':True,'trusted_hash':row['currentHash']}}}
        private_config.write_text('\n'.join(k+'='+toml(v) for k,v in local.items())+'\n', encoding='utf8')
        config_expected = sha(private_config)
        trusted = listing('native-trusted-preflight')
        assert trusted['trustStatus']=='trusted' and trusted['enabled'] is True
        patch = '*** Begin Patch\n*** Add File: advisory-marker.txt\n+NCKH_R38_NATIVE_ADVISORY\n*** End Patch'
        prompt = 'Use the native apply_patch tool exactly once in this authorized disposable project. Do not inspect files, use shell/other tools, call agents, retry or work around denial. After the single tool attempt say QUICK_NATIVE_FINISHED and stop. Exact patch:\n'+patch
        save(RUN/'request.json', {'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'patch_sha256':hashlib.sha256(patch.encode()).hexdigest(),'marker_preimage':None})
        argv = [BIN,'--ask-for-approval','never','exec','--ephemeral','--skip-git-repo-check','--json','--sandbox','workspace-write','--model','gpt-5.6-luna','--cd',str(PROJECT),prompt]
        outcome, stdout, stderr = monitor.run_command('codex-native-advisory',argv,cwd=PROJECT,timeout=180)
        callback = read(PROJECT/'evidence/native-callback.json')
        receipts = list((PROJECT/'evidence/policy-receipts').glob('*.json'))
        frames = [json.loads(line) for line in stdout.decode().splitlines()]
        marker = PROJECT/'advisory-marker.txt'
        assert outcome['exit_code']==0 and callback['native_tool']=='apply_patch'
        assert callback['native_model']=='gpt-5.6-luna' and callback['native_command_sha256']==hashlib.sha256(patch.encode()).hexdigest()
        assert callback['runner_exit_code']==0 and 'deny' not in json.dumps(callback['runner_output']).casefold()
        assert len(receipts)==1 and read(receipts[0])['decision']=='block' and read(receipts[0])['hook_mode']=='advisory'
        assert marker.read_bytes()==b'NCKH_R38_NATIVE_ADVISORY\n'
        assert any(f.get('type')=='turn.completed' for f in frames)
        save(RUN/'observation.json', {'status':'scoped-native-pass','host':'codex-cli-exec','version':out.decode().strip(),
            'model_requested':'gpt-5.6-luna','effort_requested':'medium','model_callback':callback['native_model'],
            'effort_effective':'medium; native config/read before invocation','callback':callback,'receipt':read(receipts[0]),
            'marker_sha256':sha(marker),'native_exit_code':outcome['exit_code'],'frames':frames,
            'global_config_hash':before[str(Path(r'C:/Users/USER/.codex/config.toml'))],
            'cost':'unknown','backend_model_attestation':'unobserved','full_native_gate':'unchecked'})
    finally:
        removed=[]
        if hook_path.exists():
            assert sha(hook_path)==hook_hash
            removed.append({'path':str(hook_path),'sha256':sha(hook_path)})
            hook_path.unlink()
        for row in staged:
            target=Path(row['path'])
            assert sha(target)==row['sha256']
            target.unlink()
            removed.append(row)
        assert sha(private_config)==config_expected
        removed.append({'path':str(private_config),'sha256':config_expected,'private_values_retained':False})
        private_config.unlink()
        secret_values = [settings.get('experimental_bearer_token'), *settings.get('http_headers',{}).values()]
        for path in HOME.rglob('*'):
            if path.is_file() and any(isinstance(value,str) and len(value)>12 and value.encode() in path.read_bytes() for value in secret_values):
                removed.append({'path':str(path),'sha256':sha(path),'private_values_retained':False})
                path.unlink()
        after=protected()
        save(RUN/'protected-after.json',after)
        assert before==after, 'Protected source/install/global bytes changed'
        identities={}
        for receipt in (RUN/'commands').glob('*.process-tree.json'):
            command=read(receipt.with_name(receipt.name.replace('.process-tree.json','.json')))
            root_ticks=command['creation_filetime_ticks']
            for row in read(receipt)['processes']:
                if row['creation_filetime_ticks']>=root_ticks: identities[(row['pid'],row['creation_filetime_ticks'])]=row
        live=[row for row in identities.values() if live_identity(row)]
        save(RUN/'cleanup.json', {'status':'pass' if not live else 'owned-process-pending','removed_matching_files':removed,
            'protected_file_count':len(before),'protected_unchanged':before==after,'protected_tree_sha256':digest_record(before),
            'qualified_observed_process_count':len(identities),'owned_live':live,'global_trust_write':False,
            'native_home_config_absent':not private_config.exists(),'project_hook_absent':not hook_path.exists(),
            'receipts_and_failed_outputs_preserved':True})
        assert not live, 'Reconcile exact owned processes before completing'

if __name__=='__main__':
    main()
