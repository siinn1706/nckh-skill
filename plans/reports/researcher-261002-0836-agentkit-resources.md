# Đối chiếu thiết kế resource của AgentKit và NCKH

**Thời điểm:** 2026-10-02, Asia/Saigon  
**Phạm vi:** review read-only cho câu hỏi vì sao NCKH chủ yếu dùng Markdown
thay vì CSV/JSON. Không sửa source NCKH, cài đặt, gọi provider hay đổi cấu hình
toàn cục.

## Kết luận

NCKH đã tách format theo consumer: Markdown cho instructions, boundary,
heuristic và reference cần đọc theo route; JSON cho contract được validate,
catalog/compatibility, lock và record máy đọc. `nckh-kit/skills/core` hiện có
16 `.md`, không có CSV/JSON; `nckh-kit/core` có 32 `.json`, 10 `.md`, 12 `.py`.
Đây không phải kết luận rằng CSV/JSON vô ích, mà là dấu hiệu chúng chỉ nên
được thêm khi đã có reader, schema và acceptance check cụ thể.

AgentKit cho cùng một ranh giới: UI/UX và AI-Artist dùng CSV cho tìm kiếm theo
dòng, sau đó trả Markdown hoặc JSON; research, copywriting, multimodal và
skill-authoring vẫn là workflow/reference bằng Markdown. Khuyến nghị xếp hạng:
(1) hybrid có chọn lọc, (2) Markdown-only cho guidance mới, (3) không port
toàn bộ CSV/JSON của AgentKit.

## Evidence/provenance cục bộ

| Nguồn | Quan sát trực tiếp | Độ tin cậy |
|---|---|---|
| `nckh-kit/core/schema.py:87-89`; `nckh-kit/core/build.py:39-45,175-198` | `schema.py` đọc/validate JSON; build đọc catalog JSON, đóng dependency qua link Markdown và package `.md/.json/.yaml/.toml/.py`. | Cao: executable owner |
| `nckh-kit/core/registry/source-lock/source-lock.json:2,741-775` | `copied_third_party_content=false`, `release_rights=local-package-only`, inspirations AgentKit là `design inspiration only`, revision `18`. | Cao: release/provenance |
| `nckh-kit/core/registry/catalog/skills.json:2-3,62-143` | `nckh-research`, `nckh-evidence`, `nckh-method`, `nckh-write`, `nckh-taste`, `nckh-visuals` là experimental và source-locked. | Cao: machine registry |
| `C:/Users/USER/.agents/skills/ak-skill-creator/SKILL.md:48-72`; `references/skill-anatomy-and-requirements.md:19-76` | AgentKit yêu cầu progressive disclosure: SKILL.md ngắn, reference tải khi cần, scripts và assets tách riêng. | Cao: authoring contract |
| `C:/Users/USER/.codex/plugins/cache/agentkit-local/ak-engineer/0.2.0/.codex-plugin/plugin.json`; `.agentkit/install-manifest.json` | Plugin record là `0.2.0`; `native-skill-hashes.json` ghi source path/hash. Hash bản user-scope khác cache, nên cache chỉ là provenance metadata, không phải nội dung hiện hành. | Vừa: package metadata |

Không cần web lookup: mọi nhận định dựa trên file/script local. Plugin record
không được xem là Git source revision.

## Vì sao skill layer của NCKH dùng Markdown nhiều

1. `nckh-research/SKILL.md:13-32` có review mode, locator, access và bounded
   synthesis; `nckh-visuals/SKILL.md:13-34` tách source truth, native
   editability, render, accessibility và scientific meaning. Đây là quy trình
   có nhánh/điều kiện, không phải bảng record; Markdown giữ được thứ tự, lý do,
   ngoại lệ và boundary để nạp đúng route.
2. Contract máy đã có owner mạnh hơn: `nckh-evidence/SKILL.md:36-41` link
   source/evidence/claim schemas; `nckh-method/SKILL.md:34-37` link brief schema;
   `schema.py` validate JSON. Đổi sang CSV sẽ làm mất nested arrays, required
   fields, enum, hash và lỗi contract có cấu trúc.
3. Reference route-specific vốn nhỏ: `nckh-research/references/review-modes.md:1-9`,
   `nckh-write/references/fidelity-and-glossary.md:1-14`,
   `nckh-visuals/references/visual-acceptance.md:1-8`. Tải đúng file khi route
   áp dụng làm giảm context; bảng mirror không có consumer tương ứng.

## AgentKit: artifact nào được reader nào dùng

### CSV: chỉ đáng dùng khi có row-search reader

`ak-ui-ux-pro-max` khai báo file/cột domain ở `scripts/core.py:17-73`;
`_load_csv` gọi `csv.DictReader` ở `scripts/core.py:152-178`, BM25 tìm trên
selected columns rồi trả selected fields. `SKILL.md:134-146` ghi
`ui-reasoning.csv` dùng cho design-system selection; `SKILL.md:151-180` ghi
result được persist thành `MASTER.md` và page override. Inventory có 15 CSV,
trong đó `google-fonts.csv` 1,924 dòng, `styles.csv` 85, `colors.csv` 162,
`ux-guidelines.csv` 100.

