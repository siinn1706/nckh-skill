# NCKH resource quality — execution checkpoint

Ngày 2026-10-02; yêu cầu `/goal ak-codex-goal ak-cook plan.md --auto`.

## Trạng thái

P1–P3 hoàn tất kỹ thuật; P4 đã có preparation/checker nhưng **qualification còn pending**. Plan có 27/29 phase tasks được ghi complete, ba trong bốn phase complete. Đây là trạng thái công việc, không phải tỷ lệ quality acceptance. Goal chưa đạt toàn bộ vì hai task cần actual human/runtime inputs. Stable/public release: **NO-GO**.

Candidate source **revision 22**, source-lock/bundle format **2**, **215 pins**; canonical source-lock hash:

`5aa333170906f909a374f256a7093702a399f9038421856bd7589066a0a6917d`

[Final freeze](../evaluation/resource-quality/final-freeze.json) phân biệt canonical lock hash với hash của file lock, source snapshot và từng receipt. Rollback dùng source/schema/lock khớp nhau; không restore lock cũ đơn độc. Các `dist`, `dist-runner` và `dist-runner-cleanup` cũ được giữ; candidate mới ở dist-resource-quality-r22 (historical evidence path: `../../nckh-kit/dist-resource-quality-r22/`; unavailable in the cleaned checkout).

## Thay đổi

- Sửa negative oracle cho cả 37 identities: reject đúng skill, owner/handoff rõ, không thực thi task thuộc skill khác. Closed case/family/protocol validation kiểm fields/types/maps/receipts; protected helper trả pending/NOT_CALLABLE. Không đổi lịch sử verdict.
- Giữ đúng **37 skills / 148 package cases / 19 required families / 224 native cells**. Baseline source 18 có snapshot và lock riêng; [evaluator freeze 19](../evaluation/resource-quality/evaluator-freeze.json) khớp 46 evaluator members đã quan sát. Không tái dựng historical test receipt bị thiếu.
- Một registry chọn bốn resources từ ba nguồn, với năm consumer identities. Source bytes, full commit/file hashes, license và attribution giữ nguyên; local code và copied-upstream có provenance khác nhau. Không clone repo, chạy upstream code, mix namespaces hay tạo corpus mới.
- Shared verifier hỗ trợ format 1 local-only và format 2 copied-content. Registry allowlist, explicit closure, path/cycle/private/unregistered-data guards và cả ba installer consumers được kiểm. Cùng code/instruction policy giữa on/off; off vẫn có standalone reader/registry và không chứa copied bytes.
- CRO đã được mở rộng theo lựa chọn trực tiếp của người dùng: kiểm canonical/noindex từ HTML/header thực, giữ intentional directives và unknown live indexing. Broader crawl/search analysis vẫn thuộc SEO. [Scope amendment](../evaluation/resource-quality/cro-scope-amendment.json) không rerun/regrade failure lịch sử.

| Resource | Nội dung có thật | Consumer | Giới hạn |
|---|---|---|---|
| `R-reporting-lookup` | 15 reporting entries; K-Dense MIT | method, write | Clinical/health design lookup; không áp universal CS/reporting compliance |
| `R-publisher-profile` | 8 publisher profiles; K-Dense MIT | visuals | Dated planning snapshot; Science historical/ACS legacy warnings và exact venue applicability chưa duyệt |
| `R-ui-lookup` | 119 unchanged UX rows; UI UX Pro Max MIT | frontend | UI heuristics; code examples là data, không được execute |
| `R-nature-reference` | Manifest-routed English language fragment; Nature Skills Apache-2.0 | write, taste | Optional advice; không phải VI/EN prose corpus hoặc universal Nature policy |

[Resource map](../261002-0832-nckh-skill-resource-quality/resource-map.md), [registry](../../nckh-kit/core/registry/catalog/resources.json), [source inspection](../evaluation/resource-quality/staging/source-inspection.json) và [promotion receipt](../evaluation/resource-quality/promotion-receipt.json) là các owner records. Identity còn lại giữ MD-only; VI/EN genre corpus và real chart measurements vẫn blocked-input.

## Verification trên revision 22

| Kiểm tra | Kết quả quan sát | Receipt |
|---|---|---|
| `evals/run-evals.py --validate-only` | Pass; 37/148/19/224, package/native cases vẫn not-run | [Structure](../evaluation/resource-quality/structure-r22.json) |
| Full deterministic suite | **106 tests, exit 0, OK, không skipped**; thực tế 450.402 giây khi chạy cùng các build checks | [Deterministic](../evaluation/resource-quality/deterministic-r22.json) |
| Same-base build reproducibility | Pass cho 4 hosts × on/off × standalone/plugin; hai empty-destination builds cho mỗi tổ hợp | [Reproducibility](../evaluation/resource-quality/verification-reproducibility-r22.json) |
| Persistent candidate build | Pass cho 8 host/treatment bundles, có optional plugin projection; không register/enable/trust | [Artifact build](../evaluation/resource-quality/verification-artifacts-r22.json) |
| Actual archive extraction và relocated reader | Pass cho cả 8 archives; 24 on resource-read và 24 off disabled-reader observations; external CWD, Python `-I`, unset PYTHONPATH | [Extracted smoke](../evaluation/resource-quality/extracted-smoke-r22.json) |
| Matched manifest checker | Integrity pass; 6 conditions, accepted count 0, benefit unknown, qualification pending | [Matched integrity](../evaluation/resource-quality/matched-integrity.json) |
| Historical bytes/linkage | Initial corpus/review/result hashes giữ nguyên; 312 receipt hashes được kiểm, một answer thiếu vẫn missing | [Final freeze](../evaluation/resource-quality/final-freeze.json) |

