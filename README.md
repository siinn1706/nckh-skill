# nckh-skill

Bộ **43 skill NCKH** cho nghiên cứu, viết, kỹ thuật và marketing, kèm sáu vai trò
agent tùy chọn. Hướng dẫn của skill bằng tiếng Anh; đầu ra theo ngôn ngữ được yêu
cầu trong công việc.

| Nhóm | Số skill |
|---|---:|
| Core | 16 |
| Engineer | 13 |
| Marketing | 13 |
| Xia | 1 |

## Phạm vi bản công khai

Source lock và bốn package phân phối cùng dùng **experimental r46**. Chủ sở hữu
đã chấp nhận hợp đồng debug → fix và cho phép đưa bản mới nhất lên GitHub ngày
10/10/2026. Xem [kế hoạch xuất bản và dọn bản cũ](plans/261010-1106-r46-publish-and-cleanup/plan.md)
và [hợp đồng engineer](nckh-kit/docs/engineer.md). Các giới hạn native, scientific,
human và metadata process lịch sử vẫn được giữ; stable qualification tiếp tục
NO-GO. Package được xuất ở chế độ
**`resource-access on`**. Tài nguyên đi kèm luôn được bật trong các package phân
phối: đủ 43 skill, 13 nhóm tài nguyên, reader, giấy phép, ghi công và công cụ cài
đặt. Skill chọn phần tham khảo phù hợp với công việc; người dùng vẫn có thể cung
cấp tài liệu hoặc dữ liệu riêng.

Mỗi package có manifest và source lock để kiểm tra đúng phiên bản và tính toàn
vẹn. Các trường quyền và qualification trong bản ghi gốc được giữ nguyên;
repository này là bản chia sẻ instructions, tài nguyên và công cụ, chưa phải bản
stable đã được kiểm định đầy đủ. Xem [phạm vi và quyền](docs/public-edition.md).

## Cấu trúc

[Chỉ mục workspace](docs/README.md) dẫn tới source, resources tham khảo, kế hoạch
và evidence. Đọc [quy tắc bảo quản repository](docs/repository-maintenance.md)
trước khi dọn file hoặc xuất bản thêm nội dung.

- `packages/claude/`: package cho Claude Code.
- `packages/codex/`: package cho Codex CLI, desktop và IDE.
- `packages/cursor/`: package cho Cursor CLI và IDE.
- `packages/agy/`: package cho Antigravity CLI và IDE.
- `nckh-kit/installer/`: công cụ preview, cài, cập nhật, doctor và gỡ theo ownership.
- `scripts/verify-public-package.py`: kiểm tra package trước khi dùng.

Mỗi package chứa 43 thư mục skill và sáu agent tùy chọn. Các adapter là cấu hình
được đóng gói; việc có package chưa xác nhận mọi phiên bản ứng dụng và hệ điều
hành đã được kiểm tra thực tế.

## Kiểm tra và cài đặt

Đọc instructions trực tiếp không cần Python. Công cụ kiểm tra và cài đặt cần
**Python 3.11 trở lên**, dùng thư viện chuẩn.

Chạy từ thư mục repository:

```text
python scripts/verify-public-package.py
python nckh-kit/installer/nckh-installer.py list-skills
```

Ví dụ preview cài đủ ba nhóm vào một project dùng Codex desktop:

```text
python nckh-kit/installer/nckh-installer.py install --package packages --runtime codex-desktop --scope project --project PATH_TO_PROJECT --kits core engineer marketing --mode copy --models balanced --with-agents --hooks advisory --dry-run
```

Thay `PATH_TO_PROJECT` bằng đường dẫn project thực. Đọc preview, giải quyết các
xung đột nếu có, rồi chạy lại cùng lựa chọn, thay `--dry-run` bằng `--yes` để cài.

| Ứng dụng | Giá trị `--runtime` |
|---|---|
| Claude Code | `claude-code` |
| Codex desktop | `codex-desktop` |
| Codex CLI | `codex-cli` |
| Codex IDE | `codex-ide` |
| Cursor IDE | `cursor-ide` |
| Cursor CLI | `cursor-cli` |
| Antigravity IDE | `agy-ide` |
| Antigravity CLI | `agy-cli` |

