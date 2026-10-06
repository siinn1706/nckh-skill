# Kiểm tra nhanh callback native r38 advisory

Status: DONE_WITH_CONCERNS

## Phạm vi và revision

Một lượt model thật, một yêu cầu `apply_patch`, một callback `PreToolUse` trên Codex CLI **0.154.0**, Windows. Requested model **gpt-5.6-luna / medium**; callback xác nhận model, native `config/read` xác nhận medium trước invocation. Backend model attestation và chi phí vẫn chưa quan sát.

Candidate được build riêng từ **source-lock revision 38**, 281 pins, canonical lock hash `5d1170901478171385027f953cfbd4a469e0e77a65d1f22cba7458f13f10a097`. Không reuse `dist/codex` v1 lịch sử thiếu hook closure. Không sửa kit source, installed skills, grants hoặc các báo cáo/gate cũ.

Grant hiện có cho native definitions và GPT5.6Luna/medium được đọc cùng chỉ đạo trực tiếp kiểm tra nhanh của user. `CODEX_HOME`, config tối thiểu, exact hook trust, sqlite/log và payload stage đều nằm trong disposable project dưới owned run root. Native CLI dùng `workspace-write`, approval `never`, ephemeral; không dùng dangerous/bypass flags. Windows process preflight được auto-review cho chạy ngoài sandbox sau CIM access failure; sandbox của native tool vẫn giữ nguyên.

## Quan sát thật

| Oracle | Kết quả |
|---|---|
| Native discovery và exact local hook trust | Một project definition, enabled, trusted; không có definition ngoài scope |
| Genuine callback | `PreToolUse`, `apply_patch`, gpt-5.6-luna; patch SHA khớp đúng yêu cầu |
| r38 advisory runner | Exit **0**, output **`{}`**; không có deny |
| Policy receipt | Giữ **`block` / `plan-only-mutation`**, `hook_mode=advisory` |
| Native turn | CLI exit **0**, `turn.completed`, final `QUICK_NATIVE_FINISHED` |
| Benign marker side effect | **BLOCKED** ở native sandbox; marker không có |

Callback non-denial đã được quan sát với policy vốn trả block. Mutation oracle chưa đạt: stderr native ghi `patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings`, dù invocation yêu cầu workspace-write. Không gọi marker absence là hook denial, không đổi policy receipt thành native prevention PASS, không retry inference.

Native startup cũng ghi plugin featured-cache HTTP 401 và curated-cache path-too-long trong local native home. Các lỗi này được giữ trong raw stderr; không cài package hay chạy helper upstream. Unknown cost vẫn là unknown. Native token usage được giữ trong stdout, không suy ra hóa đơn.

## Preservation và cleanup

- **791 tracked file hashes giữ nguyên** ở pre/post cleanup: 281 pinned source files, source-lock file, 506 installed files, ba global Codex config/hooks/auth files. Hash snapshot này thuộc thời điểm r38 native run; controller đã bắt đầu upgrade source sau cleanup. Nó không chứng nhận inventory/source-lock của revision đang upgrade.
- Matching project hook config, staged runner/dependency payload và private local host config đã gỡ. Private provider values không được ghi trong public receipts; local files có chứa copied private values được hash-bound cleanup.
- Final audit kiểm đúng **27 known PID + creation-time identities**, dùng actual exit state: **0 owned-live**. Hai native metadata appservers đóng stdin và exit 0. Không kill process ngoài ownership; không claim kiểm kê toàn hệ thống.
- Giữ raw stdout/stderr, callback, policy receipt, trust/config metadata đã lọc private fields, snapshots, runtime build và failures trước đó. Native-home config và project hook config đều absent.

Failures giữ nguyên: helper encoding error trước native launch; CIM sandbox access failure trước launch; CLI parser exit 2 do vị trí `--ask-for-approval` trước inference. Corrected sub-attempt có đúng một lượt inference thật. Không fake callback, marker hoặc screenshot.

## Evidence bindings

- [Summary và toàn bộ binding hashes](../runs/nckh-upgrade-native-261006-0850-attempt-01/verification-summary.json)
- [Genuine native callback](../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/project/evidence/native-callback.json)
- Raw native stdout (historical evidence path: `../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/commands/codex-native-advisory.stdout.txt`; unavailable in the cleaned checkout) và stderr (historical evidence path: `../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/commands/codex-native-advisory.stderr.txt`; unavailable in the cleaned checkout)
- [Exact trusted definition](../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/native-trusted-preflight.json) và [sanitized effective model/effort](../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/native-trusted-preflight.effective.json)
- [Cleanup](../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/cleanup.json), [protected postimage](../runs/nckh-upgrade-native-261006-0850-attempt-01/corrected-cli-02/protected-after.json), [final known-process audit](../runs/nckh-upgrade-native-261006-0850-attempt-01/final-process-audit.json)

## Giới hạn quyết định

Callback advisory observation đủ cho controller dùng làm checkpoint kiểm tra nhanh trước upgrade theo chỉ đạo user. **Full quick acceptance về benign tool side effect vẫn blocked**; full native qualification, các surfaces/events khác, legacy 44/45 và task native trong phase 03 đều giữ trạng thái mở. Không commit, publish hoặc sửa acceptance history.
