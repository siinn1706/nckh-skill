# Review đầu ra Cursor r24: năm ca nguồn thật

Ngày: 2026-10-03, Asia/Saigon. Phạm vi: kiểm tra artifact và receipt theo case contract đã chuẩn bị; không chấm thay chủ dự án.

## Kết quả

| Case | Sự thật/nguồn | Output contract | Kết luận kiểm tra artifact |
|---|---|---|---|
| VI prose/taste | pass | pass | Ba neo nguyên văn, quan sát và giới hạn đúng; khẩu vị cá nhân còn chờ chủ dự án. |
| EN scientific fidelity | pass | pass | Ledger năm dòng khớp nguồn; kết luận 144 từ, giữ association và giới hạn excerpt. |
| World Bank visual | pass cho dữ liệu/lineage; lưu ý từ “chính xác” ở phép chia | unmet | Không có SVG; memo blocker giữ đúng contract unavailable. |
| Django code review | pass cho nguồn và failure path | fail một phần required-edit | Finding có căn cứ; lựa chọn chỉ sửa message không khắc phục failure path đã nêu. |
| UCI analytics | pass | fail một observable hình thức | Giá trị/đếm đúng; thiếu bảng tổng hợp target mà case yêu cầu. |

Không được ghi “5/5 output contract pass”. Hai sửa đổi memo có phạm vi nhỏ; visual vẫn thiếu capability thực tế. Sáu reader receipt khớp source đang cài. Owner feedback của mọi case vẫn `pending-personal-review`.

## Phạm vi và cách kiểm tra

- Đọc case manifest (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cases/real-source-cases.json`; unavailable in the cleaned checkout) và prompt Cursor r24 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24-prompt.txt:1`; unavailable in the cleaned checkout), năm memo cùng sáu receipt.
- Đọc source đúng case: record trong pack đã cài, abstract/title/license của XML PMC, hai fixture Django và ba test method được chỉ định, mười dòng CSV đầu trong archive UCI, snapshot JSON World Bank. Không đọc private issue/benchmark patch/task text.
- Tính lại SHA-256 của artifact, receipt, reader và resource; canonical record hash dùng đúng `json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(',', ':'))` như reader. Đối chiếu content receipt với record trong pack đang cài.
- Đối chiếu chữ/giá trị và tính số học bằng đọc file cục bộ; không chạy reader, Django/test suite, provider/model evaluation, UI hoặc external write. Không làm lại qualification source/package/install.
- Một lần kiểm tra đọc file bị lỗi encoding khi in tiếng Việt; đã chạy lại với stdout UTF-8 và hoàn tất. Không có lỗi kiểm tra còn bị che.
- Receipt lưu trên đĩa là evidence về nội dung/lineage có thể kiểm tra. Báo cáo này không tự xác nhận process telemetry, effective model, thời gian hay chi phí. Prompt chỉ cho phép Cursor Grok 4.7 Extra High, không fallback; selected label không phải effective-model evidence.

## Findings cần sửa

### [P2] Django: lựa chọn chỉ đổi message không sửa thiếu sót assertion

