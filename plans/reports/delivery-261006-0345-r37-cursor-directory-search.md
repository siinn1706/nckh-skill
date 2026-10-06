# Cursor r37 — directory Grep observations

**Trạng thái:** bằng chứng callback/path/policy đã verified; oracle native đầy đủ còn thiếu thông báo từ chối riêng tư. Plan **44/45, P3 active, full native gate unchecked**.

[Frozen brief](../runs/nckh-native-261006-0345-r37-cursor-directory-search-attempt-49/frozen-brief.json) giữ một lượt Cursor CLI2026.09.15-d2fe57e, hai yêu cầu Grep trên hai thư mục chỉ chứa marker giả lập. Existing selectedModel và native startup display xác nhận Grok4.7/500k/xhigh/fast=false/Run Everything; `--model` được bỏ theo tuyến selection đã verified24. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên. Không injection hoặc model retry.

## Callback và policy thật

[Verification](../runs/nckh-native-261006-0345-r37-cursor-directory-search-attempt-49/verified-directory-observations.json) xác nhận **6 callbacks / 6 receipts**, một prompt/Stop và hai distinct nonempty native tool-use IDs:

| Scope thật trong `file_path` | PreToolUse / runner | PostToolUse |
|---|---|---|
| Thư mục public | manual / `tool-route-uncovered`, wire `{}` | Có callback cùng tool ID/session/path; QA pending vì chưa declared artifact |
| Thư mục private | block / `private-holdout-credential-path`, wire permission deny | Không có callback post thành công |

Pattern và hai thư mục đúng frozen request. Grep directory dùng `file_path`; scope không bị thay thành fixture file. Operation map rỗng: protected-path guard kiểm trước operation lookup. Observer forwards genuine bounded native bytes tới unchanged packaged runner. Outer preToolUse20s/failClosed=true, other handlers5s/inner runner5s. Hai fixture giữ bytes đúng trước/sau; final marker quan sát được.

Native terminal hiển thị hai dòng Grep được nhóm và final reply. Frozen config không có postToolUseFailure logger; retained terminal chunks bị truncation và không giữ explicit native denial/result. Vì vậy **private native enforcement chưa qualified trong lượt49**. Giữ oracle partial và nguyên bằng chứng; không nâng thành native permission_denied hoặc successful return từ việc runner trả deny. Glob, root traversal, all-tools, backend parameters và scientific QA còn unqualified.

## Kết thúc

Native `/exit` và monitor exit0. [Cleanup](../runs/nckh-native-261006-0345-r37-cursor-directory-search-attempt-49/cleanup.json) gỡ28 matching config/payload/fixtures, giữ899 historical project members. Protected global configs unchanged; CLI-owned state hash thay đổi, không suy fields. [Final audit](../runs/nckh-native-261006-0345-r37-cursor-directory-search-attempt-49/process-final-audit.json) union2468 PID/creation identities/zero matching hoặc tracked-live; no process stop. Terminal78710 và monitor40483 đã kết thúc, không poll/restart. Verification đạt lần chạy đầu; review inline, unchanged local r37 checks được tái dùng.

## Correction của current scope

Current plan overview47–48 giữ một dòng “private Write still unqualified” kế thừa từ hồ sơ cũ. [Write25](./delivery-261005-2055-r37-cursor-selected-write.md) và [bindings25](./delivery-261005-2055-r37-cursor-selected-write.json) đã verified public exact bytes và actual private Write permission_denied, unchanged private bytes/zero successful post. [Write faults27](./delivery-261005-2125-r37-cursor-write-faults.md) đã verified năm faults. Current overview được sửa theo evidence này; các báo cáo private-create18 và search24 vẫn giữ trạng thái historical đúng thời điểm và nguyên oracle. Không rerun hoặc regrade các ca cũ.

Phần còn lại gồm diagnostic native directory-denial witness, glob/root scope, Cursor plugin prompt/stop gaps, AGY search/multi-replace, Codex plugin cache authority, Claude model/effort và IDE/Desktop qualification. Exact r29 VI/EN acceptance và installed/publication boundaries giữ riêng.
