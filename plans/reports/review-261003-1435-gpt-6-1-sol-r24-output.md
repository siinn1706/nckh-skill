# Review artifact VI: current app gpt-6.1-sol r24, attempt 02

Ngày: 2026-10-03, Asia/Saigon. Case: `real-source-vi-prose-taste-01`. Phạm vi: artifact/trace/source; không chấm khẩu vị thay chủ dự án, không xử lý runtime matrix.

## Kết quả

Artifact VI có đủ năm phần bắt buộc, ba neo nguyên văn và các quan sát có vị trí; output prose dùng được trong phạm vi một child passage. Trace chứng minh reader đúng resource/source_id đã hoàn tất exit 0 và receipt khớp installed source hiện tại.

**Chưa thể ghi tất cả hard gates pass:** trace có một lần đọc file ngoài project-only boundary của prompt; một trích dẫn phụ bị đổi chữ hoa đầu; trường đường dẫn controller lưu trong artifact không khớp actual save path trong execution receipt. Không có evidence về effective model: receipt giữ null, requested model là `gpt-6.1-sol`, fallback false.

## Inputs và snapshot

- Artifact (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/artifact.md`; unavailable in the cleaned checkout), SHA-256 `d70ea5eb9e468ce709c9be80adf7d32f8f639e66a0118a41dee93934f02c62ff`.
- Prompt (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/prompt.txt:1`; unavailable in the cleaned checkout), SHA-256 `c3e7079da22989e58945a28d318182b7043ba12cc83d7defd772ebcac9349b09`.
- Execution receipt (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/receipt.json`; unavailable in the cleaned checkout), SHA-256 `bbc36fc3c944a241a255a19483ff39a94b71ed77cc934d92a0af7a13a65caa25`.
- Trace events (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/events.jsonl`; unavailable in the cleaned checkout), SHA-256 `67d93e5e289f14a5393ce000d541b21806f9979da9fda3299cc71816327ac4f7`.
- stderr SHA-256 `3e5aeb14518bd0f538ebd1f3293fa85b1a9d7ccf19d1bc212157ff273313fc22`.

Prompt, events, stderr và artifact hiện có đều khớp hash ghi trong execution receipt. Final agent message tại trace dòng 25 khớp artifact khi bỏ whitespace ngoài cùng. Không chạy reader/model/provider/UI/tests trong review; chỉ đọc artifact/trace/source và đối chiếu hash/chuỗi. Không sửa output/source/installed skills.

## Findings

### [P2] Trace vượt biên đọc project-only

**Vị trí:** events.jsonl dòng 9 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/events.jsonl:9`; unavailable in the cleaned checkout) khởi chạy đọc `C:/Users/USER/.claude/rules/development-rules.md`; dòng 10 ghi `command_execution`, completed, exit_code 0.

**Contract:** prompt dòng 1 giới hạn work context `C:/Users/USER/Downloads/test-skill only` và chỉ đọc required files của case. File global này nằm ngoài project, không phải source/input hay installed skill reference cần thiết mà prompt liệt kê. Đây là quan sát command trong trace, không suy từ sandbox permission hoặc catalogue.

**Tác động:** authority/project-boundary check của attempt này fail. Không có mutation được thể hiện bởi command đó; không suy thêm external write, data loss hay secret leak.

**Repair:** giữ trace attempt hiện tại và ghi failure scope; loại lần đọc global file ở lượt chạy được phép tiếp theo, dùng project instructions đã cấp. Sửa memo không thể biến trace cũ thành một run project-only. Root sở hữu quyết định có rerun hay không; review này không dispatch model mới.

### [P3] Trích dẫn phụ đổi capitalization của source

**Vị trí:** artifact dòng 79 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/artifact.md:79`; unavailable in the cleaned checkout) viết `“Mại bản”` như trích dẫn source. Record thực tế ghi `Duy có người mại bản tên là Đặng-cách-luân`; `Mại bản` không có trong passage, `mại bản` có.

**Contract:** preservation policy giữ quote/protected bytes đúng nguyên văn; đây là drift ở một quote phụ, không phải neo bắt buộc hoặc thay đổi nghĩa từ.

**Repair:** đổi riêng trích dẫn sang `“mại bản”`. Giữ nhận xét khẩu vị và mọi chữ lịch sử khác; không hiện đại hóa từ. Ba content anchor bắt buộc vẫn nguyên vẹn.

### [P3] Mislabeled actual controller save path

**Vị trí:** artifact dòng 9 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/artifact.md:9`; unavailable in the cleaned checkout) đặt nhãn “Đường dẫn controller lưu” cho `plans/evaluation/personal-use/native/real-source-vi-prose-taste-01.md`. Receipt dòng 26 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/receipt.json:26`; unavailable in the cleaned checkout) và artifact đang review cho thấy actual path là thư mục `app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/artifact.md`.

**Repair:** đổi nhãn thành “Đường dẫn yêu cầu trong case”, hoặc cập nhật actual saved path trong controller handoff gắn với hash. Dòng 128 nói artifact chưa được lưu/hash tại thời điểm model trả final là ranh giới bàn giao hợp lý; execution receipt hiện đã bind file/hash, không cần bịa self-hash trong final text.

## Observable checks của case VI

| Observable có sẵn | Kết quả | Evidence ở artifact |
|---|---|---|
| Source_id, child oldid, parent oldid, locator đúng | pass | Dòng 12–21, `vi-wikisource-19383`, 19383, 106841 và locator exact. |
| Cả ba content anchor không sửa chính tả | pass | Dòng 44, 46, 48; source và artifact đều chứa ba chuỗi exact. |
| Register/rhythm/vocabulary/audience/genre có vị trí | pass cho nội dung quan sát | Dòng 54–97 chỉ đúng cảnh/quote; quote phụ `Mại bản` cần correction đã nêu. |
| Tối đa hai đề xuất, rõ ràng tách khỏi source | pass | Dòng 115–119: hai chú giải ngoài passage, không đổi source hay áp dụng rewrite. |
| Không human gold, authority rộng, completeness/scientific verdict | pass | Dòng 58, 89, 109–111, 123–128 và `pending-personal-review`. |

