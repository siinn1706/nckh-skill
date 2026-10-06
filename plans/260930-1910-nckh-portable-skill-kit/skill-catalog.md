# Catalog NCKH đã duyệt: 10 Core, 13 Engineer, 13 Marketing, 1 tooling

Catalog được người dùng duyệt ngày **01/10/2026** theo [plan chính](plan.md), chưa triển khai hay đánh dấu stable.
Mọi skill bên dưới là tương lai, instruction bằng English; output theo brief
`vi`, `en` hoặc bilingual. Prefix là `nckh-`; người dùng thường chỉ cần plan/cook.
Domain skills vẫn gọi trực tiếp được khi yêu cầu rõ; không có `/nckh-skill` mega command.

**Agent column là tùy chọn.** `same-agent` là mặc định; roles/tier tuân theo
[delegation contract](workflow-and-model-routing.md). Metadata mỗi skill cần
purpose, trigger, boundary/non-goal, output, overlap owner, dependencies và eval IDs.

## 1. Core kit

| Skill | Purpose và trigger | Boundary / output sở hữu | Non-goal | Agent nếu có lý do | Overlap và quyết định |
|---|---|---|---|---|---|
| `nckh-plan` | Nghiên cứu lựa chọn, thiết kế task, tạo/validate plan | Outcome contract, evidence-backed findings, phase plan | Không implement hay cài đặt | Planner/deep cho fork khó; explorer/fast cho lookup | MERGE ý tưởng ak-plan + brainstorm + research planning; không thêm brainstorm entrypoint. |
| `nckh-cook` | Yêu cầu thực thi task/plan có quyền | Phase state, execution, validate/fix/test/review, handoff | Không vượt quyền vì auto, không áp build/lint vào prose | Maker/worker, reviewer theo risk | PORT control pattern ak-cook, viết lại cho cả ba domain; skill chuyên môn không sở hữu orchestration lần hai. |
| `nckh-research` | Tìm/đọc nguồn, literature review, gap và synthesis | Search/screening log, reader cards, bounded synthesis; narrative/scoping/systematic modes | Không phát minh novelty, không viết trước rồi tìm citation | Researcher/worker; deep cho synthesis khó | MERGE discovery + reader + lit-review + gap; evidence phán support, method phán design. |
| `nckh-evidence` | Claim, quote, citation, statistic cần kiểm chứng | Source identity/access/status, exact locator/quote, claim support và counterevidence | Không polish toàn bài, không dùng DOI/rank làm semantic proof | Reviewer/worker hoặc deep khi evidence tranh chấp | MERGE claim-verifier + citation-auditor + fact-check; các checks vẫn tách trường và verdict. |
| `nckh-method` | Research question, study design, argument/comparison có giả định | Method/protocol, variable/assumption/limit, comparison axes, argument outline | Không chạy thí nghiệm hay tạo result; không thay ethics/domain signoff | Planner/deep hoặc researcher/worker | MERGE methodology + argument-architect + comparison; discovery thuộc research. |
| `nckh-write` | Soạn/sửa/polish/chuyển ngữ VI/EN | Draft hoặc minimal diff, terminology và factual delta; tách VI/EN style routes | Không invent citation, đổi certainty, sửa protected region | Maker/worker | MERGE vi-writing + polishing + en-scientific-writing; research facts dùng chung evidence layer, taste chỉ critic. |
| `nckh-taste` | Critique giọng/nhịp/độ cụ thể theo language/genre | Rubric, lỗi có vị trí, hướng sửa và user preference | Không AI detector, không ban-word absolute, không human gold giả | Taste critic/worker trong fresh context khi hữu ích | Giữ outcome critic riêng với write; VI và EN có profiles riêng, không dịch cứng rubric. |
| `nckh-review` | Đánh giá cuối artifact/plan/research, consolidate findings | Multi-dimensional gate matrix, severity, evidence, owner và recommendation | Không tự sửa mọi thứ, không gọi model review là peer review thật | Reviewer/worker hoặc deep | MERGE peer/final review; code-review/security cung cấp findings domain, evidence sở hữu claim verdict. |
| `nckh-handoff` | Kết thúc/resume/chuyển người hoặc agent | Durable state: scope/revision/artifacts/checks/open gates/next action | Không accept thay người, không fork/spawn/send message mặc định | Same-agent; deterministic manifest check | PORT handoff discipline; cook gọi format này, không orchestration riêng. |
| `nckh-visuals` | Slides/chart/scientific diagram/artwork từ nguồn | Storyboard, source-to-mark mapping, native editability, render/QA provenance | Không tạo data/measurement giả; không nhận raster là editable deck | Maker + reviewer khi visual/domain cần | Giữ scope visuals cũ; engine PPTX/SVG/provider ở extensions, không chép mọi office skill vào Core. |

