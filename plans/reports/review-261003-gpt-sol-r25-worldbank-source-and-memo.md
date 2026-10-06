# Audit nguồn và memo World Bank — GPT-6.1 Sol r25

## Kết luận

PASS trong phạm vi source truth, phép tính, source-to-mark, hash/lineage và trung thực về trạng thái QA của đầu ra gốc. Không phát hiện finding cụ thể cần sửa ở các phạm vi này. Các cổng native/layout/editability/owner chưa được audit này chấp nhận. Không chạy lại model, reader, checker hay renderer; chỉ đọc trace và tự tính lại dữ liệu bằng thao tác trong bộ nhớ.

## Artifact cố định

- Markdown SHA256: `e4f37b5304af9a684b3acfb9fdc6a39c0ad3727c0113de777c72f353d9bc91a0`.
- SVG SHA256: `a85e1a4aaa336d20e7d3096362dd019041e7d73e44f887f972fa58773cdafb3e`.
- Events SHA256: `4710abed842aeb5e86c419a00a7d2c83d708e09217ca3eac2fdbed4b35fe0988`.
- Raw API SHA256: `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781`.
- Derived source SHA256: `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2`.
- Record canonical SHA256: `65b7007d7ea17cae6091e2925ec725bf88433573635536386868bfa4c1304800`.

## Kiểm tra độc lập

| Điều kiện | Kết quả |
|---|---|
| raw_projection_26 | PASS |
| counts | PASS |
| marks_polyline_table_exact | PASS |
| y_ticks | PASS |
| x_ticks | PASS |
| arithmetic | PASS |
| metadata | PASS |
| artifact_receipt_hashes | PASS |
| source_hashes | PASS |
| exact_extraction | PASS |
| binding_render_hashes | PASS |
| actual_reader_and_checker | PASS |
| reader_record_hash | PASS |

26 quan sát gốc khớp projection về năm, giá trị nguyên, country, indicator và unit trống. 26 circle khớp data-year/data-value; title từng điểm giữ giá trị chính xác. Polyline và bảng 26 hàng dùng cùng tọa độ. Dùng Decimal kiểm tra x = 200 + 40 × (year − 2000), y = 700 − (value − 75000000) × 510 / 30000000; sai số tối đa cho tọa độ 6 chữ số là 0.0000005. Tick x 2000/2005/2010/2015/2020/2025; tick y 75–105 triệu cách 5 triệu, nhãn baseline lệch 6 so với đường grid đúng thiết kế. Trục không bắt đầu 0 được công khai.

| Năm | Giá trị gốc | x | y chính xác | cy SVG |
|---|---:|---:|---:|---:|
| 2000 | 77154011 | 200 | 663.381813 | 663.381813 |
| 2001 | 77969361 | 240 | 649.520863 | 649.520863 |
| 2002 | 78772224 | 280 | 635.872192 | 635.872192 |
| 2003 | 79563777 | 320 | 622.415791 | 622.415791 |
| 2004 | 80338971 | 360 | 609.237493 | 609.237493 |
| 2005 | 81088313 | 400 | 596.498679 | 596.498679 |
| 2006 | 82167897 | 440 | 578.145751 | 578.145751 |
| 2007 | 83633375 | 480 | 553.232625 | 553.232625 |
| 2008 | 85175788 | 520 | 527.011604 | 527.011604 |
| 2009 | 86460018 | 560 | 505.179694 | 505.179694 |
| 2010 | 87455152 | 600 | 488.262416 | 488.262416 |
| 2011 | 88468314 | 640 | 471.038662 | 471.038662 |
| 2012 | 89510356 | 680 | 453.323948 | 453.323948 |
| 2013 | 90573104 | 720 | 435.257232 | 435.257232 |
| 2014 | 91679578 | 760 | 416.447174 | 416.447174 |
| 2015 | 92823254 | 800 | 397.004682 | 397.004682 |
| 2016 | 94000117 | 840 | 376.998011 | 376.998011 |
| 2017 | 95176977 | 880 | 356.991391 | 356.991391 |
| 2018 | 96237319 | 920 | 338.965577 | 338.965577 |
| 2019 | 97173776 | 960 | 323.045808 | 323.045808 |
| 2020 | 98079191 | 1000 | 307.653753 | 307.653753 |
| 2021 | 98935098 | 1040 | 293.103334 | 293.103334 |
| 2022 | 99680655 | 1080 | 280.428865 | 280.428865 |
| 2023 | 100352192 | 1120 | 269.012736 | 269.012736 |
| 2024 | 100987686 | 1160 | 258.209338 | 258.209338 |
| 2025 | 101598527 | 1200 | 247.825041 | 247.825041 |

