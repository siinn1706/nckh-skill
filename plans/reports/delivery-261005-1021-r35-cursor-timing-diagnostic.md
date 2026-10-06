# Cursor r35: chẩn đoán native timeout5s

## Kết quả

[Structured bindings](./delivery-261005-1021-r35-cursor-timing-diagnostic.json) ghi một genuine Read turn trên Cursor CLI `2026.09.15-d2fe57e` với exact Grok4.7/500K/xhigh grant. Hook chẩn đoán trả `permission:allow` ngay, không gọi packaged runner hoặc NCKH policy. Callback PreToolUse flush output trong **3.076ms** và ghi Python atexit sau **3.695ms**; Cursor vẫn trả native **Hook script timed out after 5000ms** và không đọc được fixture.

Đây là counterexample cho giả thuyết timeout chỉ do policy NCKH chạy lâu. Thời gian đo bắt đầu trong Python, không bao gồm toàn bộ shell startup/transport/executor của host; atexit không phải OS process-exit notification. Nguyên nhân chính xác của host timeout còn unresolved, production template5s vẫn unqualified. Source r35/281 pins không đổi.

| Sự kiện | Callback | Output flush | Python atexit |
|---|---:|---:|---:|
| sessionStart | 1 | 3.598ms | 4.497ms |
| beforeSubmitPrompt | 0 | Không quan sát | Không quan sát |
| preToolUse | 1 | 3.076ms | 3.695ms |
| postToolUse | 0 | Read thất bại | Không quan sát |
| stop | 0 | Không quan sát | Không quan sát |

## Bảo toàn và giới hạn

Definition giữ timeout5s và failClosed. Chỉ có public synthetic Read fixture; exact bytes/hash giữ nguyên. Cleanup gỡ26 matching config/payload members, giữ368 historical project members và raw protected global hashes. Audit sau khi CLI kết thúc không còn matching process; các PID CLI/callback/parent đã không còn trong inventory.

Run dùng callback chẩn đoán riêng được ghi và hash-bound; không phải production runner qualification. Attempt collector kế thừa trường `observer_invoked=false` cho observer cũ; structured bindings nêu rõ callback chẩn đoán thực sự đã chạy. Native stdout, metadata, definitions, input hashes và receipts giữ nguyên; không ghi raw prompt/transcript/email trong callback receipts. Verifier đối chiếu tool use ID, command/streams, fixture, cleanup, historical hashes và source lock.

Plan giữ **in-progress44/45**, full native checkbox unchecked. Prompt/stop của print route vẫn unobserved; không kết luận hai events universally unsupported. Direct IDE receipts và các host/routes còn lại vẫn cần evidence riêng. Các [bốn direct template controls](./delivery-261005-0905-r35-cursor-template-controls.md) tiếp tục được giữ là native failures.
