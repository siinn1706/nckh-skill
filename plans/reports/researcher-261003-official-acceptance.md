# Tiêu chí acceptance có nguồn cho 37 NCKH skills

**Ngày nghiên cứu:** 03/10/2026, Asia/Saigon  
**Phạm vi:** catalog 37 identity trong `nckh-kit/core/registry/catalog/skills.json`; qualification hiện hành; rubric proposal; chuẩn đóng gói/eval Agent Skills; chuẩn và hướng dẫn chính thức theo các họ research, writing, visuals, engineering và marketing.  
**Lane áp dụng:** mặc định self-use của owner, có feedback lặp; không tự biến thành chứng nhận stable/scientific.

**Machine-readable companion:** [`researcher-261003-official-acceptance.json`](./researcher-261003-official-acceptance.json) chứa đúng 37 identity, criteria strings và `source_ids` đã resolve về source matrix bên dưới.

## Kết quả điều hành

Khuyến nghị dùng một acceptance vector có 5 cổng cho mọi skill, sau đó gắn thêm các tiêu chí miền trong ma trận 37 dòng ở dưới:

1. **Identity và route:** đúng skill, đúng family, đúng trigger, đúng scope, đúng revision; negative/near-miss phải được từ chối, defer hoặc chuyển owner phù hợp.
2. **Positive behavior:** prompt thực tế tạo đúng loại output mà brief yêu cầu trong clean context, kèm input và expected output.
3. **Output và facts:** artifact tồn tại và đọc được; mọi claim, số liệu, quote, code, hình, source, version, modality, quyền và uncertainty đều giữ đúng phạm vi bằng chứng.
4. **Authority và side-effect guard:** không tự thực hiện provider call, external write, publish, spend, deploy, migration, upload dữ liệu nhạy cảm hoặc review chuyên môn khi chưa có grant phù hợp.
5. **Receipt và feedback:** ghi verdict, located evidence, source/artifact hash, route/model/tool nếu quan sát được, lỗi và feedback của owner; sửa skill rồi chạy lại iteration mới.

Các cổng này dùng `pass | fail | pending | not-applicable`, không dùng một tỷ lệ phần trăm áp chung. Với self-use, owner có thể chọn acceptance score cuối cùng từ vector này và feedback cá nhân. Khuyến nghị hard-gate là identity, negative route, facts/authority và artifact; taste, polish, latency/cost hoặc human/domain review có thể `pending` nếu owner ghi rõ rằng đó là giới hạn của bản dùng cá nhân. Cổng `pending` không được ghi thành stable/scientific acceptance.