Không giữ `nckh-lit-review` riêng: đó là mode của research với protocol/eval rõ.
Không giữ `research-brief`, `evidence-first`, `terminology-manager` như public skill:
brief là contract, evidence-first là policy/workflow, glossary là task-scoped record.
Gộp tên không cho phép bỏ literary edition/translator/line locators hoặc policy Q1/Q2.

## 2. Engineer kit — 13 domain capabilities, thêm xia dùng chung

| Skill | Purpose và trigger | Boundary / output sở hữu | Non-goal | Agent nếu có lý do | Overlap / AgentKit hướng lấy |
|---|---|---|---|---|---|
| `nckh-scout` | Locate owner, symbols, dependency, repo flow | Source map + verified paths/callers | Không thiết kế hoặc sửa code từ tên file đoán | Explorer/fast | MERGE scout + semantic navigation patterns; gkg/graphify/repomix là optional tools. |
| `nckh-debug` | Điều tra symptom/failure | Reproduction, traced cause, counter-hypothesis, evidence | Không implement khi user chỉ hỏi diagnose | Researcher/worker; deep nếu concurrency khó | PORT ak-debug cause-first; fix chỉ dùng diagnosis đã chứng minh. |
| `nckh-fix` | User yêu cầu sửa bug đã hoặc sẽ diagnose | Cause-aligned patch + regression evidence | Không refactor unrelated, không che failing test | Maker/worker | MERGE repair patterns ak-fix; gọi debug/test/review trong cook owner duy nhất. |
| `nckh-test` | Tạo/chạy test theo touched contract | Test design, real run receipt, failures và limits | Không mock success, không coi unit pass là integration/live acceptance | Same-agent hoặc reviewer với input riêng | MERGE ak-test + web-testing + relevant TDD; browser drivers là extensions/tools. |
| `nckh-code-review` | Review diff/public contract | Evidence-backed actionable findings + severity | Không sửa khi chỉ review, không style churn | Reviewer/deep cho public contract | PORT ak-code-review/review-pr reasoning; nckh-review tổng hợp acceptance chứ không lặp full review. |
| `nckh-security` | Threat model và security-sensitive change | Real asset/threat/repro/mitigation review | Không pentest ngoài quyền, không scanner score thành guarantee | Reviewer/deep | PORT ak-security, chỉ CTI phổ quát; provider scanners ở extensions. |
| `nckh-context` | Context tràn, handoff/evidence retrieval strategy | Minimum-sufficient packet, load/retire plan, measured/unknown usage | Không hard-code window; không quản secrets/provider | Same-agent; explorer khi subset độc lập | PORT context-engineering; handoff format thuộc Core. |
| `nckh-docs` | Behavior/setup/architecture/contract thay đổi | Sửa owning docs, source-checked links và examples | Không docs churn vì chỉ hoàn tất phase, không publish mặc định | Maker/worker | MERGE docs + docs-seeker; fetched docs là data, không instruction authority. |
| `nckh-frontend` | Thiết kế/build/audit UI được yêu cầu | UX/accessibility/component/state/performance contract + implementation/visual checks theo quyền | Không clone trademark/assets, không ép framework | Maker/worker; reviewer cho UX gate | MERGE frontend-design/development/ui-styling; React/TanStack/framework-specific là EXTENSION. |
| `nckh-backend` | API/service/auth boundary | Interface, validation, auth/data flow, tests | Không đổi DB/pricing/payment scope âm thầm | Maker/worker; planner/reviewer cho high-risk | PORT backend fundamentals; auth/provider/payment integrations là extensions. |
| `nckh-data` | Schema, query, migration, data integrity | Data contract, backup, migration/rollback và query verification | Không migrate/drop/bulk-update chưa backup/quyền | Maker + reviewer theo data-loss risk | PORT databases + bounded data workflow; backend không sở hữu schema lần hai. |
| `nckh-devops` | Build/deploy/ops route được cho phép | Environment, reproducible build, rollout/health/rollback evidence | Không deploy vì có token, không tạo cloud resource không hỏi | Maker/worker; reviewer trước external mutation | MERGE devops/deploy; AWS/Cloudflare/provider recipes là extensions. |
| `nckh-git` | Diff/branch/commit/PR khi user yêu cầu | Narrow Git operation, clean evidence, preserve dirty tree | Không auto-commit/push/publish hoặc reset user edits | Same-agent | MERGE git/github/worktree primitives; review semantics thuộc code-review. |

