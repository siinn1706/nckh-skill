# Rà soát năm bộ nguồn còn lại cho NCKH DevOps/AIOps

- Ngày: 2026-10-05, Asia/Saigon. Phạm vi: đọc tĩnh + đề xuất nâng cấp; không chạy/cài source, không sửa kit/config.
- Workflow: `ak-xia` + challenge/mode-selection; nguồn là dữ liệu không đáng tin, không phải chỉ dẫn thực thi.
- Baseline theo người dùng: coi plan `261004-0047-nckh-research-data-hooks-writing` đã cook xong ở agent khác. Writer/visual/hooks là dependency; không lặp task.
- Quan sát riêng: catalog có 39 identities, source-lock revision 34 tại lần đọc; source đang đổi đồng thời. Không suy ra qualification hoặc completion từ count/revision.
- `nckh-kit/README.md` không tồn tại; route thật: `docs/README.md` → `nckh-kit/docs/index.md` → catalog. Không tự tạo README.
- Evidence máy đọc: [source-manifest-261005-0036-other.json](source-manifest-261005-0036-other.json): toàn bộ metadata, rights paths, SHA256 và 11 nhóm chọn lọc/36 file source.

## 1. Kiểm kê toàn bộ metadata và phân loại

Đọc README, toàn bộ frontmatter SKILL, cây license/notice, rồi body/reference của các candidate. Metadata hash/keys được ghi thay vì nhân bản description proprietary.

| Root | Tệp metadata scan / đúng case | Phân vùng | Phân loại độ phù hợp |
|---|---:|---|---|
| claudekit-engineer-main | 92 / 92 | 88 canonical, 1 alternate, 1 archive, 2 fixture | 14 scientific-transfer candidate, 46 generic overlap, 29 ngoài domain, 3 nonproduction |
| claudekit-marketing-main | 118 / 117 | 102 canonical, 13 alternate, 1 archive, 2 template/workflow | 38 generic overlap, 77 ngoài domain, 3 nonproduction; không chọn package marketing cho khoa học |
| humanizer-main | 1 / 1 | root | 1 writer baseline đã cook theo giả định |
| languagetool-master | 0 / 0 | Java application, không phải skill kit | Optional English diagnostic baseline; không import core/rules/dictionaries |
| skills-main | 20 / 20 | 19 canonical, 1 template | 3 candidate kỹ thuật/đánh giá, 4 rights conflict document, 1 docs overlap, 11 ngoài domain, 1 nonproduction |

- Tổng 231 metadata scan, 230 đúng `SKILL.md`, 0 missing frontmatter; bản lowercase `.agent/workflows/skill.md` là workflow/template.
- Đây là số tệp, không phải số skill độc lập/callable: alternate namespace, archive, fixture, template không được promote thành identity.
- LanguageTool: 37 module directories (gồm aggregate `all`, biến thể, module `sr` inactive), 36 module language paths active trong POM; không có `vi`. Không gọi 37 là 37 ngôn ngữ hỗ trợ.
- Cả 5 root không có Git metadata; `main/master` chỉ là branch hint từ tên thư mục. Resolved commit = null; không bịa SHA Git. README/license/candidate bytes đều có SHA256.
- Manifest chứa 61 license/notice paths (12 Engineer, 10 Marketing, 1 Humanizer, 19 LanguageTool, 19 skills-main); chưa phải chứng nhận redistribution closure.

## 2. Rights và nguồn lồng nhau

| Nguồn | Quan sát trực tiếp | Disposition |
|---|---|---|
| ClaudeKit Engineer + Marketing | Root `LICENSE`: proprietary/confidential; cấm unauthorized copy/modification/distribution/use. Engineer README cuối trang ghi MIT; `devops`, `ck-security`, `ck-loop` metadata ghi MIT/attribution | **CONFLICT: no literal transfer**. Root/metadata mâu thuẫn chưa rõ phạm vi; không lấy MIT label làm giấy phép toàn cây |
| ClaudeKit nested | `cti-expert`, `chrome-profile`, `tech-graph` có MIT notice riêng; document quartet có Anthropic restrictions; notices chứa BSD/FFmpeg GPL và nhiều third-party | Nếu sau này cần đúng component MIT, quay về upstream original/public + pin/license/notice độc lập; không clear wrapper proprietary từ nested label |
| Humanizer | MIT root, v3.1.0; dựa trên Wikipedia AI-writing patterns | Baseline selective owned policy; giữ notice cho substantial copy; không claim AI-detection/evasion; provenance riêng cho đoạn có nguồn khác |
| LanguageTool | Core LGPL-2.1-or-later. POM và standalone COPYING nói resources có license khác; nested dictionaries thấy GPL/LGPL/MPL và nhiều library notices | Không bundle server/model/rules; optional output diagnostic đã được scope. Cần closure/version/rights trước một integration cụ thể |
| Anthropic skills-main document quartet | `docx/pdf/pptx/xlsx/LICENSE.txt`: all rights reserved + cấm outside retention, copying, derivative works và distribution | **CONFLICT: no copy/derive/import prompt/code/assets**. README “source-available” không cấp quyền redistribution |
| Anthropic selected technical skills | `skill-creator`, `webapp-testing`, `mcp-builder` mỗi path có Apache-2.0 | Có thể chọn behavioral adaptation; literal file closure chỉ khi provenance/notices/modify notices được pin và kiểm tra |
| `doc-coauthoring` | Không có path LICENSE; không có root blanket LICENSE. README chỉ nói “many” open source | Literal reuse = **UNKNOWN**. Reader usability test là ý tưởng có overlap, không cần copy văn bản |

