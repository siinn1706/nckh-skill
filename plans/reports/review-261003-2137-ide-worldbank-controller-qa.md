# Final review — controller QA hai World Bank IDE artifacts

## Verdict

PASS cho source/render/native QA trong phạm vi receipt hiện tại. Không có concrete gate failure mới chặn bàn giao hai artifact. DONE_WITH_CONCERNS giữ provenance/model telemetry, quyền/owner/scientific và accessibility runtime giới hạn như đã ghi. Không sửa artifacts hay rerun model/provider/renderer/Illustrator; đã xem cả4 PNG thực tế bằng view_image.

## Kết quả integrity/native

| Host folder | Check | Verdict |
|---|---|---|
| agy-gemini-r25-visual-01 | qa_hash | PASS |
| agy-gemini-r25-visual-01 | all_receipt_bound_hashes | PASS |
| agy-gemini-r25-visual-01 | guarded_mutations_success | PASS |
| agy-gemini-r25-visual-01 | edit_restore_success_claims | PASS |
| agy-gemini-r25-visual-01 | cycle_two_save_close_reopens | PASS |
| agy-gemini-r25-visual-01 | edited_text_retained | PASS |
| agy-gemini-r25-visual-01 | edited_point_retained | PASS |
| agy-gemini-r25-visual-01 | restored_exact_native_texts | PASS |
| agy-gemini-r25-visual-01 | marks26_rasters0 | PASS |
| agy-gemini-r25-visual-01 | coordinate_delta | PASS |
| agy-gemini-r25-visual-01 | frames_inside | PASS |
| agy-gemini-r25-visual-01 | controller_render_source | PASS |
| cursor-grok-r25-visual-01 | qa_hash | PASS |
| cursor-grok-r25-visual-01 | all_receipt_bound_hashes | PASS |
| cursor-grok-r25-visual-01 | guarded_mutations_success | PASS |
| cursor-grok-r25-visual-01 | edit_restore_success_claims | PASS |
| cursor-grok-r25-visual-01 | cycle_two_save_close_reopens | PASS |
| cursor-grok-r25-visual-01 | edited_text_retained | PASS |
| cursor-grok-r25-visual-01 | edited_point_retained | PASS |
| cursor-grok-r25-visual-01 | restored_exact_native_texts | PASS |
| cursor-grok-r25-visual-01 | marks26_rasters0 | PASS |
| cursor-grok-r25-visual-01 | coordinate_delta | PASS |
| cursor-grok-r25-visual-01 | frames_inside | PASS |
| cursor-grok-r25-visual-01 | controller_render_source | PASS |

Chuỗi kết quả tool thực tế có input/action/result tuần tự: open SVG → save_as AI copy không overwrite → guard trước từng text/point edit và save/close → reopen AI đúng path → query text+point edited retained → guard trước restore → save/close/reopen → query restored texts/structure → guard export. Ba save_document gồm một save_as và hai save; hai close không discardChanges; hai reopen đúng bản AI project-local.

AGY restored29 text strings và Cursor166 text strings đều exact multiset so với SVG nguyên bản. Mỗi bản26 point paths,0raster/images. AGY delta tâm mark 2.2937484004614817e-05; Cursor 4.8828130047695595e-05; cả hai≤0.0001 user units. Tất cả native text bounds trong artboard. Nội dung raw SVG/MD không thay hash.

## Quan sát ảnh cuối

Đã xem native-render.png và controller-render.png của từng folder. AGY1400×1100; Cursor1400×1794 (tool display resize nhỏ nhưng file gốc vẫn đúng). Không thấy clipping, unintended text overlap, mất dấu tiếng Việt hay điểm dữ liệu. Cursor bảng đủ26 hàng tới2025 hiện đầy đủ; tick x xoay90, label y dọc không bị cắt. Các khác biệt font rasterization giữa native và rsvg không làm mất nội dung. Đây là quan sát visual của ảnh hiện tại, không phải user accessibility test hay chứng nhận khoa học.

## Hash evidence

| Host | controller-qa.json | native AI | illustrator-evidence.json |
|---|---|---|---|
| agy-gemini-r25-visual-01 | `09d29563af58465582b2f387872361389c057df9d773e44a1d81155261e09c39` | `c0f04eed48e1e752356d6220e69487f5640a5a182258d8396b38a661f2fcacb1` | `292570442ee1720b0bbefb13f5378c5324fed35cc26db3fc4cdc2ae26657d012` |
| cursor-grok-r25-visual-01 | `48130dd59282be4ae035bb6c32928a62187707db61268eb058e317b15c59a1b7` | `5723660550739f4c7c31b092de2fc64c6952c153e76ac914e5f52fc9c006d9ca` | `1c731544659e5fb087ead1fe15515ea83a7ebd09fa27ac194454db36a6342e2c` |

Source audit đã đọc lại: plans/reports/review-261003-2137-ide-worldbank-source-and-receipts.md SHA256 `2e21ab8a03ecc7c5735b84ed56a93c9278d39993f807d2c73f3d7b3a9a6eee94`. Raw AGY finding source truth pass sớm được giữ ở audit lịch sử; current controller verdict kiểm tra actual final artifacts độc lập, không chấp nhận generation-time claim ngược thời gian.

## Gates còn giới hạn

- Effective provider model/effort chưa có telemetry; userselected prompts completed không trở thành effective-model-confirmed.
- AGY identity bằng GPT Sol vẫn không chứng minh independent Gemini generation; receipts giống không xác thực fresh reader execution độc lập.
- Accessibility structural/contrast only. AGY role/aria có; Cursor title/desc/lang nhưng không role/aria theo thiết kế công khai. Không AT usertesting; SVG metadata persistence trong AI chưa được chứng minh.
- Current native/edit/save/reopen/render/layout gates đã có bằng chứng pass trong phạm vi này. Exact rights/publishing clearance, scientific/stable/globalhost compatibility không được cấp từ QA.
- Owner pending-personal-review. Không chấp nhận hoặc ghi điểm thay owner.

## Blockers

Không có blocker mới trong scope source/render/native QA. Giữ raw/history/current receipts và chờ owner quyết định acceptance sau dùng.
