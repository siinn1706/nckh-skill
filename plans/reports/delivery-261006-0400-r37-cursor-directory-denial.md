# Cursor r37 — native denial cho private-directory Grep

**Trạng thái:** verified cho đúng một thư mục; plan **44/45, P3 active, full native gate unchecked**.

[Frozen brief](../runs/nckh-native-261006-0400-r37-cursor-directory-denial-attempt-50/frozen-brief.json) giữ một lượt **Cursor CLI2026.09.15-d2fe57e / Grok4.7 / 500k / xhigh / fast=false / Run Everything**. Existing selectedModel và native startup display xác nhận lựa chọn; không backend/billing attestation. Một yêu cầu Grep trên thư mục chỉ có marker giả lập, không retry/injection. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi.

## Bằng chứng native

[Verification](../runs/nckh-native-261006-0400-r37-cursor-directory-denial-attempt-50/verified-directory-denial.json) xác nhận **5 callbacks / 4 policy receipts**:

- PreToolUse thật ghi Grep, nonempty tool-use ID và absolute `file_path` trỏ đúng private directory; unchanged packaged runner trả permission deny/`private-holdout-credential-path`.
- Native **postToolUseFailure** ghi **Grep / permission_denied / private-holdout-credential-path**. Tool ID, session, selected directory và version khớp PreToolUse; duration0/is_interruptfalse.
- Không successful PostToolUse callback. Marker giữ nguyên exact bytes trước/sau và final reply quan sát được. Thông báo failure là metadata native thật, không policy receipt được đổi tên thành host response.

Operation map vẫn rỗng: protected path guard chạy trước operation lookup. Outer preToolUse20s/failClosed=true, inner runner5s/other handlers5s; diagnostic failure logger10s/matcher `^Grep$`. Observer forwards genuine payload; diagnostic chỉ ghi bounded metadata/hash/scrubbed error, không gọi policy hoặc đọc transcript.

[Lượt49](./delivery-261006-0345-r37-cursor-directory-search.md) thiếu actual native failure witness. Lượt50 thêm đúng diagnostic đã giao native trong Write25, chọn tool Grep và directory; đây là thay đổi thu evidence có căn cứ. Original frozen oracle49 vẫn partial và không được regrade. Current evidence chỉ qualified **một exact directory trong `file_path`**; glob/root traversal, all-tools/default enforcement và direct producer5s search còn unqualified. Scientific QA giữ gate riêng.

## Kết thúc và phần còn lại

Native `/exit` và monitor exit0. [Cleanup](../runs/nckh-native-261006-0400-r37-cursor-directory-denial-attempt-50/cleanup.json) gỡ27 matching config/payload/fixture members, giữ921 historical project members/protected global configs. CLI-owned state hash thay đổi, không suy fields; controller không direct-write global. [Final audit](../runs/nckh-native-261006-0400-r37-cursor-directory-denial-attempt-50/process-final-audit.json) union2592 PID/creation identities/zero matching hoặc tracked-live/no process stop. Terminal25793 và monitor61453 đã kết thúc, không poll/restart.

Verification đạt lần chạy đầu; review inline. Raw terminal chunks truncated, native tool-return content không retained; selected native failure metadata được giữ riêng. Unchanged local r37 tests/build được tái sử dụng, không gọi thành native proof.

Codex project/plugin cache authority và Claude model/effort vẫn chưa có direct reply. Cursor plugin prompt/stop gaps, remaining event/tool/fault cells, AGY search/multi-replace, unknown-host-event và IDE/Desktop qualification còn mở. Exact r29 VI/EN owner acceptance và installed/publication boundaries giữ nguyên.