Thêm `--with-agents` nếu muốn cài sáu agent tùy chọn. Model mặc định kế thừa cấu
hình của ứng dụng; profile `balanced` tự nó không xác nhận model hay effort thực
sự được áp dụng. Cài đặt không gọi model hoặc tự bật plugin.

Sau khi cài, dùng state directory của project để kiểm tra và preview gỡ:

```text
python nckh-kit/installer/nckh-installer.py doctor --state-dir PATH_TO_PROJECT/.nckh-state
python nckh-kit/installer/nckh-installer.py uninstall --state-dir PATH_TO_PROJECT/.nckh-state --install-id INSTALL_ID --dry-run
```

Lấy `INSTALL_ID` từ biên nhận cài đặt. Update có kiểm tra candidate evidence riêng;
`--yes` không bỏ qua ownership, file đã chỉnh sửa hoặc các điều kiện cập nhật.

### Windows: chạy `install.ps1`

Mở PowerShell trong thư mục repository. Script nằm tại
`nckh-kit/installer/install.ps1`; chạy script cần truyền thao tác, chẳng hạn
`install`, `doctor` hoặc `list-skills`. Chạy riêng `install.ps1` in hướng dẫn và
ba lệnh mẫu rồi thoát với exit code 2. Thao tác `install` mở wizard khi chạy
trong terminal tương tác và chưa truyền đủ lựa chọn.

```powershell
python --version
& .\nckh-kit\installer\install.ps1 --help
& .\nckh-kit\installer\install.ps1 list-skills
```

Ví dụ dưới đây cài đủ ba nhóm và sáu agent vào project dùng Codex desktop.
Thay đường dẫn project và runtime theo bảng phía trên. Project phải tồn tại;
đường dẫn có khoảng trắng được giữ bằng mảng đối số.

```powershell
$nckhProject = 'C:\Projects\My Research'
$nckhArgs = @(
    'install',
    '--runtime', 'codex-desktop', '--scope', 'project',
    '--project', $nckhProject, '--kits', 'core', 'engineer', 'marketing',
    '--mode', 'copy', '--models', 'balanced', '--with-agents', '--hooks', 'advisory'
)
& .\nckh-kit\installer\install.ps1 @nckhArgs --dry-run
# Sau khi đọc preview và xử lý xung đột:
& .\nckh-kit\installer\install.ps1 @nckhArgs --yes
& .\nckh-kit\installer\install.ps1 doctor --state-dir "$nckhProject\.nckh-state"
```

Nếu muốn chọn các tùy chọn qua wizard, chạy trong terminal tương tác với thao
tác `install` và đường dẫn package/project đã có:

```powershell
& .\nckh-kit\installer\install.ps1 install --project $nckhProject
```

Wizard hỏi runtime, kit, scope, mode và model policy rồi hiển thị transaction.
Chọn `cancel` ở bước cuối để dừng trước khi cài.

Engine tự tìm manifest trong `nckh-kit/dist`, rồi `packages` của repository.
Có thể dùng `--package` để chọn tường minh một package khác; lựa chọn này luôn
được ưu tiên và được kiểm tra hash trước khi dùng.

Wrapper thử Python có phiên bản từ 3.11 và executable đọc được để hook tính hash;
alias WindowsApps không đáp ứng điều kiện sẽ được bỏ qua. Interpreter đã chọn
được ghi trên stderr. Có thể đặt `NCKH_PYTHON` thành đường dẫn Python thực.

Để dùng skill global, preview bằng lệnh dưới đây rồi thay `--dry-run` bằng
`--yes` khi preview hợp lệ. Global bắt buộc dùng `--hooks off`.

```powershell
& .\nckh-kit\installer\install.ps1 install --runtime codex-desktop --scope global --kits core engineer marketing --mode copy --models balanced --with-agents --hooks off --dry-run
```