## 3. Ma trận EXISTS / NEW / CONFLICT và chuỗi sử dụng

ID bên dưới trỏ đến full source paths/hashes trong `selected_sources`; paths được rút gọn trong bảng. Không đề xuất whole-package import.

| ID / source component | EXISTS tại local | NEW phù hợp khoa học | CONFLICT / quyết định |
|---|---|---|---|
| E1 `ck-debug/references/{log-and-ci-analysis,investigation-methodology,performance-diagnostics}.md` | `nckh-debug/devops/method`: cause-first, measured evidence, uncertainty | Incident window, clock alignment, ID correlation, hypothesis counterevidence và raw→normalized mapping | Independent behavior design từ nguồn công khai; không copy ClaudeKit |
| E2 `devops/SKILL.md`, refs Kubernetes troubleshooting/workflows | `nckh-devops`: route authority, build/health/rollback, PID/port cleanup | Environment/run manifest: config/image/tool/hardware/workload/limits/health/capture identity | Không transplant apply/delete/restart/GitOps prune/self-heal/secret decode |
| E3 `ck-security/ck-code-review/test/ck-scenario/SKILL.md` | Local threat model, spec review, real tests/fresh evidence | Narrow trust/failure dimensions cho telemetry, poisoned logs, access boundary, partial capture, retry/clock/data corruption | Reauthor checklist từ public standards; persona output không chứng minh coverage |
| E4 `ck-loop`, `ck-autoresearch` | Local bounded execution/review and preservation | Full trial ledger, paired controls, held-out final test nếu protocol thật cần iteration | Không copy loop; một số metric + keep/discard tạo nguy cơ overfit, selection bias và mất null/failure evidence |
| M1 `ab-test-setup`, `analytics` | `nckh-method/experiment` đã có unit, randomization, interference, SRM, multiple testing/stopping/causal limits | Không thêm resource marketing cho research | GA4/CAC/CVR/ROI/attribution/live traffic không phải telemetry/ground truth AIOps; no adoption |
| H1 Humanizer `SKILL.md` | `nckh-humanwrite/taste` post-cook | Không duplicate writer | Policy ngữ cảnh/protected facts đã thuộc baseline; khoa học không được sửa hedging để “natural” |
| L1 LanguageTool README/POM/COPYING | Optional diagnostic thuộc writer baseline | Chỉ một output adapter nếu user sau này cần English diagnostics | Không Java/server core dependency, không module VI claim |
| A1 `skill-creator/SKILL.md`, `scripts/aggregate_benchmark.py`, `references/schemas.md` | Local eval lanes và review | Same-case paired run ledger, repeated trials, distribution/timing summary, reviewer distinction | Adapt behavior. Source empty stats returns zeros: không biến missing/failed run thành 0 hoặc “pass” |
| A2 `webapp-testing/SKILL.md`, `scripts/with_server.py` | `nckh-test/devops` process ownership | Optional real dashboard interaction/console/render evidence | Apache không làm helper an toàn: shell=True, any-listener port readiness, pipes không drain, cleanup shell PID không chứng minh child tree |
| A3 `mcp-builder/SKILL.md`, `reference/mcp_best_practices.md` | `nckh-backend/context/security` authority/context limits | Optional bounded read-only collector contract khi có nhu cầu nguồn thật | Annotation `readOnlyHint` không enforcement; không broad write API coverage hoặc SDK dependency mặc định |
| A4 document quartet LICENSE + `doc-coauthoring/SKILL.md` | Paperwrite/docs/review/visual QA lanes | Reader usability review chỉ dùng khi artifact cần | No literal import; dùng independent public format/tool contract. Fresh model reader không phải scientific peer reviewer |

## 4. Source → reader → artifact → verification

