# NCKH r30 — native model/tool checkpoint

Quyền mới cho phép `gpt-5.6-luna` hoặc `gpt-6.1-sol`, mức `medium`, được lưu trong [model grant](../runs/nckh-native-261004-1707-attempt-01/model-medium-grant.json). Cả hai xuất hiện trong native `model/list`; lượt kiểm chứng này dùng `gpt-5.6-luna/medium`. [Structured evidence](delivery-261004-1707-r30-model-tools.json) bind source, definition, callbacks, completed turns, oracle và cleanup.

## Quan sát thực

Codex CLI **0.154.0**, Windows, route `app-server --stdio → thread/start → turn/start → native model exec_command/unifiedExecStartup`, event **PreToolUse**, matcher/native tool **Bash**. Có **8 completed model turns, 8 genuine callbacks, 5 policy receipts và 6 tệp oracle**. Native thread và payload cùng báo đúng model, effort `medium`; không có fallback sang model khác trong thread. Đây là runtime metadata, chưa có gateway/backend model attestation hoặc hóa đơn provider.

| Ca | Native hook | Tệp oracle được tạo | Policy |
|---|---|---|---|
| Allow | `completed` | Có | allow |
| Policy deny | `blocked` | Không | block |
| Malformed runner input (injected) | `blocked` | Không | block |
| Malformed output (injected) | `failed` | Có | Không có policy receipt |
| Timeout 2 giây / sleep 8 giây | `failed` | Có | Không có policy receipt |
| Observer crash exit17 | `failed` | Có | Không có policy receipt |
| Unsupported selected codec | `failed` | Có | block |
| Bash thiếu controller mapping | `completed` | Có | manual |

`allow` thực sự chạy shell exit0 và tạo tệp; `policy-deny` nhận callback với cùng kiểu action, trả deny `plan-only-mutation`, native hook `blocked`, không có completed command item và không có tệp. Malformed runner input được inject sau callback cũng chặn. Đây là preventive evidence cho đúng route/event/version đã thử.

Output JSON hỏng, timeout, crash và unsupported selected codec có native `failed` rồi shell vẫn exit0/tạo tệp: **bốn failure cases fail-open**. Không nâng deterministic `block` receipt của unsupported codec thành host prevention. Observer cố ý crash exit17; Windows host command layer báo exit1. Native unsupported-event/tool vẫn chưa được chứng minh: test selected-codec khác event, còn uncovered case dùng Bash thật nhưng bỏ controller mapping.

## Phạm vi và isolation

Definition hash: `sha256:f26dcc9290135bcf225d52cdff4a72130753dc33758b46a5ebf2a5b314e71206`. Normal native TUI review/trust/enable riêng đúng project hook, rồi disable. Mỗi lượt actual `hooks/list` xác nhận 27 user hooks disabled theo invocation; effective config xác nhận ba configured MCP servers và 13 plugins disabled. Hook runner/policy không gọi provider; model turn do controller gọi theo quyền mới. TUI trust/cleanup dùng endpoint refused-loopback, không chạy inference.

Bash payload có `tool_input.command`, không có structured `file_path/path`; phép thử này không xác nhận protected-path extraction/credential-path blocking. Hosted tools, shell continuations, Codex project/plugin duplicate, các event còn lại, direct TUI/desktop/IDE inference đều chưa có coverage từ tám cases này. Chưa activate production route như enforcement.

Source giữ **r30/281 pins**, hash `55a4b60779228f3be3ae42d7691a49dec1df1b4e6f26139a32435aa1914562e1`. Full deterministic/build/extract evidence đã có cho cùng source nên không chạy lại. Hai mẫu owner VI/EN giữ acceptance/hashes ban đầu; installed r25 chưa đổi.

## Cleanup

[Matching cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex-model/tool-probe-cleanup.json) gỡ một config và 26 staged payload members sau native UI disable. [Native list sau cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex-model/model-metadata-attempt-03.json) không còn project hook callable. Một test key mới còn trusted/disabled; cộng ba key lịch sử là bốn test keys disabled, không phải bốn hash hiện hành của cùng UserPromptSubmit key. Unrelated native user-hook state không đổi. [Final process audit](../runs/nckh-native-261004-1707-attempt-01/process-audit-model-tools-final.json) có 0 matching run processes. Giữ sáu tệp oracle, contexts và receipts làm evidence.

## Điều kiện còn thiếu

[Host preflight mới](../runs/nckh-native-261004-1707-attempt-01/host-model-grant-prerequisites.json): Cursor CLI vẫn chưa đăng nhập. AGY `models` qua kết nối thật exit0, danh mục không có hai GPT models được cấp quyền; command này không xác nhận prompt eligibility hoặc native hook coverage. Claude Code chưa có configured route tới hai GPT models trong phần settings đã đọc; chưa gọi model khác. Không chuyển quyền GPT thành quyền dùng mặc định Claude/Gemini.

Codex CLI `plugin add` dùng marketplace selector; installed `PluginInstallParams` không có destination/scope field. [Official local marketplace guide](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo) mô tả repo marketplace và enabled state; [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) nói refresh có thể install/refresh cả khi disabled. Chưa xác định và thử route duplicate không ghi global plugin state; không cài plugin global để đóng gate.

Plan giữ **in-progress, 44/45**: native host/version/surface/event task còn unchecked. Model grant đã tháo điều kiện provider cho hai lựa chọn được nêu; các host/account/surface prerequisites và native cells còn thiếu được giữ riêng. Goal turn này là progress, chưa complete.
