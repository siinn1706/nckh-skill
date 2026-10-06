"""Publish current observed counts with hashes; never infer semantic acceptance."""

import collections
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

AREA = Path(__file__).resolve().parent
PROJECT = AREA.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    corpus_path = AREA/'development-corpus.json'
    corpus = json.loads(corpus_path.read_text('utf-8'))
    catalog = json.loads((PROJECT/'nckh-kit/core/registry/catalog/skills.json').read_text('utf-8'))
    kits = {v['id']:v['kit'] for v in catalog['skills']}
    reviews_path = AREA/'controller-reviews.json'
    reviews = json.loads(reviews_path.read_text('utf-8'))['reviews']
    observed = {}
    attempts = []
    for p in sorted((AREA/'private').glob('round-*/nckh-*/receipt.json')):
        receipt = json.loads(p.read_text('utf-8'))
        if receipt.get('status') == 'reserved-for-controller-policy-change':
            continue
        attempts.append(receipt)
        skill = receipt['skill_id']
        if skill not in observed or receipt['round'] >= observed[skill]['round']:
            observed[skill] = receipt
    latest = {}
    for review in reviews:
        if 'answer_sha256' in review and sha(AREA/review['answer_reference']) != review['answer_sha256']:
            raise ValueError('Reviewed answer changed; review is stale')
        if 'native_receipt_sha256' in review and sha(AREA/review['native_receipt_reference']) != review['native_receipt_sha256']:
            raise ValueError('Reviewed receipt changed; review is stale')
        if 'trace_sha256' in review and sha(AREA/review['trace_reference']) != review['trace_sha256']:
            raise ValueError('Reviewed trace changed; review is stale')
        for kind, value in review['case_verdicts'].items():
            key = review['skill_id']+':'+kind
            if key not in latest or review['round'] >= latest[key]['round']:
                latest[key] = dict(value, round=review['round'], skill_id=review['skill_id'],
                                   answer_reference=review['answer_reference'])
    cases = []
    for case in corpus['cases']:
        verdict = latest.get(case['id'],{'verdict':'not-reviewed','round':None})
        cases.append({'id':case['id'],'skill_id':case['skill_id'],'kit':kits[case['skill_id']],
                      'type':case['type'],'review':verdict})
    counts = collections.Counter(v['review']['verdict'] for v in cases)
    usage = collections.Counter()
    usage_count = 0
    for receipt in attempts:
        for event in receipt.get('usage',[]):
            usage.update(event)
            usage_count += 1
    result = {'schema_version':1,'recorded_at':datetime.now(timezone.utc).isoformat(),
              'evidence_class':'agent-authored-exposed-development-observations-and-controller-review',
              'corpus_sha256':sha(corpus_path),'case_count':len(cases),'skill_count':len(kits),
              'observed_completed_sessions':sum(v.get('status')=='completed-unreviewed' for v in attempts),
              'observed_running_sessions':sum(v.get('status')=='running' for v in attempts),
              'observed_timeout_attempts':sum(v.get('status')=='timeout-unknown' for v in attempts),
              'native_attempts':[{'skill_id':v['skill_id'],'round':v['round'],'status':v['status'],
                                 'case_ids':v['case_ids'],'timeout_seconds':v.get('timeout_seconds')}
                                for v in attempts],
              'case_verdict_counts':dict(counts),'native_usage_session_coverage':usage_count,
              'reported_usage':dict(usage),'billing_cost':'unknown','effective_model':'unknown',
              'stable_accepted_task_count':0,'human_acceptance':'not-evaluated','holdout':'none',
              'cases':cases,'review_record_sha256':sha(reviews_path),
              'review_history':reviews,
              'first_round_verdict_counts':dict(collections.Counter(value['verdict'] for review in reviews
                  if review['round']==1 for value in review['case_verdicts'].values()))}
    (AREA/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    lines = ['# Kết quả thử trực tiếp NCKH — development', '',
             'Cập nhật UTC: '+result['recorded_at'], '',
             f"37 skill, 148 tình huống; đã hoàn tất {result['observed_completed_sessions']} phiên native, {result['observed_running_sessions']} phiên đang chạy; giữ {result['observed_timeout_attempts']} attempt từng bị timeout.", '',
             f"Agent review: {counts.get('pass',0)} pass, {counts.get('fail',0)} fail, {counts.get('pending',0)} pending, {counts.get('not-reviewed',0)} chưa chấm.", '',
             'Đây là dữ liệu tổng hợp do agent soạn và tự chấm. Không có human gold, holdout kín hoặc promotion stable. Đầu ra và receipts được giữ nguyên; pass kỹ thuật không đóng gate khoa học/người thật.', '',
             '| Skill | Nhóm | Positive | Outcome | Negative | Failure | Native |',
             '|---|---|---|---|---|---|---|']
    for skill in sorted(kits):
        status = observed.get(skill,{}).get('status','not-run')
        verdicts = []
        for kind in ('positive','outcome','negative','failure'):
            reviewed = latest.get(skill+':'+kind,{})
            value = reviewed.get('verdict','not-reviewed')
            if reviewed.get('round',1) > 1:
                value = '['+value+' (r'+str(reviewed['round'])+')]('+reviewed['answer_reference']+')'
            verdicts.append(value)
        label = '['+skill+'](workspaces/round-1/'+skill+'/answer.md)' if (AREA/'workspaces/round-1'/skill/'answer.md').is_file() else skill
        lines.append('| '+label+' | '+kits[skill]+' | '+' | '.join(verdicts)+' | '+status+' |')
    lines += ['', '## Lỗi và bằng chứng còn thiếu', '']
    for case in cases:
        if case['review']['verdict'] in ('fail','pending'):
            lines.append('- **'+case['id']+' — '+case['review']['verdict']+'**: '+case['review'].get('evidence',''))
    lines += ['', '## Lịch sử development', '',
              'Đếm vòng 1 đã chấm: '+json.dumps(result['first_round_verdict_counts'],ensure_ascii=False)+'. Các verdict cũ và trace vẫn được giữ trong review history.', '',
              'Lượt tiếp theo chỉ xử lý điểm thiếu/lỗi đã quan sát. Phạm vi catalog, lưu rollout và việc bỏ deadline được ghi riêng; không có best-of-N hoặc thay oracle sau kết quả.', '',
              '## Telemetry', '',
              f"Có usage cho {usage_count} phiên hoàn tất. Input: {usage.get('input_tokens',0):,}; trong đó cached input: {usage.get('cached_input_tokens',0):,}. Output: {usage.get('output_tokens',0):,}; trong đó reasoning output: {usage.get('reasoning_output_tokens',0):,}.", '',
              'Cached input và reasoning là thành phần của các số tổng, không cộng hai lần. Chi phí tiền và model/effort thực sự của provider vẫn unknown; cấu hình yêu cầu gpt-6.1-sol/max được kế thừa.', '',
              '[Prompt/protocol đã khóa](development-corpus.json) · [Review có bằng chứng](controller-reviews.json) · [Kiểm tra trace/file](observation-audit.json) · [Kết quả máy đọc](results.json)', '']
    (AREA/'results.md').write_text('\n'.join(lines),'utf-8')
    print(json.dumps({k:result[k] for k in ('observed_completed_sessions','observed_running_sessions','case_verdict_counts','native_usage_session_coverage')}))


if __name__=='__main__':
    main()