Các native projections là file encoding; không chứng minh discovery, invocation, effective model hoặc plugin runtime. Windows local subprocess/installer fixtures không qualify macOS/Linux, native editor, accessibility hoặc scientific meaning. Không có real installation, provider/native/human run hay release trong checkpoint này.

### Thất bại giữ lại và sửa nguyên nhân

Staging đã giữ lỗi test dùng sai return contract của `plan_install()` và lỗi external-CWD guard quá rộng; successful reruns có receipt riêng. Revision 21 có **37 tests/1 error**: owned attribution Markdown kéo copied license vào off closure. Đã lưu [failed snapshot](../evaluation/resource-quality/source-revision-21-failed.zip) và [observed failure summary](../evaluation/resource-quality/focus-check-revision-21.json). Common off closure được giới hạn vào reader/registry; targeted rerun pass và toàn bộ suite revision 22 pass. Một invocation thiếu `--write` chạy test với stale pin cũng được [ghi riêng](../evaluation/resource-quality/freeze-invocation-correction.json), rồi corrective freeze hoàn tất. Không xóa hoặc relabel các failure đó thành pass.

## Review và lịch sử

Review nội bộ theo `ak-code-review` tập trung changed source, schemas, docs, public build/installer callers và regression evidence. Simplifier đã thực hiện scoped edits ở `core/resources.py` và `scripts/search-resource.py`, kiểm compile và 10 focused guards; parent giữ integration/final review. Đây không phải independent human/domain qualification.

[Final change manifest](../evaluation/resource-quality/change-manifest-final.json) ghi 83 changed pinned files, 1,234 Python lines of change. Cả 37 case manifests đã được so với original archive: chỉ negative oracle thay đổi, các field khác giữ nguyên. Adapter AGY byte-identical với revision 18; noise do newline trong diff cũ đã được loại khỏi final manifest. Licensed bytes đối chiếu exact source pins; license/provenance/rights flow được review riêng khỏi current scientific truth. [Final diff](./code-diff-261002-resource-quality-final.diff) giữ toàn bộ thay đổi để người dùng review. Không phát hiện blocker kỹ thuật còn mở trong phạm vi đã kiểm.

Direct historical lane vẫn là **installed revision 14**, exposed synthetic development và controller-agent review: first round **137 pass / 4 fail / 7 pending**, latest **147 pass / 1 fail**. [Direct linkage](../evaluation/resource-quality/direct-linkage.json) có 158 review rows cho 148 unique IDs. `workspaces/round-1/nckh-cook/answer.md` không tồn tại; không tạo lại answer. CRO failure giữ nguyên. Các verdict này không chứng nhận source 18 hoặc candidate 22.

## P4 còn thiếu

[Matched manifest](../evaluation/resource-quality/matched-manifest.json) giữ đủ no-skill, relevant permitted upstream, same-agent off/on và selective-delegation off/on. Base/instruction/registry/corpus/split/wrapper/config và actual bundle closures có hash khi đã tồn tại. No-skill/upstream subject chưa chọn vẫn null; không relabel resource imports thành upstream baseline. Không có output hash hoặc effective model tự tạo. Migration revision 14 → 22 được ghi descriptive history riêng.

[Human review queue](../evaluation/resource-quality/human-review-queue.json) giữ năm rubric references nhưng reviewer, threshold, input artifact và review receipt vẫn null. Wrapper files là specification-only, driver binding/budget chưa chọn. Historical round counts được đọc từ actual review file; không allocation/reset vòng mới. Giới hạn 3 development rounds, 1 protected holdout run, exposure → development giữ nguyên. Protected holdout vẫn pending/NOT_CALLABLE; current adapter development-only, 1–900 giây/case. Case dài hơn cần một route được duyệt, không cắt bớt task hoặc nâng timeout âm thầm.

Để chạy và review qualification còn cần:

1. Corpus VI/EN và quyền sử dụng/phân chia của mẫu thật; chart measurements/source-map thật khi task visuals cần.
2. Reviewer cho VI taste, EN fidelity, domain/science và native/visual artifacts; threshold, coverage và blind/private review references.
3. Actual host/OS/model/interface và effective-model evidence route; permitted upstream skill subject được pin nếu dùng baseline đó.
4. Provider/process budget, acceptable economics và authority cho exact run configuration. Hash, registry, ambient credentials hoặc `--auto` không thay thế các inputs/grants này.

Chưa có bằng chứng resource benefit, human/scientific acceptance, accepted-task economics hoặc stable release. Phần kỹ thuật đã hoàn tất; tổng thể plan/goal chưa complete.

## Finalization

Đã đọc lại và cập nhật plan index, bốn phases và đủ 37 resource dispositions theo bằng chứng thực thi. `ak plan validate` pass, `parse` ghi 27/29 tasks và 3/4 phases complete; local AgentKit index được reindex bằng runtime trong workspace, không ghi global index. Journal đã tạo qua CLI và `ak journal validate` pass: [local journal](../journals/2026-10-02-nckh-resource-quality-technical-candidate-qualification-pend.md). AgentWiki publish skipped.

[Final integrity](../evaluation/resource-quality/final-integrity.json) đã kiểm 12 documents/84 local links, không broken link; 15 freeze references, 8 archive hashes và 24 on/24 off observations khớp revision 22. [Plan/journal validation](../evaluation/resource-quality/plan-journal-validation.json) giữ raw CLI outcomes. Đây là structure/record integrity, không clear hai human/runtime tasks còn pending.
