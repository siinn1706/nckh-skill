# Personal Vietnamese Writing & Research Skills — Blueprint v1.0

## 1. Mục tiêu

Bộ skill này được thiết kế cho ba mục tiêu chính:

1. **Viết tiếng Việt tốt hơn**
   - Văn phong tự nhiên hơn.
   - Có “taste” về câu chữ, nhịp điệu, độ chính xác và mức độ học thuật.
   - Hạn chế văn phong AI, sáo rỗng, dịch máy, lên gân hoặc lạm dụng thuật ngữ.
   - Có khả năng phân biệt giữa câu “đúng ngữ pháp” và câu “viết hay”.

2. **Giảm ảo giác và tăng độ tin cậy**
   - Không tự bịa nguồn, trích dẫn, số trang, DOI, câu thơ, câu văn.
   - Phân biệt rõ dữ kiện, suy luận, diễn giải và giả thuyết.
   - Kiểm chứng claim trước khi biến nó thành câu văn hoàn chỉnh.
   - Không làm mạnh hơn mức độ chắc chắn của nguồn trong quá trình rewrite.

3. **Hỗ trợ nghiên cứu khoa học**
   - Đọc và phân tích paper, sách, tài liệu học thuật.
   - Tìm, kiểm tra và tổng hợp tài liệu.
   - Xây dựng literature review.
   - Xác định research gap.
   - Kiểm tra logic nghiên cứu, phương pháp, bằng chứng và trích dẫn.
   - Hỗ trợ peer review và final audit.

---

# 2. Triết lý thiết kế

Không xây một `SKILL.md` khổng lồ xử lý mọi thứ.

Nên tách hệ thống thành các skill có trách nhiệm rõ ràng:

```text
READ
↓
EXTRACT EVIDENCE
↓
VERIFY CLAIMS
↓
BUILD ARGUMENT
↓
WRITE
↓
CRITIQUE
↓
POLISH
↓
AUDIT
```

Nguyên tắc quan trọng:

> Writing, reasoning, verification và polishing không nên bị trộn thành một bước duy nhất.

Một model vừa viết vừa tự đánh giá câu mình vừa viết thường có xu hướng chấp nhận chính output của nó.

Vì vậy:

- Writer viết.
- Critic phê bình.
- Verifier kiểm chứng.
- Auditor kiểm tra cuối.

---

# 3. Kiến trúc đề xuất

```text
my-skills/
│
├── skills/
│   ├── vi-writing/
│   ├── vi-taste/
│   ├── vi-polishing/
│   │
│   ├── research-reader/
│   ├── evidence-first/
│   ├── claim-verifier/
│   ├── citation-auditor/
│   │
│   ├── argument-architect/
│   ├── literature-review/
│   ├── research-gap/
│   ├── research-methodology/
│   ├── peer-reviewer/
│   ├── fact-checker/
│   ├── terminology-manager/
│   ├── comparison-engine/
│   └── final-audit/
│
└── shared/
    ├── vietnamese-style/
    ├── epistemic-rules/
    ├── citation-rules/
    ├── anti-hallucination/
    ├── academic-writing/
    ├── examples/
    └── schemas/
```

Không nhất thiết phải build toàn bộ ngay từ đầu.

Phiên bản đầu chỉ nên tập trung vào khoảng 7–10 skill cốt lõi.

---

# 4. Nhóm skill ưu tiên cao nhất

## S-Tier

### 4.1. `vi-writing`

Skill viết chính bằng tiếng Việt.

Nhiệm vụ:

- Viết đoạn văn.
- Viết bài nghị luận.
- Viết tiểu luận.
- Viết phân tích văn học.
- Viết học thuật.
- Viết lại từ outline hoặc evidence đã có.

### Nguyên tắc văn phong

Ưu tiên:

- Ý nghĩa trước vẻ đẹp câu chữ.
- Cụ thể trước trừu tượng.
- Chính xác trước cầu kỳ.
- Động từ rõ nghĩa trước danh từ hóa.
- Mỗi đoạn phải có nhiệm vụ lập luận cụ thể.
- Nhịp câu nên thay đổi tự nhiên.
- Không dùng thuật ngữ chỉ vì nó nghe “học thuật”.