Các quote mô tả nhịp, lời thoại và cử chỉ đều có trong passage, ngoại trừ capitalization của `Mại bản`: `Uả hay!`, `mững rỡ`, `thiệt thọ`, `mắt măng mắt vược`, hai câu hỏi song song, các cử chỉ ghen tuông và đoạn bắt đầu `Lúc Lý-khắc-lai chết giữa đường` đã được đối chiếu trực tiếp. Không phát hiện quote bị bịa, sửa content anchor hay claim sai niên đại/translator từ năm truyện 1815.

Giới hạn thiếu kỳ XIV được ghi đúng là dữ kiện brief, chưa xác minh riêng parent trong run này. Metadata page-level CC BY-SA và underlying-work public-domain rationale được tách; không suy universal redistribution. Nhận xét taste vẫn là advisory, không phải điểm human/native reader.

## Reader và trace evidence

- Trace dòng 8 đọc installed `nckh-taste/SKILL.md`; dòng 12 đọc shared policies/profile/resource-lookup; dòng 14 đọc `nckh-write/SKILL.md` và personal-use JSON; dòng 18 đọc fidelity/resource reference và đúng acceptance rows.
- Trace dòng 16 (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-02/gpt-6.1-sol/events.jsonl:16`; unavailable in the cleaned checkout) ghi command reader completed exit 0: installed `.agents/skills/nckh-taste/references/_shared/scripts/search-resource.py`, `R-vi-wikisource-passages`, consumer `nckh-taste`, domain `language-literary`, locale `vi`, genre `prose-verse-samples`, query `vi-wikisource-19383`, JSON.
- Aggregated output dòng 16 parse thành receipt schema 2, matched, resource_read true, một actual-passage record. Content bằng record đang cài, canonical record hash khớp `13149ead6bebde7171e5697919acfacfda9b22850023caf6e51971edf7080566`.
- Resource hash khớp `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f`; reader bytes khớp `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`.
- Trace dòng 22 ghi acquisition JSONL hash/size; dòng 24 ghi installed passage bằng acquisition passage và ba anchor True. Review xác nhận lại source text equality, acquisition hash `16175d1edc8116d07d9e952584f3ef47b3227cf8bd7d599cc30c695bff4f893e`, 221904 byte. Không sử dụng fallback.
- Artifact dòng 40 phân biệt raw JSON/HTML lineage hashes đã đọc với hash raw files chưa tính lại trong run; không giả claim đã tính lại chúng.
- Trace dòng 2–4 có config/unstable-feature warnings trước turn; reader commands vẫn hoàn tất. Các warning này không chứng minh model unavailable hay artifact fidelity failure; không sửa global config.

## Gate matrix và giới hạn

| Gate | Kết quả trong review |
|---|---|
| Identity/VI case/source route | pass |
| Positive observable behavior/usable memo | pass |
| Output facts/quote/provenance | fail hẹp: quote capitalization và save-path label cần sửa |
| Authority/project-only reads | fail: một đọc global file ngoài boundary |
| Reader/source/hash integrity | pass |
| Process đã ghi exit 0/cleanup | receipt-bound observation; root quản lý runtime matrix |
| Effective model/effort | unknown/null; requested `gpt-6.1-sol`, no fallback là configuration evidence |
| Owner taste score | pending-personal-review |
| Human/native/scientific/stable qualification | không được review này xác nhận |

Đây là native executable dispatch với final artifact được controller lưu, đúng evidence limit trong receipt; không phải main-window UI run. Không có external holdout/reviewer prerequisite cho personal-use. Không dùng exit 0 hoặc source match để vượt các fail/pending gates.

Status: DONE_WITH_CONCERNS

Summary: Artifact VI có nội dung/neo nguồn đúng và reader trace hợp lệ; phát hiện một đọc ngoài project, một quote capitalization drift và nhãn save path sai. Hash của final artifact khớp receipt.

Concerns/Blockers: Scope failure của trace không thể sửa bằng chỉnh memo; effective-model telemetry và owner score vẫn chưa xác nhận. Root quyết định bước sửa/rerun trong phạm vi người dùng chỉ cho phép app 6.1 Sol.

## Controller resolution: mandatory host instruction-authority read

Controller đã đối chiếu instruction hierarchy của phiên: developer instruction bắt buộc đọc và tuân thủ `~/.claude/rules/development-rules.md`. Vì vậy, đọc file đó tại trace dòng 9–10 là một **ngoại lệ authority bắt buộc của host**, không phải evidence về unauthorized external-project test hoặc global mutation. Command/read quan sát được và mismatch với cách viết project-only tuyệt đối của standalone brief được giữ trong lịch sử ở trên; đánh giá blanket authority failure được thay bằng resolution này.

Standalone prompt có ambiguity giữa case/source boundary và required host-authority reads. Runner tiếp theo phải giữ case files/sources/output/tests trong project, khai báo riêng ngoại lệ mandatory development rules, tuân thủ host instruction hierarchy và ghi các read authority quan sát được riêng. Không suy permission cho global edits hay unrelated source/config/user-data reads.

Theo resolution hiện tại, retry sửa artifact chỉ cần xử lý quote capitalization và nhãn actual save path; không cần retry chỉ để xóa lần đọc authority bắt buộc khỏi trace. Effective-model telemetry và owner score vẫn chưa được xác nhận. Artifact/trace/hash ban đầu không bị sửa.