**Vị trí:** memo Django, dòng 46 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-django-code-review-01.md:46`; unavailable in the cleaned checkout), lặp lại ở dòng 52. Finding nêu đúng tác động ở dòng 44: transaction-end marker có thể đứng trước `DROP TABLE` mà test vẫn qua các assertion về thứ tự.

**Nguồn:** fixture test, dòng 480 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/source-acquisition/raw/swe-django-02cd16-test_commands.py:480`; unavailable in the cleaned checkout) lấy `index_drop_table`; dòng 497–499 buộc DROP TABLE đứng sau author comment; dòng 502 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/source-acquisition/raw/swe-django-02cd16-test_commands.py:502`; unavailable in the cleaned checkout) chỉ so `index_tx_end > index_op_desc_unique_together`. Không có assertion buộc `index_tx_end > index_drop_table`.

**Failure path có căn cứ, chưa chạy:** các vị trí `tx_start < unique_together < tx_end < tribble < author < drop_table` thỏa cả chuỗi so sánh hiện có, nhưng transaction đã kết thúc trước DROP TABLE. Đây là suy luận trực tiếp từ comparator trong bytes, không phải kết quả test runtime.

**Repair cho artifact:** giữ finding và nhánh sửa comparator sang `index_drop_table`; bỏ nhánh “or change the message” như một sửa chữa đầy đủ cho impact này. Nếu muốn chỉ đề xuất sửa message thì phải giảm finding thành message mismatch và không nói nó khắc phục thiếu kiểm tra thứ tự. Owner thực hiện: phiên sửa memo; không sửa fixture/source theo yêu cầu review-only này.

### [P3] UCI: thiếu bảng tổng hợp target được yêu cầu tường minh

**Vị trí:** memo UCI, dòng 45 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-uci-analytics-01.md:45`; unavailable in the cleaned checkout) viết đúng `no=10`, `yes=0` bằng prose. Bảng dòng 51–62 là bảng mười quan sát, chỉ có `no`, không phải bảng tổng hợp có cả hai target.

**Contract:** case manifest, dòng 490 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cases/real-source-cases.json:490`; unavailable in the cleaned checkout): “The target table reports y=no=10 and y=yes=0 without presenting it as a population response rate.”

**Repair cho artifact:** thêm bảng hai dòng `no | 10 | 10`, `yes | 0 | 10`, với mẫu số ghi rõ là mười dòng đầu. Giữ giới hạn không suy thành response rate population. Không cần thay đổi nguồn hoặc số liệu.

### Lưu ý độ chính xác World Bank

Memo World Bank, dòng 48 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-worldbank-visual-01.md:48`; unavailable in the cleaned checkout) gọi chuỗi thập phân hữu hạn là “Phần trăm chính xác”. Chuỗi đó khớp phép tính Decimal với precision 50, và prefix yêu cầu `31.682754639936995` đúng. Giá trị chính xác là phân số `2444451600/77154011` phần trăm; chuỗi in ra là biểu diễn thập phân ở precision 50. Nên ghi precision hoặc dùng ký hiệu xấp xỉ, giữ nguyên công thức. Lưu ý này không làm sai endpoint hoặc chênh lệch tuyệt đối và không thay đổi blocker visual.

## Observable checks theo từng case

`pass` dưới đây chỉ xác nhận observable/facts trong artifact đã kiểm tra. `fail` là sai/lệch contract đã có thể sửa; `unmet` là deliverable chưa tồn tại. Các trạng thái này không cấp human/scientific/native acceptance.

### 1. real-source-vi-prose-taste-01

Artifact: memo VI (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-vi-prose-taste-01.md`; unavailable in the cleaned checkout).

| Observable trong case | Kết quả | Evidence ở artifact |
|---|---|---|
| Đúng source_id, child oldid, parent oldid và locator | pass | Dòng 7–12. |
| Cả ba neo nguyên văn, không sửa chính tả | pass | Dòng 32–34; từng chuỗi có mặt nguyên vẹn trong source và memo. |
| Quan sát register, rhythm, vocabulary, audience/genre có vị trí | pass | Dòng 38–42: câu mở, dấu `--`, từ cổ, hai dạng Mã-lặc-nhi/Mã-lạc-nhi và translated-novel đều có trong record. |
| Đề xuất có giới hạn, tách khỏi source | pass | Dòng 54–57: đúng hai đề xuất đặt ngoài đoạn, không thay thế hay hiện đại hóa source. |
| Không claim human gold, authority rộng, completeness hay scientific validity | pass | Dòng 61–65 và rights boundary dòng 63. |

Các đoạn bắt buộc đều hiện diện. Mọi từ được trích làm ví dụ ở dòng 40 có trong source, gồm `mững rỡ` và `nằn nì`. Record kết ở `Chú thích`; extraction metadata thực sự ghi loại references/navigation. Không phát hiện factual delta hoặc neo giả. Không chấm một khẩu vị VI “đạt chuẩn” thay chủ dự án.

### 2. real-source-en-scientific-fidelity-01

Artifact: memo khoa học (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-en-scientific-fidelity-01.md`; unavailable in the cleaned checkout).

