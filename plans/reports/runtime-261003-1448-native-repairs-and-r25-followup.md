# Runtime follow-up: native repairs và candidate r25

Ngày: 2026-10-03, Asia/Saigon. Snapshot lúc 15:26. Project: `C:/Users/USER/Downloads/test-skill`. Phạm vi báo cáo là task current-app đã review và các gate còn lại; không phải owner acceptance.

## Task current-app đã hoàn tất trong scope được phép

Người dùng chỉ cho phép **GPT-6.1 Sol** ở current-app. [Model matrix](../evaluation/personal-use/native-model-matrix.json) ghi `artifact-checks-passed-for-VI-case`, artifact thật và no fallback. Tám model khác giữ `excluded-by-user-current-scope`; failure startup cũ không được đổi thành kết luận unavailable và không dispatch lại.

[Attempt 03 receipt](../evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-03/gpt-6.1-sol/real-source-vi-prose-taste-01/receipt.json) ghi exit 0, PID 51372, 274.813 giây và owned-process-group-closed. [Review VI delta](review-261003-1448-gpt-6-1-sol-r24-repair-01.md) xác nhận quote `mại bản` giữ chữ thường, actual controller path đúng, cả ba neo nguồn và các trích dẫn phụ khớp; reader trace dòng 14 hoàn tất exit 0. Mandatory instruction-authority read ở trace dòng 8 được ghi riêng và reconcile theo host hierarchy. Artifact SHA-256 là `5022f64430f66c039ad4f51a039a16d417fc3a1c0a3a4c1ce3378c0c895ac9de`.

Task catalogue/bounded real-source current-app được đánh dấu hoàn tất trong [phase runtime](../261003-0101-nckh-personal-use-sources-and-standards/phase-04-runtime.md). Tổng checkbox sau cập nhật là **25/26**; task IDE repairs/SVG/QA vẫn mở. Controller cập nhật plan index/checklist riêng; báo cáo này không đổi frontmatter hoặc status cell.

Requested/configured model và effort được giữ riêng với effective telemetry null. Current-app evidence là native executable dispatch, chưa có fresh main-window UI evidence. Theo controller, readonly capture sau manual IDE repairs không thành công vì foreground window không báo PID; report không biến requested/last-observed labels thành quan sát UI mới.

## Repair artifacts của hai IDE

Người dùng tự gửi repair prompts trong các ứng dụng. [Cursor repair review](review-261003-1448-cursor-r24-repair-01.md) đóng hai lỗi artifact: Django nêu đúng assertion `self.assertGreater(index_tx_end, index_drop_table)` và bỏ message-only repair; UCI có bảng `no=10`, `yes=0`, denominator 10, giữ dữ liệu/giới hạn. Hai receipt trùng bytes với bản trước nên content/lineage pass không tự chứng minh reader execution mới.