Hạn chế các cấu trúc AI thường gặp:

```text
không chỉ... mà còn...
qua đó cho thấy...
có thể thấy rằng...
từ đó có thể khẳng định...
đồng thời...
bên cạnh đó...
trong bối cảnh...
đóng vai trò quan trọng...
mang ý nghĩa sâu sắc...
góp phần làm nổi bật...
```

Không cấm tuyệt đối.

Chỉ dùng khi thực sự có chức năng.

---

## 4.2. `vi-taste`

Đây nên là một trong những skill quan trọng nhất.

Mục tiêu:

> Dạy AI phân biệt giữa câu “ổn” và câu “hay”.

Skill này chủ yếu **phê bình**, không trực tiếp viết.

### Những vấn đề cần phát hiện

- Sáo ngữ.
- Abstract language.
- Fake depth.
- Dùng thuật ngữ quá mức.
- Nhịp câu máy móc.
- Quá nhiều cấu trúc song song.
- Văn phong dịch từ tiếng Anh.
- Câu nghe học thuật nhưng không tạo thêm ý nghĩa.
- Câu áp dụng được cho hàng trăm tác phẩm khác nhau.
- Câu quá “AI”.

Ví dụ:

```text
Sentence:
"Không gian nghệ thuật trong tác phẩm không chỉ là nơi diễn ra
các sự kiện mà còn là phương tiện thể hiện thế giới nội tâm nhân vật."

Problems:
- generic academic template
- cliché structure
- vague terminology
- claim too broad
- sentence could apply to hundreds of works

Taste score:
weak

Rewrite direction:
Specify which spatial transformation corresponds to which
psychological or narrative transformation.
```

---

## 4.3. `vi-polishing`

Nhiệm vụ:

- Làm câu văn tự nhiên hơn.
- Giảm lặp.
- Sửa nhịp câu.
- Sửa liên kết đoạn.
- Chuẩn hóa thuật ngữ.
- Tăng độ chính xác.

Luật quan trọng:

> Polishing không được thay đổi mức độ chắc chắn của claim.

Ví dụ:

Sai:

```text
Original:
"Nghiên cứu này gợi ý rằng..."

Rewrite:
"Nghiên cứu này chứng minh rằng..."
```

Đúng:

```text
Original:
"Nghiên cứu này gợi ý rằng..."

Rewrite:
"Kết quả của nghiên cứu cho thấy khả năng..."
```

---

# 5. Nhóm chống hallucination

## 5.1. `evidence-first`

Đây nên là luật nền của toàn bộ research stack.

Workflow sai:

```text
viết đoạn
↓
tìm nguồn để gắn citation
```

Workflow đúng:

```text
question
↓
source
↓
evidence
↓
claim
↓
argument
↓
prose
```

### Claim object

Có thể chuẩn hóa dưới dạng:

```yaml
claim_id: C01
claim: "..."
source: "..."
page: 161
evidence_type: direct
confidence: high
status: supported
allowed_wording:
  - "cho thấy"
  - "gợi ý"
forbidden_wording:
  - "chứng minh"
```

---

## 5.2. `claim-verifier`

Nhiệm vụ:

Kiểm tra từng claim trước khi nó được đưa vào bài.

### Phân loại

```text
VERIFIED
SUPPORTED
REASONABLE INFERENCE
INTERPRETATION
UNVERIFIED
CONTRADICTED
```

Ví dụ:

```text
Claim:
"Sơ kính tân trang đánh dấu bước chuyển quan trọng
của thi pháp truyện thơ Nôm."

Questions:
- "bước chuyển" so với giai đoạn nào?
- tiêu chí nào xác định là "quan trọng"?
- có nguồn học thuật nào khẳng định?
- đây là nhận định của nguồn hay inference của người viết?
- corpus so sánh gồm những tác phẩm nào?
```

Nếu chưa đủ evidence:

```text
Status: UNVERIFIED
```

