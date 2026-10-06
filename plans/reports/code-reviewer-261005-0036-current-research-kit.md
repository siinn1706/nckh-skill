# Rà soát NCKH: nghiên cứu, dữ liệu và DevOps/AIOps

## Phạm vi và snapshot

- Planning-only; đã đọc nguồn, contracts, readers, tests và plan. Không chạy build/install/provider/source scripts; không sửa nguồn.
- Snapshot đọc 2026-10-05 00:41:24–00:45:30 +07: source-lock **r34**, **281 pins**, **0 missing/drift** khi băm trực tiếp từng pin. Raw lock SHA-256 `671512337bf36942ab9b79eaac6fffac335280aaec45f8219301a7d7d87eb25a` không đổi ở các lần đọc đầu/cuối; đã sửa lỗi chép thừa một ký tự trong report. Workspace không có Git worktree; không gán commit giả.
- Catalog hiện có **39 identities / 156 base eval IDs**, mọi status `experimental`; registry có **9 resources**. `nckh-kit/README.md` không tồn tại; navigation thật là `docs/README.md` → `nckh-kit/docs/index.md`.
- Installed snapshot khác source: `.agents/skills` có **37 directories**; `.nckh-state/ownership.json:83`–`:88` ghi provenance lock `adc642…1968c`, khớp identity của history **r25**, surface `codex-desktop`, copy/project. Không có hai writer mới trong installed tree. Đây là inventory/ownership observation, không phải doctor/native acceptance.
- Plan đang thực thi (historical evidence path: `</C:/Users/USER/Downloads/test-skill/plans/261004-0047-nckh-research-data-hooks-writing/plan.md:16>`; unavailable in the cleaned checkout) ghi r34/in-progress, 44/45 tasks và native coverage còn mở; owner feedback được ghi cho hai mẫu r29. Không suy ra accepted r34 từ feedback cũ.
- **Mốc thiết kế theo chỉ đạo user:** giả định plan `261004-0047` sẽ cook hoàn toàn bởi agent khác. Writer split/locale, research-only visual gate, portable hooks và integration của plan đó là dependency hậu cook, không phải task mới trong review này. Snapshot có thể thay đổi sau thời điểm đọc.

## Findings theo mức ưu tiên

### P1 — Chưa có owner cho vòng đời dataset nghiên cứu

**Evidence:** nckh-data (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-data/SKILL.md:3>`; unavailable in the cleaned checkout) owns schema/query/migration; inputs/output tại `:13`–`:15` và workflow `:28`–`:34` bảo vệ mutation/backup. Method (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/core/nckh-method/SKILL.md:26>`; unavailable in the cleaned checkout) yêu cầu sampling, splits/leakage nhưng chỉ trả protocol; source schema (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/contracts/source.schema.json:4>`; unavailable in the cleaned checkout) ghi source identity/access/rights, không ghi sample IDs, split membership hoặc transformations.

**Impact:** scientific intake, dedup/curation, label lineage và split audit dễ rơi vào database migration hoặc chỉ dừng ở prose; không có artifact riêng để phát hiện cùng entity/incident xuất hiện trong nhiều splits.

**Upgrade target:** `nckh-dataset` riêng cho research intake/curation/split/lineage; giữ `nckh-data` cho schema/mutation. Contract phải bind source version/raw hash, transformation/code/config, sample/entity/time IDs, exclusions/missingness, labels/quarantine và immutable split manifest. Project data/private labels nằm ngoài source/dist.

**Acceptance:** nguồn thiếu rights dừng acquisition; record trùng/label conflict đi quarantine; same entity/incident/time overlap làm split fail; split thay đổi invalidates downstream runs; source rows trước/sau transform reconcile được. Dữ liệu thật cần nguồn được user cấp hoặc rights-cleared, không bịa corpus.

### P1 — Generic DevOps/debug chưa cung cấp chuỗi telemetry → AIOps evaluation

**Evidence:** DevOps (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-devops/SKILL.md:13>`; unavailable in the cleaned checkout) owns artifact/environment/build/rollout/health/rollback; debug (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/engineer/nckh-debug/SKILL.md:13>`; unavailable in the cleaned checkout) owns symptom/reproduction/traced cause. Các references hiện chỉ execution/authority và review/handoff. Không thấy AIOps/incident/root-cause/fault-injection contract trong các owning skill directories, `core/contracts`, `core/profiles` đã kiểm.

**Impact:** không có artifact chuẩn cho timestamp/unit/resource/trace joins, incident windows, root-cause gold, hoặc metric denominator; một diagnosis có vẻ hợp lý chưa thể dùng làm RCA benchmark verdict.

**Upgrade target:** `nckh-telemetry` owns bounded normalization/quality/joins cho logs/metrics/traces và giữ raw lineage; `nckh-aiops` consumes frozen telemetry+dataset để RCA/anomaly/retrieval/agent evaluation. DevOps tiếp tục owns local environment/process/rollback; debug tiếp tục owns code/test diagnosis. Không thêm production remediation, live fault injection hoặc auto operations.

**Acceptance:** thiếu timezone/unit/trace linkage giữ unknown; clock skew, duplicate events, gaps và many-to-many joins hiện trong quality report; gold labels không vào model input; incident/entity/temporal leakage fail; ranking ties/unknown/no-answer và failed runs được báo đúng; metrics bind exact incident set, denominator và prediction hashes.

### P1 — Scientific statistics và reproducible experiment thiếu specialty owner

**Evidence:** experiment (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/marketing/nckh-experiment/SKILL.md:3>`; unavailable in the cleaned checkout) là A/B protocol/readout; analytics (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/marketing/nckh-analytics/SKILL.md:3>`; unavailable in the cleaned checkout) là KPI/funnel/campaign. Current guards (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/guards.py:234>`; unavailable in the cleaned checkout) kiểm rate denominator/time và A/B fields/stopping. Method (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/core/nckh-method/SKILL.md:32>`; unavailable in the cleaned checkout) không chạy experiment; cook (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/skills/core/nckh-cook/SKILL.md:37>`; unavailable in the cleaned checkout) owns lifecycle và để specialty outputs cho domain skills.