| Lỗi | Cách xử lý |
|---|---|
| Không tìm thấy package/manifest | Thông báo liệt kê các đường dẫn đã thử. Dùng `--package` nếu package nằm ở nơi khác. |
| `Python 3.11+ is required` | Kiểm tra `python --version` hoặc `py --version`; cài Python phù hợp rồi mở lại terminal. Script không tải Python. |
| PowerShell báo script bị chặn | Với bản tải đáng tin cậy, dùng `Unblock-File .\nckh-kit\installer\install.ps1`; nếu chính sách của máy vẫn chặn, dùng lệnh Python phía trên hoặc làm theo quản trị viên. |
| `duplicate visibility` | Preview kiểm tra đích và compatibility/global roots ở ancestor. Cài project còn kiểm project con trong tám cấp, bỏ qua thư mục vendor/build và link; cài global không quét project con dưới home. Dùng ownership/doctor để xác định bản đang dùng. `--yes` không bỏ qua xung đột. |
| File đã chỉnh sửa hoặc đang bị ứng dụng khóa | Giữ biên nhận và nội dung đã sửa; đóng ứng dụng đang giữ file rồi preview lại. Không xóa state để ép cài. |

### Linux/macOS: chạy `install.sh`

Từ thư mục repository, dùng shell wrapper với cùng thao tác và lựa chọn:

```sh
sh nckh-kit/installer/install.sh --help
sh nckh-kit/installer/install.sh install --runtime codex-cli --scope project --project "/path/to/project" --kits core engineer marketing --mode copy --models balanced --with-agents --hooks advisory --dry-run
```

Đọc preview rồi thay `--dry-run` bằng `--yes`. Wrapper cần `python3` hoặc
`python` hoặc fallback `py -3` phiên bản 3.11 trở lên. Kiểm tra trên Windows/Git Bash không thay thế
kiểm thử thực tế trên Linux/macOS.

## Dùng skill

Chọn `nckh-*` phù hợp, nêu đầu ra cần có, cung cấp tài liệu hoặc dữ liệu, ngôn ngữ
và giới hạn công việc. Các package phân phối luôn giữ resource access ở chế độ **on**;
khi gọi reader lookup, truyền `--resource-access on` hoặc dùng mặc định `on`.
Reader đọc nguồn đã đóng gói, kiểm tra hash và trả lại record phù hợp cùng nguồn
và giới hạn sử dụng. Nếu tài nguyên bị thiếu hoặc sai hash, xử lý lỗi đó; không
tự chuyển package sang `off`.

Biểu đồ, sơ đồ và ảnh cần công cụ tạo/render tương ứng của môi trường. Skill
không tự cung cấp dịch vụ tạo ảnh hoặc chứng nhận file chỉnh sửa được.

## Portable hooks

Mỗi package r46 có runner, codec, template và công cụ preview/apply/remove hook
trong `hooks/`. Cài hoặc cập nhật ở scope project mặc định đăng ký hook ở chế độ
**nhắc/kiểm tra (advisory), không chặn thao tác hoặc lệnh shell**. Thêm
`--hooks off` để bỏ qua cấu hình hook. Cài skill global cần `--hooks off` vì hook
có context và ownership riêng theo project. Host vẫn quản lý quyền và trust.
Hai skill viết
mới là `nckh-humanwrite` và `nckh-paperwrite`.
Xem [hướng dẫn hook](docs/portable-hooks.md).


## Source đầy đủ và rebuild

`nckh-kit/` chứa đầy đủ source experimental r46 đã freeze: skills, agents, adapters,
contracts, policies, workflows, profiles, data, hooks, installer, scripts,
test và protocol/case đánh giá. Canonical lock và package cùng là r46; lock r41–r45
được giữ trong history. Bốn package có thêm plugin projection; ứng dụng quản lý
việc đăng ký, enable và trust plugin.

Các lệnh dưới đây rebuild đúng source được canonical lock r46 pin. Thay đổi source
tiếp theo cần được review và freeze riêng trước khi build.

```text
python nckh-kit/scripts/build-artifacts.py --all --plugin --resource-access on --check
python nckh-kit/scripts/build-artifacts.py --all --plugin --resource-access on --output dist
```

Output build phải chưa tồn tại hoặc rỗng. Data nguồn dùng để rebuild nằm trong
`nckh-kit/core/profiles/resources/`, cùng registry, provenance, license và notices.
Bốn skill nghiên cứu mới là `nckh-dataset`, `nckh-statistics`, `nckh-telemetry`
và `nckh-aiops`. Xem [tài liệu kit](nckh-kit/docs/index.md) và
[ghi công data](docs/resource-attribution.md).