Không được tự động biến thành fact khi rewrite.

---

## 5.3. `citation-auditor`

Nhiệm vụ:

- Kiểm tra nguồn.
- Kiểm tra tác giả.
- Kiểm tra năm.
- Kiểm tra tên bài.
- Kiểm tra nhà xuất bản.
- Kiểm tra DOI.
- Kiểm tra số trang.
- Kiểm tra quote.

### Luật tuyệt đối

```text
NEVER invent:
- page number
- quotation
- poem line
- publication year
- publisher
- DOI
- author
```

Đối với direct quote:

```yaml
direct_quote:
  source_verified: true
  exact_match: true
  page_verified: true
```

Thiếu một trong ba:

```text
DO NOT USE AS DIRECT QUOTE
```

---

## 5.4. `fact-checker`

Khác với `claim-verifier`.

`fact-checker` tập trung vào dữ kiện cụ thể:

- Tên người.
- Địa danh.
- Ngày tháng.
- Niên đại.
- Tên tác phẩm.
- Tên học giả.
- Thuật ngữ.
- Số liệu.
- Sự kiện.

---

# 6. Nhóm research

## 6.1. `research-reader`

Skill đọc tài liệu sâu.

Không chỉ summarize.

Nên tạo một representation có cấu trúc:

```text
SOURCE
├── metadata
├── research question
├── thesis
├── concepts
├── methodology
├── evidence
├── conclusions
├── limitations
├── exact quotations
├── useful pages
├── possible connections
└── do-not-overclaim
```

Ví dụ:

```text
Claim của tác giả:
...

Evidence:
pp. 42–45

Direct quote:
"..."

Interpretation:
...

Relevant to:
- không gian nghệ thuật
- tính dục
- diễn ngôn giới

Do NOT claim:
...
```

---

## 6.2. `literature-review`

Workflow:

```text
Research question
↓
Search strategy
↓
Candidate sources
↓
Screening
↓
Evidence extraction
↓
Thematic clustering
↓
Agreement / disagreement
↓
Limitations
↓
Research gap
↓
Narrative synthesis
```

Không được:

```text
Viết literature review trước
↓
sau đó tìm citation để khớp
```

---

## 6.3. `research-gap`

Mục tiêu:

Tránh kiểu AI tự nghĩ ra:

```text
"Hiện nay chưa có nhiều nghiên cứu..."
```

mà không có căn cứ.

Research gap phải dựa trên:

- corpus đã search;
- phạm vi thời gian;
- nhóm nguồn;
- phương pháp;
- đối tượng;
- biến nghiên cứu;
- limitations từ các paper trước.

Phân biệt:

```text
empirical gap
methodological gap
theoretical gap
population gap
context gap
temporal gap
contradictory evidence
```

---

## 6.4. `research-methodology`

Nhiệm vụ:

- Kiểm tra câu hỏi nghiên cứu.
- Kiểm tra giả thuyết.
- Đề xuất phương pháp.
- Kiểm tra phương pháp có thực sự trả lời được research question hay không.
- Phân biệt exploratory / descriptive / explanatory.
- Kiểm tra operationalization.
- Kiểm tra limitations.

---

# 7. Nhóm reasoning & argument

## 7.1. `argument-architect`

Không viết prose ngay.

Trước tiên dựng logic:

```text
THESIS
│
├── CLAIM 1
│   ├── evidence
│   ├── reasoning
│   └── limitation
│
├── CLAIM 2
│   ├── evidence
│   ├── reasoning
│   └── counterargument
│
└── CLAIM 3
```

Một paragraph object có thể gồm:

```yaml
paragraph:
  purpose:
  claim:
  evidence:
  interpretation:
  connection:
  limitation:
  transition:
```

---

## 7.2. `comparison-engine`

Đặc biệt hữu ích cho Văn học.

Nhiệm vụ:

- So sánh hai tác phẩm.
- So sánh hai lý thuyết.
- So sánh hai nghiên cứu.

Không được chỉ:

```text
A cũng...
B cũng...
```

Mà phải xác định:

```text
comparison axis
similarity
difference
degree
function
historical context
limits of comparison
```