[Antigravity repair review](review-261003-1448-agy-r24-repair-01.md) xác nhận EN claim, Django finding và UCI interpretation đã sửa. VI còn chú giải chưa phân biệt nghĩa đã xác minh với diễn giải theo ngữ cảnh; EN còn nhãn self-count thiếu phương pháp, dù kết luận có 161 whitespace-separated tokens và đáp ứng độ dài. Prompt repair 02 (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r24-repair-02-prompt.txt`; unavailable in the cleaned checkout) chỉ sửa hai điểm này, giữ nguyên kết luận EN và nguồn. Output/review repair 02 vẫn pending ở snapshot này.

Cursor chỉ Grok 4.7 Extra High, Antigravity Gemini 3.8 Flash High, current-app chỉ GPT-6.1 Sol; không fallback. Original outputs/receipts và các đánh giá trước được giữ. Các reviews trên không xác nhận effective model, toàn bộ hành vi 37 skills hoặc owner taste score.

## r25 đã freeze, verification còn đang chạy

Source r25 đã freeze **243 files**, source-lock hash `adc6422394da5a833e1059d922b27c5658eb6699b2ab950568a557d48d71968c`. Installed project vẫn **r24**. [Source binding review](review-261003-1448-visual-task-binding.md) không có implementation finding chặn route trong scope được giao, có focused source/extracted checks và correction docs đã kiểm lại; đó chưa phải fresh r25 build/install acceptance.

[Lần verification đầu](../evaluation/personal-use/candidate-r25-attempt-01/full-suite.json) giữ `timeout-unknown` sau deadline 900 giây của wrapper cũ, kèm errors/failures và thông báo raw traces phải nằm ngoài source/distribution/agent workspace. [Failure record](../evaluation/personal-use/candidate-r25-attempt-01/failure.json), [attempt commands](../evaluation/personal-use/candidate-r25-attempt-01/attempts.json) và [driver receipt](../evaluation/personal-use/candidate-r25-driver-01/receipt.json) được giữ; driver exit 3, cleanup owned-process-group-closed. Không ghi test pass từ lần này.

Theo chẩn đoán/observation controller, TEMP bên trong project đã chạm raw-trace boundary và static fixture checks. Controller xác minh owned PIDs đã vắng mặt, kiểm containment rồi chỉ xóa disposable TEMP; failure receipts/stdout/stderr được giữ. Một representative test với default external TEMP đạt trong 1.809 giây. Kết quả hẹp này hỗ trợ sửa harness/environment; chưa xác lập source defect hoặc full-suite pass.

[Driver hiện tại](../evaluation/personal-use/candidate-r25-driver-02/receipt.json) ghi PID 51816. [Attempts hiện tại](../evaluation/personal-use/candidate-r25-attempt-02/attempts.json) ghi structure-validation exit 0 và full unittest discovery `-v` đang chạy từ **15:23:35**, PID 48416, timeout null, cleanup pending. Stream stderr (historical evidence path: `../evaluation/personal-use/candidate-r25-attempt-02/full-suite.stderr.txt`; unavailable in the cleaned checkout) có tiến độ thật. Harness ở plans gọi owned process với no deadline; không đổi frozen nckh-kit source. [Structure receipt](../evaluation/personal-use/candidate-r25-attempt-02/structure-validation.json) pass chỉ là static structure evidence.

Snapshot này chưa có completed full-suite verdict, r25 on/off build/extracted verification, owned preview/update hoặc post-install doctor. Các gate đó vẫn pending; không suy pass từ partial progress hoặc source review. Controller tiếp tục theo dõi owned processes và giữ kết quả/failure theo attempt thực.

## Visual capability và bước còn lại

[Controller native probe](../evaluation/personal-use/visual-engine-probe-01/native-observation.json) đã quan sát editable SVG text/path trong Illustrator, edit/save/reopen/restore và previews; actual renderer probe có receipts tại [probe 02](../evaluation/personal-use/visual-engine-probe-02/render.json). Task binding integrity và extracted checker đã được kiểm trong source review. Đây là probe evidence; chưa phải final World Bank SVG hoặc QA.

Sau khi r25 verification/build/owned install có evidence hoàn tất, IDE phải thực sự đọc explicit task binding và tạo artifact World Bank. Final source-to-mark truth, editable objects, open/edit/save/reopen/render, accessibility và hash-bound QA vẫn cần observations của chính artifact cuối. Antigravity repair 02 cần output và delta review. Task IDE/SVG chỉ được đóng khi các deliverables đó đạt; owner tự chấm sau personal use, trạng thái hiện tại `pending-personal-review`.

Status: DONE

Summary: Task current-app được đóng đúng scope GPT-6.1 Sol sau attempt 03 artifact review; phase ghi 25/26. Báo cáo giữ Cursor repairs pass, Antigravity repair 02 pending, first r25 failure và verification mới đang chạy.

Concerns/Blockers: r25 build/install và final World Bank SVG/QA chưa hoàn tất. Effective telemetry, fresh UI observation và owner acceptance vẫn chưa được xác nhận.