| Observable trong case | Kết quả | Evidence ở artifact |
|---|---|---|
| Source_id, PMCID, DOI, raw XML hash, article-level CC BY 4.0 | pass | Dòng 7–24; DOI/title/license sentence khớp raw XML. |
| Numerical claim trong ledger traceable và đúng nghĩa/format | pass | Năm dòng ledger 32–36 khớp excerpt và abstract XML. |
| Association/aOR/p-value/CI không nâng thành causality | pass | Dòng 36 và 40; forbidden-overclaim column nêu rõ giới hạn. |
| Tách excerpt giới hạn khỏi full XML | pass | Dòng 20–26 và 46: excerpt đúng 9.000 ký tự, kết ở `Scopus profiles, and`. |
| Không citation/count/generalization/scientific verdict vô căn cứ | pass | Dòng 40, 44–48; số trong limits đều có trong abstract. |

Kết luận dòng 40 có **144 từ khi đếm theo khoảng trắng**, trong yêu cầu 120–180. Các số 1,375/1,332/1,334, 675/657, 486/848, 50.7%/49.3%/36.4%/63.6%, χ²=98.23, p<0.001, aOR=0.93 và CI 0.90–0.97 khớp nguồn. Các association theo publication year và t/risk-difference/CI ở phần limits cũng khớp abstract; không dùng chúng như nhân quả. Không phát hiện defect fidelity trong phạm vi claim này. Đây không phải peer review hoặc xác nhận nghiên cứu hợp lệ.

### 3. real-source-worldbank-visual-01

Artifact: memo blocker World Bank (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-worldbank-visual-01.md`; unavailable in the cleaned checkout). Không có `real-source-worldbank-visual-01.svg`.

| Observable trong case | Kết quả | Evidence ở artifact |
|---|---|---|
| Receipt có 26 observations/non-null cho 2000–2025 | pass | Dòng 43–44; cả 26 năm khác nhau và 26 value non-null khớp raw API. |
| Endpoint 77154011/101598527 và unit blank | pass | Dòng 43, 45–46; unit ở mọi observation là chuỗi rỗng. |
| Source-to-mark map, axis/caption/VI alt/reading order | unmet | Dòng 57, 61: không có hình và không có mapping/axis/alt gắn với hình. |
| SVG source-native/editable với text/data objects | unmet | Dòng 3, 57: SVG không được tạo; không có raster thay thế. |
| Giữ render/inspection chưa chạy/chưa pass | pass về báo cáo gate | Dòng 65–67 ghi không chạy, không ghi pass. Không phải actual QA pass. |

`response_lastupdated=2026-07-13`, source locator/hash và rights caveat được giữ ở dòng 27–50. Chênh lệch `101598527 - 77154011 = 24444516` đúng. Dữ liệu receipt khớp tất cả value/unit trong snapshot API; không nội suy.

Blocker khớp installed engine contract (historical evidence path: `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-visuals/references/_shared/extensions/native-documents/contract.json:5`; unavailable in the cleaned checkout): status unavailable, engine_binding null ở dòng 13. SKILL.md dòng 28 (historical evidence path: `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-visuals/SKILL.md:28`; unavailable in the cleaned checkout) và visual-acceptance dòng 14 (historical evidence path: `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-visuals/references/visual-acceptance.md:14`; unavailable in the cleaned checkout) cấm coi binding trống là capability có sẵn. Prompt r24 cho phép blocker memo, đánh output contract unmet và tiếp tục case khác. Memo tuân thủ nhánh này; **điều đó không hoàn thành editable SVG output contract**.

### 4. real-source-django-code-review-01

Artifact: memo Django (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-django-code-review-01.md`; unavailable in the cleaned checkout).