---

## 7.3. `terminology-manager`

Nhiệm vụ:

- Tạo glossary.
- Giữ thuật ngữ nhất quán.
- Tránh thay đổi thuật ngữ chỉ để tránh lặp.
- Phân biệt các khái niệm gần nghĩa.

Ví dụ:

```text
không gian nghệ thuật
không gian tự sự
không gian địa lý
không gian tâm lý
không gian biểu tượng
```

Không được dùng thay thế tùy tiện.

---

# 8. `peer-reviewer`

Nên chạy nhiều reviewer role độc lập.

Ví dụ:

```text
R1 — Logic reviewer
R2 — Evidence reviewer
R3 — Vietnamese style reviewer
R4 — Domain reviewer
```

Sau đó:

```text
EDITOR
↓
merge duplicate comments
↓
prioritize
```

Priority:

```text
CRITICAL
MAJOR
MINOR
STYLISTIC
```

### R1 — Logic reviewer

Kiểm:

- thesis;
- claim;
- reasoning;
- contradiction;
- missing premise;
- causal leap.

### R2 — Evidence reviewer

Kiểm:

- claim có evidence không;
- evidence có đúng claim không;
- overclaim;
- citation mismatch;
- unsupported generalization.

### R3 — Vietnamese style reviewer

Kiểm:

- AI-like phrasing;
- abstract writing;
- repetition;
- rhythm;
- diction;
- coherence.

### R4 — Domain reviewer

Kiểm theo lĩnh vực:

- văn học;
- xã hội học;
- CNTT;
- AI;
- lịch sử;
- v.v.

---

# 9. `final-audit`

Gate cuối trước khi xuất bài.

Checklist:

```text
[ ] Không có citation bịa
[ ] Không có quote chưa verify
[ ] Không có số trang bịa
[ ] Không có claim unsupported
[ ] Không có contradiction
[ ] Không tăng mức độ certainty
[ ] Thuật ngữ nhất quán
[ ] Paragraph logic rõ
[ ] Không lạm dụng sáo ngữ AI
[ ] Không có câu rỗng
[ ] Không có kết luận vượt evidence
```

---

# 10. Shared rules

## 10.1. `shared/epistemic-rules`

Đây có thể là phần quan trọng nhất của repo.

```text
1. Không biết → nói không biết.

2. Không đọc được nguồn → không giả vờ đã đọc.

3. Không xác minh được quote → không đặt trong ngoặc kép.

4. Observation ≠ interpretation.

5. Interpretation ≠ fact.

6. Correlation ≠ causation.

7. Author's claim ≠ established fact.

8. Absence of evidence ≠ evidence of absence.

9. Preserve uncertainty.

10. Do not strengthen claims during rewriting.

11. Every factual correction requires evidence.

12. If sources disagree, preserve disagreement.

13. Never fabricate bibliographic metadata.

14. Never invent page numbers.

15. Never invent quotations.

16. If evidence is insufficient, weaken the claim rather than invent support.
```

---

# 11. Shared Vietnamese Style

## `shared/vietnamese-style/`

```text
vietnamese-style/
├── rhythm.md
├── diction.md
├── paragraph.md
├── transitions.md
├── academic-voice.md
├── literary-criticism.md
└── translationese.md
```

---

# 12. Anti-pattern library

```text
shared/anti-hallucination/
```

và:

```text
shared/examples/
```

Nên có tập các ví dụ BAD / BETTER.

Ví dụ:

### BAD

```text
Không gian không chỉ là nơi diễn ra câu chuyện mà còn đóng vai trò
quan trọng trong việc thể hiện đời sống tinh thần của nhân vật.
```

### WHY BAD

```text
- generic
- predictable
- abstract
- no observable evidence
- applicable to almost any narrative text
```

### BETTER

```text
Mỗi lần nhân vật bị đẩy sang một không gian mới,
phạm vi lựa chọn của họ lại thay đổi.
```

Sau đó mới đưa evidence cụ thể.

---

# 13. `vi-taste` corpus

