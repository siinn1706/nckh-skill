"""Append a controller verdict, binding the observed answer and receipt hashes."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

AREA = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    incoming = json.load(sys.stdin)
    additions = incoming if isinstance(incoming, list) else [incoming]
    path = AREA / 'controller-reviews.json'
    record = json.loads(path.read_text('utf-8'))
    existing = {(v['skill_id'], v['round']) for v in record['reviews']}
    for review in additions:
        skill, number = review['skill_id'], review.get('round', 1)
        key = (skill, number)
        if key in existing:
            raise ValueError('Existing review must be retained, not overwritten')
        if not review['case_verdicts'] or not set(review['case_verdicts']) <= {'positive', 'outcome', 'negative', 'failure'}:
            raise ValueError('Review must cover declared frozen case types')
        if any(v['verdict'] not in {'pass', 'fail', 'pending'} or not v['evidence'].strip()
               for v in review['case_verdicts'].values()):
            raise ValueError('Verdict and concrete observed evidence are required')
        receipt = AREA / 'private' / f'round-{number}' / skill / 'receipt.json'
        observed = json.loads(receipt.read_text('utf-8'))
        if observed['status'] in {'starting', 'running'}:
            raise ValueError('Do not grade a running session')
        if any(skill + ':' + kind not in observed['case_ids'] for kind in review['case_verdicts']):
            raise ValueError('Do not grade a case absent from the observed attempt')
        answer = AREA / 'workspaces' / f'round-{number}' / skill / 'answer.md'
        trace = receipt.with_name('stdout.jsonl')
        review.update(round=number, answer_reference=answer.relative_to(AREA).as_posix(),
                      answer_available=answer.is_file(),
                      native_receipt_reference=receipt.relative_to(AREA).as_posix(),
                      native_receipt_sha256=sha(receipt),
                      trace_reference=trace.relative_to(AREA).as_posix(), trace_sha256=sha(trace),
                      reviewed_at=datetime.now(timezone.utc).isoformat())
        if answer.is_file():
            review['answer_sha256'] = sha(answer)
        review.setdefault('limits', ['Explicit invocation, shared scenario session and controller-agent judgment; no human/domain/stable acceptance.'])
        record['reviews'].append(review)
        existing.add(key)
    temporary = path.with_suffix('.json.new')
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    temporary.replace(path)
    print(json.dumps({'appended': len(additions), 'review_count': len(record['reviews'])}))


if __name__ == '__main__':
    main()
