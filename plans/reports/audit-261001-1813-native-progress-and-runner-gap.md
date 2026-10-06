# NCKH: discovery, cài lại và phần runner còn thiếu

## Kết quả quan sát

Catalog native của phiên Codex hiện tại liệt kê đủ 37 identity `nckh-*`, tất cả trỏ về `.agents/skills` trong project. Observation record (historical evidence path: `../../nckh-kit/evals/results/codex-catalog-observation.json`; unavailable in the cleaned checkout) ghi nguồn bằng chứng là catalog do runtime cung cấp, phương pháp controller đối chiếu IDs và hash file đã cài. Đây là discovery trong phiên này; chưa chứng minh invocation hoặc kết quả hành vi.

Cài lại đúng giao dịch đã được người dùng duyệt qua `installer/install.ps1` trả exit 0 và **0 thay đổi**. Repeat observation (historical evidence path: `../../nckh-kit/evals/results/codex-repeat-observation.json`; unavailable in the cleaned checkout) đối chiếu 43 tree hashes, ownership bytes và model-policy hash trước/sau: đều giữ nguyên. Windows `10.0.26200.0`, PowerShell `7.6.6`; host app version vẫn unverified. Ba lock records đều released. Ownership và journal trước lần chạy được giữ tại `.nckh-state/history/project-copy-before-repeat`.

Đây là bằng chứng scoped cho đường cài Windows project-copy và `owned-install-noop`. Các cell OS/surface khác, update, interruption, rollback, uninstall, global scope, symlink và effective model vẫn chưa nghiệm thu. Candidate ban đầu và receipts của revision 14 được giữ nguyên.

## Đối chiếu P7 với source

| Yêu cầu | Source/bằng chứng hiện có | Trạng thái |
|---|---|---|
| Catalog 37 skills và positive/negative/outcome/failure cases | Catalog + 148 case definitions, deterministic receipt | Có definitions và local guards; agent outcomes chưa chạy. |
| Reproducible closure cho bốn host | Hai build mỗi host + checksums, source revision 14 | Đã có bằng chứng local; chưa là native qualification. |
| Native discovery | Catalog của phiên Codex này có đủ 37 IDs | Quan sát một surface/session; seven other surfaces vẫn pending. |
| Idempotent project-copy install | First install 43 changes; PowerShell repeat 0; actual hashes giữ nguyên | Quan sát một Windows/project/copy scope. |
| Authorized deterministic/agent runner adapters | `evals/run-evals.py` chỉ có `--validate-only`, `--run-deterministic`; `core/evaluation.py` chỉ validate cases/rounds | **Phần agent runner trong File ownership P7 chưa được triển khai.** |
| Human/native/provider qualification | Protocol còn pending rights/reviewers/thresholds; paid budget not-authorized | Chưa có quyền và đầu vào để chạy tương ứng. |

Review này dùng `ak-code-review`, tập trung spec compliance; không phải independent model review hoặc human gold. Không thể coi phần local implementation đã hết việc khi agent runner còn thiếu. Việc này nằm trong scope P7 đã duyệt và cần triển khai trước khi trình một lượt provider evaluation để xin quyền.

## Interface evidence và bước triển khai tiếp theo

Live `codex exec --help` xác nhận stdin prompt, JSONL events, read-only/workspace-write sandbox, ephemeral run và explicit working root. Chỉ chạy help; chưa gọi model/provider. Help trả exit 0 kèm warning không ghi/cleanup được arg0/PATH helper trong Codex home được sandbox bảo vệ; không tự sửa hoặc xóa các thư mục đó.

Tiếp tục triển khai adapter opt-in theo interface quan sát được, preflight/preview và receipts thực, giữ native/provider execution mặc định tắt. Kiểm tra paths/source/input rights/freeze/grant trước dispatch; trace thô vào private store, không tự chấm human/scientific quality, không nâng timeout/failure thành pass. Other-host interfaces giữ unsupported/unverified cho tới khi có binding thực; không xóa scope bốn host/tám surfaces. Sau source change cần freeze lại, chạy affected checks và build candidate mới; không tự update bản revision 14 đã cài.

## Gate còn mở

Giữ plan in-progress, 28/36 tasks, zero fully accepted phases. Có việc implementation P7 còn làm được; chưa ở trạng thái impasse và không đánh dấu goal complete/blocked. Corpus VI/EN, người review, protected holdout, native lab/grants, provider budget, redistribution và publication authority vẫn pending.
