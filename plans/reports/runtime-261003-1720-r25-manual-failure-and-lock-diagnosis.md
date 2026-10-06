# r25: lỗi cài thủ công và quan sát Cursor đang dùng file

Ngày: 03/10/2026 · Asia/Saigon · Project: `C:/Users/USER/Downloads/test-skill`.

## Lượt cài người dùng chạy

Người dùng đã chạy [script cài r25](../evaluation/personal-use/complete-r25-install.ps1) trong PowerShell của mình. [Receipt](../evaluation/personal-use/install-r25-manual-20261003-100901-2601237/receipt.json) ghi stage `update`, status `failed`, từ 17:09:01 đến 17:09:34. Preview (historical evidence path: `../evaluation/personal-use/install-r25-manual-20261003-100901-2601237/preview/stdout.json`; unavailable in the cleaned checkout) vẫn đúng một replacement `nckh-visuals`, 42 unchanged và zero conflicts.

[Command receipt](../evaluation/personal-use/install-r25-manual-20261003-100901-2601237/update/command-receipt.json) ghi installer exit 4. Stderr thật (historical evidence path: `../evaluation/personal-use/install-r25-manual-20261003-100901-2601237/update/stderr.txt`; unavailable in the cleaned checkout) chứa WinError 5 khi đổi tên `.agents/skills/nckh-visuals` sang `.nckh-state/transactions/e0b28729028a4ff19848292e73f10feb/backup-34`; stdout rỗng. Đây là resource denial của Windows, không phải automatic approval review rejection.

Thông báo `Installer returned unparsed output` là lỗi trình bày phụ: stderr gồm JSON preflight và JSON error nối tiếp, trong khi wrapper cũ yêu cầu đúng một JSON document. Đã sửa [wrapper](../evaluation/personal-use/install-candidate.py) để đọc chuỗi JSON, lấy status cuối và hiện error. Kiểm bằng đúng preview/stderr lưu của lượt thất bại: status `preview` và `blocked`, giữ WinError 5; không chạy lại installer để kiểm parser. Wrapper SHA-256: `b67635c433030dd713eebe597dd5d4c0e2e45a27d18b54f77754d501de372e34`.

## Integrity sau rollback

[Kiểm tra controller](../evaluation/personal-use/install-r25-manual-20261003-100901-2601237/controller-postfailure.json) đạt lúc 17:18:35:

- Journal đúng transaction `e0b28729028a4ff19848292e73f10feb`, `rolled-back`, recovery conflicts rỗng.
- Ownership bằng `journal.index_before`; 43 owned items.
- Installed `nckh-visuals` đúng before hash `926c745ec2c504abf67aeccd9b0591bf82f57422f90fbd47f6c24b4e59b0b43f`.
- Stage đúng after hash `fe0403204d22a2aa5e5b1dc587bd959cbb340d7784109e359c8de3eccc5116e0`; backup chưa tạo.
- Doctor mới (historical evidence path: `../evaluation/personal-use/install-r25-manual-20261003-100901-2601237/controller-doctor.stdout.json`; unavailable in the cleaned checkout) exit 0, 43 current.

Project vẫn cài r24. Kết quả này chỉ chứng minh integrity sau rollback; không chứng minh cài r25.

## Chẩn đoán resource đang mở

Đã tạo [helper Windows](../evaluation/personal-use/diagnose-r25-install.py), giới hạn exact project/target. Nó mở rồi đóng handles và dùng Restart Manager Start/Register/GetList/End; không rename/delete, thay ACL, enable privileges, shutdown hoặc dừng ứng dụng. Restart Manager tạo metadata phiên tạm của hệ điều hành.

Run sandbox đầu không thể Start session: error 29; không coi empty process list là không có khóa. [Run controller với escalation](../evaluation/personal-use/diagnose-r25-20261003-102033-b6d28ded.json) hoàn tất lúc 17:20:33:

- Mở `FILE_READ_ATTRIBUTES` và `DELETE` handle đều thành công, không thực hiện delete.
- Đăng ký 21 regular files; Start/Register/GetList/End đều exit 0.
- Windows trả về Cursor PID **31492**, start time UTC `2026-10-02T17:51:28.423751+00:00`, đang dùng các file đã đăng ký.

Đây là bằng chứng ứng dụng đang dùng file, chưa chứng minh duy nhất nguyên nhân rename bị từ chối. Restart Manager không bao phủ mọi directory handle hoặc filesystem filter; successful DELETE open không chứng minh toàn bộ rename/destination permissions. Không suy user token từ context do caller khai báo.

Đã yêu cầu người dùng lưu và thoát hẳn Cursor, giữ PowerShell rồi báo đã đóng. Controller sẽ reobserve trước khi retry transaction. Không yêu cầu đổi model, thay ACL hay cài đè. Nếu vẫn thất bại sau khi resource holder đã thoát, giữ failure mới và tiếp tục chẩn đoán.

## Bộ kiểm SVG đã sửa

Đã sửa [checker](../evaluation/personal-use/check-worldbank-svg.py) và thêm [kiểm tra hồi quy giới hạn](../evaluation/personal-use/test-worldbank-svg-check.py): dữ liệu endpoint sai không còn gây chia cho zero trước receipt; parse toàn bộ points grammar; so circles/polyline trong cùng affine coordinate frame. Common translation/rotation/skew/scale được hỗ trợ. CSS transform, origin/box, nested viewports và coordinate animations chưa hỗ trợ trả `unverified-for-stated-checks`, exit 2.

Delegate thực thi báo run cuối **12 tests pass, 0.329 giây, exit 0**; controller đã đọc source/test và đối chiếu đúng hai hashes. Checker `928ea920eb3a91f8edc7edeadf108d3ebfb4c86e88b2afadfdc25b2429fa83bd`; tests `b784dde1c55bef07e27446adcce60600546c2f05cea075d126a5d3108d239aab`. Independent review turn bị lỗi provider 503, nên không ghi independent source review hoàn tất cho patch này. Các diagnostic SVG sử dụng giá trị nguồn thật để kiểm code, không phải native output hoặc visual acceptance.

First test attempt lỗi quyền Windows TEMP trước khi thực thi checker. Successful-run fixtures đã cleanup; controller sau đó kiểm exact paths/creation time/no reparse/empty contents và xóa đúng 15 thư mục rỗng do failed attempt tạo, zero remaining. Không thay ACL. Candidate r25 source/bundles và native originals không đổi; không lặp full suite/build đã đạt.

## Còn lại

1. Reobserve sau khi người dùng thoát Cursor; hoàn tất cài r25 và installed binding checks theo receipts mới.
2. Nhận Antigravity repair 02; review delta chú giải VI/self-count EN.
3. Sau installed checks đạt, người dùng gửi hai World Bank prompts; kiểm actual SVG/source/axes/caption/render/native edit-save-reopen/accessibility.
4. Reconcile plan/checklist/index; owner tự chấm sau dùng.

Plan **in-progress, 25/26**; goal active. Cursor chỉ Grok 4.7 Extra High, Antigravity Gemini 3.8 Flash High, current app chỉ GPT-6.1 Sol. Không fallback. Chưa có repair 02 hoặc World Bank final SVG.
