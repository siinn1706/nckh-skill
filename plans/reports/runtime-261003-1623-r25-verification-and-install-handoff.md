# r25: kiểm tra đạt, cài đặt đang chờ

Ngày: 2026-10-03 · Asia/Saigon · Project: `C:/Users/USER/Downloads/test-skill`.

## Kết quả

Candidate r25 đã đạt kiểm tra kỹ thuật; project vẫn cài r24. Lượt update r25 thất bại khi Windows từ chối rename thư mục `nckh-visuals` vào backup. Giao dịch đã rollback, ownership và nội dung r24 còn nguyên vẹn. Chưa có final World Bank SVG/QA.

Người dùng xác nhận các IDE vừa xong **vòng sửa 01**. Cursor Django/UCI đã đạt [review](review-261003-1448-cursor-r24-repair-01.md); Antigravity còn sửa trạng thái chứng cứ của chú giải VI và nhãn self-count EN theo [review](review-261003-1448-agy-r24-repair-01.md). Người dùng báo Antigravity chạy trong PowerShell với quyền `dangerous`; đây là thông tin route do người dùng cung cấp, không phải quan sát effective model/effort mới. Controller không gửi input UI.

## Kiểm tra candidate thực tế

| Gate | Kết quả |
|---|---|
| Full suite | 136 tests: 135 passed, một symlink fixture skip do WinError 1314, zero failures/errors; 1698.762 giây. |
| Lifecycle | Mười command attempts đều exit 0, không timeout, owned-process-group-closed. Driver PID 51816 đã kết thúc exit 0 sau 3072.828 giây. |
| Build | Bốn host có 37 skills; on có 514 files/host, off có 463 files/host. Reproducibility và build closures khớp từng mode/host. |
| Extracted reads | Bốn host đều pass: 21 observations, 13 consumer identities và chín resources mỗi host; isolated Python, CWD ngoài source và unset PYTHONPATH. |
| Receipt integrity | Independent read-only audit đối chiếu 20 command logs, hai driver logs, archive và candidate receipt; hashes khớp. |

[Summary](../evaluation/personal-use/candidate-r25-attempt-02/summary.json) · [Full suite](../evaluation/personal-use/candidate-r25-attempt-02/full-suite.json) · [Attempts](../evaluation/personal-use/candidate-r25-attempt-02/attempts.json) · [Candidate evidence](../evaluation/personal-use/candidate-r25-attempt-02/candidate-evidence.json).

- Source lock: `adc6422394da5a833e1059d922b27c5658eb6699b2ab950568a557d48d71968c`, revision 25, 243 pinned files.
- [Archive](../evaluation/personal-use/candidate-r25-attempt-02/nckh-personal-use-r25.zip): 5,936,339 bytes; SHA-256 `0f6a43f73c08dd8718778092db0ab132285d047f55be7987ec42053db461ecf8`.
- Candidate receipt SHA-256: `7412566bd53220e9770e9532d8ef6f59005e27d8cc7429cab630fcbf21621798`.

Attempt 01 timeout/TEMP failure vẫn giữ nguyên. Attempt 02 dùng effective temp hệ thống bên ngoài project và chạy full unittest trực tiếp, không chịu timeout tổng 900 giây của runner cũ. Technical checks không tạo native, human, scientific hoặc stable acceptance.

## Preview, failure và rollback

Preview (historical evidence path: `../evaluation/personal-use/install-r25-preview-01/stdout.json`; unavailable in the cleaned checkout) ghi một replacement `nckh-visuals`, 42 unchanged, zero conflicts; installation ID `d5811d724fe29cb5016c7c3a` giữ nguyên. Update (historical evidence path: `../evaluation/personal-use/install-r25-commit-01/stdout.json`; unavailable in the cleaned checkout) exit 4 với WinError 5 tại rename sang `backup-34`. Scoped escalation được tool chấp nhận và lệnh đã chạy; đây không phải rejection của automatic approval review.

Journal thật ở `.nckh-state/journal.json`, transaction `34b8711868b94f28bc45f9695d071238`, status `rolled-back`, recovery conflicts rỗng. Independent source/physical audit xác nhận:

- Installed tree hash đúng before hash `926c745ec2c504abf67aeccd9b0591bf82f57422f90fbd47f6c24b4e59b0b43f`.
- Stage còn đúng planned after hash `fe0403204d22a2aa5e5b1dc587bd959cbb340d7784109e359c8de3eccc5116e0`; backup chưa được tạo.
- Ownership object bằng journal index trước giao dịch, cùng canonical digest `8ae9f3a810a3814c2d1ef6a064357938ba95f0f2b5061dbbe6cb39a6b69f1712`.
- Doctor sau rollback (historical evidence path: `../evaluation/personal-use/install-r25-rollback-doctor-01/stdout.json`; unavailable in the cleaned checkout) exit 0, đủ 43 items current. [Process receipt](../evaluation/personal-use/install-r25-rollback-doctor-01/process-receipt.json) ghi PID 55252, 33.984 giây và cleanup hoàn tất.

[Read-only ACL observation](../evaluation/personal-use/install-r25-denial-observation-01.json) ghi bốn Deny entries ở parent `.agents/skills`, zero Deny entries ở target và transaction destination. Đây là bằng chứng về resource denial, chưa loại trừ handle hoặc filesystem filter cùng tham gia. Không thay ACL, cài đè tại chỗ hoặc dừng tiến trình AGY/PowerShell của người dùng. Reconciliation cuối không còn các PID controller 51816, 48416, 28544, 51908, 55252 hoặc native VI 51372; các PID thất bại cũ cũng vắng. Tiến trình AGY/PowerShell do người dùng chạy được giữ.

## Handoff đã chuẩn bị

[Script PowerShell](../evaluation/personal-use/complete-r25-install.ps1) là route bàn giao cho người dùng chạy trong PowerShell của mình. Script tạo receipt directory mới, yêu cầu fresh preview khớp đúng một replacement đã review, dùng nguyên installer transaction, kiểm doctor 43 current, post-preview 43 unchanged và ba installed binding checks. Parser syntax và independent source review đã đạt; reviewer không thấy lỗi pipeline, CWD hoặc status trong scope này. Script SHA-256 `54ad84527f2167927c5a69d8e1ae2b31d72276896b5b1f6f0bf3f5a1d9a60869`. Script chưa được chạy và chưa tạo installation success receipt.

Sau khi installation và installed checker đạt, dùng prompt World Bank Cursor (historical evidence path: `../evaluation/personal-use/native/cursor-grok-r25-visual-01-prompt.txt`; unavailable in the cleaned checkout) và prompt World Bank Antigravity (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r25-visual-01-prompt.txt`; unavailable in the cleaned checkout). Antigravity repair 02 (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r24-repair-02-prompt.txt`; unavailable in the cleaned checkout) có thể chạy độc lập để sửa hai phần còn lại của vòng 01.

Controller runner chỉ cho phép GPT-6.1 Sol. Prompt World Bank bổ sung 26 circle marks với data-year/data-value, matching polyline, source-to-mark table, bounds/formulas và exact blank-unit caveat; syntax đã kiểm. Chưa dispatch case SVG này vì project vẫn cài r24.

## Việc còn lại

1. Chạy script cài r25 từ PowerShell của người dùng; đọc actual update/doctor/post-preview/binding receipts. Nếu Windows vẫn từ chối, giữ failure và xác định resource denial trước retry.
2. Nhận Antigravity repair 02 và review delta VI/self-count EN, giữ source facts và kết luận EN đã đạt.
3. Nhận World Bank SVGs đúng model, kiểm 26 source marks/axes/metadata, render thật, native edit/save/reopen và final hash-bound QA.
4. Reconcile plan/checklist/index/journal theo receipts thật; user tự chấm sau personal use.

Plan giữ **in-progress, 25/26**. Cursor chỉ Grok 4.7 Extra High; Antigravity Gemini 3.8 Flash High; current app chỉ GPT-6.1 Sol. Tám current-app models khác vẫn excluded theo người dùng; không fallback hoặc batch authorization pending. Effective model/effort và fresh UI observations vẫn unknown. Các plan portable/resource-quality có stable/scientific/release scope riêng.