**Impact:** scientific comparison/baselines/ablations/repeated runs/statistical inference chưa có output contract; dễ dùng marketing A/B rules cho offline ML/RCA hoặc đưa bảng kết quả không bind run inputs.

**Upgrade target:** `nckh-statistics` owns estimand, assumption checks, analysis, uncertainty/effect sizes và bounded interpretation. Extend method/research/devops/cook references cho reproducible experiment manifest + actual run receipt; không thêm orchestration skill. Reuse `brief.visual_purpose.computation` bindings tại brief schema (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/contracts/brief.schema.json:216>`; unavailable in the cleaned checkout) cho visual handoff, không biến visual schema thành toàn bộ experiment contract.

**Acceptance:** frozen dataset/split/code/config/environment/run IDs và failure logs có hash; metric computation reconcile với prediction/sample counts; seeds/repeats chỉ bắt buộc khi design cần; missing/failed runs không biến thành zero; paired/unpaired assumptions đúng; no significance/causal claim khi design không support; sửa metric/protocol sau nhìn results được ghi amendment.

### P2 — Resources hiện không phải dữ liệu chấp nhận cho CS/AIOps

**Evidence:** Resource contract (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/docs/contracts.md:30>`; unavailable in the cleaned checkout) ghi 15 clinical reporting entries, 8 publisher snapshots, 119 UI rows, một Nature fragment, 3 Wikisource passages, 2 biomedical PMC projections, 26 World Bank observations trong một bundle, 2 Django code fixtures và 10 UCI marketing rows. Counts đã đọc trực tiếp. Reporting test (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/tests/resource/test_consumers.py:25>`; unavailable in the cleaned checkout) cố ý trả empty cho `domain=cs`; đây là đúng contract.

**Impact:** nine-resource inventory không tạo CS/AIOps corpus, scientific statistics reference hoặc incident benchmark. Biomedical/style/source packages không thể làm gold hay evidence cho chất lượng RCA.

**Upgrade target:** selective resources cho bốn owner mới chỉ khi có named source → producer/reader → artifact → verifier, exact provenance/rights và scope. Prioritize project input manifests, telemetry field/metric definitions và một bounded rights-cleared real incident/resource case khi nguồn được chọn; không clone upstream hoặc ép mọi skill có CSV/JSON.

**Acceptance:** consumer/domain/locale/genre mismatch không đọc; source/license/lineage drift fail; off trả disabled/no-read; relocated reader thực hiện được approved reads; copied raw/normalized bytes có hash riêng; mọi reference chưa đủ quyền giữ reference-only/unpackaged. Không dùng successful lookup làm scientific acceptance.

### P2 — Base cases hiện kiểm generic ownership; cần behavior cases cho domain mới

**Evidence:** data case (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/engineer/nckh-data.json:36>`; unavailable in the cleaned checkout) là migration plan, DevOps case (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/engineer/nckh-devops.json:36>`; unavailable in the cleaned checkout) là local package build, debug case (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/engineer/nckh-debug.json:36>`; unavailable in the cleaned checkout) là failing test, experiment case (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/marketing/nckh-experiment.json:36>`; unavailable in the cleaned checkout) là A/B design. Các case files ghi `not-run`; historical execution evidence không tự grade later source.

**Impact:** 156 base IDs + deterministic counts không đo dataset leakage, telemetry joins, statistical inference hoặc RCA metric correctness.

**Upgrade target:** bốn owner mới mỗi owner có positive/negative/outcome/failure IDs, thêm supplemental edge cases theo risks ở trên. Target giả định **43 identities / 172 base IDs** chỉ sau exact-set recheck hậu cook. Giữ 156 current IDs và historical 148/224/writer256 evidence; không sửa lịch sử thành đã test domain mới.

**Acceptance:** deterministic oracle chạy trên authorized fixtures để falsify invariants; actual agent trial phải bind prompts/resources/source revision/output+tool traces; ít nhất một bounded real project input case khi đủ rights; owner review và scientific review giữ lanes riêng. Không cấp provider/run budget từ một plan.

## Reuse và compatibility

- Reuse resource membership/rights validation (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/resources.py:45>`; unavailable in the cleaned checkout), bounded reader (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/scripts/search-resource.py:206>`; unavailable in the cleaned checkout), consumer/drift/no-read tests (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/tests/resource/test_writer_consumers.py:27>`; unavailable in the cleaned checkout), source/evidence/claim lineage, factual deltas và revision-bound state invalidation.
- Reuse acceptance policy (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/acceptance-policy.md:3>`; unavailable in the cleaned checkout) và receipt classes: integrity, agent behavior, native and human/scientific phải giữ độc lập. Existing owner feedback cho writer không trở thành domain gold của dataset/statistics/AIOps.
- Four-owner boundary: dataset owns research selection/splits; telemetry owns observation normalization/joins; statistics owns inference/readout; AIOps owns domain tasks/evaluation. Raw telemetry labeling hoặc split decisions phải handoff vào dataset; telemetry không tự quyết RCA truth.
- Exact-set migration có owners thật: build (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/build.py:35>`; unavailable in the cleaned checkout) / `:128`, `core/contracts/catalog.schema.json`, catalog, acceptance (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/acceptance.py:78>`; unavailable in the cleaned checkout), profile, cases/families, tests/count assertions, docs và new source freeze. Thêm identity vào catalog một mình sẽ fail closed; không weaken validators thành arbitrary counts.
- Qualification protocol (historical evidence path: `</C:/Users/USER/Downloads/test-skill/nckh-kit/core/evaluation.py:121>`; unavailable in the cleaned checkout) khóa `document/author/topic/claim-family` cho kit qualification. Không tái dùng trực tiếp làm research dataset/incident split schema; reuse freeze/exposure principles trong contract riêng và giữ historical protocol.
- `brief.schema.json`/source/resource schemas là closed/versioned; field mới cần owned schema/reader/test migration. Giữ legacy readers/bundle verification và preview/ownership conflict semantics. Current installed r25 không được upgrade chỉ vì plan/source thay đổi.
- Re-inventory exact post-cook revision/pins/catalog/resources/case IDs và integration evidence trước thực thi plan mới; snapshot này không chứng nhận cook completion, current native coverage hoặc release.

## Kết luận

Bốn owner mới được đề xuất giải quyết khoảng trống có bằng chứng mà vẫn giữ data migration, marketing và cook lifecycle hiện tại. DevOps đủ làm owner môi trường/quyền/process/rollback; AIOps cần dataset/telemetry/statistics/evaluation contract riêng. Không có findings mới về writer/visual/hooks trong scope hậu cook.

Status: DONE_WITH_CONCERNS
Summary: Đã đối chiếu r34/281 pins/39 skills/9 resources và installed r25/37; đề xuất chỉ nhắm baseline sau cook và bốn owner nghiên cứu mới.
Concerns/Blockers: Source đang có agent khác cook; post-cook exact baseline và domain input rights cần được recheck trước execution. Không có unresolved question chặn planning.