Taste không thể chỉ học từ rule.

Nên có corpus.

```text
vi-taste/
├── SKILL.md
│
├── principles/
│   ├── rhythm.md
│   ├── diction.md
│   ├── paragraph.md
│   ├── argument.md
│   └── academic-voice.md
│
├── anti-patterns/
│   ├── ai-cliches.md
│   ├── empty-abstraction.md
│   ├── fake-depth.md
│   ├── excessive-parallelism.md
│   └── translationese.md
│
└── examples/
    ├── bad-good-pairs.md
    ├── essays/
    ├── literary-criticism/
    └── academic/
```

---

# 14. Skill Priority

## Version 0.1

Build trước:

```text
vi-writing
vi-taste
evidence-first
claim-verifier
research-reader
citation-auditor
final-audit
```

Đây là bộ tối thiểu có thể tạo khác biệt rõ rệt.

---

## Version 0.2

Thêm:

```text
vi-polishing
argument-architect
peer-reviewer
fact-checker
terminology-manager
```

---

## Version 0.3

Thêm research stack:

```text
literature-review
research-gap
research-methodology
comparison-engine
```

---

# 15. Dependency Graph

```text
research-reader
      │
      ▼
evidence-first
      │
      ▼
claim-verifier
      │
      ▼
argument-architect
      │
      ▼
vi-writing
      │
      ▼
vi-taste
      │
      ▼
vi-polishing
      │
      ▼
citation-auditor
      │
      ▼
peer-reviewer
      │
      ▼
final-audit
```

Không phải task nào cũng cần chạy toàn bộ pipeline.

---

# 16. Workflow mẫu: viết đoạn học thuật

```text
USER REQUEST
↓
research-reader
↓
evidence-first
↓
claim-verifier
↓
argument-architect
↓
vi-writing
↓
vi-taste
↓
vi-polishing
↓
citation-auditor
↓
final-audit
```

---

# 17. Workflow mẫu: sửa một đoạn văn

```text
INPUT
↓
vi-taste
↓
claim-verifier
↓
vi-polishing
↓
final-audit
```

---

# 18. Workflow mẫu: Literature Review

```text
Research Question
↓
literature-review
↓
research-reader
↓
evidence-first
↓
claim-verifier
↓
research-gap
↓
argument-architect
↓
vi-writing
↓
citation-auditor
↓
peer-reviewer
```

---

# 19. Nguyên tắc phân quyền skill

Một skill không nên làm quá nhiều.

Ví dụ:

`vi-writing`:

```text
CAN:
- write
- organize prose
- choose wording

CANNOT:
- invent evidence
- fabricate citation
- decide whether a source exists
```

`citation-auditor`:

```text
CAN:
- verify citations

CANNOT:
- rewrite an entire essay stylistically
```

Điều này giúp debugging dễ hơn.

---

# 20. Ý tưởng schema chung

Có thể chuẩn hóa một research object:

```yaml
source:
  id:
  title:
  author:
  year:
  url:
  doi:
  verified:

evidence:
  id:
  source_id:
  page:
  type:
  text:
  verified:

claim:
  id:
  text:
  evidence_ids:
  status:
  confidence:
  interpretation_level:

paragraph:
  claim_ids:
  purpose:
  reasoning:
  limitation:
```

Skill có thể trao đổi object thay vì prose tự do.

Điều này giảm hallucination đáng kể.

---

# 21. Taste Score

Có thể để `vi-taste` đánh giá theo nhiều chiều.

```yaml
taste:
  precision: 8
  concreteness: 7
  rhythm: 6
  naturalness: 8
  originality: 5
  coherence: 9
  ai_cliche_risk: 3
```

Không nhất thiết dùng score trong output cuối.

Score chủ yếu phục vụ self-check.

---

# 22. Các loại lỗi cần track

## Style errors

```text
STYLE_GENERIC
STYLE_AI_CLICHE
STYLE_TRANSLATIONESE
STYLE_OVER_ABSTRACT
STYLE_FAKE_DEPTH
STYLE_REPETITION
STYLE_MONOTONOUS_RHYTHM
```

