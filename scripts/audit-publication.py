"""Audit tracked publication files without printing credential values."""
import hashlib
import io
import json
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET = re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|gh[pousr]_|github_pat_)[A-Za-z0-9_-]{24,}|AKIA[0-9A-Z]{16}')
PRIVATE_HOME = re.compile(rb'C:(?:[\\/]|\\\\)+Users(?:[\\/]|\\\\)+Siinn', re.I)
REVIEWED_FIXTURE = {
    'resources/scientific-agent-skills-main/tests/autoskill/test_redact.py':
    '515f77ec821e28af8c0a3bc5731259408c7c75fbb7d911d19372e2daa10ffddd',
}
LOCAL_PREFIXES = (
    '.agents/', '.codex/', '.nckh-state/', 'github-publication/',
    'plans/local-backups/', 'resources/claudekit-engineer-main/',
    'resources/claudekit-marketing-main/',
    'resources/skills-main/skills/docx/', 'resources/skills-main/skills/pdf/',
    'resources/skills-main/skills/pptx/', 'resources/skills-main/skills/xlsx/',
)


def audit_bytes(relative, data, failures):
    if SECRET.search(data):
        if REVIEWED_FIXTURE.get(relative) != hashlib.sha256(data).hexdigest():
            failures.append({'file': relative, 'reason': 'credential pattern requires review'})
    if relative.startswith('plans/') and PRIVATE_HOME.search(data):
        failures.append({'file': relative, 'reason': 'personal machine path'})


def main():
    files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    failures = []
    size = 0
    count = 0
    for relative in filter(None, files):
        path = ROOT / relative
        if relative.startswith(LOCAL_PREFIXES):
            failures.append({'file': relative, 'reason': 'local-only tree'})
        if path.name == '.env' or (path.name.startswith('.env.') and path.name != '.env.example') or path.suffix in {'.pem', '.key', '.p12', '.sqlite', '.db', '.log'}:
            failures.append({'file': relative, 'reason': 'private or runtime file'})
        if any(word in path.name for word in ('.stdout.', '.stderr.')):
            failures.append({'file': relative, 'reason': 'raw runtime output'})
        try:
            data = path.read_bytes()
        except OSError:
            failures.append({'file': relative, 'reason': 'missing tracked file'})
            continue
        count += 1
        size += len(data)
        if len(data) >= 100 * 1024 * 1024:
            failures.append({'file': relative, 'reason': 'GitHub file size limit'})
        audit_bytes(relative, data, failures)
        if relative.startswith('plans/') and path.suffix == '.zip':
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for member in archive.namelist():
                    audit_bytes(relative + ':' + member, archive.read(member), failures)
    print(json.dumps({'status': 'fail' if failures else 'pass', 'files': count,
                      'bytes': size, 'reviewed_synthetic_fixture': sorted(REVIEWED_FIXTURE),
                      'failure_count': len(failures),
                      'failure_reasons': dict(Counter(item['reason'] for item in failures)),
                      'failures': failures[:20]}, ensure_ascii=False, indent=2))
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
