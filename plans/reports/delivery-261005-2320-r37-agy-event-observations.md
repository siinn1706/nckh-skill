# AGY CLI r37: lifecycle, post-tool và Stop observations

[Bindings](./delivery-261005-2320-r37-agy-event-observations.json) ghi 28 ca sự kiện trên CLI **1.2.17 / Gemini 3.8 Flash medium / always-proceed**: 24 lượt của batch34 và bốn lượt mới batch36. Mỗi lượt có đúng một native `write_to_file`, final marker, resultSUCCESS/num_turns1 và native process exit0. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên. Đây là observer thử với outer5s/inner5s; normal direct packaged controls29 giữ evidence riêng.

## Kết quả thực tế

| Sự kiện | Ca | Native tool | Bytes revised | Policy |
|---|---|---|---|---|
| PreInvocation | allow | DONE | True | advisory |
| PreInvocation | policy-deny | DONE | True | block |
| PreInvocation | malformed-input | DONE | True | block, block |
| PreInvocation | malformed-output | DONE | True |  |
| PreInvocation | timeout | DONE | True | advisory |
| PreInvocation | crash | DONE | True |  |
| PreInvocation | unsupported-codec | DONE | True | block, block |
| PostToolUse | allow | DONE | True | advisory |
| PostToolUse | policy-deny | DONE | True | block |
| PostToolUse | malformed-input | DONE | True | block |
| PostToolUse | malformed-output | ERROR | True |  |
| PostToolUse | timeout | ERROR | True | advisory |
| PostToolUse | crash | ERROR | True |  |
| PostToolUse | unsupported-codec | ERROR | True | block |
| PostInvocation | allow | DONE | True | advisory |
| PostInvocation | policy-deny | DONE | True | block |
| PostInvocation | malformed-input | DONE | True | block, block |
| PostInvocation | malformed-output | DONE | True |  |
| PostInvocation | timeout | DONE | True | advisory |
| PostInvocation | crash | DONE | True |  |
| PostInvocation | unsupported-codec | DONE | True | block, block |
| Stop | allow | DONE | True | advisory |
| Stop | policy-deny | DONE | True | block |
| Stop | malformed-input | DONE | True | block |
| Stop | malformed-output | DONE | True |  |
| Stop | timeout | DONE | True | advisory |
| Stop | crash | DONE | True |  |
| Stop | unsupported-codec | DONE | True | block |

`PreInvocation` và `PostInvocation` trả block trong policy vẫn cho native tool hoàn tất. Wire codec ở hai event là advisory; không có preventive enforcement claim. Chỉ từ tên lifecycle event không suy thứ tự trước/sau từng thao tác tool.

Bốn lỗi `PostToolUse` malformed-output/timeout/crash/unsupported-codec tạo native ERROR **sau khi toàn bộ bytes revised đã ghi**. Policy-deny và malformed-input ở post-tool vẫn native DONE. Lỗi sau thao tác không được regrade thành preventive denial hoặc rollback. Stop faults đều sau final response và bytes đã ghi; không quan sát model resubmission.

196 callbacks observer tổng cộng: PreInvocation56, PreToolUse28, PostToolUse28, PostInvocation56, Stop28. Repetition của lifecycle chưa là controlled project/plugin duplicate. Unknown selected codec vẫn là injection sau callback được hỗ trợ; genuine unsupported native event admission còn riêng.

## Partial collector, repairs và cleanup

Batch34 freeze28 nhưng collector exit1 sau native lượt24 vì descendant wait30s chưa hết. Raw running summary23 và failure giữ nguyên; bốn ca Stop còn lại không chạy trong batch đó. Read-only inspection sau lỗi và union audit xác nhận zero live; không taskkill và không xác định nguyên nhân delay. Batch36 đóng brief riêng cho đúng bốn ca chưa chạy, không resubmit 24 lượt cũ.

Một PostInvocation timeout observer cập nhật sau snapshot: original snapshot/hash và final callback đều bound, late policy không là native permission. Verifier đầu tiên dùng LF replay trong khi observer Windows lưu CRLF. Failing verifier command/preimage/serialization diagnosis được giữ, CRLF repair chỉ sửa kiểm byte; không thay native oracle. Verifier sau repair exit0. Original PostInvocation timing label được sửa trong verified record, raw summary vẫn giữ.

Batch34 cleanup26/preserved391, audit726 identities/zero live. Batch36 cleanup26/preserved874, audit836 identities/zero live. Protected settings/hooks hashes giữ nguyên; controller không direct-write global. Installed r25/publication/owner exact r29 VI/EN acceptance giữ trạng thái trước. Inline verification; không independent reviewer.

Full native task **unchecked / 44 of45 / P3 active**. Remaining includes controlled duplicates, unsupported-event admission, other host/tool/surface cells, Claude selection/turns and app qualification.
