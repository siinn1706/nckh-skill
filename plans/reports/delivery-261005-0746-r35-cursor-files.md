# Cursor CLI file tools — r35

## Phạm vi và bằng chứng

[Structured bindings](./delivery-261005-0746-r35-cursor-files.json) đối chiếu **19 native turns** trên Cursor CLI `2026.09.15-d2fe57e`, current r35/281 pins, source-lock hash `4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255`. Exact selector `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]` và dangerous flags dùng đúng grant hiện có. Source không đổi; local delivery checks của [r35](./delivery-261005-0710-r35-patch-retest.md) được giữ theo revision. Đây là recorded native observations; có hai lượt không đạt mục tiêu thử.

## File routes và callback stages

| Ca | Native result | File |
|---|---|---|
| Write allow | Một edit success; Read allow → Write allow | Tạo đúng marker |
| Write plan-only | Read allow → Write block | Không tạo |
| Write private | Read block; không tới Write | Không tạo |
| Write uncovered mapping | Read/Write manual; edit success | Tạo marker |
| Read allow | Một read success | Fixture không đổi |
| Read private | Read block; native error | Fixture không đổi, không có tool content result |

Một outer `editToolCall` có thể phát hai `preToolUse` callbacks, `Read` rồi `Write`, cùng tool-use ID. Native outer args dùng `path`/`streamContent`; hook args dùng `file_path`/`content`. Phải nhóm theo tool ID, native tool name và callback source. Hai callbacks này không chứng minh model retry.

Project + transient plugin duplicate có một edit success, hai Read và hai Write callbacks, explicit project/plugin provenance và **hai** idempotent policy receipts, một cho mỗi tool stage. Native stream báo nội dung với LF; actual Windows marker có CRLF và exact hash được giữ. Collector ban đầu dùng LF-only hash, đã giữ preimage và sửa oracle theo observed Windows bytes, đồng thời kiểm exact native content.

## Lỗi trước thao tác ghi

Năm faults của batch đầu đều xảy ra ở preread `Read`; native edit rejected, marker absent. Supplemental tests chọn fault chỉ khi actual native tool là `Write`: malformed input, malformed output, timeout, crash và unsupported selected codec đều tới đúng Write callback, có native error và marker absent. Faults là controller injection sau genuine callback; unknown codec injection không phải bằng chứng native unsupported tool.

Ca timeout supplemental đầu dừng ở normal Read với native timeout2s, chưa tới Write. Runner observation hoàn tất khoảng 0.162s; không đủ evidence giải thích native timeout. Terminal reconciliation (historical evidence path: `../runs/nckh-native-261005-0812-r35-cursor-write-faults-attempt-01/terminal-reconciliation.json`; unavailable in the cleaned checkout) giữ failure, hai Write faults đã quan sát và các ca chưa chạy. Lượt tiếp theo dùng exact tool matchers: Read20s, Write2s, sleeper8s; ba remaining faults tới Write. Bộ lọc này theo [Cursor matcher contract](https://cursor.com/docs/hooks#matcher-configuration). Timeout observer có thể hoàn tất sau host deadline; runner allow receipt không đổi kết quả native tool bị chặn.

## Template timing chưa đạt

[Direct runner attempt](../runs/nckh-native-261005-0818-r35-cursor-template-timing-attempt-01/attempts/template-write-allow.json) gọi packaged runner trực tiếp với **template timeout5s**, không observer hoặc injection. Native host rejected với `Hook script timed out after 5000ms`; marker absent dù deterministic preflight receipt là allow. Controller dừng theo assertion, ba planned cases chưa chạy. Terminal reconciliation (historical evidence path: `../runs/nckh-native-261005-0818-r35-cursor-template-timing-attempt-01/terminal-reconciliation.json`; unavailable in the cleaned checkout) giữ raw summary và failure. Không nâng timeout hoặc gọi route này qualified; nguyên nhân intermittent native timeout còn mở. Tài liệu [Cursor hooks](https://cursor.com/docs/hooks) mô tả timeout theo giây và failClosed; actual receipts xác định kết quả ở version/surface đã thử.

## Cleanup và acceptance

Bốn batches đã gỡ **106 matching config/plugin/payload members** theo hash; historical project members giữ nguyên. Mỗi final process audit có zero matching task processes. Hai protected global config files và hai absent plugin config paths không đổi; global CLI config hash có thay đổi trong native turns và được ghi before/after. Controller không direct-write global config; không suy mọi native state unchanged.

Callbacks vẫn thiếu structured model ID/parameters; backend và billing attestation chưa observed. CLI `beforeSubmitPrompt`/`stop` chưa có callback; other tools, direct Cursor IDE và full four-host event/version/surface task còn pending. Review thực hiện inline. Plan giữ **in-progress, 44/45**, native checkbox unchecked; installed r25 và scientific/stable/install/release gates giữ riêng.
