# Codex CLI native event addendum — r34

## Current scope

Current r34 source/build/archives giữ nguyên hash `8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34`. [Main delivery](./delivery-261005-0005-r34-cursor-agy.md) ghi full local checks. Addendum này ghi Codex CLI `0.154.0` **exec** route; [structured bindings](./delivery-261005-0052-r34-codex-events.json) chứa actual callbacks, native tool items, markers, failed discovery/collector receipts, cleanup và process audit. Plan vẫn **in-progress, 44/45**.

GPT-5.6 Luna medium và native dangerous flags thuộc direct human grant. Model ID ghi trong actual callbacks; effort được yêu cầu qua invocation. Native metadata/arguments chưa là backend attestation/billing. Global MCP/plugins và 27 unrelated hook definitions được disable riêng cho invocation trước inference; controller không edit trực tiếp global file; native CLI tự persist own workspace trust như cleanup receipt ghi.

## Permission/discovery history

- App-server discovery không nhận new project hooks vì project chưa trusted, dù invocation có project trust override. Metadata failure giữ nguyên.
- Automatic approval review từ chối normal native UI project-trust step vì persistent global trust addition nằm ngoài retained authorization theo reviewer. Normal UI action này không chạy. CLI route sau đó tự persist exact own workspace/project trust key; cleanup receipt chứng minh thay đổi này. Report trước đã diễn giải nhầm workspace trust thành hook-definition trust. Không có approval mới được suy từ elapsed time.
- CLI route dùng inline **sessionFlags** definitions cùng `--dangerously-bypass-hook-trust`. Flag bypass hook-definition review cho invocation; native CLI vẫn tự lưu own workspace/project trust. Actual native source enum là `sessionFlags`; initial collector expectation `session` đã fail rồi được sửa từ native metadata, không nới scope theo tên bất kỳ.
- App-server model allow attempt tạo marker nhưng **không có hook callbacks** trên route đó; collector còn có encoding alias typo. [Reconciliation](../runs/nckh-native-261005-0052-r34-codex-attempt-01/app-server-allow-01-reconciliation.json) giữ native process/marker/error bindings. Không gọi turn này là hook qualification.
- CLI exec supports dangerous flags trực tiếp. Matching project config có hai callbacks/event; sau preserve/removal file đó, cùng inline definitions có một callback/event. Differential này support file-sensitive project+inline multiplicity trên CLI route; Cleanup receipt ghi own workspace trust persisted; plugin support vẫn chưa observed.

Official [Codex hook documentation](https://learn.chatgpt.com/docs/hooks) describes invocation-only hook-trust bypass and separates explicit tool deny from hook failure behavior. Current metadata và actual native calls ở đây giữ riêng với docs capability claims.

## Native baselines

[Baseline receipts](../runs/nckh-native-261005-0052-r34-codex-attempt-01/native-baseline-summary.json):

- Allow: five genuine selected events; một shell execution và marker đúng bytes.
- Policy deny: genuine PreToolUse policy block, marker absent; model không retry hoặc đổi write route.
- Hai inline groups: hai same-tool PreToolUse callbacks, một idempotent policy receipt, một completed shell item và marker. Plugin route vẫn unobserved.

## Event fault matrix

Twenty-five native attempts có actual selected callbacks; fault được chèn bởi owned observer sau host invocation. Không gọi đây là malformed events tự phát bởi host. Từng model/native outcome giữ nguyên trong [raw summary](../runs/nckh-native-261005-0052-r34-codex-attempt-01/native-fault-summary.json).

| Selected event | Malformed input | Malformed output | Timeout | Crash | Unsupported selected codec |
|---|---:|---:|---:|---:|---:|
| SessionStart | Có | Có | Có | Có | Có |
| UserPromptSubmit | Không | Có | Có | Có | Có |
| PreToolUse | Không | Có | Có | Có | Có |
| PostToolUse | Có | Có | Có | Có | Có |
| Stop | Có | Có | Có | Có | Có |

Bảng ghi **marker được tạo hay không**, không phải bảng pass/fail chung. Pre events xảy ra trước tool; PostToolUse/Stop sau side effect. Hook failure có thể fail-open; callback hoặc CLI exit0 không thay actual command items. Unsupported selected codec là controller gọi unknown event cho packaged runner sau callback thật. Harness timeout2s/sleeper8s chưa qualify public template5s hoặc production timing.

## Cleanup và phần còn mở

[Cleanup](../runs/nckh-native-261005-0052-r34-codex-attempt-01/project/cleanup.json) gỡ 26 matching payload members; matching project config đã park vào evidence trước matrix và không callable. Native CLI đã thêm exact own project trust key. Controller không direct-write global; hook-definition trust không persist. Unrelated parsed global state unchanged sau khi bỏ own key chỉ trong memory. [Final audit](../runs/nckh-native-261005-0052-r34-codex-attempt-01/post-cleanup-process-audit.json) zero matching task processes. All oracles, native conversations/logs, callbacks, policy receipts và failures giữ nguyên.

Lần cleanup đầu từ chối native Windows backslashes trong owned receipt trước khi xóa payload. [Failure record](../runs/nckh-native-261005-0052-r34-codex-attempt-01/cleanup-preparation-failure.json) và ba helper preimages được giữ; helper đổi đúng Windows relative path sang POSIX trước cùng containment/hash checks. Audit trước cleanup giữ riêng với audit sau cleanup. Packaged r34 source không đổi.

Required native task vẫn unchecked: normal UI trust rejection giữ trong history; native CLI đã persist own workspace trust. Project/plugin duplicate và protected-path/other tools chưa qualified. Claude model/tool, Cursor events/timeouts, direct Desktop/IDE observations còn mở. Installed r25 chưa update; stable/scientific/release lanes riêng. Source/structural validation không đóng các gates này.

## Trust reporting correction

[Correction receipt](../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json) preserves the original report/helper/document preimages and binds the unchanged native cleanup receipt plus current read-only observation. The prior report incorrectly stated that no project trust was persisted. Both this exec run and the later file run have native-owned workspace trust; hook-definition trust and controller direct writes remain distinct. Native callbacks/oracles and r34 source bindings are unchanged.
