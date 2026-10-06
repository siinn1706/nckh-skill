# Ba prompt đã có đầu ra và được kiểm tra

Ngày: 03/10/2026 · Múi giờ: Asia/Saigon · Project: `test-skill`.

Đã tìm thấy cả ba đầu ra mới lúc 21:13–21:29. Người dùng báo chạy xong ba prompt bằng các model đã chốt. Controller đã kiểm số liệu, render lại bằng đúng engine khai báo và thử sửa/lưu/mở lại hai SVG trong Illustrator. Phần bàn giao dùng cá nhân đã có đủ artifact và QA trong phạm vi dưới đây; owner tự dùng và chấm sau.

## Kết quả từng prompt

| Prompt | Kết quả kiểm tra |
|---|---|
| Antigravity repair 02 | [Review độc lập](review-261003-2137-agy-repair-02.md) đạt. Chú giải VI ghi đúng giới hạn diễn giải ngữ cảnh và bỏ attribution từ điển không có nguồn. Ba anchors và các quote được giữ. Kết luận EN không đổi, đúng 161 whitespace-separated tokens; đã bỏ con số 178 không có phương pháp. |
| Antigravity World Bank | 26 giá trị/circle/polyline/bảng/tick/formula khớp nguồn. Actual controller render tái tạo đúng PNG đã nộp. Native có 29 khung chữ và 26 điểm path; sửa chữ/điểm, lưu/đóng/mở lại giữ sửa; khôi phục/lưu/đóng/mở lại khớp nguồn. |
| Cursor World Bank | 26 giá trị/circle/polyline/bảng/tick/formula khớp nguồn. Actual controller render tái tạo đúng PNG đã nộp. Native có 166 khung chữ, gồm bảng ánh xạ trên artboard, và 26 điểm path; chuỗi thử sửa/lưu/mở lại/khôi phục đạt. |

[Review nguồn và biên nhận của hai IDE](review-261003-2137-ide-worldbank-source-and-receipts.md) đạt cho số liệu, arithmetic và hash compatibility. Controller nhìn cả ảnh nộp, ảnh render lại và ảnh native: không thấy cắt chữ, chồng chữ ngoài ý định, mất dấu hoặc mất điểm. Các native text bounds nằm trong artboard, native text khớp SVG; không có raster image. Sai lệch tâm điểm do import/save native tối đa 0.00002294 cho AGY và 0.00004883 cho Cursor, nhỏ hơn 0.0001 đơn vị SVG.

## Bằng chứng và file bàn giao

- Antigravity: [SVG gốc](../evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.svg), [AI đã khôi phục](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/native-qa-copy.ai), [QA](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/controller-qa.json).
- Cursor: [SVG gốc](../evaluation/personal-use/native/cursor-grok-r25-visual-01/real-source-worldbank-visual-01.svg), [AI đã khôi phục](../evaluation/personal-use/native/cursor-grok-r25-visual-01/controller-qa-01/native-qa-copy.ai), [QA](../evaluation/personal-use/native/cursor-grok-r25-visual-01/controller-qa-01/controller-qa.json).

AGY QA hash `09d29563af58465582b2f387872361389c057df9d773e44a1d81155261e09c39`; Cursor QA hash `48130dd59282be4ae035bb6c32928a62187707db61268eb058e317b15c59a1b7`. Mỗi receipt gắn original SVG/MD, native AI/PNG, actual render và kết quả Illustrator với hash/byte count. rsvg-convert 2.40.20 đúng executable binding; Illustrator 2024 file version 28.0.0, native font Arial.

[Review native QA độc lập](review-261003-2137-ide-worldbank-controller-qa.md) xác minh các hashes, guards, hai chuỗi edit/reopen/restore và đã nhìn cả bốn PNG cuối. Hai bộ đạt trong phạm vi source/render/native được ghi nhận; không có gate failure mới chặn bàn giao. Báo cáo review hash `16278e5a91c11986e44a8f5ee33f9f34bc6be6cd1fbc772a44b4fdeddeda3ab2`. Các render controller chạy đồng bộ và đã kết thúc; không còn process background do lượt kiểm tra này tạo.

## Sửa nhãn trạng thái và giới hạn provenance

AGY raw memo dòng 331 tự ghi `Source truth pass` trước controller review, trái nhãn pending của prompt. Giữ raw làm lịch sử; [memo đã hiệu chỉnh](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/reviewed-memo.md) ghi pending tại generation và controller pass sau kiểm tra, đồng thời ghi model theo prompt/user report riêng với effective telemetry. [Revision receipt](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/memo-revision.json) gắn hai memo và SVG bằng hash. Không chạy lại model.

AGY SVG/PNG trùng từng byte với bản GPT-6.1 Sol trước đó. Không suy ra independent Gemini generation từ các file đó. Reader receipts của repair 02 cũng có bytes bằng các receipts cũ; input integrity đã kiểm, nhưng không tự xác nhận fresh reader execution. Người dùng báo đã hoàn tất các lượt; selected model giữ Cursor chỉ Grok 4.7 Extra High, AGY Gemini 3.8 Flash High và current app chỉ GPT-6.1 Sol. Effective model/effort chưa có provider telemetry.

Accessibility đã kiểm title/desc tiếng Việt, language, thứ tự điểm và contrast; AGY có role/ARIA liên kết. Cursor có title/desc bản địa. Chưa thử bằng công nghệ hỗ trợ và không khẳng định SVG accessibility metadata được bảo toàn trong AI. Giữ unit nguồn trống, attribution, snapshot và caveat quyền bên thứ ba. Owner feedback vẫn `pending-personal-review`; không cấp human/scientific/stable certification hoặc publishing clearance.

Các giới hạn này giữ riêng với việc bàn giao personal-use. Hai plan portable/resource-quality vẫn có yêu cầu qualification rộng hơn; không tự đóng từ kết quả của ba prompt.

## Đóng mục tiêu dùng cá nhân

Plan personal-use và phase 4 đã chuyển `completed`, đủ 26/26 phase checkboxes. Validation/reindex đạt, checkpoint trước khi thêm biên nhận goal có 139 local links hợp lệ. [Biên nhận native goal](../evaluation/personal-use/personal-use-goal-completion-01.json) xác nhận trạng thái `complete`; phạm vi all-model ban đầu đã được người dùng thu hẹp còn GPT-6.1 Sol cho current-app. Owner tự dùng/chấm sau, hai plan qualification rộng hơn giữ mở.
