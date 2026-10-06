# AGY CLI r37: public Write có thêm LF, exact-byte oracle thất bại

[Verified bindings](./delivery-261005-2155-r37-agy-cli-byte-failure.json) giữ một actual `write_to_file`/DONE, preflight allow, selected TargetFile và final marker/native exit0 trên AGY CLI1.2.17/Gemini3.8FlashMedium/dangerous. Brief yêu cầu không newline; actual bytes bằng requested bytes cộng một LF. **Exact-byte oracle vẫn failed**, không regrade hoặc sửa raw evidence.

Batch28 freeze tối đa năm turns nhưng dừng sau turn đầu; bốn case còn lại không chạy. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi. Native tool frames không có CodeContent, nên chưa chứng minh newline được thêm bởi model hay host. [Batch29](./delivery-261005-2210-r37-agy-cli-controls.md) là brief riêng yêu cầu JSON decoded content kết thúc bằng đúng một LF, không thay grade của batch28.

Lượt tra models trong sandbox exit1 do log access và proxy bị chặn, zero model prompts; không phải kết luận authentication. Lượt elevated models inventory exit0, alias `gemini-3.8-flash-medium` hiện diện. CLI báo1.2.16 trước admission và1.2.17 khi prepare; controller không gọi update, nguyên nhân drift chưa verified.

Direct packaged handlers đều5s; no instrumented callback observer. Neutral policy receipts giữ advisory/preflight/pre-delivery/stop; advisory phase không phân biệt PreInvocation và PostInvocation. Post-delivery artifact QA còn pending. Native init ghi exact model alias và `always-proceed`; effort medium có trong command, backend/billing attestation chưa có. Không claim shared hook/tool ID hoặc full event matrix.

Cleanup26 matching config/payload members, preserved231 historical members và protected settings/hooks hashes. Union audit64 identities, zero matching/tracked-live, không taskkill. Source/install/publication không thay đổi; full native task **unchecked/44 of45/P3 active**.