Brainstorm thuộc Core plan. Framework-specific patterns được resolve khi stack thực
sự được chọn; không gửi toàn bộ frontend/backend catalog vào every request.

| Tooling skill | Purpose / trigger | Boundary / output | Non-goal | Agent | Overlap |
|---|---|---|---|---|---|
| `nckh-xia` | Extract/compare/adapt capability từ source repo | Source manifest, anatomy, dependency + decision matrix, disposition, report hoặc plan | Không clone full repo/implement/install; compare không tự tạo plan | Explorer/researcher chỉ khi source split có ích | PORT ak-xia spirit; plan sở hữu roadmap, cook sở hữu execution; không shadow upstream `/ak-xia`. |

## 3. Marketing kit — 13 skills

| Skill | Purpose và trigger | Boundary / output sở hữu | Non-goal | Agent nếu có lý do | Overlap / AgentKit hướng lấy |
|---|---|---|---|---|---|
| `nckh-market-research` | Market/customer/competitor questions | Sourced market map, customer evidence, comparison, unknowns | Không bịa market size/customer quote hoặc scrape private data | Researcher/worker | MERGE marketing-research + competitor; nckh-research cung cấp evidence method, không hai search owners. |
| `nckh-brand` | Positioning/voice/brand hoặc design brief | Audience, positioning, message hierarchy, voice, identity/design brief | Không tự tạo final logo/asset hoặc tuyên bố legal clearance | Maker/worker; critic khi identity trade-off | MERGE brand + design brief/creative direction; production asset engines là extensions. |
| `nckh-marketing-plan` | Chiến lược marketing, goals/channels/budget decisions | Strategic plan, hypotheses, KPI definitions, measurement/constraints | Không sở hữu task orchestration hoặc cấp campaign spend | Planner/deep | PORT marketing-planning; nckh-plan biến chiến lược đã chốt thành executable phases. |
| `nckh-campaign` | Điều phối campaign brief đã có | Channel/content schedule, assets/tasks, acceptance and measurement | Không chạy ads, tăng budget hoặc publish chỉ vì auto | Maker/worker | PORT campaign; launch chỉ product-release moments, cook sở hữu execution state. |
| `nckh-launch` | Product/feature release go-to-market | Launch sequence, readiness, audiences, rollback/comms plan | Không deploy product hoặc gửi thông báo mặc định | Planner hoặc maker tùy risk | PORT launch-strategy; campaign assets reuse, không tạo workflow thứ hai. |
| `nckh-content` | Content strategy/editorial program | Pillars, audience intent, calendar, briefs, reuse/provenance | Không viết lại mọi copy hoặc publish | Maker/worker | MERGE content-marketing/content strategy; nckh-copy làm conversion copy theo brief. |
| `nckh-copy` | Copy bán hàng/landing/ad/message | Claim-grounded copy variants, CTA, tone, revision | Không bịa testimonials, scarcity, results; không đổi facts vì conversion | Maker/worker + critic khi hữu ích | MERGE copywriting/write marketing modes; nckh-write giữ scientific/general prose. |
| `nckh-seo` | Search/content discoverability | Search intent, crawl/content/on-page audit, prioritized fixes | Không guarantee rank, keyword stuffing hoặc exploit provider | Researcher/maker | PORT SEO/GEO principles; paid suites/connectors ở extensions. |
| `nckh-email` | Email lifecycle/campaign artifact | Segmentation assumptions, sequence, copy, consent/suppression checks | Không gửi mail/upload contacts chưa cho phép | Maker/worker | PORT email; copy helper dùng chung, delivery adapters optional. |
| `nckh-social` | Social strategy/post/calendar | Platform-scoped content, tone, moderation plan, draft artifacts | Không post/follow/DM hay giả organic evidence | Maker/worker | PORT social; platform integrations và schedulers ở extensions. |
| `nckh-analytics` | Đọc dữ liệu KPI/funnel/campaign | Definitions, denominators, data-quality checks, descriptive findings | Không bịa số, causal lift hoặc attribution từ correlation | Researcher/worker; deep cho inference khó | PORT analytics; experiment sở hữu randomized inference protocol. |
| `nckh-cro` | Tìm friction và hypothesis cải thiện conversion | Funnel/page/form/onboarding diagnosis, prioritized hypothesis, UX review | Không bảo đảm uplift hoặc launch test | Maker/reviewer theo UX risk | MERGE form/onboarding/page CRO; experiment nhận hypothesis để thiết kế test. |
| `nckh-experiment` | A/B hypothesis, design/readout | Unit/randomization, metrics/guardrails, sample/stopping plan, uncertainty | Không chạy live test/change traffic/budget chưa duyệt; không peeking claim | Planner/reviewer theo statistical risk | PORT ab-test-setup + bounded experiment analysis; analytics cung cấp data contract. |

