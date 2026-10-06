# R36 Cursor direct Read → edit sequence, attempt 11

## Kết quả

[Verified bindings](./delivery-261005-1523-r36-cursor-direct-sequence.json) ghi một prompt/một model turn trên Cursor CLI `2026.09.15-d2fe57e`, selector `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`. Năm events dùng trực tiếp packaged runner, timeout5s, không observer hoặc fault injection.

Model trả final marker và Stop được ghi nhận. Ba case receipts là advisory/preflight/stop; bounded neutral-event hash của preflight khớp Read/allow. Không có Write hoặc pre-delivery receipt. Fixture vẫn đúng preimage: **write oracle FAILED**. Raw tool-use ID và native failure response không được giữ trong ca này, nên nguyên nhân thất bại vẫn **unverified**.

## Giới hạn so sánh

[Instrumented attempt10](./delivery-261005-1509-r36-cursor-read-edit-sequence.md) quan sát Read → Read → Write với outer20s/runner5s và exact requested write bytes. Hai ca khác timing và cách gọi handler. Attempt11 không dùng kết quả10 để tự chấm production5s PASS; một preflight Read không chứng minh đã gọi hoặc chặn mutation.

## Cleanup và trạng thái

Matching-byte cleanup gỡ26 members và giữ552 historical members. Native/graceful exit requests không đóng root19948; identity-verified force-stop thành công, final process audit zero matching/zero tracked-live và harness exit1 được giữ. Terminal chunks của ca11 không truncated.

Protected global hook/MCP/plugin configs giữ nguyên; CLI-owned state hash được ghi riêng trong bindings, controller direct-write=false. Source r36/281 pins không đổi. P3 full native event/version/surface gate còn unchecked, plan44/45; owner acceptance vẫn chỉ bind exact r29 VI/EN samples, installed r25 và scientific/stable/release giữ gates riêng.
