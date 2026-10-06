# R36 — genuine Cursor Read/Write sequence

[Verified bindings](./delivery-261005-1509-r36-cursor-read-edit-sequence.json) và [verifier](../runs/nckh-native-261005-1509-r36-cursor-read-edit-sequence-attempt-10/verify-read-edit-delivery.py) ghi một genuine Grok4.7/context500k/xhigh/fast=false turn trên Cursor CLI interactive `2026.09.15-d2fe57e`. Source vẫn r36/281 pins/hash `1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30`; không gửi lại prompt hoặc sửa source.

## Native callbacks và exact effect

Ca này yêu cầu đọc selected synthetic fixture rồi dùng một native file-edit tool. Có hai distinct native `tool_use_id`: ID đầu có Read pre/post; ID thứ hai có Read pre/post rồi Write pre/post trên đúng một tệp `oracles/r36-cursor-read-edit-public-10.txt`. Tool-use ID được host tái dùng cho bước Read và Write của thao tác thứ hai. Pairing dùng cả ID và tool name, không đếm ba pre callbacks thành ba distinct tool-use identities. Raw model call frames không được giữ.

Write preflight được policy allow và actual file bytes đổi đúng requested marker/newline. Before SHA256 `b731e32d12f7245ff4309d3f4f5d5442f07765a5e4edd52f04999118a8ed45fd`; after SHA256 `ced427e4c702da570bb11e47b16e56a32593ec4b10b702f1116e40f513ffcdee`. Đây là actual native Write observation trên controller-owned synthetic marker, không phải scientific output.

Chín bounded observer records gồm sessionStart1, beforeSubmitPrompt1, preToolUse3, postToolUse3, stop1; tất cả có actual version/project/event binding, runner exit0 và no fault injection. Bảy policy receipts giữ deterministic idempotence; hai Read callbacks có thể dùng cùng neutral record. Pre-delivery QA vẫn pending/artifact-final-bytes-missing-or-stale, không trở thành artifact acceptance sau khi có mutation.

## Scope và giới hạn

Observer outer20s và packaged runner5s khác direct template5s. Sequence và outer timing đều khác [single-Write controls](./delivery-261005-1415-r36-cursor-existing-mutations.md), nên một successful sequence không xác định riêng nguyên nhân của các failure trước và không regrade chúng. Native Write/pre/post được quan sát ở instrumented surface; production direct5s, genuine mutation-denial và full native matrix vẫn cần evidence riêng.

Observer chỉ giữ bounded native field names, tool name, tool-use ID, selected path và input hash; không giữ raw draft/content/tool return bytes. Một terminal chunk bị truncation. [Collector correction](../runs/nckh-native-261005-1509-r36-cursor-read-edit-sequence-attempt-10/collector-correction.json) và preimage giữ việc sửa nhầm callback-count thành distinct-use-ID count; không retry model.

## Cleanup

Native exit request và graceful taskkill chưa đóng cây. Exact PID/UTC creation checks có trước force-stop; harness exit1 được giữ. Final audit zero matching/zero live trong năm tracked PIDs. Cleanup gỡ26 matching config/payload members, giữ524 historical members; fixture-after và callback evidence được giữ. Protected global configs không đổi; CLI-owned state hash delta có trong verified bindings, controller direct-write=false.

Plan vẫn in-progress44/45, P3 full native task unchecked. Claude grant, app/IDE evidence, remaining event/tool/failure cells và scientific/stable/release gates còn riêng biệt.