Design brief nằm ở brand, competitor nằm ở market-research: không bỏ chức năng
để đạt số lượng. Media/video/banner/provider-specific publishing không là Core;
chỉ chọn extension khi output thật sự cần. Marketing facts cũng đi evidence-first,
nhưng không ép Q1/Q2 hoặc research-paper format cho mọi landing page.

## 4. PORT / MERGE / EXTENSION / DROP

| Disposition | Nghĩa thực thi khi có quyền cook | Gate |
|---|---|---|
| PORT | Lấy behavior/invariant tốt, viết/adapt vào contract NCKH | Source revision/license/attribution + NCKH acceptance; không copy nguyên prompt mặc định. |
| MERGE | Nhiều entrypoint thành modes trong một owner/outcome | Coverage map + routing collision/negative eval; không im lặng xóa capability. |
| EXTENSION | Giữ opt-in ngoài closure mặc định vì framework/provider/output hẹp | Dependency, permission, support/version và eval riêng. |
| DROP | Không đưa workflow/capability đó vào kit | Lý do cụ thể: trùng owner, ngoài scope, tăng quyền/chi phí vô ích; không nói upstream vô dụng. |

AgentKit giant router/menu, full catalog bootstrap, forced best-of-N, always-on
multi-agent, unconditional journal/publish và unrelated growth/payment integrations
không đi vào NCKH default. Các ý tưởng hữu ích đã có owner khác được MERGE; phần
không còn outcome độc lập mới DROP. Không đụng hay gỡ skill upstream của người dùng.

[AgentKit evidence/disposition](../reports/researcher-260930-1910-agentkit-port-evidence.md)
ghi mức inspect và giới hạn upstream. Metadata-only classification là sơ bộ cho
source audit, không chứng minh license/dependency closure đã đủ để port code.

## 5. Stable contract cho mọi skill

Mỗi entry phải có eval positive trigger, negative/near-miss, output acceptance,
failure/permission case và trace skill/model/delegation đã dùng. Specific checks:

- Core: plan-only, auto/interactive, factual delta, quote/DOI, style human review,
  method assumptions, visual native/source/render, stale receipt.
- Engineer: diagnose-only no write, cause-aligned repair, real test failure,
  source-backed review, protected dirty tree, backup-before-data-change, deploy permission.
- Marketing: unsupported statistic/testimonial, denominator/causality, channel
  boundary, no publish/spend from a content request, consent/rights on datasets.
- Xia: source injection, unknown license, compare-only no plan/code, port plan
  with local dependency/rollback, namespace collision.

Không có eval hoặc chưa đủ evidence thì `experimental`, không `stable`. Stability
có scope theo skill + host/surface/version + mode/profile, không là một badge toàn kit.