## Research errors

```text
CLAIM_UNSUPPORTED
CLAIM_OVERSTATED
CLAIM_AMBIGUOUS
SOURCE_UNVERIFIED
QUOTE_UNVERIFIED
PAGE_UNVERIFIED
CITATION_MISMATCH
```

## Reasoning errors

```text
LOGIC_GAP
FALSE_CAUSALITY
OVERGENERALIZATION
FALSE_EQUIVALENCE
CONTRADICTION
MISSING_PREMISE
```

---

# 23. Nguyên tắc đặc biệt cho nghiên cứu Văn học

Bộ skill nên hỗ trợ rất mạnh cho literary studies.

### Primary text > memory

Nếu phân tích tác phẩm:

```text
primary text
↓
exact passage
↓
observation
↓
interpretation
↓
secondary literature
```

Không nên:

```text
memory of plot
↓
interpretation
↓
invented quote
```

### Phân biệt

```text
TEXTUAL OBSERVATION
CRITICAL INTERPRETATION
SCHOLARLY CLAIM
PERSONAL INFERENCE
```

Bốn thứ này không được trộn vào nhau.

---

# 24. Nguyên tắc trích dẫn văn học

Đối với thơ, truyện, văn bản cổ:

```text
exact edition
translator/editor
publication year
page
line/canto/chapter if available
```

Nếu dùng bản dịch:

phải ghi rõ bản dịch nào.

Nếu có nhiều dị bản:

không được tự động coi các câu giống nhau hoàn toàn.

---

# 25. Mục tiêu dài hạn

Bộ skill này không nên chỉ trở thành:

> “AI viết văn nghe hay hơn.”

Mục tiêu nên là:

> Một hệ thống hỗ trợ viết và nghiên cứu bằng tiếng Việt có taste, có kỷ luật về bằng chứng và có khả năng tự kiểm tra mức độ chắc chắn của chính mình.

Ba trụ cột:

```text
TASTE
+
REASONING
+
EPISTEMIC DISCIPLINE
```

---

# 26. Đề xuất roadmap

## Phase 1 — Core

Build:

```text
shared/epistemic-rules
vi-taste
vi-writing
evidence-first
claim-verifier
research-reader
citation-auditor
```

## Phase 2 — Quality Control

Build:

```text
vi-polishing
argument-architect
fact-checker
peer-reviewer
final-audit
```

## Phase 3 — Research Stack

Build:

```text
literature-review
research-gap
research-methodology
comparison-engine
terminology-manager
```

## Phase 4 — Corpus & Personal Taste

Bổ sung:

- bài viết tốt;
- văn phê bình tốt;
- bài nghiên cứu tốt;
- bad/good pairs;
- lỗi AI thường gặp;
- style rules cá nhân.

Đây là giai đoạn biến bộ skill từ generic thành thực sự “của riêng mình”.

---

# 27. Hai skill nên build đầu tiên

Nếu bắt đầu ngay, ưu tiên:

## `vi-taste`

Vì nó quyết định:

- thế nào là câu hay;
- thế nào là câu AI;
- tiêu chuẩn phong cách của toàn bộ hệ thống.

## `evidence-first`

Vì nó quyết định:

- hệ thống có đáng tin hay không;
- có hallucination hay không;
- cách toàn bộ research stack xử lý evidence.

Hai skill này gần như là “linh hồn” của toàn bộ repository.

---

# 28. Tóm tắt

Bộ skill đề xuất có thể chia thành bốn lớp:

```text
STYLE
vi-writing
vi-taste
vi-polishing

EPISTEMIC
evidence-first
claim-verifier
citation-auditor
fact-checker

RESEARCH
research-reader
literature-review
research-gap
research-methodology

REASONING & QA
argument-architect
comparison-engine
peer-reviewer
final-audit
```

Shared layer:

```text
vietnamese-style
epistemic-rules
citation-rules
anti-hallucination
examples
schemas
```

Mục tiêu cuối:

```text
WRITE WELL
+
THINK CAREFULLY
+
VERIFY BEFORE CLAIMING
```