Thay đổi 2000→2025 = 24,444,516; phần trăm = 31.682754639936995% theo binary64 và mẫu số 77,154,011. Không diễn giải chuỗi này là khai triển thập phân vô hạn. Mô tả tăng từng năm được dữ liệu hỗ trợ; không có diễn giải nhân quả. Root title/desc tiếng Việt, aria-labelledby khớp IDs, raw blank-unit caveat được giữ. Đây là kiểm tra sự hiện diện/ý nghĩa nguồn, chưa xác nhận accessibility thực tế của viewer.

## Trace thực tế và ranh giới đọc

Chỉ có bốn command_execution hoàn thành, tất cả exit 0:

- events.jsonl dòng 8: `"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -LiteralPath 'C:/Users/USER\\.claude\\rules\\development-rules.md'; Get-Content -LiteralPath '.agents/skills/nckh-visuals/SKILL.md'"`
- events.jsonl dòng 10: `"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$paths = @('"'references/_shared/core/policies/authorization-policy.md','references/_shared/core/policies/evidence-policy.md','references/_shared/core/policies/preservation-policy.md','references/_shared/core/policies/acceptance-policy.md','references/visual-acceptance.md','references/_shared/extensions/native-documents/contract.json','references/resource-lookup.md'); foreach ("'$p in $paths) { Write-Output "FILE $p"; Get-Content -LiteralPath (Join-Path '"'.agents/skills/nckh-visuals' "'$p) }'`
- events.jsonl dòng 12: `"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$paths = @('"'references/_shared/docs/contracts.md','references/_shared/core/profiles/acceptance/personal-use.json'); foreach ("'$p in $paths) { Write-Output "FILE $p"; Get-Content -LiteralPath (Join-Path '"'.agents/skills/nckh-visuals' "'$p) }; python -I .agents/skills/nckh-visuals/references/_shared/scripts/search-resource.py --resource-id R-worldbank-vietnam-population --consumer nckh-visuals --domain chart-measurement --locale und --genre indicator-time-series --query worldbank-vnm-SP.POP.TOTL-2000-2025 --json; python -I .agents/skills/nckh-visuals/references/_shared/scripts/check-visual-engine.py --project "C:/Users/USER/Downloads/test-skill" --task real-source-worldbank-visual-01 --host codex --binding "plans/evaluation/personal-use/visual-engine-probe-02/codex-binding.json" --capability svg-render'`
- events.jsonl dòng 15: `"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$profile = Get-Content -Raw -LiteralPath '"'.agents/skills/nckh-visuals/references/_shared/core/profiles/acceptance/personal-use.json' | ConvertFrom-Json; "'$profile.skills.'"'nckh-visuals' | ConvertTo-Json -Depth 12; "'$r = python -I .agents/skills/nckh-visuals/references/_shared/scripts/search-resource.py --resource-id R-worldbank-vietnam-population --consumer nckh-visuals --domain chart-measurement --locale und --genre indicator-time-series --query worldbank-vnm-SP.POP.TOTL-2000-2025 --json | ConvertFrom-Json; $r.records[0].content.data | Sort-Object { [int]$_.date } | ForEach-Object { $x = 200 + 40 * ([int]$_.date - 2000); $y = 700 - ([double]$_.value - 75000000) / 30000000 * 510; '"'{0}|{1}|{2}|{3:F6}' -f "'$_.date,$_.value,$x,$y }; Write-Output ('"'change={0}; percent={1:R}' -f (101598527-77154011),((101598527-77154011)/77154011.0*100)); "'$paths = @('"'plans/evaluation/personal-use/source-acquisition/derived/reader-ready.jsonl','plans/evaluation/personal-use/source-acquisition/raw/worldbank-vnm-population-2000-2025.json','plans/evaluation/personal-use/source-acquisition/derived/worldbank-series.jsonl'); foreach ("'$p in $paths) { Get-FileHash -Algorithm SHA256 -LiteralPath $p | Select-Object Path,Hash | ConvertTo-Json -Compress }'`