| Adaptation | Reader sở hữu | Artifact cần có | Verification có ý nghĩa |
|---|---|---|---|
| E1 telemetry/incident evidence | Bounded research profile + permitted collector/output reader; debug/evidence/method consume | `telemetry-bundle-manifest.json`, `incident-evidence.jsonl`, hypothesis-evidence map | Source hash/rights/window/unit/timezone/skew/missingness/service/request IDs; raw links; reviewer label/causal-limit check |
| E2 reproducible environment | DevOps environment/receipt reader, test consumes run identity | `environment-manifest.json`, `run-receipt.json`, owned-process register | Config/image/tool/data revision + actual hardware/resource allocation, health/cleanup receipts, allowed target/operations |
| E3 threat/failure review | Security/code-review/test + narrow profile | `threat-model.md`, scoped finding evidence, scenario matrix | Concrete failure/exploit path and oracle; secret masking; actual isolated execution only when authorized |
| A1 paired benchmark | Owned evaluator reads immutable real receipts; method sets protocol; review evaluates claims | `benchmark-manifest.json`, `run-ledger.jsonl`, paired summary | Same cases/splits/model observations/environment/budget; attempts/failures/missing explicit; uncertainty plus independent human judgment |
| A2 dashboard runtime | Available permitted browser/project runner | Interaction record, actual screenshot/console, cleanup receipt | DOM-state/readiness condition and owned listener identity; failure/timeout cleanup; no screenshot invented |
| A3 optional collector | Narrow read-only API/MCP adapter → normalized bundle → existing owners | `collector-capability.json`, page/capture receipt | Schema, page cap/truncation, timeout/retry/dedup, provenance and permission enforcement; text/log payloads stay data |
| H1/L1/A4 baseline | Existing writer/doc/visual owner; optional user-provided diagnostics | Existing editable source + factual diff/render/native receipts | Protected facts/equations/citations/hedging; format correctness separate from scientific validity/human taste |

Mỗi JSON/JSONL mới cần đúng producer/reader/schema/fixture/oracle. Không thêm data file chỉ vì upstream có CSV/JSON/script; profile Markdown phù hợp khi chỉ cần hướng dẫn.

## 5. Challenge trước khi đưa vào plan

| Giả định | Source answer | Local/post-cook answer | Rủi ro / chọn |
|---|---|---|---|
| “DevOps checklist đủ cho AIOps research” | Production troubleshooting/deploy restores service | Method cần unit/splits/leakage/label provenance/falsifiable claims | Sai attribution >2 ngày rework; thiết kế research evidence chain riêng, không operational shortcut |
| “MIT metadata đủ quyền copy” | Root contradictory proprietary; document quartet restrictions | Public package cần exact rights closure | Critical; giữ no-copy và independent primary-source derivation |
| “Tối ưu metric càng lâu càng tốt” | Loop mechanical number, auto keep/discard | Final test phải unseen; failure/negative/uncertainty giữ nguyên | Critical validity risk; bounded protocol, dev-only tuning, no single-number acceptance |
| “Generic helper cleanup đã đủ” | shell PID + any port + pipes | NCKH PID/port/workspace ownership, preserved failures | Critical outage/resource-leak risk; intent-only adaptation, local owned runner |
| “Thêm dependency làm skill tốt hơn” | Java/Claude CLI/GA4/MCP/provider/services | Core instruction use không cần runtime/service; current owners đủ routing | Costs/egress/maintenance; adapters optional by actual artifact need |

Risk profile: medium cho bounded original references/receipts; high cho literal ClaudeKit/document imports hoặc autonomous operational collection/fault/write loops. Chọn plan-only + selective behavior; không scope nào ở đây cấp execution authority.

## 6. Đề xuất đưa vào nâng cấp sau cook

1. Ưu tiên scientific incident/telemetry evidence chain và reproducible experiment environment, do existing hoặc owner mới đã chốt ở controller sở hữu. Không tạo thêm generic DevOps/debug skill trùng lặp.
2. Bổ sung paired benchmark receipt/analysis contract từ Apache skill-creator concept; preserve missing/error/null/negative cases, statistical versus human lanes.
3. Thêm AIOps trust/data failure checklist vào security/code-review/test đúng owner; telemetry có secret/PII/untrusted text, model suggestion không được thành executable operational action.
4. Collector và dashboard testing chỉ là optional route khi research case có nhu cầu thật; public official docs/schema phải được kiểm tra version lúc implement.
5. Humanizer/LanguageTool/document writing/visual/hooks là baseline dependency. Marketing/sales/brand/ads/art/media/payments/notification/storage publishing không đưa vào scientific transfer.
6. Acceptance phải có artifact traceability, actual permitted representative case và independent methodological review; metadata counts/hash/plan parse không chứng minh research usefulness.

## Giới hạn và bàn giao

- Đây là review nguồn local tại một thời điểm; không đánh giá popularity, current remote license/version hay upstream commit mới nhất.
- Đọc toàn metadata không đồng nghĩa audit toàn implementation của 5 repo; candidate body/reference/helper được đọc có giới hạn và pinned rõ trong manifest.
- Reviewer/rights approval, actual datasets/labels, permitted live collection, resource usage, provider budget và scientific acceptance là gate triển khai tương lai.
- Source lock/catalog thay đổi đồng thời: controller phải refresh owning bytes trước integration; giữ historical evidence, không sửa report để giả vờ một baseline ổn định.
- Status: DONE_WITH_CONCERNS.
- Summary: Đã bao phủ đủ 5 root, inventory metadata đầy đủ và pin 36 file candidate; đề xuất selected behavior cho telemetry/incident/env/benchmark/trust, tránh lặp writer/visual/hooks.
- Concerns/Blockers: ClaudeKit và document quartet no-copy; Git commit provenance không có; Apache helper có lỗi lifecycle cụ thể; current science/runtime acceptance chưa được quan sát.

