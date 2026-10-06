"""Dispatch only the recorded diagnostic requests, retaining all earlier attempts."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import sys

AREA = Path(__file__).resolve().parent


def save(path, value):
    temporary = path.with_suffix('.json.new')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skills', nargs='+', required=True)
    parser.add_argument('--lane', required=True)
    args = parser.parse_args()
    if not re.fullmatch('[a-z][a-z0-9-]*', args.lane):
        raise ValueError('Invalid owned lane')
    protocol_path = AREA / 'followup-protocol.json'
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    options = {v['skill_id']: v for v in protocol['followups']}
    if len(args.skills) != len(set(args.skills)) or not set(args.skills) <= set(options):
        raise ValueError('Select unique recorded diagnostic skills')
    journal_path = AREA / 'private' / ('followup-' + args.lane + '.json')
    if journal_path.exists():
        raise ValueError('Existing diagnostic journal must be retained')
    journal = {'status': 'running', 'controller_pid': os.getpid(), 'lane': args.lane,
               'protocol_sha256': hashlib.sha256(protocol_bytes).hexdigest(),
               'timeout_seconds': None, 'selected_skills': args.skills, 'attempts': [],
               'started_at': datetime.now(timezone.utc).isoformat()}
    save(journal_path, journal)
    try:
        for skill in args.skills:
            if protocol_path.read_bytes() != protocol_bytes:
                raise ValueError('Recorded diagnostic conditions changed during dispatch')
            recipe = options[skill]
            if (AREA / 'private' / 'round-2' / skill).exists():
                raise ValueError('Existing diagnostic attempt is retained, never redispatched')
            journal['current_skill'] = skill
            save(journal_path, journal)
            sys.argv = ['run-native-suite.py', '--round', '2', '--lane', args.lane,
                        '--persist-session', '--skills', skill, '--case-types', *recipe['case_types']]
            if recipe['project_catalog_scope']:
                sys.argv.append('--project-catalog-scope')
            runpy.run_path(str(AREA / 'run-native-suite.py'), run_name='__main__')
            receipt_path = AREA / 'private' / 'round-2' / skill / 'receipt.json'
            receipt = json.loads(receipt_path.read_text('utf-8'))
            journal['attempts'].append({'skill_id': skill, 'status': receipt['status'],
                                        'receipt': receipt_path.relative_to(AREA).as_posix()})
            journal.pop('current_skill', None)
            save(journal_path, journal)
        journal['status'] = 'completed-unreviewed'
    except BaseException as error:
        journal.update(status='interrupted-unknown' if isinstance(error, KeyboardInterrupt) else 'fail',
                       error_kind=type(error).__name__)
        raise
    finally:
        journal['finished_at'] = datetime.now(timezone.utc).isoformat()
        save(journal_path, journal)


if __name__ == '__main__':
    main()
