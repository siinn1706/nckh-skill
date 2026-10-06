# Cursor r37 — actual uncovered Grep route và granted model selection

## Native result

Một interactive turn trên Cursor CLI `2026.09.15-d2fe57e` gọi đúng **Grep** một lần trên synthetic public fixture. Pre/post callbacks khớp cùng nonempty native tool ID, absolute path, session và version. Terminal reports one match, exact final reply marker và project Stop observed; fixture bytes giữ nguyên.

| Observation | Result |
|---|---|
| Actual native callbacks / policy receipts | 5 / 5 |
| preToolUse | `manual / tool-route-uncovered`, runner output `{}` |
| Native Grep | Completed; postToolUse observed |
| postToolUse | `pending / artifact-final-bytes-missing-or-stale` |
| Final marker / native exit | Observed / 0 |

Grep có trong native host nhưng không nằm trong operation map của controller context này. Host tiếp tục thực hiện tool khi runner trả `{}` cho manual. Bằng chứng này xác nhận **uncovered route cần xử lý thủ công**; không chứng minh tool/event unsupported của host hoặc preventive enforcement. Artifact QA vẫn có gate riêng. Observer forwards genuine bounded payload tới unchanged packaged r37 runner; không fault injection, một prompt/submission, zero model retries.

## Model và failure history

Lượt này dùng **existing selectedModel**: Grok4.7, context500k, reasoning_effortxhigh, fastfalse; bỏ explicit `--model` và xác nhận CLI hiển thị “Grok 4.7 500K Extra High · MAX” trước khi gửi prompt. Native callbacks report `grok-4.7-xhigh`; backend/billing attestation không observed. Không direct-write global config hoặc thay model/effort/context đã granted.

Admission failure23 (historical evidence path: `./delivery-261005-2004-r37-cursor-search-admission-failure.md`; unavailable in the cleaned checkout) giữ terminal rejection/exit1 với zero model turns/prompt submissions. Đây là recovery của selection route; không regrade lỗi trước đó. First nested preflight audit của controller24 tự khớp Python PID9696, exit1 trước staging/prompt. Receipt được preserve, independent audit sau khi controller exit có zero matches, preparation helper chỉ chạy một lần; recovery (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/preparation-controller-recovery.json`; unavailable in the cleaned checkout) giữ toàn bộ giới hạn.

## Cleanup và remaining gates

Ctrl+D/native exit0, final audit **zero matching / zero tracked-live**. Cleanup gỡ27 matching owned members gồm fixture, giữ767 historical members/protected global config hashes. CLI-owned state hash changes không cho biết changed fields. Source kit r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên; local checks của đúng source được reuse.

Raw terminal chunks truncated, native tool-return content không retained; selected pre/post/path/ID/receipt hashes và fixture preservation được verified riêng. Full native matrix còn mở, plan44/45/P3 active; native plugin prompt/stop gaps, actual private Write, remaining events/tools/app surfaces và Claude model/effort chưa đủ evidence. Exact r29 VI/EN acceptance, installed r25 và scientific/stable/release/publication giữ scope hiện có.

## Evidence

- Verified bindings (historical evidence path: `./delivery-261005-2119-r37-cursor-selected-model-search.json`; unavailable in the cleaned checkout)
- Original case (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/case-uncovered-search.json`; unavailable in the cleaned checkout) và summary (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/native-uncovered-summary.json`; unavailable in the cleaned checkout)
- Model selection before prompt (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/model-selection-before-prompt.json`; unavailable in the cleaned checkout), frozen brief (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/frozen-brief.json`; unavailable in the cleaned checkout), definitions (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/definitions/session.json`; unavailable in the cleaned checkout)
- Cleanup (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/cleanup.json`; unavailable in the cleaned checkout), final process audit (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/final-process-audit.json`; unavailable in the cleaned checkout), native exit0 (historical evidence path: `../runs/nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24/terminal-native-exit-poll-01.json`; unavailable in the cleaned checkout)
