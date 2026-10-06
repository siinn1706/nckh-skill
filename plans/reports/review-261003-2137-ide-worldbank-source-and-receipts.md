# Audit hai đầu ra IDE World Bank r25

## Kết luận

PASS cho source-to-mark và hash compatibility của cả AGY/Cursor. DONE_WITH_CONCERNS cho trạng thái memo AGY và bằng chứng model/runtime độc lập. Chỉ đọc artifacts/receipts và tính trong bộ nhớ; không chạy model/provider/render/Illustrator/UI.

## Finding P2 — AGY tự ghi source truth pass trước controller

AGY MD dòng331 (`6cd0955969a76383f0d5548100f3cad4fe311dd243d785d7525c493cf138ab0d`) ghi Source truth pass. Exact prompt native/agy-gemini-r25-visual-01-prompt.txt yêu cầu sourcetruth controllerpending until actual finalartifact checks. Số liệu được audit hiện tại xác minh đúng, nhưng không làm generation-time acceptance hợp lệ ngược thời gian. Controller giữ raw memo, đánh dấu tuyên bố sớm và gắn verdict thật ở receipt riêng; nếu sửa memo thì tạo revision mới. Không cần sửa dữ liệu SVG.

## Kiểm tra thực tế

| Host | Điều kiện | Verdict |
|---|---|---|
| agy | counts26 | PASS |
| agy | all_values_map | PASS |
| agy | ticks | PASS |
| agy | reader_source | PASS |
| agy | binding | PASS |
| agy | render_pins | PASS |
| agy | arithmetic_pins | PASS |
| cursor | counts26 | PASS |
| cursor | all_values_map | PASS |
| cursor | ticks | PASS |
| cursor | reader_source | PASS |
| cursor | binding | PASS |
| cursor | render_pins | PASS |
| cursor | arithmetic_pins | PASS |
| cursor | stdout_hashes | PASS |
| cursor | memo_hash | PASS |

26/26 source values/circle data-year/data-value/polyline/MD table rows đều đúng. AGY x=200+40(year−2000);y=700−(value−75000000)510/30000000, 6 decimals với sai số≤0.0000005. Cursor x=180+(year−2000)1160/25;y=668−(value−70000000)512/40000000, tọa độ Decimal kết thúc chính xác. Tick AGY y75–105 triệu bước5 triệu/x5năm; Cursor y70–110 triệu bước5 triệu/x26năm, nhãn năm rotate90 tại translate(x,680), khớp công thức.

First77,154,011/last101,598,527/delta24,444,516/percent binary64 31.682754639936995%, mẫu số77,154,011. Cursor mô tả finite repr/cắt cụt/Decimal80 digits đúng. Raw blankunit, snapshot2026-07-13, country/indicator, source locator và hashes, providerrevision và thirdpartyrights caveats giữ đủ. Hai title/desc tiếng Việt có readingorder; không suy ra AT acceptance. Source và raw input đã đọc đủ26 quan sát.

## Provenance và giới hạn

AGY SVG `a85e1a4aaa336d20e7d3096362dd019041e7d73e44f887f972fa58773cdafb3e`, PNG `ff6b8f76d4d03c7f5dfe63131c72ef43a5d98c64edd18ebba67aeebda0a73be9` byte-identical với lượt GPT Sol identity do controller cung cấp. Không suy ra independent Gemini generation, sao chép trái phép, hoặc numerical failure chỉ từ identity. AGY reader/checker là payload kết quả, không có native eventtrace/processreceipt độc lập; render JSON command/exit/version/inputoutput hashes phù hợp artifacts/binding nhưng provenance thực thi chưa được eventstream xác thực.

Cursor SVG `410c47985a1419bace3234a7d177c4e906ad37ae222e1276918c0631139a49e6`, MD `b109108ba6901e476466a41250fb800f6383abd430eae080593ed20407a6b66b`. Có command/cwd/exit/stdoutstderr hash receipts cho reader/checker/render/version, hash đọc lại khớp. Receipts tương thích reader path/query/binding/engine/version được giao; vẫn không thay full IDE trace/effective provider telemetry.

AGY MD dòng6 Gemini-only/no-fallback và Cursor MD dòng3 “Runner ... Grok4.7” là self-authored claims. Exact prompts chỉ cho phép Gemini3.8FlashHigh và Grok4.7ExtraHigh; các file này không chứng minh effective model/effort hay full compliance runtime. Giữ unverified, không kết luận vi phạm bằng sự thiếu telemetry.

Rights pass-with-caveat AGY chỉ hỗ trợ nghĩa giữ notices, chưa specific applicability/publishing clearance. Native edit/save/reopen/layout/accessibility/source truth/owner cuối là controller-owned gates; source truth tự pass đã được finding nêu riêng. Host-authority read được AGY khai báo nhưng không có eventtrace để xác minh; audit không đọc globalrules/font/executable ngoài project.

## Hash artifacts và receipts

| Tệp | SHA256 |
|---|---|
| `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/checker-receipt.json` | `c171a365d85fd211557c5a1465d685e0d6a2bb01e0062ed7987606f3b6cbb0e7` |
| `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/reader-receipt.json` | `3afca7f91305ea19c0cf96f1f0eee4c523c6c74bd9d503761155de161faa6d5d` |
| `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.md` | `6cd0955969a76383f0d5548100f3cad4fe311dd243d785d7525c493cf138ab0d` |
| `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.svg` | `a85e1a4aaa336d20e7d3096362dd019041e7d73e44f887f972fa58773cdafb3e` |
| `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/rsvg-render.json` | `61fc7273be77e5cd7f3ee2a4dd7d4dd8c54df5cef9d17d0850c4237b67de7d6e` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/checker-receipt.json` | `6ec717197cc0ec2618c6a8e970dbd3d983e29fe4163bfe023cd9c69886d728aa` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/checker.stdout.json` | `8161dc9c32306c4f0cb7262b67aa1d1c351b964806dbf16ecdfe3582381a1967` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/reader-receipt.json` | `b1978d5dea6e80c5758e38169f33c6b1fcad5885e5c5777342f8dc84cdde6cbf` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/reader.stdout.json` | `3afca7f91305ea19c0cf96f1f0eee4c523c6c74bd9d503761155de161faa6d5d` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/real-source-worldbank-visual-01.md` | `b109108ba6901e476466a41250fb800f6383abd430eae080593ed20407a6b66b` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/real-source-worldbank-visual-01.svg` | `410c47985a1419bace3234a7d177c4e906ad37ae222e1276918c0631139a49e6` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/render.json` | `db577ea510fe5ca7a223dd30e04dc8a70eeeb22dee8ca5ac28d86a9c3fb86eb3` |
| `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/version.json` | `5e3299124cdb844b5eec414ae678952a2c50c7691a2741195f3b7c460d8ce31f` |

## Blockers

Không có blocker số liệu/arithmetics/hash compatibility. Thiếu native event/providertrace chặn kết luận independent model execution, không chặn sử dụng SVG sau controllerQA. Cần ghi đúng trạng thái source truth AGY trong handoff; giữ raw output. Owner score pending-personal-review; không human/scientific/stable certification.
