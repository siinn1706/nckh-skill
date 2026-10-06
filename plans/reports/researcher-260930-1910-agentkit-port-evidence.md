# Bằng chứng AgentKit cho kế hoạch Skill Kit NCKH

**Ngày đối chiếu:** 30/09/2026, Asia/Saigon  
**Phạm vi:** nghiên cứu read-only phục vụ sửa kế hoạch; không chạy skill, không cài đặt, không gọi provider/API trả phí, không dùng credential, không sửa source/manifest.  
**Đầu ra được phép tạo:** riêng báo cáo này.  
**Nhãn bằng chứng:** `[local]` = quan sát từ binary/cache cục bộ; `[official]` = tài liệu upstream chính thức; `[repo]` = kho công khai; `[unverified]` = chưa có consumer run hoặc chưa có chứng cứ hành vi.

## Kết luận và thứ tự ưu tiên

Khuyến nghị xếp hạng như sau:

1. **Core kit host-neutral:** giữ đủ 10 identity đề xuất (`nckh-plan`, `nckh-cook`, `nckh-research`, `nckh-evidence`, `nckh-method`, `nckh-write`, `nckh-taste`, `nckh-review`, `nckh-handoff`, `nckh-visuals`); gộp brainstorm vào plan nhưng không bỏ research, evidence, taste hay visuals.
2. **Engineer kit đủ 13 capability:** giữ scout, debug, fix, test, code review, security, context, docs, frontend, backend, data, devops và git; mỗi capability có owner/boundary riêng, framework/provider-specific chỉ là extension.
3. **Marketing kit đủ 13 capability:** giữ market research, brand/design brief, marketing plan, campaign, launch, content, copy, SEO, email, social, analytics, CRO và experiment/A-B; không thu hẹp thành dissemination-only, đồng thời không tự publish/spend/upload.
4. **Bốn runtime adapter bắt buộc trong thiết kế:** Claude Code, Codex, Cursor và Antigravity/`agy`; canonical source, dependency closure, installer và eval dùng chung, còn path/plugin/hook/model semantics thuộc adapter.
5. **`nckh-xia` là tooling overlay riêng:** bảo toàn `ak-xia` hiện hữu, dùng Xia để khảo sát source/repository và chuyển sang quyết định PORT/MERGE/EXTENSION/DROP có provenance; không đổi nghĩa upstream `--compare`, không nhận tên `ak-xia` và không viết đè skill đó.
6. **Gate an toàn:** capability bắt buộc chưa được chứng minh thì `NOT_CALLABLE`; sự hiện diện của file, help, manifest hoặc plan không phải bằng chứng đã chạy, đã đánh giá chất lượng hay đã có quyền sao chép/phát hành.

### Cách hiểu đúng về phạm vi lượt này

`docs-only` là giới hạn thực thi của lượt nghiên cứu này: chỉ sửa report, không implement/cài đặt/provider-call. Đây **không** phải giới hạn product. Các domain frontend, backend, devops, CRO, experiment/A-B và marketing execution vẫn nằm trong thiết kế catalog; chúng chỉ chưa được chạy. Giá phải trả của kiến trúc đầy đủ là thêm mapping, license/attribution, venue/profile, host qualification và đánh giá đối chứng trước khi đưa từng route vào runtime.

**Target catalog cần giữ trong plan:** Core gồm `nckh-plan`, `nckh-cook`, `nckh-research`, `nckh-evidence`, `nckh-method`, `nckh-write`, `nckh-taste`, `nckh-review`, `nckh-handoff`, `nckh-visuals`; Engineer gồm `nckh-scout`, `nckh-debug`, `nckh-fix`, `nckh-test`, `nckh-code-review`, `nckh-security`, `nckh-context`, `nckh-docs`, `nckh-frontend`, `nckh-backend`, `nckh-data`, `nckh-devops`, `nckh-git`; Marketing gồm `nckh-market-research`, `nckh-brand`, `nckh-marketing-plan`, `nckh-campaign`, `nckh-launch`, `nckh-content`, `nckh-copy`, `nckh-seo`, `nckh-email`, `nckh-social`, `nckh-analytics`, `nckh-cro`, `nckh-experiment`; tooling là `nckh-xia`.

**Runtime target:** một canonical source và bốn adapter/qualification tracks: Claude Code, Codex App/CLI/IDE surface theo thực tế hiện hành, Cursor và Antigravity/`agy`. Adapter sở hữu path, invocation, plugin/hook, isolation, model/effort và receipt; core không tự nhận parity giữa các host. Installer/eval phải detect cả bốn, preview lựa chọn Core/Engineer/Marketing, hỗ trợ project/global và rollback; chưa chạy installer trong lượt này.