Đây là kết luận phù hợp với tài liệu Agent Skills chính thức: eval phải dùng prompt thực tế, expected output, input tùy chọn, trường hợp biên, baseline có/không có skill, assertion quan sát được, bằng chứng cụ thể và human feedback cho những thuộc tính khó tự động chấm ([AS-EVAL](https://agentskills.io/skill-creation/evaluating-skills), truy cập 03/10/2026). Tài liệu đó không đặt ngưỡng pass chung. Vì vậy, ngưỡng self-use là quyết định nội bộ của owner; ngưỡng human/scientific certification hiện vẫn thuộc qualification riêng trong repo.

## Phạm vi repo và trạng thái evidence

- `skills.json` có **37 entry**: 10 core, 13 engineer, 13 marketing và 1 tooling (`nckh-xia`); mọi entry hiện là `experimental`, mỗi entry có `positive`, `negative`, `outcome`, `failure` eval ID.
- `qualification.md` giữ riêng static/deterministic, agent behavior, native, human/scientific. Parse, hash, build, receipt hoặc synthetic fixture chỉ chứng minh đúng cấu trúc và đúng phạm vi test tương ứng; chúng không chứng minh prose quality, scientific validity, native editability, provider/model behavior hay human gold.
- `catalog.json` của rubric đang ở trạng thái `proposal`, `reviewer_approval: pending`, `thresholds: null`. Các rubric `outcome`, `vi-taste`, `en-fidelity`, `domain`, `scientific-visuals` là khung ghi nhận, chưa là nhãn đã được duyệt.
- Vì đây là lane self-use theo quyết định của owner, external human reviewer/blind holdout không phải delivery gate mặc định. Tuy nhiên historical stable/scientific certification vẫn giữ các gate rights, reviewer, threshold, holdout, native và domain như qualification đã ghi; không hạ chúng để làm self-use pass.

## Chuẩn nguồn được chọn

### 1. Chuẩn đóng gói, định tuyến và eval skill

| ID | Nguồn và as-of | Điều mà nguồn thực sự hỗ trợ | Hạn chế/adoption risk |
|---|---|---|---|
| **AS-FMT** | [Agent Skills Specification](https://agentskills.io/specification), current page, truy cập 03/10/2026 | Skill tối thiểu là thư mục có `SKILL.md`; frontmatter bắt buộc `name`, `description`, giới hạn tên và mô tả trigger; scripts/references/assets là tùy chọn; progressive disclosure là cấu trúc khuyến nghị. | Đây là format contract, không phải quality, security, truthfulness hay distribution standard. `allowed-tools` vẫn được ghi là experimental và client support có thể khác nhau. |
| **AS-EVAL** | [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills), current page, truy cập 03/10/2026 | Case gồm prompt, expected output và input tùy chọn; nên có phrasing đa dạng, edge case, clean context; chạy with-skill và baseline/old-skill; assertion phải observable; mechanical checks dùng script; style/feel cần human review; grade phải chỉ ra evidence; lặp theo iteration. | Không có universal threshold hoặc claim rằng baseline delta là causal/scientific proof. |
| **AS-DESIGN** | [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices), current page, truy cập 03/10/2026 | Bắt đầu từ real expertise/artifacts, refine bằng real execution, giữ coherent unit, moderate detail, progressive disclosure, defaults và procedures. | Đây là authoring guidance; mức chi tiết, model behavior và trigger accuracy vẫn phải đo trong client thật. |
| **AS-CLIENT** | [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), current page, truy cập 03/10/2026 | Skill load theo ba tầng metadata → instructions → resources; metadata dùng cho discovery; skill có thể compose và tự kích hoạt khi phù hợp trong Claude. | Product/VM/auto-trigger của Anthropic không phải hành vi bắt buộc của mọi client; không suy ra NCKH native acceptance từ tài liệu sản phẩm. |
| **AS-WAZA** | [Microsoft Waza](https://github.com/microsoft/waza), repository/documentation current as-of truy cập 03/10/2026 | Một implementation chính thức của Microsoft bổ sung spec coverage, task fixtures, graders, baseline/model comparison, snapshots/replay và adversarial packs. | Đây là tool implementation, không phải normative Agent Skills spec; provider/model/CLI có thể đổi. Dùng để lấy pattern observable, không dùng như world-best ranking. |

Các nguồn trên độc lập ở mức issuer (Agent Skills maintainers, Anthropic, Microsoft) và cùng hội tụ ở ba điểm: skill phải có scope/trigger rõ, eval phải có baseline/case thực tế, và pass phải có evidence. Chúng không hỗ trợ claim rằng một skill “đã tốt”, “đã stable” hoặc “giảm hallucination” chỉ từ format validation.

### 2. Chuẩn research, evidence, writing và publication integrity

| ID | Nguồn và version/date | Tiêu chí có thể chuyển thành check |
|---|---|---|
| **RES-EQUATOR** | [EQUATOR: reporting guideline là gì](https://www.equator-network.org/about-us/what-is-a-reporting-guideline/), và [toolkit chọn guideline](https://www.equator-network.org/library/equator-network-reporting-guideline-manual/), truy cập 03/10/2026 | Guideline là checklist/flow/structured text cho **một loại nghiên cứu cụ thể**, có methodology rõ; dùng để report completeness/transparency, không phải chứng nhận study quality. |
| **RES-PRISMA** | [PRISMA 2020](https://www.prisma-statement.org/prisma-2020), [home/scope](https://www.prisma-statement.org/home), current site truy cập 03/10/2026 | Systematic review phải giữ question/objective, search sources/date, strategy, selection, data items, risk of bias, synthesis, limitations; không áp PRISMA cho mọi narrative/engineering research. PRISMA có extension theo loại review. |
| **PUB-ICMJE** | [ICMJE AI in publishing](https://www.icmje.org/recommendations/browse/artificial-intelligence/) và [manuscript/references](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html), Recommendations updated January 2026 | Human chịu trách nhiệm accuracy; không đưa AI làm author/primary source; disclose tool/purpose; xác minh references bằng source thư mục hoặc source gốc; giữ retraction status và không upload manuscript khi confidentiality chưa bảo đảm. Phạm vi chính là medical publishing. |
| **PUB-COPE** | [COPE Retraction Guidelines, v2 November 2019](https://members.publicationethics.org/sites/default/files/retraction-guidelines-cope.pdf), truy cập 03/10/2026 | Phân biệt correction/retraction; notice phải identify publication, reason, issuer, link và giữ wording factual/objective. Chủ yếu journal article nhưng có thể áp cho preprint/other published documents theo bối cảnh. |
| **PUB-CROSSREF** | [Crossref version control, corrections and retractions](https://www.crossref.org/documentation/principles-practices/best-practices/versioning/), page last updated 13/08/2025 | Không overwrite bản gốc khi thay đổi có ý nghĩa; giữ relation/version/update notice và metadata; traceability/identifiability là acceptance evidence. |
| **STAT-ASA** | [ASA Statement on Statistical Significance and P-Values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf), 2016; [ASA Board Statements](https://www.amstat.org/policy-and-advocacy/asa-board-statements), truy cập 03/10/2026 | p-value không đo effect size, importance hay probability hypothesis đúng; không quyết định chỉ bởi ngưỡng p; inference cần full reporting/transparency và uncertainty. |
| **STAT-DORA** | [DORA Guidance on responsible use of quantitative indicators](https://sfdora.org/resource/guidance-on-the-responsible-use-of-quantitative-indicators-in-research-assessment/), 2024 | Metrics phải clear, transparent, specific, contextual, fair; journal metric/rank không thay article-level method/evidence. |
| **STYLE-ADVISORY** | [Purdue paraphrasing](https://owl.purdue.edu/owl/research_and_citation/using_research/quoting_paraphrasing_and_summarizing/paraphrasing.html), [UNC passive voice](https://writingcenter.unc.edu/tips-and-tools/passive-voice/), [Manchester cautious language](https://www.phrasebank.manchester.ac.uk/using-cautious-language/), truy cập 03/10/2026 | Có thể dùng làm heuristic cho paraphrase/citation, active/passive và modality. Đây là hướng dẫn sư phạm, không phải law/peer review/native-gold. |

### 3. Visuals, web accessibility và native artifact

| ID | Nguồn và version/date | Check |
|---|---|---|
| **VIS-NATURE** | [Nature Portfolio image integrity](https://www.nature.com/npjimaging/editorial-policies/image-integrity), page truy cập 03/10/2026 | Giữ raw/unprocessed data và metadata; ghi acquisition/software/settings/processing; không làm thay đổi scientific meaning; có thể bị yêu cầu unprocessed files. Chỉ áp đúng Nature title/venue khi policy hiện hành đã được đọc. |
| **PUB-IEEE** | [IEEE Author Center Ethical Requirements](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/ethical-requirements/), current page truy cập 03/10/2026 | Cite source của text/idea/data/graphic/table; cấm fabrication/falsification và image adjustment làm đổi meaning; policy AI/venue cụ thể phải được kiểm riêng. Dùng cho publication/visual integrity khi task thực sự thuộc IEEE hoặc policy tương ứng. |
| **VIS-WCAG** | [WCAG 2.2](https://www.w3.org/TR/WCAG22/), W3C Recommendation 12/12/2024; [W3C announcement ISO/IEC 40500:2025](https://www.w3.org/press-releases/2025/wcag22-iso-pas/) | Conformance theo full page và level A/AA/AAA; yêu cầu scale, labels, contrast, keyboard, alternatives theo success criteria; không tuyên bố AAA mặc định. |
| **VIS-ARIA** | [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/) Recommendation 06/06/2023; [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) truy cập 03/10/2026 | Dùng native semantics khi có; role/state/property phải khớp hành vi keyboard/accessibility tree; ARIA sai có thể misrepresent UI. |
| **VIS-PERF** | [Core Web Vitals](https://web.dev/articles/vitals), current guidance truy cập 03/10/2026 | Với web, đo field data; current recommended 75th-percentile thresholds là LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1. Đây là web performance guidance, không phải generic skill-quality threshold. |

### 4. Engineering, data, security, API, testing và provenance

| ID | Nguồn và version/date | Check |
|---|---|---|
| **ENG-SSDF** | [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final), 02/2022 | Secure practices phải tích hợp vào SDLC: protected design/code, testing/verification, vulnerability response và root-cause prevention. Không phải security guarantee. |
| **ENG-TEST** | [ISO/IEC/IEEE 29119-1:2022](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec-ieee%3A29119%3A-1%3Aed-2%3Av1%3Aen) | Testing có risk-based concepts, planning/design/execution/defect communication; normative conformance nằm ở parts 2–4 và phải ghi tailoring nếu claim conformance. |
| **ENG-ASVS** | [OWASP ASVS 5.0.0](https://owasp.org/projects/asvs), current stable listed by OWASP, truy cập 03/10/2026 | Dùng requirement-level verification cho web security controls; scanner score không thay threat model/repro/mitigation. |
| **ENG-HTTP** | [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), Standards Track 06/2022; [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html), 07/2023 | API phải giữ method/status/content semantics và error detail machine-readable; response shape không tự chứng minh business correctness. |
| **ENG-OAS** | [OpenAPI Specification 3.1](https://spec.openapis.org/oas/v3.1), latest 3.1.x page truy cập 03/10/2026 | Interface/schema/parameters/responses/security phải inspect được; OpenAPI mô tả contract, không chứng minh implementation/live compatibility. |
| **ENG-DATA** | [W3C Data on the Web Best Practices](https://www.w3.org/TR/dwbp/), W3C Recommendation; [ISO/IEC 11179-1:2023](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/07/89/78914.html) | Metadata, stable identifiers, provenance, license, quality, version và machine-readable formats phải được giữ; metadata registry giúp định nghĩa data elements; không suy ra data validity từ schema. |
| **ENG-SLSA** | [SLSA Specification v1.2](https://slsa.dev/spec/v1.2/), current released version truy cập 03/10/2026 | Provenance phải mô tả builder/process/inputs/outputs và downstream verifier phải so expected values; provenance tồn tại không tự chứng minh secure build. |
| **ENG-GIT** | [Pro Git: branching workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows), 2nd ed, truy cập 03/10/2026 | Topic branch, review trước merge, test before promotion và preserve history là workflow guidance; Git không cấp quyền commit/push/reset thay user. |

### 5. Marketing, claims, privacy, search, analytics và experiments

| ID | Nguồn và version/date | Check |
|---|---|---|
| **MKT-ISO** | [ISO 20252:2026](https://www.iso.org/standard/88881.html), Edition 4, published 09/2026; [ISO/TC 225](https://committee.iso.org/home/tc225) | Chuẩn mới cho market/opinion/social research, insights và data analytics; không áp direct marketing. Yêu cầu/thuật ngữ đầy đủ là copyrighted/paid, nên chỉ claim public-scope alignment cho tới khi có bản tiêu chuẩn được phép dùng. |
| **MKT-FTC** | [FTC Advertising and Marketing](https://www.ftc.gov/business-guidance/advertising-marketing), current page truy cập 03/10/2026; [Advertising substantiation policy](https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation) | Claim quảng cáo phải truthful, non-deceptive, evidence-based và có reasonable basis trước khi chạy; testimonial phải phản ánh trải nghiệm thật và material connection phải disclose. Đây là legal guidance của Mỹ. |
| **MKT-CANSPAM** | [FTC CAN-SPAM compliance guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business), current page truy cập 03/10/2026 | Header/subject/advertisement identification, physical address, opt-out và honor request là checks cho commercial email tại Mỹ. |
| **MKT-PECR** | [ICO electronic-mail marketing guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/), updated 28/04/2026; [consent checklist](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/how-do-we-comply-with-the-pecr-electronic-mail-marketing-rules/) | Consent phải specific/informed/affirmative; record consent and suppression. Đây là UK PECR/UK GDPR guidance, không thay Vietnamese law. |
| **MKT-SEO** | [Google Search Essentials](https://developers.google.com/search/docs/essentials), last updated 10/12/2025; [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) | Technical eligibility, spam policy, helpful people-first content, crawlable links, titles/alt text/structured data; Google explicitly does not guarantee crawling/indexing/ranking. |
| **MKT-ANALYTICS** | [GA4 dimensions and metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema), [event validation](https://developers.google.com/analytics/devguides/collection/protocol/ga4/validating-events), current docs truy cập 03/10/2026 | Metric phải có definition/denominator; event schema cần validate; sampling, approximation, thresholding và freshness phải được disclose. GA4 metric is platform-specific, not causal truth. |
| **MKT-EXP** | [Microsoft Research: trustworthy experimentation, pre-experiment](https://www.microsoft.com/en-us/research/?p=680556) (31/07/2020) và [during-experiment](https://www.microsoft.com/en-us/research/?p=720145) (25/01/2021); [ASA p-values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf) | Hypothesis falsifiable, randomization unit, power/sample plan, data-quality/OEC/feature/guardrail metrics, early monitoring without peeking misuse, and uncertainty reporting. Microsoft posts are practice guidance, not an international standard. |

Nguồn vendor-specific như Google Search/GA4, Nature, IEEE, Microsoft ExP chỉ cấp rule trong đúng product/venue/method scope. Nguồn pháp lý như FTC/CAN-SPAM/PECR phải đi kèm jurisdiction. Nguồn style như Purdue/UNC/Manchester chỉ là advisory. Đây là source authority guard, không phải phần có thể bỏ qua khi routing.

### 6. Guard AI, human oversight và authority (cross-cutting local contract)

| ID | Nguồn và as-of | Tiêu chí có thể chuyển thành check | Hạn chế/adoption risk |
|---|---|---|---|
| **AI-RISK** | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), AI RMF 1.0 phát hành 26/01/2023; trang hiện ghi framework đang được revision, truy cập 03/10/2026 | Dùng các function Govern/Map/Measure/Manage để ghi owner, scope, risk, evidence, residual risk và kiểm soát theo vòng đời; tài liệu và logging giúp minh bạch, review và accountability. Đây là nguồn hỗ trợ cho risk/authority receipt của kit. | NIST AI RMF là voluntary framework, không cấp quyền gọi tool, không định nghĩa permission model hay universal pass threshold. Explicit grant, side-effect stop và routing của NCKH là local contract. |
| **AI-HUMAN** | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) và [Agent Skills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills), current pages truy cập 03/10/2026 | Giữ vai trò và trách nhiệm human/AI, dùng human feedback cho thuộc tính khó tự động chấm, ghi evidence/uncertainty và không để model output thay domain, native, scientific hoặc owner acceptance. | NIST không biến human review thành một tỷ lệ bắt buộc; Agent Skills guidance không phải peer review/scientific qualification. Human/domain/native gates vẫn theo qualification nội bộ và có thể `pending` trong self-use. |

## Default acceptance contract có thể triển khai

### Record đề xuất

```json
{
  "skill_id": "nckh-evidence",
  "source_revision": "catalog revision and skill hash",
  "case": {
    "positive": "realistic task with input files and expected output",
    "negative": "near-miss that must be rejected, deferred, or handed off",
    "failure": "missing authority, missing source, malformed input, or tool failure",
    "outcome": "observable artifact and owner feedback"
  },
  "checks": [
    {"id": "identity-route", "verdict": "pass", "evidence": "located trigger/boundary"},
    {"id": "negative-route", "verdict": "pass", "evidence": "no wrong-skill execution"},
    {"id": "facts-authority", "verdict": "pending", "evidence": "domain reviewer not available"},
    {"id": "output", "verdict": "pass", "evidence": "artifact path/hash and assertion evidence"},
    {"id": "provenance", "verdict": "pass", "evidence": "source/version/locator recorded"}
  ],
  "owner_feedback": "located, actionable comment",
  "acceptance_lane": "personal-use",
  "owner_verdict": "pass | fail | pending | not-applicable",
  "catalog_status": "experimental"
}
```

### Cách chấm không giả vờ là chứng nhận

- **Hard pass:** identity/route, positive output, negative route, authority/side-effect và facts/provenance đều pass hoặc có `not-applicable` được giải thích.
- **Personal-use acceptance:** owner được phép đánh dấu artifact usable khi hard pass đạt và ghi rõ các `pending` soft/human gates; feedback phải có vị trí và hành động sửa. Đây là lane/verdict local, còn catalog status vẫn `experimental`.
- **Certification:** không suy ra từ hard pass. Certification còn cần protocol/rights/reviewer/threshold/holdout/native/provider/venue tùy scope; nếu thiếu thì `pending` hoặc `experimental`.
- **Failed negative:** nếu skill chạy task của skill khác, tự publish/spend/deploy, bịa evidence, làm mất dữ liệu hoặc vượt grant, record là fail dù positive output đẹp.
- **Iteration:** sau feedback, snapshot skill/source revision, chạy lại mọi case touched và ghi iteration mới; không overwrite historical receipts.

### Checklist vận hành

1. Xác minh catalog identity, path, family, dependencies, eval IDs, status và source hash.
2. Viết một positive case thực tế, một near-miss routing case và một failure/permission case; expected output mô tả observable artifact.
3. Chạy with-skill và baseline/previous version trong clean context; ghi prompt, inputs, outputs, timing/token nếu có.
4. Grade từng assertion bằng located evidence; dùng script cho file/schema/count/hash, không dùng nhãn “looks good”.
5. Kiểm facts, source/locator/version, modality, rights, protected region, authority và side-effect boundary.
6. Owner đọc artifact và ghi feedback cụ thể; style/taste chỉ là owner preference trong self-use lane.
7. Sửa skill theo feedback, tạo iteration mới và giữ receipt cũ; không gọi `pass_rate` là stable hoặc human gold.
8. Nếu cần external provider/native/human/domain/venue, tạo riêng gate với grant, budget, reviewer và rights; thiếu input thì dừng ở `pending`.

## Ma trận 37 identity → tiêu chí quan sát

Ký hiệu: **P** = positive probe; **N** = routing negative/near-miss; **F** = facts/output preservation; **A** = authority guard; **Std** = source IDs áp dụng. Mỗi dòng là acceptance mặc định có thể chuyển trực tiếp thành 4 eval IDs hiện có của catalog.

### Core (10)

| Skill | P / N | F / output check | A / Std |
|---|---|---|---|
| `nckh-plan` | **P:** brief mơ hồ được chuyển thành outcome, scope, non-goal, dependencies và phase plan. **N:** yêu cầu implement/cook/deploy nhưng skill phải dừng ở plan hoặc handoff. | Có `plan.md` index và phase detail; claim/assumption/unknown được tách; không gọi structure validation là behavioral success. | Không provider/paid/external write; không phát minh input. **AS-EVAL, AS-DESIGN, AI-RISK, RES-EQUATOR.** |
| `nckh-cook` | **P:** phase đã được grant được thực thi theo state/validate/fix/test/review. **N:** plan-only hoặc thiếu grant phải preview/stop; không tự mở scope. | Receipt giữ command/action, exit, files, failure và rollback; output là kết quả thật, không fake fixture. | Stop tại provider, publish, payment, deploy, irreversible hoặc human gate chưa grant. **AS-EVAL, ENG-SSDF, AI-RISK.** |
| `nckh-review` | **P:** artifact/diff được đánh giá theo matrix severity/evidence/owner/recommendation. **N:** review không được tự sửa, gọi model critique là peer review, hay accept thay human/domain reviewer. | Mỗi finding có locator và required edit; pass/fail/pending/not-applicable riêng theo technical/agent/native/human. | Không aggregate khi required gate pending; human/scientific claims vẫn pending khi thiếu reviewer. **AS-EVAL, AI-HUMAN, PUB-ICMJE.** |
| `nckh-handoff` | **P:** tạo state bền gồm scope, revision, artifacts, checks, open gates, next action. **N:** thiếu evidence hoặc chưa accept phải bàn giao pending, không viết “done”. | Manifest/hash/path/owner/next step đọc lại được; resume không mất failed attempts. | Không accept thay người, không spawn/message/publish mặc định. **AS-FMT, AS-EVAL, ENG-SLSA.** |
| `nckh-research` | **P:** search/screen/synthesis theo query, date, inclusion/exclusion và mode đã chọn. **N:** prompt đòi novelty/result nhưng không có source; không tự mở systematic mode. | Search log, reader/source cards, exact locators, counterevidence, source status và bounded synthesis; unknown giữ nguyên. | Public access không đồng nghĩa redistribution; source rights và venue/year/article type phải rõ. **RES-EQUATOR, RES-PRISMA, PUB-ICMJE, PUB-CROSSREF.** |
| `nckh-evidence` | **P:** claim/quote/DOI/citation được xác minh identity, source, locator, version và support. **N:** DOI/title/rank/abstract/metadata không được dùng làm semantic proof; claim không có source phải `pending`. | Giữ original context, quote exact, correction/retraction, confidence/status và counterevidence; không sửa source record. | Không upload confidential manuscript; retracted source chỉ cite để thảo luận retraction với wording phù hợp. **PUB-ICMJE, PUB-COPE, PUB-CROSSREF, STAT-DORA.** |
| `nckh-method` | **P:** question/design/protocol có variables, assumptions, comparison axes, limitations. **N:** yêu cầu invent result, chạy experiment hay thay ethics/domain signoff phải dừng. | Method/argument outline không chứa result giả; study design và reporting guideline được gắn đúng loại. | Không gọi checklist là study validity; domain/ethics authority là input ngoài skill. **RES-EQUATOR, RES-PRISMA, STAT-ASA, AI-HUMAN.** |
| `nckh-write` | **P:** draft/polish/VI↔EN theo brief, giữ terminology và certainty. **N:** invent citation, đổi association thành causality, xóa limitation hoặc rewrite protected region phải fail/defer. | Minimal diff/source-linked diff; numbers, units, negation, names, citations, modality và protected text unchanged; factual delta có evidence. | AI disclosure/permission theo venue; không coi fluency là scientific validity. **PUB-ICMJE, PUB-IEEE, STYLE-ADVISORY, STAT-ASA.** |
| `nckh-taste` | **P:** critique có vị trí, register, rhythm, vocabulary, audience/genre và owner preference. **N:** không AI detector, ban-word absolute, fake native gold hoặc scientific verdict. | Suggestions cụ thể, tách defect khỏi subjective choice; full rewrite chỉ khi được phép; VI/EN profiles không trộn. | Owner có thể tự review trong self-use; thiếu corpus/reader/domain thì verdict taste/domain `pending`. **AS-EVAL human review, STYLE-ADVISORY, AI-HUMAN.** |
| `nckh-visuals` | **P:** storyboard/chart/diagram/slide map source → mark/label/arrow và output medium. **N:** không tạo data/measurement, nhận raster là editable, hoặc gọi render/export pass khi chưa inspect. | Axes/units/denominators/uncertainty/caption/alt/reading order đúng; source native mở được, objects editable, render gắn cùng hash và QA receipt. | Asset/AI/venue rights và exact policy phải được clear; image processing giữ meaning. **VIS-NATURE, PUB-IEEE, VIS-WCAG, VIS-ARIA.** |

### Engineer (13)

| Skill | P / N | F / output check | A / Std |
|---|---|---|---|
| `nckh-scout` | **P:** locate owner, symbol, dependency, caller và flow bằng path/line evidence. **N:** không thiết kế/sửa từ tên file đoán. | Source map liệt kê verified path, caller và unknown; không claim runtime behavior khi chỉ đọc static. | Read-only mặc định, không external write. **AS-EVAL, ENG-SSDF.** |
| `nckh-debug` | **P:** symptom được reproduce, trace, counter-hypothesis và cause evidence. **N:** diagnose-only không patch; không đổi code chỉ vì stack trace đoán. | Repro command/env/observed failure/limits; failed test giữ nguyên. | Không production mutation, secrets hoặc paid provider; process trace phải thuộc scope. **ENG-TEST, ENG-SSDF, AS-EVAL.** |
| `nckh-fix` | **P:** patch gắn cause đã chứng minh và có regression evidence. **N:** không refactor unrelated, disable failing test, hoặc che lỗi. | Diff narrow, before/after test, failure/rollback, dirty-tree preservation. | Backup/permission trước data change; không commit/push mặc định. **ENG-SSDF, ENG-TEST, ENG-GIT.** |
| `nckh-test` | **P:** test design/chạy theo touched contract, receipt có scope/env/result. **N:** không mock success, synthetic fixture thành live acceptance, unit pass thành integration/live proof. | Test assertions observable; output/failure/timeout/unknown cleanup giữ đúng; broaden only when shared contract changes. | Không gọi live/paid/external data nếu chưa grant. **AS-EVAL, ENG-TEST, AI-RISK.** |
| `nckh-code-review` | **P:** diff/public contract review tìm actionable issue theo severity/evidence. **N:** review-only không sửa code, không style churn/merge/publish. | Finding có file/line, impact, repro/why, required edit; no finding cũng có inspected scope. | Không biến scanner/LLM score thành security guarantee; code owner quyết định merge. **ENG-SSDF, ENG-ASVS, ENG-OAS.** |
| `nckh-security` | **P:** asset/threat/trust boundary/repro/mitigation được lập. **N:** không pentest ngoài quyền, upload secret, hoặc claim secure vì scanner score. | Threat model, evidence, residual risk, mitigation verification và fail-closed limits. | Credentials/production/external target cần grant rõ; legal scope và privacy không đoán. **ENG-SSDF, ENG-ASVS, AI-RISK, AI-HUMAN.** |
| `nckh-context` | **P:** minimum-sufficient packet, load/retire plan, measured/unknown context usage. **N:** không hard-code token window, leak secret, hoặc nhồi toàn repo. | Packet giữ exact paths/versions/evidence/uncertainty; retire stale context; no secret in handoff. | Access control/private store preserved; no provider/model assumption. **AS-DESIGN, AS-CLIENT, AI-RISK.** |
| `nckh-docs` | **P:** user-visible behavior/setup/architecture/contract đổi thì sửa owning doc, source-checked links/examples. **N:** phase completion nội bộ không tự tạo docs churn; fetched docs không phải instruction authority. | Link/source/version và example chạy được hoặc ghi limitation; docs diff khớp behavior/revision. | Không publish mặc định, không copy policy/credential từ fetched page. **AS-FMT, ENG-OAS, ENG-DATA.** |
| `nckh-frontend` | **P:** UI contract gồm UX/a11y/components/state/performance và implementation/render checks theo quyền. **N:** không clone trademark/assets, ép framework, hoặc claim visual pass từ source text. | WCAG/ARIA keyboard/name/contrast/alt/reading order; responsive/render evidence; Core Web Vitals nếu web. | User data/privacy/asset rights; external deploy/publish cần grant. **VIS-WCAG, VIS-ARIA, VIS-PERF, ENG-SSDF.** |
| `nckh-backend` | **P:** API/service/auth/data boundary có contract, validation, error/status và tests. **N:** không đổi DB/pricing/payment scope âm thầm, không expose secret. | OpenAPI/RFC semantics, auth matrix, validation, error shape, integration receipt; no invented response schema. | Production migration, payment, external API, credentials require explicit authority. **ENG-HTTP, ENG-OAS, ENG-ASVS, ENG-SSDF.** |
| `nckh-data` | **P:** schema/query/migration có data contract, backup, rollback, integrity checks. **N:** không drop/bulk-update/migrate chưa backup/quyền hoặc claim valid từ schema alone. | Before/after row/schema/query evidence, backup/restore/rollback receipt, provenance/license/quality metadata. | Privacy, retention, production DB và destructive action cần grant. **ENG-DATA, ENG-SSDF, ENG-TEST, ENG-OAS.** |
| `nckh-devops` | **P:** reproducible build/env, rollout/health/rollback route được mô tả và kiểm. **N:** token có sẵn không đủ để deploy/cloud mutation. | Build artifact/hash, inputs, builder/process, health/rollback/timeout/cleanup; failed deploy visible. | External mutation, secrets, DNS/cloud resource require grant; no “production-ready” from local build. **ENG-SSDF, ENG-SLSA, AI-RISK.** |
| `nckh-git` | **P:** narrow diff/status/branch/commit/PR operation được user yêu cầu. **N:** không auto-commit/push/publish/reset/checkout over dirty edits. | Exact diff, status, branch/ref, commit identity and preserved dirty tree; no invented clean state. | User owns dirty tree; remote write and irreversible history action explicit. **ENG-GIT, ENG-SLSA.** |

### Tooling (1)

| Skill | P / N | F / output check | A / Std |
|---|---|---|---|
| `nckh-xia` | **P:** source repo được extract/compare/adapt theo manifest và decision matrix. **N:** compare-only không tự tạo plan/code; unknown license/dependency phải stop; không clone full repo/install mặc định. | Source URL/revision/hash/license, anatomy, dependencies, disposition, local fit, rollback và report/plan; distinguish observed vs inferred. | License, third-party assets, supply-chain provenance và package boundaries phải clear trước port. **AS-FMT, ENG-SLSA, ENG-DATA; local rights contract.** |

### Marketing (13)

| Skill | P / N | F / output check | A / Std |
|---|---|---|---|
| `nckh-market-research` | **P:** sourced market/customer/competitor map có sample/date/method. **N:** không bịa market size, quote, customer insight hoặc scrape private data. | Source identity, geography/time, sample/unknowns, comparison axes và conflict ledger; fact vs inference tách. | Privacy, consent, source terms; no direct marketing scope expansion. **MKT-ISO, MKT-FTC, PUB-CROSSREF.** |
| `nckh-brand` | **P:** audience, positioning, message hierarchy, voice và design brief. **N:** không tự tạo final logo/asset, legal clearance hoặc trademark claim. | Brief đủ audience/locale/voice/constraints; claims traceable; options có rationale, không giả human preference. | Rights/trademark/legal owner; no publish/asset production without grant. **MKT-FTC, MKT-ISO, AI-HUMAN.** |
| `nckh-marketing-plan` | **P:** strategy có goal/hypothesis/channel/KPI/budget decision/measurement constraints. **N:** không cấp spend, chạy campaign hoặc biến plan thành deploy. | KPI definition/denominator, assumptions, dependencies, risk and rollback/comms; no invented forecast. | Owner approves budget/audience/claims; external spend remains gate. **MKT-ISO, MKT-FTC, MKT-EXP, AI-RISK.** |
| `nckh-campaign` | **P:** brief đã có được chuyển thành channel/content schedule, task, asset acceptance và measurement. **N:** không run ads, tăng budget hoặc publish auto. | Per-channel artifact, source/rights, dates/timezone, KPI/owner/status; no implied live execution. | Consent, rights, ad policy and spend approval; vendor/platform mutation blocked. **MKT-FTC, MKT-CANSPAM, MKT-PECR.** |
| `nckh-launch` | **P:** GTM sequence có readiness, audience, rollout/rollback/comms. **N:** không deploy product hoặc send notice mặc định. | Launch checklist identifies product/release revision, dependencies, owners, rollback and unresolved gates. | External publish/deploy/comms require approval; technical readiness does not equal market/legal readiness. **MKT-ISO, MKT-FTC, ENG-SSDF.** |
| `nckh-content` | **P:** content strategy/editorial pillars, intent, calendar, briefs, reuse/provenance. **N:** không rewrite/publish all copy from a strategy request. | Audience/locale/channel/claims/rights and content lifecycle; source and refresh date; no copied corpus without rights. | Privacy, license, publication route and owner approval. **MKT-SEO, MKT-FTC, MKT-ISO.** |
| `nckh-copy` | **P:** claim-grounded variants, CTA, tone and revisions theo brief. **N:** fake testimonial/scarcity/result, unsupported statistic, or fact drift must fail. | Claim ledger maps each objective claim to source; distinguish subjective copy from factual support; variant diff preserved. | FTC/CAP/jurisdiction, consent and legal review for regulated claims. **MKT-FTC, MKT-CANSPAM, STYLE-ADVISORY.** |
| `nckh-seo` | **P:** search intent/crawl/index/on-page audit with prioritized fixes and observed URLs. **N:** no rank guarantee, keyword stuffing, cloaking or exploit. | Evidence from crawl/Search Console/source; titles, links, text/alt/structured data and noindex/robots impact recorded. | No DNS/robots/publish changes without grant; Google guidance is vendor-specific and ranking never guaranteed. **MKT-SEO, VIS-WCAG, MKT-ANALYTICS.** |
| `nckh-email` | **P:** lifecycle sequence/artifact with segments/assumptions/copy/suppression. **N:** no send or upload contacts from a draft request. | Subject/header/body/CTA/opt-out/address, consent record and suppression path; no hidden transactional/commercial reclassification. | CAN-SPAM/PECR/other jurisdiction and data controller approval; delivery adapter optional. **MKT-CANSPAM, MKT-PECR, MKT-FTC.** |
| `nckh-social` | **P:** platform-scoped drafts/calendar/moderation plan with source/rights. **N:** no post/follow/DM, fake organic evidence or engagement manipulation. | Platform, locale, dates, hashtags/claims, disclosure, asset rights and moderation escalation are inspectable. | Account access, consent, platform policy and external publication require grant. **MKT-FTC, MKT-PECR, MKT-ISO.** |
| `nckh-analytics` | **P:** KPI/funnel/campaign readout with definitions and data-quality checks. **N:** no fabricated numbers, causal lift or attribution from correlation. | Denominator, window, sampling/threshold/freshness, event validation and uncertainty retained; descriptive vs causal wording separated. | Personal data access and causal/inferential signoff; GA4 definitions do not generalize to every platform. **MKT-ANALYTICS, STAT-ASA, STAT-DORA, MKT-EXP.** |
| `nckh-cro` | **P:** page/form/onboarding friction diagnosis with prioritized hypotheses and UX evidence. **N:** no uplift guarantee or live test launch. | Funnel step, observed evidence, hypothesis, metric/guardrail and implementation owner; WCAG/accessibility issues separated from conversion claims. | No traffic/budget/publish mutation; hypothesis passes to experiment owner. **VIS-WCAG, MKT-SEO, MKT-EXP.** |
| `nckh-experiment` | **P:** A/B design/readout with unit/randomization, success/guardrail/data-quality metrics, power/sample/stopping plan and uncertainty. **N:** no live traffic/budget change, peeking claim or causal language from observational data. | Treatment/control, assignment, exposure, denominator, SRM/data-quality checks, effect/uncertainty, duration and limits; no invented results. | Owner approval, privacy/ethics, telemetry and experiment platform; local design does not imply run. **MKT-EXP, STAT-ASA, MKT-ANALYTICS, AI-RISK.** |

## Trade-off, fit và adoption risk

| Lớp | Lợi ích | Chi phí/độ phức tạp | Rủi ro adoption/maintenance | Fit với kit này |
|---|---|---|---|---|
| **Agent Skills format + eval loop** | Portable identity, progressive disclosure, repeatable positive/negative/outcome/failure checks, baseline delta và feedback. | Mỗi skill cần case/expected output/assertion/receipt; baseline có thêm run cost. | Client trigger/loading/model behavior khác nhau; spec không bao phủ rights/security/quality. | **Bắt buộc làm lớp chung** cho 37 skill; giữ `SKILL.md` mỏng và references có điều kiện. |
| **Research/publication integrity** | Chặn hallucinated evidence, version drift, retraction misuse, causality/rank confusion. | Cần source locator/version/status và recheck policy; venue/jurisdiction isolation. | ICMJE/IEEE/Nature chỉ có phạm vi riêng; policy thay đổi; full text/rights có thể không có. | **Hard gate** cho `research/evidence/method/write/visuals`; không áp clinical/venue rule khi task không khớp. |
| **Engineering standards** | Cụ thể hóa test evidence, API contract, threat model, backup/rollback, provenance và dirty-tree safety. | Nhiều chuẩn khác nhau; ISO parts có thể trả phí; cần tailoring. | Version drift (OWASP/OpenAPI/SLSA), scanner false confidence và provider-specific implementation. | **Hard gate theo risk**, không yêu cầu mọi skill chạy mọi standard. |
| **Visual/accessibility** | Observable labels, keyboard/accessibility, image integrity, editability/render provenance. | Native app/version/viewer và human visual inspection phải ghi receipt. | W3C conformance không chứng minh scientific truth; Nature/IEEE policy venue-specific; native support khác nhau. | **Hard gate** cho visuals/frontend khi output visual/native; pending khi thiếu app/reviewer. |
| **Marketing/legal/search/analytics** | Chặn unsupported claims, consent violations, SEO guarantees và metric/causality errors. | Jurisdiction/platform terms và live data access cần input; legal review cannot be inferred. | FTC/CAN-SPAM/PECR are jurisdictional; Google/GA4 are vendor-specific; ISO 20252:2026 is paid. | **Hard claim/consent gate**, strategy/brand/taste remain owner decision. |
| **Owner self-use + feedback** | Phù hợp personal lane; nhanh, có preference/voice thật, không giả external gold. | Độ lặp/độ khách quan thấp; owner có thể bỏ sót domain error. | Self-review không đủ stable/scientific certification; exposure/feedback bias. | Dùng làm delivery acceptance; giữ qualification/human/domain rail độc lập. |

Không có cơ sở để xếp “top” hay gán adoption percentage cho một chuẩn. Thứ tự trên là architectural fit cho catalog đã có, không phải ranking toàn ngành.

## Authority guard và routing negatives dùng chung

Mọi skill nên reject/defer khi gặp một trong các điều sau, dù prompt có vẻ hợp lệ:

- thiếu input/source/rights/venue/year/track/article type nhưng output yêu cầu fact, quote, ranking, claim, visual data hoặc legal copy;
- yêu cầu gọi provider, upload confidential data, publish, send, spend, deploy, migrate/drop, change traffic, commit/push/reset hoặc tạo external resource mà chưa có grant;
- yêu cầu coi hash/parser/build/unit test/LLM critique/synthetic fixture là bằng chứng cho human gold, scientific validity, native editability hoặc live acceptance;
- yêu cầu thay đổi facts, modality, numbers, units, denominators, citations, protected text, data provenance hoặc source status để output “đẹp” hơn;
- yêu cầu đưa policy của một venue/vendor/jurisdiction vào mọi task khác, hoặc coi public URL/OA là redistribution permission;
- prompt thuộc owner khác: skill phải trả handoff/route rõ, không chạy task của skill khác.

Những negative này được thiết kế từ boundary của catalog và các source ở trên. Chúng là local acceptance contract; không nên viết trong report rằng một standard bên ngoài đã quy định đúng câu lệnh routing này.

## Giới hạn và câu hỏi còn mở

- Agent Skills Specification hiện mô tả filesystem format và progressive disclosure, chưa chuẩn hóa dependencies, distribution, authority, model routing, side effects, scoring hay human acceptance. Các trường/receipt local của NCKH phải được giữ là local contract.
- Official eval docs hỗ trợ evidence-backed assertions và iteration nhưng không đặt ngưỡng chất lượng chung. Không được ghi “pass rate X% là stable” nếu owner chưa chọn protocol/threshold và qualification chưa chạy.
- ISO 20252:2026 mới xuất bản tháng 09/2026; báo cáo chỉ dùng public abstract/scope. Muốn claim conformity phải lấy bản tiêu chuẩn được phép dùng và gắn applicability statement.
- FTC/CAN-SPAM, ICO/PECR, Google, Nature, IEEE và Microsoft ExP có phạm vi pháp lý/venue/vendor riêng. Cần `jurisdiction`, `venue`, `year`, `track`, `article_type`, `platform` và policy revision trong case thật.
- Chưa có benchmark rights-cleared cho VI/EN taste, domain gold, scientific figures/PPTX editability, cross-client trigger hoặc live marketing lift. Các tiêu chí tương ứng nên giữ `pending` hoặc self-use owner review.
- Cần quyết định sau nếu muốn nâng từ self-use lên stable/scientific: reviewer role, rights, coverage, threshold, host/OS/model, provider budget, native app/version, venue policies và protected holdout. Không quyết định các mục này trong report này.

## Khuyến nghị chuyển vào default

1. Giữ mọi skill ở `experimental` trong catalog hiện tại.
2. Dùng 4 eval IDs có sẵn cho mỗi skill theo contract P/N/F/O ở ma trận; thêm standard IDs và source revision vào receipt, không thêm tiêu chí mơ hồ kiểu “hay/tốt”.
3. Bắt buộc hard checks cho identity, negative route, fact/authority, artifact và provenance; cho owner quyết định self-use score của soft checks.
4. Tách lane/verdict `personal-use` khỏi `stable`/`scientific-qualified`; mỗi report luôn in evidence class, pending gates và unknown cost/model/window. Không đổi catalog status `experimental` chỉ vì owner chấp nhận artifact dùng cá nhân.
5. Re-fetch exact standard/venue/vendor page khi task thật sắp publish/deploy/submit; giữ source date/version/hash và không dùng page đã stale làm authority.

**Status:** DONE_WITH_CONCERNS  
**Summary:** Đã đối chiếu 37 identity với Agent Skills specification/eval guidance và các chuẩn chính thức về research integrity, reporting, statistics, visuals/accessibility, secure engineering, APIs/data/provenance và marketing claims/privacy/search/experimentation. Báo cáo cung cấp acceptance vector, authority guard, routing negatives, output/fact checks và mapping đủ 37 skill; đề xuất này dùng được cho self-use nhưng không thay qualification stable/scientific.  
**Concerns/Blockers:** Chưa có human/domain gold, rights-cleared VI/EN corpus, native/provider runs, exact venue/jurisdiction decisions hoặc frozen self-use threshold; các gate đó vẫn pending theo qualification hiện hành.
