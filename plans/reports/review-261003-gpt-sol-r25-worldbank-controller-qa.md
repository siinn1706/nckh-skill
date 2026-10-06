# Review độc lập — controller QA World Bank r25

## Kết luận

PASS cho integrity và các bước QA native được ghi nhận; không có finding chặn bàn giao trong phạm vi kiểm tra. Đã đọc biên nhận công cụ thực tế và xem cả hai PNG hiện có bằng view_image; không vận hành Illustrator, chạy lại render/model/provider hoặc thay đổi artifact. Báo cáo này không chấp nhận thay owner.

## Hash cố định

- controller-qa.json: `cb1b454d25c44fe981ddf39f8bc5b871647d9ea46d9abefbab39af8b236b5ae7`.
- native-qa-copy.ai: `7a33d6b055fd447dc03669d00843154f3626d4b91ee75dbee926b95de1a6f0b7`.
- illustrator-tool-evidence.json: `ad86a536041b52c530ae38ffdbd494b9213d6267273ab973c6252d5d2823dd38`.
- SVG nguyên bản: `a85e1a4aaa336d20e7d3096362dd019041e7d73e44f887f972fa58773cdafb3e`.
- PNG rsvg: `ff6b8f76d4d03c7f5dfe63131c72ef43a5d98c64edd18ebba67aeebda0a73be9`.
- PNG Illustrator: `5d16da6909d333a11c1c96100a684a366c5ac11b338b3081b29be61d25ed830f`.
- Source review: `6960f0e47bfe80eaefd617d65530b9a5c4ad0e61aca211e372de8838e20024e4`; khớp báo cáo audit trước.

## Các điều kiện

| Điều kiện | Kết quả |
|---|---|
| controller_receipt_hash | PASS |
| ai_hash | PASS |
| bound_file_hashes_and_bytes | PASS |
| source_review_hash | PASS |
| edit_guard | PASS |
| point_edit_guard | PASS |
| edited_save_guard | PASS |
| close_guard | PASS |
| restore_title_guard | PASS |
| restore_point_guard | PASS |
| restore_save_guard | PASS |
| restored_close_guard | PASS |
| export_guard | PASS |
| success_mutations_save_close_reopen | PASS |
| edited_title_retained | PASS |
| edited_point_retained | PASS |
| restored_29_exact_strings | PASS |
| restored_26_marks | PASS |
| no_rasters | PASS |
| all_29_frames_inside_artboard | PASS |
| both_png_dimensions | PASS |
| contrast_recomputed | PASS |

## Chuỗi bằng chứng native

illustrator-tool-evidence.json chứa kết quả tuần tự từ controller. open/info xác nhận SVG 1400×1100. save_guard xác nhận đúng SVG trước save_as sang native-qa-copy.ai (overwritten=false). Mọi edit/save/close/restore/export guard sau đó chỉ đúng bản AI trong case. title_edit xác nhận thêm “ · kiểm tra sửa”; point_edit di chuyển bounds x từ195 sang196. edited_save success; edited_close success không discard changes; edited_reopen success đúng đường dẫn AI. Các truy vấn sau reopen xác nhận cả text đã sửa và point x196 còn nguyên.

Sau đó title_restore/point_restore đưa tiêu đề về nguyên bản và bounds x195. restored_save/close/reopen đều success. Close saved=false không phải lỗi: tài liệu đã được save ở bước trước và discardedChanges=false. restored_frames có đúng29 nội dung text, so sánh multiset khớp SVG từng chuỗi; restored_structure có26 point paths và không có raster/image. Sai khác tâm mark tối đa 2.2937484004614817e-05 đơn vị SVG, khớp receipt và sai số lưu/import native; không có mất điểm hay thay giá trị nguồn. title_detail sau restore xác nhận Arial Bold 32pt. Tất cả29 text bounds nằm trong artboard. export_guard vẫn đúng bản AI đã restore; export success PNG72dpi scale1.

## Quan sát ảnh độc lập

Đã xem đầy đủ artifact-rsvg.png và artifact-illustrator.png, cả hai1400×1100. Không thấy clipping, text overlap ngoài ý định, mất dấu tiếng Việt hoặc mất điểm. Tiêu đề/nhãn/trục/chú thích và caveat đều hiện đủ. Khác biệt rasterization/font metrics nhỏ giữa hai engine được thấy nhưng không làm sai source-to-mark hoặc thiếu nội dung. Caption pending là trạng thái lúc model tạo raw; controller-qa.json tách biệt ghi QA thực hiện sau, không sửa lịch sử.

## Phạm vi còn giới hạn

- Effective provider model và effort vẫn null/unknown; dispatch yêu cầu không thành telemetry thực tế.
- Accessibility được xác nhận ở cấu trúc SVG và các tỷ lệ contrast đã tính lại; không có assistive-technology user testing.
- AI là bản derivative đã chứng minh chỉnh sửa/lưu/mở lại; metadata title/desc/ARIA nguồn SVG có còn trong AI hay không chưa được đảm bảo.
- Family/style Arial native được quan sát. Receipt ghi version/font files nhưng audit này không đọc lại file font hoặc executable ngoài project; rsvg font-file resolution không được exposed.
- Các kết quả công cụ có sequence, không có timestamp mỗi call hoặc bản command-input đầy đủ. Guard results và nội dung query sau reopen hỗ trợ kết luận được giao; không biến receipt integrity thành chứng nhận mọi hành vi ngoài trace.
- Owner feedback pending-personal-review. Không có human/scientific/stable certification, publishing clearance hoặc kết luận compatibility mọi host.

## Việc còn lại

Không có blocker trong phạm vi native QA được ghi. Owner review artifact hiện tại và quyết định acceptance; giữ SVG/MD raw, AI derivative cùng biên nhận.