| Observable trong case | Kết quả | Evidence ở artifact |
|---|---|---|
| Mỗi finding có fixture/line, impact, why/repro, required edit | fail một phần | Dòng 42–46 đủ vị trí/impact/why; branch sửa message không sửa failure path như finding đã nêu. |
| Inspected scope nếu no-finding | pass cho scope thực tế | Dòng 29–32 liệt kê implementation và cả ba method. Kết quả là một finding, không phải no-finding toàn case. |
| Commit, fixture hashes và BSD scope | pass | Dòng 18–30; bytes content hai fixture khớp raw file và hash. |
| Không private issue/task/patch text | pass trong artifact/receipt được đọc | Dòng 22–23 chỉ liệt kê tên các field bị loại; reader pack chứa code_fixtures và task locator. Không có body/patch private. |
| Review-only, không code change/merge/publish/security guarantee | pass trong nội dung bàn giao | Dòng 3, 34, 56; không có patch hay claim runtime. Báo cáo artifact không chứng minh mọi side effect của phiên host. |

Failure claim ở dòng 44–45 được source hỗ trợ. Implementation `self.output_transaction = migration.atomic` ở fixture dòng 53; plan một node ở dòng 57; `collect_sql` ở dòng 58 rồi trả chuỗi join ở dòng 59. Không có căn cứ từ hai fixture để biến ghi chú instance reuse dòng 48 thành defect runtime, và memo đã giữ nó unverified. Chỉ cần sửa repair-direction của memo; không chạy test hay sửa Django fixture.

### 5. real-source-uci-analytics-01

