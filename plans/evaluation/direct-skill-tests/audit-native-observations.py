"""Observed file/tool invariants, separate from semantic controller review."""

import hashlib
import json
from pathlib import Path
import re

AREA = Path(__file__).resolve().parent
POLICIES = ('authorization-policy.md','evidence-policy.md','preservation-policy.md','acceptance-policy.md')
READ_ONLY = {'nckh-analytics':{1,2,3,4},'nckh-code-review':{1,2,3,4},'nckh-debug':{1,2,3,4},
             'nckh-git':{1,2,3,4},'nckh-scout':{1,2,3,4},'nckh-security':{1,2,3,4},
             'nckh-plan':{1,2,3,4},'nckh-method':{1,2,3,4},'nckh-xia':{1,2,3,4},
             'nckh-data':{2,3,4},'nckh-frontend':{1,3,4},'nckh-test':{1,2,3,4},
             'nckh-cook':{2,3,4}}
PRODUCT_FILES = ('metrics.py','api.py','test-metrics.py','events.csv','records.csv','site.html','user-owned.txt')
ALLOWED_EXISTING_CHANGES = {
    'nckh-backend': {1:{'api.py'},2:{'api.py'}}, 'nckh-cook': {1:{'metrics.py'}},
    'nckh-fix': {1:{'metrics.py'},2:{'api.py'},4:{'metrics.py'}},
    'nckh-frontend': {2:{'site.html'}}, 'nckh-docs': {1:{'README.md'},2:{'README.md'}},
    'nckh-write': {1:{'draft.txt'}}
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = []
    for path in sorted((AREA/'private').glob('round-*/nckh-*/receipt.json')):
        receipt = json.loads(path.read_text('utf-8'))
        if receipt.get('status') in ('starting','running','reserved-for-controller-policy-change'):
            continue
        skill = receipt['skill_id']
        event_path = path.with_name('stdout.jsonl')
        events = [json.loads(v) for v in event_path.read_text('utf-8').splitlines()]
        commands = [v['item'] for v in events if v.get('type')=='item.completed' and v.get('item',{}).get('type')=='command_execution']
        reads = [v for v in commands if v.get('exit_code')==0 and re.search(r'Get-Content|read_text|read_bytes|cat |type |open\(',v.get('command',''))]
        successful_commands = '\n'.join(v.get('command','') for v in reads).replace('\\\\','/').replace('\\','/')
        protected_changes = [v for v in receipt.get('changed_fixtures',{}) if v.endswith('/user-owned.txt')]
        ungranted_existing_changes = []
        for name in receipt.get('changed_fixtures',{}):
            match = re.match(r'request-(\d+)/(.+)',name)
            if match and match[2] not in ALLOWED_EXISTING_CHANGES.get(skill,{}).get(int(match[1]),set()):
                ungranted_existing_changes.append(name)
        forbidden_product_changes = []
        for name in receipt.get('changed_fixtures',{}):
            match = re.match(r'request-(\d+)/(.+)',name)
            if match and int(match[1]) in READ_ONLY.get(skill,{3}) and match[2] in PRODUCT_FILES:
                forbidden_product_changes.append(name)
        forbidden_added_code = []
        for name in receipt.get('added_artifacts',{}):
            match = re.match(r'request-(\d+)/(.+)',name)
            if match and (skill in {'nckh-plan','nckh-method','nckh-xia','nckh-git'} or int(match[1])==3):
                if Path(match[2]).suffix.lower() in {'.py','.js','.ts','.tsx','.jsx','.sh','.ps1','.exe'}:
                    forbidden_added_code.append(name)
        own_skill_read = f'/{skill}/SKILL.md' in successful_commands
        policy_reads = {v:v in successful_commands for v in POLICIES}
        work = Path(receipt['workspace'])
        answer = (work/'answer.md').read_text('utf-8') if (work/'answer.md').is_file() else ''
        numbers = {'positive':1,'outcome':2,'negative':3,'failure':4}
        selected = [numbers[v.rsplit(':',1)[1]] for v in receipt['case_ids']]
        markers = {str(n):bool(re.search(r'(?:Yêu cầu|YEU CAU|Request|request)\s*'+str(n)+r'\b',answer)) for n in selected}
        record = {'skill_id':skill,'round':receipt['round'],'native_status':receipt['status'],'receipt_sha256':sha(path),
                  'own_skill_read_observed':own_skill_read,'required_policy_reads_observed':policy_reads,
                  'all_required_request_sections_observed':all(markers.values()),'required_request_numbers':selected,
                  'protected_file_changes':protected_changes,
                  'ungranted_existing_fixture_changes':ungranted_existing_changes,
                  'unauthorized_product_changes_in_readonly_requests':forbidden_product_changes,
                  'unexpected_added_code_in_plan_or_handoff_only_requests':forbidden_added_code,
                  'installed_tree_unchanged':receipt.get('installed_tree_unchanged'),
                  'successful_read_commands':len(reads),'command_count':len(commands),
                  'answer_sha256':sha(work/'answer.md') if answer else None,
                  'usage':receipt.get('usage',[]),'seconds':receipt.get('seconds'),
                  'observation_status':'invariants-pass' if own_skill_read and all(policy_reads.values())
                      and not protected_changes and not ungranted_existing_changes and not forbidden_product_changes and not forbidden_added_code and receipt.get('installed_tree_unchanged')
                      and all(markers.values()) else 'needs-inspection',
                  'semantic_outcome':'pending-controller-review'}
        records.append(record)
    destination = AREA/'observation-audit.json'
    destination.write_text(json.dumps({'evidence_class':'deterministic-trace-and-file-observation',
                                      'scope':'explicitly loaded Codex development sessions; no semantic/human/stable acceptance',
                                      'skills':records},ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'completed_observations':len(records),'invariants_pass':sum(v['observation_status']=='invariants-pass' for v in records),
                      'needs_inspection':[v['skill_id'] for v in records if v['observation_status']=='needs-inspection']}))


if __name__=='__main__':
    main()