Ma trận runtime chi tiết, version/help quan sát được và các `[unverified]` probe còn lại nằm trong `plans/reports/researcher-260930-1910-runtime-compatibility.md`; báo cáo này dùng nó làm giới hạn kiến trúc, không chuyển support claim thành execution proof.

## Snapshot cục bộ và provenance

| Hạng mục | Quan sát read-only |
|---|---|
| CLI | `C:/Users/USER\bin\ak.exe`, `ak 2.19.0`; SHA-256 `B2076291DF31E58D72C8328AB637E523EE2E2251BA72F31FEB5FF147DFAF172C` `[local]` |
| Config | `C:/Users/USER\.agentkit\config.yaml`: coding level 5, kit mặc định `engineer`, telemetry tắt, Codex adapter bật `[local]` |
| Engineer manifest | `C:/Users/USER\.agentkit\cache\kits\engineer\codex\2.19.0\engineer\kit.yaml`; kit `0.2.0`, tier `paid`, 103 skill export; SHA-256 `A5ADDC09CF4CE4DB93B2E4769DFAFBB91D0F74DBA5910210C72057DC48A3177C` |
| Marketing manifest | `C:/Users/USER\.agentkit\cache\kits\marketing\codex\2.19.0\marketing\kit.yaml`; kit `0.2.0`, tier `paid`, 82 skill export; SHA-256 `4828D5F948A6BC965F1F05B0BDCA705125E13696E2704DCAB95AA98ED96676CE` |
| Skill đã đọc sâu | `ak-xia`, `ak-plan`, `ak-cook`, `ak-debug`, `ak-fix`; các đường dẫn dưới `C:/Users/USER\.agents\skills\` `[local]` |
| Xia hash | `ak-xia/SKILL.md`: `3511FCF2463AF2B3718ADC223D9E86D01D302ED1B53E6D576A76C35DA02A7BB1` |
| Plan/cook/debug/fix hash | lần lượt `81DF1AB9FB73A0A90CFD8DEF643C3B856C12CD59DEF78D9014B329D134620813`, `FB1551B6FAF8C5605483F7C5BD679AFDDAF87620CDFC75D40481D43312484ECD`, `BEAD05D76313566ABA051F54BB55FADA5993DE590A510109DA1C76DF8A01F720`, `603FBCFE683D0CE3F2861DF76E8041E0DE8EB2F9CB55BFFF7CC39BC4320BC97A` |

`ak self-update --check --json --no-interactive` trả `current_version: 2.19.0`, `available: false`, `status: unknown`, `reason: release_check_unavailable`; vì vậy biết version cục bộ nhưng **chưa xác minh freshness từ remote**. Kiểm kê regex read-only trên hai manifest cho kết quả 103/82, 39 shared, 64 engineer-only, 43 marketing-only, union 146; không có ID thiếu hoặc trùng sau khi bổ sung bốn mục bị bỏ sót.

Public docs hiện không khớp tuyệt đối snapshot paid: tài liệu Engineer mô tả khoảng 102 identity và Marketing khoảng 85 identity, trong khi manifest cục bộ là 103/82. Xem đây là catalog/alias/snapshot drift, không tự coi manifest cục bộ sai. Public `bestagentkits/ak-cli` hiện hiển thị package `@bestagentkits/ak` `0.1.0-beta.0`, còn `bestagentkits/agency-skills` có 842 skill; không dùng hai số này để suy ra binary native `ak 2.19.0` hoặc paid kits có cùng implementation.

### Nguồn upstream/public đã đối chiếu

- [Xia stable guide](https://docs.agentkit.best/en/stable/kits/engineer/skills/xia) và [Xia beta guide](https://docs.agentkit.best/en/beta/kits/engineer/skills/xia): mode, recon, Challenge và handoff `[official]`.
- [CLI reference](https://docs.agentkit.best/en/beta/reference/cli), [`ak run`](https://docs.agentkit.best/en/beta/reference/cli/run) và [AgentKit architecture](https://docs.agentkit.best/en/beta/concepts/architecture): separation giữa kit, runtime adapter và execution `[official]`.
- [Engineer plan](https://docs.agentkit.best/en/stable/kits/engineer/skills/plan), [Engineer research](https://docs.agentkit.best/en/stable/kits/engineer/skills/research) và [skill creator](https://docs.agentkit.best/en/stable/kits/engineer/skills/skill-creator): planning, source discipline và evaluation caveats `[official]`.
- [Marketing catalog](https://docs.agentkit.best/en/stable/kits/marketing/skills), [marketing research](https://docs.agentkit.best/en/stable/kits/marketing/skills/marketing-research), [marketing planning](https://docs.agentkit.best/en/stable/kits/marketing/skills/marketing-planning), [copywriting](https://docs.agentkit.best/en/stable/kits/marketing/skills/copywriting), [analytics](https://docs.agentkit.best/en/stable/kits/marketing/skills/analytics), [slides](https://docs.agentkit.best/en/stable/kits/marketing/skills/slides) và [write](https://docs.agentkit.best/en/stable/kits/marketing/skills/write): catalog và output boundary `[official]`.
- [Official organization](https://github.com/bestagentkits), public [`ak-cli`](https://github.com/bestagentkits/ak-cli) và public [`agency-skills`](https://github.com/bestagentkits/agency-skills): public-source context, không phải parity proof của local paid snapshot `[repo]`.

## `ak-xia`: semantics phải giữ nguyên

Nguồn local `ak-xia/SKILL.md` nêu usage/flags ở L23–L38, pipeline sáu phase và Challenge gate ở L47–L53, ranh giới recon ở L55–L75, handoff theo mode ở L135–L157 và recovery ở L183–L189. Reference `mode-selection.md` L3–L9 và `challenge-framework.md` L5–L40 bổ sung mode/risk scoring `[local]`. Stable/beta guide và CLI reference xác nhận cùng họ semantics `[official]`:

| Mode | Nghĩa cần bảo toàn | Giới hạn khi đưa vào NCKH |
|---|---|---|
| mặc định | khảo sát, hiểu cấu trúc, kiểm tra rủi ro rồi handoff kế hoạch | chỉ là reconnaissance/planning, không phải implementation hay scientific validation |
| `--compare` | báo cáo side-by-side; **không** tạo implementation plan | dùng cho lựa chọn nguồn; phải ghi nguồn, ngày, version/hash và điều kiện license |
| `--copy` | kế hoạch adaptation tối thiểu từ source về local | không suy ra quyền copy/re-distribute; cần license/attribution gate riêng |
| `--improve` | copy có refactor theo convention local | không làm mất provenance hay biến refactor thành kết quả tốt hơn |
| `--port` | kế hoạch rewrite idiomatic; là mặc định khi intent là port | hợp với `nckh-xia` chỉ sau khi khóa artifact, scope và claim |
| `--auto` | tự duyệt gate routine trong workflow | không cấp quyền code, credential, dependency, external effect, commit, publish hoặc deploy |
| `--fast` | docs mô tả skip research/Challenge | mâu thuẫn với tuyên bố Challenge là hard gate; không dùng cho adoption decision, chọn flow mặc định hoặc `--compare` |

Recon phải coi repository, README, issue và comment là dữ liệu không tin cậy; không execute source, không install package từ source. Non-compare handoff sang `ak:plan`; Xia không implement và cuối flow gợi ý `ak:cook <plan-path>`. `nckh-xia` nên là namespace/adapter NCKH gọi cơ chế tương đương với hợp đồng riêng, không tuyên bố upstream `--compare` đã có bước lập kế hoạch.

## Phương án kiến trúc và trade-off

| Xếp hạng | Phương án | Hiệu năng/độ gọn | Độ phức tạp/bảo trì | Adoption risk và provenance | Fit với NCKH |
|---|---|---|---|---|---|
| 1 | Một core Agent Skills host-neutral + adapter mỏng + coordinator cục bộ | Tốt; nạp theo task, ít context thừa | Vừa; cần routing/receipt và contract adapter | Thấp hơn fork; license và hash tách được | Tốt nhất; giữ venue/evidence gates |
| 2 | Dùng capability AgentKit qua adapter, không đóng gói lại kit | Tốt nếu scope hẹp | Vừa; phụ thuộc catalog/version drift | Vừa; paid snapshot và license file-by-file phải kiểm | Tốt cho prototype/đối chứng |
| 3 | Cài nhiều skill độc lập rồi thêm router | Có thể rộng nhưng dễ trùng context | Cao; conflict routing và khó đo consumer | Cao; nhiều nguồn/quyền/namespace chồng nhau | Trung bình; chỉ nên làm reference |
| 4 | Fork nguyên Engineer/Marketing rồi sửa thành NCKH | Ban đầu nhanh, về sau context nặng | Rất cao; upstream merge và drift khó | Cao; paid kit không mặc nhiên cho quyền phát hành lại | Kém; lẫn venue, sales và scientific claims |

AgentKit architecture/CLI/plan/research docs mô tả separation giữa kit, adapter, execution và planning `[official]`; các manifest/cache ở trên chỉ chứng minh snapshot local. `agency-skills` README nói packaging/importer phải giữ source attribution/license `[repo]`; điều này củng cố lựa chọn adapter/attribution, không cấp license cho toàn bộ paid kit.

## Engineer: disposition chính cho NCKH

| Capability | Disposition | Cách dùng và rào chắn |
|---|---|---|
| `ak-scout` | **MERGE** | source/corpus scouting có query, ngày, provenance và stop condition; generic repository scout không đủ làm evidence review |
| `ak-debug` | **PORT** | diagnosis cho software/data/evidence pipeline; giữ no-fix-before-root-cause và không biến lỗi parser thành lỗi khoa học |
| `ak-fix` | **MERGE** | repair theo cause, giữ receipt/diff và verify sau sửa; không tự hạ claim để che lỗi |
| `ak-test` | **MERGE** | deterministic fixture, reproducibility, schema/round-trip và regression; không gọi pass là human gold hay real training |
| `ak-code-review` | **PORT** | review code/public contract/methodology theo evidence và severity; generic PR review không thay peer review |
| `ak-security` | **PORT** | privacy, secret, license, external-resource và release checks; không suy an toàn từ lint |
| `ak-context-engineering` | **PORT** | minimum-sufficient context theo source/evidence/task; không hard-code window hoặc cho model tự thêm unsupported claims |
| `ak-docs` | **MERGE** | durable behavior/setup/architecture/source records, link về machine-owned artifact; không gọi report phase là evergreen authority |
| `ak-frontend-design` | **MERGE** | gộp với frontend-development/ui-styling thành UI capability có accessibility/state/performance/visual checks theo quyền |
| `ak-backend-development` | **PORT** | API/service/auth/data boundary, interface validation và tests; không đổi DB/pricing/payment scope âm thầm |
| `ak-databases` | **PORT** | schema/query/migration/data-integrity contract, backup/rollback và verification; không migrate/drop/bulk-update chưa duyệt |
| `ak-devops` | **MERGE** | gộp với deploy thành build/deploy/ops route có environment, health và rollback evidence; không tự tạo cloud resource |
| `ak-git` | **MERGE** | freeze version/hash, diff, branch/provenance; không automatic push/publication |
| `nckh-xia` | **PORT** | adapter khảo sát/port có attribution, license, artifact và Challenge gate; giữ nguyên `ak-xia` |

`ak-plan` và `ak-brainstorm` được MERGE vào Core skill `nckh-plan`; `ak-cook` được PORT thành Core skill `nckh-cook`, nơi sở hữu execution/validate/fix/test/review và không vượt quyền `--auto`. Việc chưa implement trong lượt này không làm mất các capability Engineer khỏi catalog.

## Marketing: disposition chính cho NCKH

| Capability | Disposition | Cách dùng và rào chắn |
|---|---|---|
| market research + `ak-competitor` | **MERGE** | gộp market-research/competitor thành sourced market map; giữ ngày, nguồn, unknowns và không bịa market size/customer quote |
| `ak-brand` + design brief | **MERGE** | gộp brand/design brief thành audience, positioning, message hierarchy và voice; production asset/legal clearance ở extension |
| `ak-marketing-planning` | **PORT** | giữ strategy/goals/channels/budget hypotheses và KPI definitions; không cấp campaign spend |
| `ak-campaign` | **PORT** | campaign brief/schedule/assets/tasks/measurement; không chạy ads hoặc publish chỉ vì auto |
| `ak-launch-strategy` | **PORT** | product/feature GTM readiness, sequence, comms và rollback; không deploy product hay gửi thông báo mặc định |
| `ak-content-marketing` | **MERGE** | gộp content strategy/editorial program; giữ audience, pillars, calendar, briefs và provenance, không tự publish |
| `ak-copywriting` | **MERGE** | gộp marketing copy với write modes; claim-grounded variants/CTA/tone, không bịa testimonial/scarcity/results |
| `ak-seo` | **PORT** | search intent/crawl/content/on-page audit; không guarantee rank, keyword stuffing hoặc exploit provider |
| `ak-email` | **PORT** | lifecycle/campaign artifact với consent/suppression checks; không gửi mail/upload contacts chưa cho phép |
| `ak-social` | **PORT** | platform-scoped content/calendar/moderation draft; không post/follow/DM hay giả organic evidence |
| `ak-analytics` | **PORT** | reporting mechanics; không thay scientific evaluation bằng CTR, funnel hay conversion KPI |
| CRO/form | **MERGE** | gộp form/onboarding/page CRO thành friction diagnosis và prioritized hypotheses; không bảo đảm uplift hoặc tự launch test |
| experiment/`ak-ab-test-setup` | **PORT** | giữ unit/randomization, metrics/guardrails, sample/stopping plan và uncertainty; không chạy live test/change traffic/budget chưa duyệt |

Marketing facts vẫn evidence-first khi là factual claim, nhưng không ép Q1/Q2 hoặc research-paper format cho mọi landing page/campaign. Marketing kit là domain capability đầy đủ; publish/spend/upload vẫn là permission gate.

## Appendix: ánh xạ exhaustive 146 skill ID

Mỗi ID dưới đây xuất hiện đúng một lần trong các dòng disposition; chỉ dùng bốn class: `MERGE`, `PORT`, `EXTENSION`, `DROP`. Core là **layer/catalog owner**, không phải class thứ năm: các upstream primitive được gộp vào Core vẫn mang disposition MERGE hoặc PORT. Chỉ các body nêu ở phần provenance được đọc sâu; các mục còn lại là mapping từ manifest + metadata, chưa phải đánh giá hành vi.

### Shared: 39 ID

- **MERGE (20):** `ak-ask`, `ak-brainstorm`, `ak-codex-goal`, `ak-copywriting`, `ak-design`, `ak-docs`, `ak-docs-seeker`, `ak-enhance-ux-ax`, `ak-fix`, `ak-folder-context`, `ak-frontend-design`, `ak-git`, `ak-journal`, `ak-plan`, `ak-research-prompt`, `ak-scout`, `ak-sumup`, `ak-test`, `ak-ui-ux-pro-max`, `ak-worktree`.
- **PORT (3):** `ak-cook`, `ak-debug`, `ak-handoff`.
- **EXTENSION (12):** `ak-agent-browser`, `ak-agentkit`, `ak-ai-multimodal`, `ak-ak`, `ak-explain`, `ak-hyperframes`, `ak-interview-docs`, `ak-mermaidjs-v11`, `ak-preview`, `ak-remotion`, `ak-skill-creator`, `ak-tech-graph`.
- **DROP (4):** `ak-bro`, `ak-google-adk-python`, `ak-sowat`, `ak-watzup`.

### Engineer-only: 64 ID

- **MERGE (11):** `ak-deploy`, `ak-devops`, `ak-frontend-development`, `ak-github`, `ak-goal-warmup`, `ak-issue-to-plan`, `ak-orchestrate`, `ak-problem-solving`, `ak-research`, `ak-ui-styling`, `ak-web-testing`.
- **PORT (8):** `ak-backend-development`, `ak-code-review`, `ak-context-engineering`, `ak-databases`, `ak-fable-thinking`, `ak-review-pr`, `ak-security`, `ak-xia`.
- **EXTENSION (38):** `ak-advise`, `ak-ai-artist`, `ak-autoresearch`, `ak-better-auth`, `ak-chrome-profile`, `ak-cti-expert`, `ak-deep-swe`, `ak-diagram`, `ak-document-skills`, `ak-excalidraw`, `ak-find-skills`, `ak-gkg`, `ak-graphify`, `ak-llms`, `ak-loop`, `ak-markdown-novel-viewer`, `ak-media-processing`, `ak-mintlify`, `ak-mobile-development`, `ak-page-builder`, `ak-payment-integration`, `ak-plans-kanban`, `ak-predict`, `ak-project-management`, `ak-project-organization`, `ak-react-best-practices`, `ak-repomix`, `ak-retro`, `ak-scenario`, `ak-shader`, `ak-ship`, `ak-shopify`, `ak-stitch`, `ak-tanstack`, `ak-team`, `ak-threejs`, `ak-web-frameworks`, `ak-webmcp`.
- **DROP (7):** `ak-agentize`, `ak-bootstrap`, `ak-coding-level`, `ak-help`, `ak-mcp-builder`, `ak-show-off`, `ak-vibe`.

GKG chỉ là EXTENSION khi đã duyệt structured corpus/project graph; loop chỉ là EXTENSION khi có baseline, metric và stop condition. Đây là lý do loại chúng khỏi Core closure, không phải phủ nhận giá trị của chúng trong extension.

### Marketing-only: 43 ID

- **MERGE (8):** `ak-brand`, `ak-cip-design`, `ak-competitor`, `ak-content-marketing`, `ak-form-cro`, `ak-marketing-research`, `ak-onboarding-cro`, `ak-write`.
- **PORT (9):** `ak-ab-test-setup`, `ak-analytics`, `ak-campaign`, `ak-email`, `ak-launch-strategy`, `ak-marketing-planning`, `ak-seo`, `ak-slides`, `ak-social`.
- **EXTENSION (18):** `ak-assets-organizing`, `ak-banner-design`, `ak-content-hub`, `ak-creativity`, `ak-design-system`, `ak-elevenlabs`, `ak-gamification-marketing`, `ak-logo-design`, `ak-marketing-dashboard`, `ak-marketing-ideas`, `ak-motion-design`, `ak-motion-graphics`, `ak-motion-video`, `ak-pricing-strategy`, `ak-storage`, `ak-video`, `ak-youtube`, `ak-youtube-thumbnail-design`.
- **DROP (8):** `ak-ads-management`, `ak-affiliate-marketing`, `ak-free-tool-strategy`, `ak-init`, `ak-marketing-psychology`, `ak-paid-ads`, `ak-play`, `ak-referral-program-building`.

Slides chỉ xuất HTML theo upstream material đã đọc, không được gọi là native PPTX; vì vậy nó PORT vào visual workflow chỉ khi native-editability contract có engine riêng. Write được MERGE vào marketing copy mode nhưng vẫn phải giữ evidence/claim/venue guardrail. A/B setup được PORT vào nckh-experiment, không tự chạy live test.

## Adoption risk, license và giới hạn

- **Maturity/drift:** local binary 2.19.0 và paid kit 0.2.0 chưa được chứng minh parity với stable/beta docs, public Node ak-cli hoặc agency-skills; release check remote hiện unavailable. Trước release phải chụp lại version/help/docs và hash.
- **Behavioral proof:** chưa consumer-run bất kỳ skill nào; chưa chạy hook/plugin/subagent/parallel/paid model/provider. Không báo “preserved behavior”, “implemented”, “human-reviewed” hoặc “scientifically valid” từ manifest/help/plan.
- **License:** manifest ghi `tier: paid`; public packaging có attribution/license guidance nhưng không cấp quyền re-distribute paid kit. Trước copy/port phải đọc license của từng source/asset, lưu attribution và xin quyền nếu cần.
- **Runtime fit:** host-specific path, slash dispatch, model/effort, hook failure, isolation và context budget cần adapter; không bê nguyên frontmatter/event name từ host này sang host khác.
- **Measurement:** chưa có corpus NCKH, marketing baseline, benchmark, human gold, baseline hay acceptance rubric cho tiếng Việt/English/slide/hình/campaign. `lint`, validator, parser smoke test và notebook pass không chứng minh chất lượng skill.
- **Venue:** phải hỏi `venue_id`, loại venue, category, metric/data-year và version guideline; không suy Q1/Q2, peer review, license hoặc compliance từ Scholar/public access.

### Câu hỏi còn mở trước khi triển khai

1. Bốn adapter Claude Code, Codex, Cursor và Antigravity/`agy` đã là product scope; cần chốt surface/version qualification order và permission profile nào trước release.
2. `nckh-xia` được phép khảo sát loại source/repository nào, output schema/hash/attribution nào, và có venue/license profile bắt buộc không?
3. Corpus giọng viết, human reviewers, holdout và baseline nào được duyệt để đánh giá thay vì tự chấm?
4. Route publish/spend/upload nào được cấp cho từng task; trước khi có approval, giữ external writes ở draft-only nhưng không loại marketing capability khỏi catalog.

## Status

**Status:** DONE_WITH_CONCERNS  
**Summary:** Đã đối chiếu snapshot AgentKit local và nguồn upstream/public, xác định semantics upstream Xia, xếp hạng kiến trúc, lập disposition cho Core/Engineer/Marketing và ánh xạ exhaustive 146 skill ID; đề xuất nckh-xia là overlay riêng, không overwrite upstream ak-xia.  
**Concerns/Blockers:** Chưa có consumer run, implementation-source parity, hook/plugin probe, provider/model call, license clearance, human evaluation, venue approval hoặc release-freshness check; không được coi báo cáo này là bằng chứng triển khai hay nghiệm thu runtime.