Artifact: memo UCI (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24/real-source-uci-analytics-01.md`; unavailable in the cleaned checkout).

| Observable trong case | Kết quả | Evidence ở artifact |
|---|---|---|
| 10 rows, 17 columns, delimiter ; và DOI/locator | pass | Dòng 8–9, 20–21, 43. |
| Target table no=10/yes=0, không population response rate | fail hình thức; facts pass | Dòng 45 có counts đúng nhưng thiếu count table; bảng quan sát 51–62 không có row yes=0. |
| Month counts và balance -88 traceable | pass | Dòng 47–49, 53–62; số đếm và từng ô bảng khớp CSV thật. |
| Tách descriptive/causal và nêu duration leakage | pass | Dòng 3, 30–37, 68–78; không invent causal lift/forecast. |
| Raw archive và derived record hashes | pass | Dòng 15–19; receipt content khớp installed record, mười dòng khớp archive bank.csv. |

Receipt giữ đủ 17 cột và raw string của mười dòng. Bảng memo dùng đúng mười trường case yêu cầu; không có requirement mới buộc mọi cột phải được lặp lại trong bảng prose. Đếm độc lập: `no=10`, `yes=0`, `may=5`, `apr=2`, `feb=1`, `jun=1`, `oct=1`; dòng 10 có balance `-88`. Sentinel `pdays=-1`, `unknown`, zero và balance âm không bị chuẩn hóa sai. Không phát hiện số liệu giả hoặc lỗi arithmetic. Chỉ thiếu bảng tổng hợp target theo observable tường minh.

## Receipt/source integrity

Tất cả sáu receipt có schema_version 2, `status=matched`, `resource_read=true`, đúng consumer/domain/locale/genre, query đúng một source_id và một record. Resource hash, reader hash, canonical record hash và content đều khớp installed source đang đọc. `human_acceptance=not-evaluated` được giữ.

Reader SHA-256 chung: `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`.

| Receipt trong cursor-grok-r24/reader-receipts | SHA-256 file receipt |
|---|---|
| nckh-taste__R-vi-wikisource-passages__vi-wikisource-19383.json | `def004febd95f984aa353888d543c9af4609e38e46580273f1b6474119a7e267` |
| nckh-write__R-vi-wikisource-passages__vi-wikisource-19383.json | `40a058ed49cc9f78eb5b24c62a71491cd6dfc7ccca7269b7ed508931af410939` |
| nckh-write__R-pmc-scientific__pmc-PMC13623154.json | `90818d10ce0f8eb9a9f4271a20c7434b095b2d38bfe786925239066c4f4ef29d` |
| nckh-visuals__R-worldbank-vietnam-population__worldbank-vnm-SP.POP.TOTL-2000-2025.json | `3afca7f91305ea19c0cf96f1f0eee4c523c6c74bd9d503761155de161faa6d5d` |
| nckh-code-review__R-django-sqlmigrate-fixtures__django__django-10087.json | `705d2b978dd7e58539e6dec380dca9d73e534ca4d390d6b4c5dfc2ba419e548a` |
| nckh-analytics__R-uci-bank-marketing__uci-bank-marketing-bank-csv-first-10.json | `b0100b18d4d3ffd96e4458bbea9a5b3a7daaabec88824ac518146f86116ef1e6` |

## Hash-bound snapshot của review

| Artifact đầu vào | SHA-256 |
|---|---|
| native/cases/real-source-cases.json | `d4b926e855cbf8203d8f434db3fa6a427eb71fbd02a07d274fe5ef485cfeb875` |
| native/cursor-grok-r24-prompt.txt | `16e62a1d850a5f6c3680dac342bc634e3c766f7145ed25c782165312a316e1de` |
| cursor-grok-r24/real-source-vi-prose-taste-01.md | `fc9fbf65c2fc21c180f85889c760f83dd1ea4fb2e7aba41928b0b1bcd251ff3d` |
| cursor-grok-r24/real-source-en-scientific-fidelity-01.md | `f41fe9aa6d1a1d3d7ac611914f6dae862a0c51e2d1f2375fdbaebcd6d7500a79` |
| cursor-grok-r24/real-source-worldbank-visual-01.md | `f96c9cf1c57fd8ea19fa7ce73608f4648aaec710de94f956dfed07d35fa7647e` |
| cursor-grok-r24/real-source-django-code-review-01.md | `f11d5980067173426c88e1d2f15efc8f5fae91e59ec8b7071a475ddd567cda5a` |
| cursor-grok-r24/real-source-uci-analytics-01.md | `e80e562268652416ab00571643672c68c53b8416f069b680f7e58acdfd00925b` |

Các hash này bind review vào revision hiện tại; sửa memo làm review/check tương ứng stale cho tới khi đối chiếu delta. Root giữ owner gate và quyết định sửa ở attempt tiếp theo. Không thay đổi source-lock r24 hay installed contract để đóng visual gate.

## Khuyến nghị bàn giao

Giữ VI và EN fidelity dưới kết quả kiểm tra artifact pass; sửa hai memo Django/UCI theo findings rồi review delta. Giữ World Bank output contract unmet tới khi có engine binding thực tế được phép và SVG/open/render/editability evidence tương ứng. Có thể bàn giao nguồn và memo blocker để người dùng biết giới hạn; không gọi đó là successful visual delivery.

Owner tự chấm sau khi dùng theo personal-use profile. Không thêm external holdout/reviewer prerequisite; không suy native/domain/scientific certification từ review này.

Status: DONE_WITH_CONCERNS

Summary: Đã kiểm tra năm output và sáu reader receipt theo contract/nguồn. Facts và source integrity khớp; Django có repair-direction defect, UCI thiếu target count table, World Bank chưa có SVG do engine unavailable.

Concerns/Blockers: Visual capability vẫn unavailable; mọi owner score và effective-model telemetry không được review này xác nhận.