Smoke read-only đã trả 2 rows và `file=ux-guidelines.csv`:

```text
python .../ak-ui-ux-pro-max/scripts/search.py
  "SaaS dashboard accessibility" --domain ux --max-results 2 --json
=> domain=ux, file=ux-guidelines.csv, count=2
```

Đây là runtime proof của CSV reader AgentKit, không phải proof NCKH.

`ak-ai-artist/scripts/core.py:17-146` dùng cùng pattern: map domain→CSV,
`DictReader`, BM25 và output columns; `ak-ai-artist/SKILL.md:76-129` mô tả
prompt database/consumer. Smoke search đã trả `file=awesome-prompts.csv,
count=2`. CSV hợp với lookup table lớn, ổn định; không phải format mặc định
cho mọi rule NCKH.

### Markdown và JSON: workflow, interchange, contract

`ak-research/SKILL.md:17-63` yêu cầu scope và cross-reference;
`ak-copywriting/SKILL.md:17-40` route theo brief/reference;
`ak-ai-multimodal/SKILL.md:31-57,97-125` ưu tiên native vision trước provider
recipe và yêu cầu credential phù hợp. Đây là decision workflow, không phải row
database.

`ak-copywriting/scripts/extract-writing-styles.py:28-32,80-204` nhận Markdown,
text, document và media; trích sections/tables; có thể serialize output thành
JSON. Đây là Markdown làm input linh hoạt và JSON làm interchange, không phải
JSON thay authoring. UI/UX design-system smoke cũng đọc nhiều CSV nhưng xuất
Markdown: structured data cho retrieval, Markdown cho artifact người/model đọc.

`ak-skill-creator/assets/eval-cases.example.json` và
`assets/semantic-routing/cases.json` dùng JSON cho fixed cases, split và
machine assertions; `references/testing-and-iteration.md:1-24,31-47` yêu cầu
holdout cố định và record có cấu trúc. JSON contract/catalog/source-lock NCKH
có cùng vai trò machine-stability. Chỉ dùng JSONL cho record append/stream theo
dòng; không chuyển prose thành JSON chỉ để “có cấu trúc”.

## Trade-off và lựa chọn xếp hạng

| Lựa chọn | Retrieval/validation | Chi phí | Drift/licensing | Xếp hạng |
|---|---|---:|---:|---|
| Hybrid có chọn lọc | Mạnh nơi có contract/reader; prose vẫn rõ | Thấp-vừa | Thấp nếu giữ lock/ownership | 1, khuyến nghị |
| Markdown-only | Dễ sửa, yếu schema/search | Thấp nhất | Thấp | 2, chỉ cho guidance |
| Port CSV/JSON toàn bộ | Cần reader/schema/test/migration | Cao | Cao; lock không cho coi inspiration là copied content | 3, loại |

## Kế hoạch artifact tối thiểu (chỉ plan)

1. Giữ `SKILL.md` và route reference NCKH bằng Markdown; không tạo CSV mirror
   cho prose.
2. Giữ JSON Schema làm canonical cho source, evidence, claim, brief, receipt,
   task-state, catalog và source-lock. Chỉ thêm schema khi đã rõ producer và
   validator. Reader-card record và source-to-mark map là ứng viên optional,
   chưa nên thêm khi chưa có consumer.
3. Chỉ thêm CSV cho hotspot retrieval có row schema ổn định (ví dụ index
   venue-policy/glossary lớn). Kèm stdlib reader/search, cột chính xác,
   provenance/version và test; Markdown là authority, CSV chỉ là index.
4. Dùng JSON/JSONL cho eval cases, receipts và observation append; giữ expected
   outcomes/raw private traces ngoài prose của skill.
5. Trước implementation, lập consumer matrix gồm artifact path, reader, output
   shape, owner, rights, version/hash và acceptance check; validate link/schema,
   freeze source lock, rồi chạy một smoke case thật. Static validation không
   thay cho runtime/scientific acceptance.

## Giới hạn và câu hỏi mở

Đây là comparison về format, không phải audit behavior mới. Báo cáo direct
development ghi 148 case và tách installed revision 14 khỏi source revision 18
(`plans/reports/testing-261001-direct-skill-development.md:5,27,34-35`); tôi
không chấm lại. Smoke probe chỉ chạy AgentKit local scripts, không chứng minh
NCKH routing, human/domain acceptance, rights clearance hay scientific validity.
Không clone external AgentKit repository và không coi nó là authority.

Câu hỏi mở: workflow NCKH nào sẽ own reader-card validator, và có row corpus
lớn thực sự cần CSV retrieval hay không? Nếu chưa có consumer, thêm CSV/JSON sẽ
là format-first scope expansion, không phải artifact hữu ích.