Dòng 12 thực sự trả JSON status matched/resource_read true với toàn bộ 26 quan sát, resource/record/reader hash khớp và JSON binding integrity-verified. Dòng 15 gọi reader lại, xuất đủ 26 kết quả tọa độ và phép tính; dấu phẩy thập phân của PowerShell được biểu diễn bằng dấu chấm đúng trong SVG. Không cần fallback. contracts.md mà dòng12 đọc là resource rights contract theo liên kết trong resource-lookup.md; không có bằng chứng model mở worldbank-rights.md riêng, nhưng memo không khẳng định tên tệp này.

Đọc ngoài dự án tại dòng8 chỉ là C:/Users/USER/.claude/rules/development-rules.md, đã được prompt cho phép thành ngoại lệ instruction-authority và memo/receipt ghi riêng. Checker được phép đọc engine chỉ định qua binding; không có lệnh model tự đọc engine ngoài dự án, chạy test, viết file, UI, nested agent hay provider mutation trong trace. Chỉ xác nhận những sự kiện có thể quan sát trong trace này.

## Quyền nguồn và QA

Điều khoản chính thức [World Bank Summary Terms of Use](https://data.worldbank.org/summary-terms-of-use), đọc trong audit ngày 2026-10-03, hỗ trợ nhãn CC BY 4.0 mặc định khi metadata không quy định khác, yêu cầu attribution và caveat chỉ báo bên thứ ba có thể có điều kiện bổ sung. Artifact giữ URL điều khoản, attribution World Bank và caveat; không tuyên bố clearance cụ thể hay được World Bank chứng nhận. worldbank-rights.md là authored rights record, không phải bản chép terms. Applicability cụ thể tiếp tục unverified; audit không cấp quyền publishing.

Bản raw Markdown đặt render/source-to-mark/editability/final hashes là pending ở thời điểm model hoàn thành, không tự nhận đã lưu hay render. Controller extraction và source-to-mark receipts xuất hiện sau đó, hash khớp artifact nguyên bản. Render receipt chỉ xác nhận rsvg-convert exit0, input SVG và output PNG hashes khớp cùng engine binding; không xác nhận bố cục/font/native editability. Requested model gpt-6.1-sol / effort low, no fallback theo receipt; effective telemetry null, không nâng thành effective-model-confirmed. Owner remains pending-personal-review.

## Biên nhận đọc và hash

| Tệp case/nguồn | SHA256 |
|---|---|
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/artifact.md` | `e4f37b5304af9a684b3acfb9fdc6a39c0ad3727c0113de777c72f353d9bc91a0` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/artifact.svg` | `a85e1a4aaa336d20e7d3096362dd019041e7d73e44f887f972fa58773cdafb3e` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/receipt.json` | `6526e303db224e0e7fc8bb098fe28098b2f396e418b88311e8ad8e6267761814` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/events.jsonl` | `4710abed842aeb5e86c419a00a7d2c83d708e09217ca3eac2fdbed4b35fe0988` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/extraction.json` | `4fa372e1419e5c5b5a2d0e334b3fdb14008c6869b6fd8b376fdc53d765b272ed` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/source-to-mark-check.json` | `213cc0361c17e149f37632a912ef82aa605bcb2b0d7d9685d5796c3e5d30ede0` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/rsvg-render.json` | `031118ebb0227d7c7bfffade9e9f0ecd7a552d448b93f835db89c34672d01f64` |
| `plans/evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/prompt.txt` | `c8bcc7527808b46e030e087d98aa291ad7f7912c658126a8e12d049433a9b6ce` |

## Findings và việc còn lại

Không có finding chặn source truth hoặc memo trong phạm vi audit. Controller tiếp tục native layout/editability với cùng hash; owner quyết định acceptance sau sử dụng. Bất kỳ sửa SVG/MD nào phải giữ raw và gắn revision/hash mới.
