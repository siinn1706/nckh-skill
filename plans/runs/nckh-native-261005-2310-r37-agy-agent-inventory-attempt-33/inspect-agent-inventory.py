"""Read current AGY agent metadata without a model prompt or configuration mutation."""

import importlib.util
import json
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
BASE=WORK/'plans/runs/nckh-native-261005-2255-r37-agy-read-tools-attempt-32'
PROJECT=WORK/'plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model'
spec=importlib.util.spec_from_file_location('owned_agent_inventory',BASE/'owned-cli-command.py')
owned=importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
owned.RUN=RUN
AGY=r'C:/Users/USER\AppData\Local\agy\bin\agy.exe'
assert not (PROJECT/'.agents/hooks.json').exists()
for name,args in (('agy-agents-help',['help','agents']),('agy-agent-inventory',['agents'])):
    outcome,stdout,stderr=owned.run_command(name,[AGY,'--log-file',str(RUN/(name+'.native.log')),*args],cwd=PROJECT,timeout=60)
    print(json.dumps({'command':name,'exit_code':outcome['exit_code'],'stdout':stdout.decode('utf8',errors='replace')[:7000],
        'model_prompts':0,'configuration_write_performed':False}),flush=True)
    assert outcome['exit_code']==0,'Agent inventory failed; preserve observations'
